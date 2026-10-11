# Run p075_s0_d7b54bfe

* study: `shortcut_dose`  variant: `p075`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 291s, final train loss 0.9023, final in-distribution val acc 0.773
* steps to val acc 0.5/0.9/0.99: 100/None/None

## Controls (measured)

* in_distribution_acc: 0.7633333333333333
* pos_offset_0_acc: 0.7633333333333333

## Validity checks

* eval_examples_checked: 600
* eval_examples_with_violations: 0
* n_train_sampled: 3000
* n_eval: 600
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_in_distribution | default | 300 | 0 | 0.763 | 0.712 | 0.808 | 0.913 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.763 | 0.712 | 0.808 | 0.913 |
| order | induction_order=fixed | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| order | induction_order=shuffled | 300 | 0 | 0.107 | 0.077 | 0.147 | 3.409 |
