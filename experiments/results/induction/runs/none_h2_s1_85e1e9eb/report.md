# Run none_h2_s1_85e1e9eb

* study: `induction`  variant: `none_h2`  seed: 1
* positional method: `none`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 233s, final train loss 0.6279, final in-distribution val acc 0.871
* steps to val acc 0.5/0.9/0.99: 700/None/None

## Controls (measured)

* in_distribution_acc: 0.8566666666666667
* pos_offset_0_acc: 0.8566666666666667
* pos_offset_64_acc: 0.8566666666666667

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
| control_in_distribution | default | 300 | 0 | 0.857 | 0.812 | 0.892 | 0.676 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.857 | 0.812 | 0.892 | 0.676 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.857 | 0.812 | 0.892 | 0.676 |
| length | seq_len=34 | 300 | 0 | 0.853 | 0.809 | 0.889 | 0.631 |
| length | seq_len=50 | 300 | 0 | 0.580 | 0.523 | 0.634 | 2.246 |
| length | seq_len=66 | 300 | 0 | 0.483 | 0.427 | 0.540 | 2.805 |
| length | seq_len=96 | 300 | 0 | 0.300 | 0.251 | 0.354 | 3.748 |
| order | induction_order=fixed | 300 | 0 | 0.723 | 0.670 | 0.771 | 1.347 |
| order | induction_order=shuffled | 300 | 0 | 0.820 | 0.773 | 0.859 | 0.725 |
