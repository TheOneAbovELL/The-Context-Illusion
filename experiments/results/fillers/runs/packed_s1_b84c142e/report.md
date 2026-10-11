# Run packed_s1_b84c142e

* study: `fillers`  variant: `packed`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 563s, final train loss 1.3230, final in-distribution val acc 0.262
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.29333333333333333
* evidence_removed_acc: 0.02666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.45
* cf_distractor_edit_rate_given_orig_correct: 0.6704545454545454
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.8766666666666667
* cf_evidence_move_rate_given_orig_correct: 0.8295454545454546
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.97
* cf_filler_resample_rate_given_orig_correct: 1.0
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.2833333333333333
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.23333333333333334
* cf_value_edit_rate_given_orig_correct: 0.36363636363636365
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.29333333333333333

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.450 | 0.395 | 0.507 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.877 | 0.835 | 0.909 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.970 | 0.944 | 0.984 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.283 | 0.235 | 0.337 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.233 | 0.189 | 0.284 | nan |
| control_evidence_removed | default | 300 | 0 | 0.027 | 0.014 | 0.052 | 10.615 |
| control_in_distribution | default | 300 | 0 | 0.293 | 0.245 | 0.347 | 1.328 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.293 | 0.245 | 0.347 | 1.328 |
| in_format | n_queries=4 | 400 | 0 | 0.320 | 0.276 | 0.367 | 1.316 |
