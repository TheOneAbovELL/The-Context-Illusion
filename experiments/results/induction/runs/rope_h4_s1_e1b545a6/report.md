# Run rope_h4_s1_e1b545a6

* study: `induction`  variant: `rope_h4`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 334s, final train loss 0.0000, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 700/700/700

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
| length | seq_len=34 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| length | seq_len=50 | 300 | 0 | 0.700 | 0.646 | 0.749 | 3.695 |
| length | seq_len=66 | 300 | 0 | 0.650 | 0.594 | 0.702 | 4.254 |
| length | seq_len=96 | 300 | 0 | 0.647 | 0.591 | 0.699 | 3.146 |
| order | induction_order=fixed | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| order | induction_order=shuffled | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
