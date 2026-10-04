#!/usr/bin/env bash
# Execute validate_paper_metrics.ipynb for each paper model in its original conda environment.
# Usage (from this folder): ./run_validation.sh [fp32] [brevitas]
set -euo pipefail
cd "$(dirname "$0")"
declare -A ENV=( [fp32]=pytorch_23 [brevitas]=pytorch_brevitas )
models=("$@"); [ ${#models[@]} -eq 0 ] && models=(fp32 brevitas)
for m in "${models[@]}"; do
  echo "=== $m (${ENV[$m]}) $(date -Is)"
  REPLICA_MODEL=$m NO_ALBUMENTATIONS_UPDATE=1 /opt/conda/envs/${ENV[$m]}/bin/jupyter nbconvert --to notebook --execute \
      --ExecutePreprocessor.timeout=-1 --output "validate_paper_metrics.executed_${m}.ipynb" validate_paper_metrics.ipynb
  echo "=== $m done $(date -Is)"
done
