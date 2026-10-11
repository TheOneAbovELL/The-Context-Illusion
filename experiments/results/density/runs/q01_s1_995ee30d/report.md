# Run q01_s1_995ee30d

* study: `density`  variant: `q01`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 341s, final train loss 3.7376, final in-distribution val acc 0.035
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.05333333333333334
* pos_offset_0_acc: 0.05333333333333334

## Validity checks

* eval_examples_checked: 600
* eval_examples_with_violations: 0
* n_train_sampled: 3000
* n_eval: 600
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_in_distribution | default | 300 | 0 | 0.053 | 0.033 | 0.085 | 3.740 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.053 | 0.033 | 0.085 | 3.740 |
| order | induction_order=fixed | 300 | 0 | 0.043 | 0.025 | 0.073 | 3.840 |
| order | induction_order=shuffled | 300 | 0 | 0.057 | 0.036 | 0.089 | 3.714 |
