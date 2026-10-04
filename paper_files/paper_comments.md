# Paper comments — inconsistencies detected during transcription

Source: `paper_files/original.pdf` (authoritative) and its transcription `paper_files/paper.md`.
These items were found while transcribing the PDF (2026-10-03). They were **not** corrected in `paper.md`, which must stay faithful to the PDF. Corrections belong in the revised manuscript.

Evidence levels: VERIFIED / STRONG EVIDENCE / INFERENCE / HYPOTHESIS / UNKNOWN.

| # | Location | Issue | Evidence level | Status |
|---|---|---|---|---|
| 1 | Figure numbering (pp. 5–8) | FIGURE 4 does not exist | VERIFIED | Open |
| 2 | §II-C5 "Model Sparsity" (p. 7) | Circular cross-reference to Section II-C5 | VERIFIED | Open |
| 3 | Table 4, row Conv4.4 (p. 9) | Input printed as `24x32`, without the superscript | VERIFIED | Open |
| 4 | Figure 9a legend (p. 13) | Legend reads "MobileNetV Nano" | VERIFIED | Open |
| 5 | Figure 9b (p. 13) vs. text / Table 9 | The PYNQ-Z1 power bar seems inconsistent with 144 mW | HYPOTHESIS | Open — needs check |
| 6 | References [13] and [29] (p. 14) | Conference years look wrong | [29]: VERIFIED inconsistency; [13]: INFERENCE | Open — needs check |
| 7 | Table 1, row FASDD CV, Test "Both" (p. 4) | 3558 should be 3358 (the row does not sum) | VERIFIED | Open |
| 8 | Table 2, row MobileNetV3 (p. 8) | Parameters (1.52 M) and F1-Macro (97.07 %) come from two different runs | STRONG EVIDENCE | Open |

---

## 1. FIGURE 4 is missing

- **Location:** figure sequence. FIGURE 3 "Spatial SVD." is on p. 5 and the next figure is FIGURE 5 "BED architectures." on p. 8.
- **Observation:** no float labelled FIGURE 4 appears anywhere in the PDF, and the text never refers to "Figure 4".
- **Evidence:** `pdftotext` of all 15 pages plus visual inspection of every page.
- **Likely cause (HYPOTHESIS):** a figure was removed from the LaTeX source, or a LaTeX float counter was advanced.
- **Proposed fix:** renumber the figures (5→4, 6→5, …, 9→8) and update every in-text reference, or restore the missing figure if it was removed by mistake.

## 2. Circular cross-reference in §II-C5

- **Location:** §II-C5 "Further Optimizations", bullet "Model Sparsity" (p. 7).
- **Text as printed:** "The effect of this transformation is reported in Section II-C5."
- **Observation:** the sentence sits inside Section II-C5, so it refers to itself. The sparsity results are actually reported in §III-B6 "Further Optimizations: Image Dimensions and Sparsity" (p. 11, Figure 8).
- **Proposed fix:** change the reference to "Section III-B6" (check the label in the LaTeX source).

## 3. Table 4 — missing superscript in row Conv4.4

- **Location:** Table 4 "BED architecture optimized and adapted for the FPGA." (p. 9), row `Conv4.4`.
- **As printed:** Input = `24x32`. Every other row uses the squared form (e.g. `24²x64` for Conv4.3).
- **Consistency check:** Conv4.3 (input 24²x64, 1×1 kernel) outputs 32 channels at 24×24, so the input to Conv4.4 should be `24²x32`. The next row (Conv4.5) has input 22²x60, which matches a valid 3×1/1×3 convolution applied to 24×24.
- **Proposed fix:** `24x32` → `24²x32`.

## 4. Figure 9a — truncated model name in legend

- **Location:** Figure 9a "Raspberry Pi inference times." (p. 13), last legend entry.
- **As printed:** "MobileNetV Nano".
- **Proposed fix:** "MobileNetV2 Nano" (the name used throughout the text and tables). Also check the other legend labels against the naming in the text, e.g. "MobileViTV3".

## 5. Figure 9b — PYNQ-Z1 power bar vs. 144 mW

- **Location:** Figure 9b "Power and F1-Macro of the selected models operating near 30 fps." (p. 13). Related text: Abstract, §III-C, Table 9.
- **Observation (visual reading of the rendered figure, not verified against source data):** the PYNQ-Z1 bar, plotted on the "Power (W)" axis, appears to sit at roughly 2.5 W, with a small error bar. The text says that Figure 9b shows the Vivado-estimated **programmable-logic** power of MobileNetV2 Nano near 30 fps. Table 9 and Table 10 give 144 mW (0.144 W) for that point (4 MHz).
- **Possible explanations (HYPOTHESIS):**
  - the bar is a board-level PYNQ-Z1 value, which would contradict §IV ("the total PYNQ-Z1 board power was not measured");
  - the figure comes from an earlier version of the analysis;
  - the bar uses a different quantity or unit.
- **Action required:** locate the source data and the script or spreadsheet that produced Figure 9b, and find out which quantity the bar shows. Then align either the figure or the text. This interacts with reviewer comments on power comparison methodology, if any.

## 6. Reference years — [13] and [29]

- **[29]** Q. Wang et al., "ECA-Net: …", *2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 11 531–11 539, **2019**.
  - **Observation (VERIFIED, internal inconsistency):** the venue says 2020 and the year field says 2019.
  - **Also:** the page range is printed as "11 531–11 539", with thin-space thousands separators. It should probably read "11531–11539".
- **[13]** M. Sandler et al., "MobileNetV2: Inverted Residuals and Linear Bottlenecks," *The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, **2019**, pp. 4510–4520.
  - **Observation (INFERENCE, not checked against the bibliographic record):** MobileNetV2 was published at CVPR 2018, so the year 2019 looks wrong.
- **Action required:** check both entries against the official records (CVF Open Access / IEEE Xplore) and fix the BibTeX.

## 7. Table 1 — FASDD CV test "Both" count

- **Location:** Table 1 "DFire and FASDD datasets." (p. 4), row FASDD CV, Test column "Both".
- **As printed:** 3558. The row then sums to 6533 + 3902 + 2091 + 3558 = 16,084, but the printed Total is 15,884.
- **Evidence (VERIFIED 2026-10-04):**
  - `~/uav/datasets/fasdd/fasdd_cv/annotations/YOLO_CV/test.txt` lists 3358 `bothFireAndSmoke_CV*` images, and 6533 + 3902 + 2091 + 3358 = 15,884;
  - the Test "Total" row (Both 5556 = 895 + 1303 + 3358) is only consistent with 3358;
  - all other rows of Table 1 sum correctly.
- **Proposed fix:** 3558 → 3358.

## 8. Table 2 — MobileNetV3 row mixes two models

- **Location:** Table 2 "Reference Models." (p. 8), row MobileNetV3: 1.52 M parameters, 55 M MAC, F1-Macro 97.07 %.
- **Evidence (STRONG EVIDENCE, 2026-10-04, `02_audit/f0_selection_bias`):**
  - F1-Macro 97.07 matches `~/uav/code/classifier_transfer_learning/experiments/test_v01_mobilenetv3_full_ds` (full fine-tuning session; best saved mean F1 0.9707), whose log reports **945,538** parameters (≈ 0.95 M);
  - 1.52 M matches `test_v05_mobilenetv3Deep_full_ds` (**1,519,906** parameters), whose best F1-Macro is **97.16**.
- **Proposed fix:** decide which model is the reference and report its own parameters, MAC and F1 (either 0.95 M / 97.07 or 1.52 M / 97.16). The MAC value (55 M) must be checked for the chosen model.

