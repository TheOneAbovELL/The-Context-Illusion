# Run learned_h4_fixed_order_s1_79789755

* study: `induction`  variant: `learned_h4_fixed_order`  seed: 1
* positional method: `learned`; layers=2, d_model=64, heads=4; parameters=149504 (positional: 32768)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 551s, final train loss 0.0000, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 200/200/200

## Controls (measured)

* in_distribution_acc: 1.0
* pos_offset_0_acc: 1.0
* pos_offset_64_acc: 0.013333333333333334

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
| control_position_offset | pos_offset=64 | 300 | 0 | 0.013 | 0.005 | 0.034 | 7.553 |
| length | seq_len=34 | 300 | 0 | 0.067 | 0.044 | 0.101 | 19.730 |
| length | seq_len=50 | 300 | 0 | 0.047 | 0.028 | 0.077 | 7.190 |
| length | seq_len=66 | 300 | 0 | 0.033 | 0.018 | 0.060 | 8.854 |
| length | seq_len=96 | 300 | 0 | 0.023 | 0.011 | 0.047 | 10.044 |
| order | induction_order=fixed | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| order | induction_order=shuffled | 300 | 0 | 0.067 | 0.044 | 0.101 | 19.894 |
