# Run p050_s1_1324a27f

* study: `shortcut_dose`  variant: `p050`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=4; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 290s, final train loss 0.3911, final in-distribution val acc 0.992
* steps to val acc 0.5/0.9/0.99: 200/1800/2900

## Controls (measured)

* in_distribution_acc: 0.9866666666666667
* pos_offset_0_acc: 0.9866666666666667

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
| control_in_distribution | default | 300 | 0 | 0.987 | 0.966 | 0.995 | 0.045 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.987 | 0.966 | 0.995 | 0.045 |
| order | induction_order=fixed | 300 | 0 | 0.987 | 0.966 | 0.995 | 0.038 |
| order | induction_order=shuffled | 300 | 0 | 0.987 | 0.966 | 0.995 | 0.051 |
