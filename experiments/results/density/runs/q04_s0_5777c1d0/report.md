# Run q04_s0_5777c1d0

* study: `density`  variant: `q04`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `induction`, training lengths (34, 34)
* training: 3000 steps, 614s, final train loss 2.8269, final in-distribution val acc 0.266
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2733333333333333
* pos_offset_0_acc: 0.2733333333333333

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
| control_in_distribution | default | 300 | 0 | 0.273 | 0.226 | 0.326 | 2.890 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.273 | 0.226 | 0.326 | 2.890 |
| order | induction_order=fixed | 300 | 0 | 0.240 | 0.195 | 0.291 | 2.930 |
| order | induction_order=shuffled | 300 | 0 | 0.290 | 0.242 | 0.344 | 2.862 |
