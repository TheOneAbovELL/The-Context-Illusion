# Run separate_marker_s1_90f8d5e2

* study: `value_type`  variant: `separate_marker`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 454s, final train loss 1.3230, final in-distribution val acc 0.262
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.32
* evidence_removed_acc: 0.023333333333333334
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4633333333333333
* cf_distractor_edit_rate_given_orig_correct: 0.5729166666666666
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.93
* cf_evidence_move_rate_given_orig_correct: 0.9375
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9833333333333333
* cf_filler_resample_rate_given_orig_correct: 1.0
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.23333333333333334
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.20333333333333334
* cf_value_edit_rate_given_orig_correct: 0.3020833333333333
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.32

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.463 | 0.408 | 0.520 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.930 | 0.895 | 0.954 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.983 | 0.962 | 0.993 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.233 | 0.189 | 0.284 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.203 | 0.162 | 0.252 | nan |
| control_evidence_removed | default | 300 | 0 | 0.023 | 0.011 | 0.047 | 10.341 |
| control_in_distribution | default | 300 | 0 | 0.320 | 0.270 | 0.375 | 1.324 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.320 | 0.270 | 0.375 | 1.324 |
| in_format | n_queries=4 | 400 | 0 | 0.258 | 0.217 | 0.303 | 1.348 |
