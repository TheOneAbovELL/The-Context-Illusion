# Run q04_s2_5f70bcf9

* study: `density`  variant: `q04`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 584s, final train loss 3.4648, final in-distribution val acc 0.059
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.12
* pos_offset_0_acc: 0.12

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
| control_in_distribution | default | 300 | 0 | 0.120 | 0.088 | 0.162 | 3.401 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.120 | 0.088 | 0.162 | 3.401 |
| order | induction_order=fixed | 300 | 0 | 0.013 | 0.005 | 0.034 | 3.736 |
| order | induction_order=shuffled | 300 | 0 | 0.067 | 0.044 | 0.101 | 3.542 |
