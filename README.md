### 1. KDD Attack Strategy Evolution (`data/kdd_attack_evolution.csv`)

This benchmark simulates concept drift induced by adversarial strategy shifts across 10 sequential time windows. The construction protocol follows Section 7.2.1 (1) of the paper.

**Source dataset**. Samples are drawn from the KDD Cup 1999 dataset (Tavallaee et al., 2009 [1]), one of the most widely used network-intrusion benchmarks. We adopt the standard five-category attack taxonomy defined in the original dataset documentation: **DoS** (denial of service), **Probe** (surveillance and probing), **R2L** (remote-to-local unauthorized access), **U2R** (user-to-root privilege escalation), and **Normal** (benign traffic).

**Construction procedure**. We manually selected samples from each attack category according to the per-window class-prior schedule specified in Table 8 of the paper, then concatenated the 10 windows in temporal order. Drift points consequently occur near sample indices 98K, 178K, 257K, and 336K. The exact per-window distribution is reproduced below for reference:

| Time | DoS | Probe | R2L | U2R | Normal | Total |
|------|-----|-------|-----|-----|--------|-------|
| T1   | 39674 | 0 | 0 | 0 | 9728 | 49402 |
| T2   | 39674 | 0 | 0 | 0 | 9728 | 49402 |
| T3   | 20000 | 4107 | 0 | 0 | 15567 | 39674 |
| T4   | 20000 | 4107 | 0 | 0 | 15567 | 39674 |
| T5   | 5000 | 4107 | 1126 | 0 | 29441 | 39674 |
| T6   | 5000 | 4107 | 1126 | 0 | 29441 | 39674 |
| T7   | 0 | 4107 | 1126 | 52 | 34389 | 39674 |
| T8   | 0 | 4107 | 1126 | 52 | 34389 | 39674 |
| T9   | 0 | 0 | 1126 | 52 | 38496 | 39674 |
| T10  | 0 | 0 | 1126 | 52 | 38496 | 39674 |

**File format**. The CSV file contains 41 numeric/categorical features and one binary `label` column (1 = attack of any category, 0 = normal). The five-category attack taxonomy is reflected in the per-window proportions of attack samples rather than as an explicit column, in line with the binary intrusion-detection setting evaluated in our experiments. Researchers wishing to recover the per-category labels can do so by joining the CSV against the original KDD Cup 1999 records using the source dataset's standard category mapping.

**Independent reconstruction**. Any researcher can independently reconstruct this benchmark from publicly available sources by: (1) downloading KDD Cup 1999, (2) partitioning samples by the standard five-category taxonomy, and (3) selecting samples per window in the proportions specified in the table above.
The dataset will be uploaded to this repository later.


### 2. Spam Attack Intensity Surge (`data/spam_intensity_surge.csv`)

This benchmark simulates volumetric attack surges, such as large-scale spam campaigns, by progressively increasing the spam proportion across 10 sequential time windows. Unlike the KDD-based benchmark, which focuses on qualitative changes in attack strategies, this benchmark is designed to emulate intensity-driven drift caused by changes in attack volume.

**Source dataset.** Samples are drawn from the Spam Filtering corpus, a publicly available email-classification dataset. Each row represents a feature vector extracted from an email, with the binary class label `spamorlegitimate ∈ {spam, legitimate}`. In the original corpus used for reconstruction, the dataset contains 9,324 samples, including 2,387 spam samples and 6,937 legitimate samples.

**Construction procedure.** Following Section 7.2.1 (1) of the paper, we manipulate the spam-to-legitimate ratio across 10 sequential time windows. The spam proportion gradually increases from 10% to 90%, simulating drift induced by volumetric spam campaign surges. Each time window contains `floor(9324 / 10) = 932` samples. The resulting benchmark contains 9,320 temporally ordered samples, with the remaining 4 samples excluded due to integer partitioning.

The detailed construction schedule is shown below:

| Time window | Spam fraction | Spam samples | Legitimate samples | Total |
| --- | --- | --- | --- | --- |
| T1 | 10.00% | 93 | 839 | 932 |
| T2 | 18.89% | 176 | 756 | 932 |
| T3 | 27.78% | 258 | 674 | 932 |
| T4 | 36.67% | 341 | 591 | 932 |
| T5 | 45.56% | 424 | 508 | 932 |
| T6 | 54.44% | 507 | 425 | 932 |
| T7 | 63.33% | 590 | 342 | 932 |
| T8 | 72.22% | 673 | 259 | 932 |
| T9 | 81.11% | 755 | 177 | 932 |
| T10 | 90.00% | 838 | 94 | 932 |

**File format.** The CSV file contains the original Spam corpus features and one categorical label column named `spamorlegitimate`, with values `spam` and `legitimate`. The samples are concatenated according to the temporal order of the 10 windows, from `T1` to `T10`.

**Independent reconstruction.** Researchers can reconstruct this benchmark by:  
(1) obtaining the Spam Filtering corpus;  
(2) partitioning samples according to the binary `spam`/`legitimate` label;  
(3) sampling the required number of spam and legitimate samples for each time window according to the schedule above; and  
(4) concatenating the sampled windows in temporal order.

