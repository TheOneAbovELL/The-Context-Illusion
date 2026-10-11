# Run shared_marker_s2_89ae7e04

* study: `value_type`  variant: `shared_marker`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 341s, final train loss 1.7128, final in-distribution val acc 0.281
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.3233333333333333
* evidence_removed_acc: 0.03333333333333333
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.5
* cf_distractor_edit_rate_given_orig_correct: 0.6288659793814433
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.79
* cf_evidence_move_rate_given_orig_correct: 0.7010309278350515
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9533333333333334
* cf_filler_resample_rate_given_orig_correct: 0.9690721649484536
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.2966666666666667
* cf_key_swap_rate_given_orig_correct: 0.07216494845360824
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.22666666666666666
* cf_value_edit_rate_given_orig_correct: 0.36082474226804123
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.3233333333333333

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.500 | 0.444 | 0.556 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.790 | 0.740 | 0.832 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.953 | 0.923 | 0.972 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.297 | 0.248 | 0.351 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.227 | 0.183 | 0.277 | nan |
| control_evidence_removed | default | 300 | 0 | 0.033 | 0.018 | 0.060 | 7.619 |
| control_in_distribution | default | 300 | 0 | 0.323 | 0.273 | 0.378 | 1.577 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.323 | 0.273 | 0.378 | 1.577 |
| in_format | n_queries=4 | 400 | 0 | 0.305 | 0.262 | 0.352 | 1.607 |
