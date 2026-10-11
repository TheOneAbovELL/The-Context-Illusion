# Run none_h4_s1_f63939d1

* study: `induction`  variant: `none_h4`  seed: 1
* positional method: `none`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 259s, final train loss 0.6884, final in-distribution val acc 0.832
* steps to val acc 0.5/0.9/0.99: 900/None/None

## Controls (measured)

* in_distribution_acc: 0.85
* pos_offset_0_acc: 0.85
* pos_offset_64_acc: 0.85

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
| control_in_distribution | default | 300 | 0 | 0.850 | 0.805 | 0.886 | 0.632 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.850 | 0.805 | 0.886 | 0.632 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.850 | 0.805 | 0.886 | 0.632 |
| length | seq_len=34 | 300 | 0 | 0.800 | 0.751 | 0.841 | 0.762 |
| length | seq_len=50 | 300 | 0 | 0.563 | 0.507 | 0.618 | 2.265 |
| length | seq_len=66 | 300 | 0 | 0.420 | 0.366 | 0.477 | 3.189 |
| length | seq_len=96 | 300 | 0 | 0.287 | 0.238 | 0.340 | 4.137 |
| order | induction_order=fixed | 300 | 0 | 0.570 | 0.513 | 0.625 | 1.827 |
| order | induction_order=shuffled | 300 | 0 | 0.827 | 0.780 | 0.865 | 0.756 |
