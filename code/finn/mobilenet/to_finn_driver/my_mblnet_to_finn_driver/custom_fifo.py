# ________________________________________________________ #
# Created to be able to set max_depth=2^15=32768
# If not, max_depth=tensor_size...
# ________________________________________________________ #

import warnings
from qonnx.transformation.base import Transformation
from qonnx.transformation.general import (
    GiveReadableTensorNames,
    GiveUniqueNodeNames,
)

from qonnx.core.modelwrapper import ModelWrapper
from finn.builder.build_dataflow_config import (
    DataflowBuildConfig,
)
from finn.analysis.fpgadataflow.dataflow_performance import dataflow_performance
from finn.transformation.fpgadataflow.annotate_cycles import AnnotateCycles
from finn.transformation.fpgadataflow.create_stitched_ip import CreateStitchedIP
from finn.transformation.fpgadataflow.hlssynth_ip import HLSSynthIP
from finn.transformation.fpgadataflow.insert_dwc import InsertDWC
from finn.transformation.fpgadataflow.insert_fifo import InsertFIFO
from finn.transformation.fpgadataflow.prepare_ip import PrepareIP
from finn.transformation.fpgadataflow.specialize_layers import SpecializeLayers

def custom_step_set_fifo_depths(model: ModelWrapper, cfg: DataflowBuildConfig):
    """
    Depending on the auto_fifo_depths setting, do one of the following:
    * if auto_fifo_depths=True:  Run the appropriate auto-sizing transformation
    to attempt to determine the FIFO sizes that provide full throughput.
    May take a long time.
    * if auto_fifo_depths=False:  Assume the folding config file contains FIFO
    sizes as well. Runs the `InsertFIFO` transformation, then
    `ApplyConfig(cfg.folding_config_file)`, and finally `RemoveShallowFIFOs`.
    Coherency with config file node naming is ensured by calling
    `GiveUniqueNodeNames`.
    """

    if cfg.auto_fifo_depths:
        if cfg.auto_fifo_strategy == "characterize":
            model = model.transform(InsertDWC())
            model = model.transform(SpecializeLayers(cfg._resolve_fpga_part()))
            model = model.transform(GiveUniqueNodeNames())
            model = model.transform(
                PrepareIP(cfg._resolve_fpga_part(), cfg._resolve_hls_clk_period())
            )
            model = model.transform(HLSSynthIP())
            model = model.transform(PrepareRTLSim())
            model = model.transform(AnnotateCycles())
            period = model.analysis(dataflow_performance)["max_cycles"] + 10
            model = model.transform(DeriveCharacteristic(period))
            model = model.transform(DeriveFIFOSizes())
            model = model.transform(
                InsertFIFO(
                    vivado_ram_style=cfg.large_fifo_mem_style,
                    max_qsrl_depth=256,
                    create_shallow_fifos=True,
                )
            )
            model = model.transform(SpecializeLayers(cfg._resolve_fpga_part()))
            model = model.transform(GiveUniqueNodeNames())
            model = model.transform(GiveReadableTensorNames())
        elif cfg.auto_fifo_strategy == "largefifo_rtlsim":
            # multi-in/out streams currently not supported in our C++ verilator driver
            model_multi_io = len(model.graph.input) > 1 or len(model.graph.output) > 1
            force_python_sim = model_multi_io or cfg.force_python_rtlsim
            if model_multi_io:
                warnings.warn(
                    "Multi-in/out streams currently not supported "
                    + "in FINN C++ verilator driver, falling back to Python"
                )
            model = model.transform(
                InsertAndSetFIFODepths(
                    cfg._resolve_fpga_part(),
                    cfg._resolve_hls_clk_period(),
                    max_depth=2**15,
                    swg_exception=cfg.default_swg_exception,
                    vivado_ram_style=cfg.large_fifo_mem_style,
                    force_python_sim=force_python_sim,
                )
            )
            # InsertAndSetFIFODepths internally removes any shallow FIFOs
            # so no need to call RemoveShallowFIFOs here
        else:
            assert "Unsupported auto_fifo_strategy: " + cfg.auto_fifo_strategy
    else:
        # assume folding cfg json contains FIFO sizes too
        # insert DWCs, FIFOs and run ApplyConfig once more
        model = model.transform(InsertDWC())
        # need to make sure all FIFOs are created so that their depth can be
        # set by ApplyConfig, so create_shallow_fifos=True
        model = model.transform(InsertFIFO(create_shallow_fifos=True))
        model = model.transform(SpecializeLayers(cfg._resolve_fpga_part()))
        model = model.transform(GiveUniqueNodeNames())
        model = model.transform(GiveReadableTensorNames())
        if cfg.folding_config_file is not None:
            model = model.transform(ApplyConfig(cfg.folding_config_file))

    # extract the final configuration and save it as json
    hw_attrs = [
        "PE",
        "SIMD",
        "parallel_window",
        "ram_style",
        "depth",
        "impl_style",
        "resType",
        "mem_mode",
        "runtime_writeable_weights",
        "inFIFODepths",
        "outFIFODepths",
        "depth_trigger_uram",
        "depth_trigger_bram",
    ]
    extract_model_config_to_json(model, cfg.output_dir + "/final_hw_config.json", hw_attrs)

    # perform FIFO splitting and shallow FIFO removal only after the final config
    # json file has been written. otherwise, since these transforms may add/remove
    # FIFOs, we get name mismatch problems when trying to reuse the final config.
    if cfg.split_large_fifos:
        model = model.transform(SplitLargeFIFOs())
    model = model.transform(RemoveShallowFIFOs())

    # after FIFOs are ready to go, call PrepareIP and HLSSynthIP again
    # this will only run for the new nodes (e.g. FIFOs and DWCs)
    model = model.transform(PrepareIP(cfg._resolve_fpga_part(), cfg._resolve_hls_clk_period()))
    model = model.transform(HLSSynthIP())
    return model