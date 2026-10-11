# Run separate_marker_s0_e7f66347

* study: `value_type`  variant: `separate_marker`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 458s, final train loss 1.3276, final in-distribution val acc 0.281
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.3466666666666667
* evidence_removed_acc: 0.03666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.37666666666666665
* cf_distractor_edit_rate_given_orig_correct: 0.4807692307692308
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.8733333333333333
* cf_evidence_move_rate_given_orig_correct: 0.8557692307692307
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.96
* cf_filler_resample_rate_given_orig_correct: 0.9807692307692307
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.2633333333333333
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.30333333333333334
* cf_value_edit_rate_given_orig_correct: 0.4807692307692308
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.3466666666666667

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.377 | 0.324 | 0.433 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.873 | 0.831 | 0.906 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.960 | 0.931 | 0.977 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.263 | 0.217 | 0.316 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.303 | 0.254 | 0.358 | nan |
| control_evidence_removed | default | 300 | 0 | 0.037 | 0.021 | 0.064 | 10.516 |
| control_in_distribution | default | 300 | 0 | 0.347 | 0.295 | 0.402 | 1.320 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.347 | 0.295 | 0.402 | 1.320 |
| in_format | n_queries=4 | 400 | 0 | 0.247 | 0.208 | 0.292 | 1.346 |
