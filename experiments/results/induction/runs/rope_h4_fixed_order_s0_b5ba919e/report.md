# Run rope_h4_fixed_order_s0_b5ba919e

* study: `induction`  variant: `rope_h4_fixed_order`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 163s, final train loss 0.0000, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 100/100/200

## Controls (measured)

* in_distribution_acc: 1.0
* pos_offset_0_acc: 1.0
* pos_offset_64_acc: 1.0

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
| control_position_offset | pos_offset=64 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| length | seq_len=34 | 300 | 0 | 0.067 | 0.044 | 0.101 | 19.708 |
| length | seq_len=50 | 300 | 0 | 0.057 | 0.036 | 0.089 | 13.851 |
| length | seq_len=66 | 300 | 0 | 0.020 | 0.009 | 0.043 | 13.167 |
| length | seq_len=96 | 300 | 0 | 0.020 | 0.009 | 0.043 | 13.195 |
| order | induction_order=fixed | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| order | induction_order=shuffled | 300 | 0 | 0.067 | 0.044 | 0.101 | 19.587 |