Because the high-intensity windows require more spam samples than are available in the original corpus, sampling with replacement may be used for the spam class during reconstruction. To ensure reproducibility, researchers are encouraged to fix the random seed when performing the sampling process.

### 3. CIFAR-100-C Visual Adversarial Evolution (`data/visual_evolution/`)

This benchmark simulates progressively intensifying visual adversarial threats across 10 sequential tasks. Unlike the KDD- and Spam-based benchmarks, which target structured-stream drift, this benchmark is designed to emulate the cumulative evolution of visual adversarial attacks, ranging from single-corruption low-severity perturbations to composite multi-corruption high-severity attacks.

**Source dataset.** Samples are drawn from CIFAR-100-C (Hendrycks & Dietterich, 2019 [2]), a publicly available robustness benchmark derived from CIFAR-100. The dataset contains 50,000 images per corruption type, organized as five blocks of 10,000 images corresponding to severity levels 1 through 5. We use 15 corruption types in total: `gaussian_noise`, `shot_noise`, `impulse_noise`, `defocus_blur`, `glass_blur`, `motion_blur`,`zoom_blur`, `frost`, `snow`, `fog`, `brightness`, `contrast`, `elastic_transform`, `pixelate`, and `jpeg_compression`.

**Construction procedure.** Following Section 7.2.1 (2) and Table 9 of the paper, we partition the 100 CIFAR-100 classes into 10 disjoint tasks of 10 classes each (Task `t` contains classes `{10t, 10t+1, ..., 10t+9}`) and assign each task a specific combination of corruption types and severity levels. The construction simulates an environment that becomes progressively more hostile, evolving from single-corruption Severity 1 perturbations to composite Severity 5 attacks combining up to five corruption types. The full task-corruption schedule is shown below:

| Task | Classes | Corruption Type(s) | Severity |
|------|---------|--------------------|----------|
| T0 | 0–9 | Gaussian Noise | 1 |
| T1 | 10–19 | Shot Noise | 1 |
| T2 | 20–29 | Motion Blur | 2 |
| T3 | 30–39 | Frost | 2 |
| T4 | 40–49 | Contrast | 3 |
| T5 | 50–59 | Gaussian Noise + Motion Blur | 3 |
| T6 | 60–69 | Shot Noise + Frost + Contrast | 4 |
| T7 | 70–79 | Gaussian Noise + Defocus Blur + Snow + Brightness | 4 |
| T8 | 80–89 | Impulse Noise + Glass Blur + Fog + Elastic Transform | 5 |
| T9 | 90–99 | Gaussian Noise + Motion Blur + Frost + Contrast + JPEG Compression | 5 |

For tasks involving multiple corruption types (T5–T9), we combine the specified corruptions through **pixel-wise averaging** of the per-corruption images at the given severity level. This averaging scheme preserves the original Severity-level intensity calibration of CIFAR-100-C, whereas sequentially compounding multiple corruptions would amplify intensity beyond the documented severity levels. Each task's images are split into training and test sets at a 70%/30% ratio, partitioned independently per class to maintain class balance. The random seed is fixed at `42` for full reproducibility.

**File format.** The benchmark is saved as 10 per-task pickle pairs under `data/visual_evolution/`, plus a metadata file:

```
data/visual_evolution/
├── task_0_train, task_0_test
├── task_1_train, task_1_test
├── ...
├── task_9_train, task_9_test
└── meta
```

Each `task_t_train` and `task_t_test` file is a pickle-serialized Python dictionary in CIFAR-100-compatible format with the following keys:
- `data`: a NumPy array of shape `(N, 3072)`, where each row is a flattened 32×32×3 image (uint8);
- `fine_labels`: a list of length `N` containing the integer class labels (0–99).

The `meta` file stores the standard CIFAR-100 fine-label name list (`fine_label_names`).

This per-task file structure is deliberately chosen to support class-incremental learning evaluation, including the computation of Backward Transfer (BWT, Eq. 10 in the paper), which requires evaluating the model on each historical task independently after training on subsequent tasks.

**Independent reconstruction.** Researchers can reconstruct this benchmark by:  
(1) downloading the CIFAR-100-C source dataset from its official release;  
(2) running the provided construction script: `python data/build_visual_evolution.py`;  
(3) verifying that the output directory matches the structure shown above.

The construction script encodes the full task-corruption schedule, the pixel-wise averaging scheme, the 70%/30% train/test split, and the fixed random seed; running it on the same source dataset will produce a byte-identical benchmark.



## References
[1] M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani, 
"A detailed analysis of the KDD CUP 99 data set," 
in *Proceedings of the 2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications*, 2009, pp. 1–6. 
doi: 10.1109/CISDA.2009.5356528.

[2] D. Hendrycks and T. Dietterich, 
"Benchmarking Neural Network Robustness to Common Corruptions and Perturbations," 
arXiv:1903.12261, 2019. 
Available: https://arxiv.org/abs/1903.12261.
