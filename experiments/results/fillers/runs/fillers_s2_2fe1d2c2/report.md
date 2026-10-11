# Run fillers_s2_2fe1d2c2

* study: `fillers`  variant: `fillers`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (48, 48)
* training: 3000 steps, 511s, final train loss 1.3248, final in-distribution val acc 0.289
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2633333333333333
* evidence_removed_acc: 0.023333333333333334
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.37
* cf_distractor_edit_rate_given_orig_correct: 0.5569620253164557
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.9533333333333334
* cf_evidence_move_rate_given_orig_correct: 0.9620253164556962
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.98
* cf_filler_resample_rate_given_orig_correct: 0.9873417721518988
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.2633333333333333
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.2
* cf_value_edit_rate_given_orig_correct: 0.26582278481012656
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.2633333333333333

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.370 | 0.317 | 0.426 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.953 | 0.923 | 0.972 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.980 | 0.957 | 0.991 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.263 | 0.217 | 0.316 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.200 | 0.159 | 0.249 | nan |
| control_evidence_removed | default | 300 | 0 | 0.023 | 0.011 | 0.047 | 10.845 |
| control_in_distribution | default | 300 | 0 | 0.263 | 0.217 | 0.316 | 1.335 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.263 | 0.217 | 0.316 | 1.335 |
| in_format | n_queries=4 | 400 | 0 | 0.295 | 0.252 | 0.341 | 1.313 |
