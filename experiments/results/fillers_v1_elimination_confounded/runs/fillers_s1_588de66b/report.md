# Run fillers_s1_588de66b

* study: `fillers`  variant: `fillers`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (48, 48)
* training: 3000 steps, 494s, final train loss 0.8085, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 700/800/1200

## Controls (measured)

* in_distribution_acc: 1.0
* evidence_removed_acc: 0.02666666666666667
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
| control_evidence_removed | default | 300 | 0 | 0.027 | 0.014 | 0.052 | 8.768 |
| control_in_distribution | default | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.007 |
| control_position_offset | pos_offset=0 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.007 |
| in_format | n_queries=4 | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.006 |
