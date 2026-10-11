# Run none_h4_s2_14335b66

* study: `induction`  variant: `none_h4`  seed: 2
* positional method: `none`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 258s, final train loss 0.8156, final in-distribution val acc 0.734
* steps to val acc 0.5/0.9/0.99: 900/None/None

## Controls (measured)

* in_distribution_acc: 0.7633333333333333
* pos_offset_0_acc: 0.7633333333333333
* pos_offset_64_acc: 0.7633333333333333

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
| control_in_distribution | default | 300 | 0 | 0.763 | 0.712 | 0.808 | 0.883 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.763 | 0.712 | 0.808 | 0.883 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.763 | 0.712 | 0.808 | 0.883 |
| length | seq_len=34 | 300 | 0 | 0.783 | 0.733 | 0.826 | 0.748 |
| length | seq_len=50 | 300 | 0 | 0.553 | 0.497 | 0.609 | 2.295 |
| length | seq_len=66 | 300 | 0 | 0.377 | 0.324 | 0.433 | 3.270 |
| length | seq_len=96 | 300 | 0 | 0.300 | 0.251 | 0.354 | 3.710 |
| order | induction_order=fixed | 300 | 0 | 0.540 | 0.483 | 0.596 | 2.091 |
| order | induction_order=shuffled | 300 | 0 | 0.817 | 0.769 | 0.856 | 0.749 |
