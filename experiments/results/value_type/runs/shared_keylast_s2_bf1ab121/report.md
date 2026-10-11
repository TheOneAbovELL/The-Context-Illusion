# Run shared_keylast_s2_bf1ab121

* study: `value_type`  variant: `shared_keylast`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 622s, final train loss 0.0083, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 300/500/1000

## Controls (measured)

* in_distribution_acc: 0.9966666666666667
* evidence_removed_acc: 0.03666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 1.0
* cf_distractor_edit_rate_given_orig_correct: 1.0
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.99
* cf_evidence_move_rate_given_orig_correct: 0.9933110367892977
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 1.0
* cf_filler_resample_rate_given_orig_correct: 1.0
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.9933333333333333
* cf_key_swap_rate_given_orig_correct: 0.9933110367892977
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.9966666666666667
* cf_value_edit_rate_given_orig_correct: 0.9966555183946488
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.9966666666666667

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
| control_counterfactual | distractor_edit | 300 | 0 | 1.000 | 0.987 | 1.000 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.990 | 0.971 | 0.997 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 1.000 | 0.987 | 1.000 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.993 | 0.976 | 0.998 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.997 | 0.981 | 0.999 | nan |
| control_evidence_removed | default | 300 | 0 | 0.037 | 0.021 | 0.064 | 11.713 |
| control_in_distribution | default | 300 | 0 | 0.997 | 0.981 | 0.999 | 0.006 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.997 | 0.981 | 0.999 | 0.006 |
| in_format | n_queries=4 | 400 | 0 | 0.993 | 0.978 | 0.997 | 0.017 |
