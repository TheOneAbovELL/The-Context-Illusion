# Run none_h4_s0_5ca12584

* study: `induction`  variant: `none_h4`  seed: 0
* positional method: `none`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 258s, final train loss 1.1660, final in-distribution val acc 0.707
* steps to val acc 0.5/0.9/0.99: 900/None/None

## Controls (measured)

* in_distribution_acc: 0.6833333333333333
* pos_offset_0_acc: 0.6833333333333333
* pos_offset_64_acc: 0.6833333333333333

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
| control_in_distribution | default | 300 | 0 | 0.683 | 0.629 | 0.733 | 1.239 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.683 | 0.629 | 0.733 | 1.239 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.683 | 0.629 | 0.733 | 1.239 |
| length | seq_len=34 | 300 | 0 | 0.697 | 0.642 | 0.746 | 1.253 |
| length | seq_len=50 | 300 | 0 | 0.417 | 0.362 | 0.473 | 2.642 |
| length | seq_len=66 | 300 | 0 | 0.323 | 0.273 | 0.378 | 3.564 |
| length | seq_len=96 | 300 | 0 | 0.207 | 0.165 | 0.256 | 4.355 |
| order | induction_order=fixed | 300 | 0 | 0.403 | 0.349 | 0.460 | 2.539 |
| order | induction_order=shuffled | 300 | 0 | 0.663 | 0.608 | 0.714 | 1.271 |
