# Run learned_h2_s0_5c85c4aa

* study: `induction`  variant: `learned_h2`  seed: 0
* positional method: `learned`; layers=2, d_model=64, heads=2; parameters=149504 (positional: 32768)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 258s, final train loss 0.0000, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 700/700/900

## Controls (measured)

* in_distribution_acc: 1.0
* pos_offset_0_acc: 1.0
* pos_offset_64_acc: 0.19666666666666666

## Validity checks

* eval_examples_checked: 1800
* eval_examples_with_violations: 0
* n_train_sampled: 3000
* n_eval: 1800
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_in_distribution | default | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| control_position_offset | pos_offset=0 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.197 | 0.156 | 0.245 | 13.847 |
| length | seq_len=34 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| length | seq_len=50 | 300 | 0 | 0.657 | 0.601 | 0.708 | 6.461 |
| length | seq_len=66 | 300 | 0 | 0.490 | 0.434 | 0.546 | 8.685 |
| length | seq_len=96 | 300 | 0 | 0.340 | 0.289 | 0.395 | 12.089 |
| order | induction_order=fixed | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| order | induction_order=shuffled | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
