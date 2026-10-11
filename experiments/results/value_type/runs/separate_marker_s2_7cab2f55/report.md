# Run separate_marker_s2_7cab2f55

* study: `value_type`  variant: `separate_marker`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 300s, final train loss 1.3245, final in-distribution val acc 0.273
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.32
* evidence_removed_acc: 0.03666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.41333333333333333
* cf_distractor_edit_rate_given_orig_correct: 0.625
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.8733333333333333
* cf_evidence_move_rate_given_orig_correct: 0.8541666666666666
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.97
* cf_filler_resample_rate_given_orig_correct: 0.9479166666666666
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.2733333333333333
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.24333333333333335
* cf_value_edit_rate_given_orig_correct: 0.3645833333333333
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
| control_counterfactual | distractor_edit | 300 | 0 | 0.413 | 0.359 | 0.470 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.873 | 0.831 | 0.906 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.970 | 0.944 | 0.984 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.273 | 0.226 | 0.326 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.243 | 0.198 | 0.295 | nan |
| control_evidence_removed | default | 300 | 0 | 0.037 | 0.021 | 0.064 | 10.349 |
| control_in_distribution | default | 300 | 0 | 0.320 | 0.270 | 0.375 | 1.314 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.320 | 0.270 | 0.375 | 1.314 |
| in_format | n_queries=4 | 400 | 0 | 0.278 | 0.236 | 0.323 | 1.350 |
