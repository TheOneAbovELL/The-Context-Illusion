# Run none_h2_s2_58066cb5

* study: `induction`  variant: `none_h2`  seed: 2
* positional method: `none`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 233s, final train loss 1.0659, final in-distribution val acc 0.727
* steps to val acc 0.5/0.9/0.99: 800/None/None

## Controls (measured)

* in_distribution_acc: 0.7233333333333334
* pos_offset_0_acc: 0.7233333333333334
* pos_offset_64_acc: 0.7233333333333334

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
| control_in_distribution | default | 300 | 0 | 0.723 | 0.670 | 0.771 | 1.127 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.723 | 0.670 | 0.771 | 1.127 |
| control_position_offset | pos_offset=64 | 300 | 0 | 0.723 | 0.670 | 0.771 | 1.127 |
| length | seq_len=34 | 300 | 0 | 0.747 | 0.695 | 0.793 | 1.042 |
| length | seq_len=50 | 300 | 0 | 0.490 | 0.434 | 0.546 | 2.456 |
| length | seq_len=66 | 300 | 0 | 0.390 | 0.337 | 0.446 | 3.053 |
| length | seq_len=96 | 300 | 0 | 0.227 | 0.183 | 0.277 | 3.945 |
| order | induction_order=fixed | 300 | 0 | 0.387 | 0.333 | 0.443 | 2.671 |
| order | induction_order=shuffled | 300 | 0 | 0.687 | 0.632 | 0.737 | 1.171 |
