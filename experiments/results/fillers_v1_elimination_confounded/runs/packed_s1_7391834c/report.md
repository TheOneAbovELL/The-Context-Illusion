# Run packed_s1_7391834c

* study: `fillers`  variant: `packed`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 249s, final train loss 0.8105, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 500/600/1100

## Controls (measured)

* in_distribution_acc: 1.0
* evidence_removed_acc: 0.04
* chance_acc: 0.03125
* pos_offset_0_acc: 1.0

## Validity checks

* eval_examples_checked: 400
* eval_examples_with_violations: 0
* n_train_sampled: 3000
* n_eval: 400
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_evidence_removed | default | 300 | 0 | 0.040 | 0.023 | 0.069 | 7.691 |
| control_in_distribution | default | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.006 |
| control_position_offset | pos_offset=0 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.006 |
| in_format | n_queries=4 | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.005 |
