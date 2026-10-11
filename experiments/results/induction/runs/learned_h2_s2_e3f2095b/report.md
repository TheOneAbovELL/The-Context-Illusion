# Run learned_h2_s2_e3f2095b

* study: `induction`  variant: `learned_h2`  seed: 2
* positional method: `learned`; layers=2, d_model=64, heads=2; parameters=149504 (positional: 32768)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 257s, final train loss 2.6143, final in-distribution val acc 0.188
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.19
* pos_offset_0_acc: 0.19
* pos_offset_64_acc: 0.05

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
| control_in_distribution | default | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.658 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.658 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.050 | 0.031 | 0.081 | 4.388 |
| length | seq_len=34 | 300 | 0 | 0.127 | 0.094 | 0.169 | 2.676 |
| length | seq_len=50 | 300 | 0 | 0.030 | 0.016 | 0.056 | 4.904 |
| length | seq_len=66 | 300 | 0 | 0.037 | 0.021 | 0.064 | 5.487 |
| length | seq_len=96 | 300 | 0 | 0.033 | 0.018 | 0.060 | 5.866 |
| order | induction_order=fixed | 300 | 0 | 0.237 | 0.192 | 0.288 | 2.563 |
| order | induction_order=shuffled | 300 | 0 | 0.197 | 0.156 | 0.245 | 2.545 |
