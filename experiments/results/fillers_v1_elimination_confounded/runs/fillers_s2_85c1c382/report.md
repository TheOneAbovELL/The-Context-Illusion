# Run fillers_s2_85c1c382

* study: `fillers`  variant: `fillers`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (48, 48)
* training: 3000 steps, 497s, final train loss 0.9369, final in-distribution val acc 0.914
* steps to val acc 0.5/0.9/0.99: 800/2800/None

## Controls (measured)

* in_distribution_acc: 0.94
* evidence_removed_acc: 0.03666666666666667
* chance_acc: 0.03125
* pos_offset_0_acc: 0.94

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
| control_evidence_removed | default | 300 | 0 | 0.037 | 0.021 | 0.064 | 8.438 |
| control_in_distribution | default | 300 | 0 | 0.940 | 0.907 | 0.962 | 0.203 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.940 | 0.907 | 0.962 | 0.203 |
| in_format | n_queries=4 | 400 | 0 | 0.917 | 0.886 | 0.941 | 0.211 |
