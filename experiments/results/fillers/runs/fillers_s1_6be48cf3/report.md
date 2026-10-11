# Run fillers_s1_6be48cf3

* study: `fillers`  variant: `fillers`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (48, 48)
* training: 3000 steps, 634s, final train loss 1.3227, final in-distribution val acc 0.254
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.24666666666666667
* evidence_removed_acc: 0.02666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4033333333333333
* cf_distractor_edit_rate_given_orig_correct: 0.5405405405405406
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.95
* cf_evidence_move_rate_given_orig_correct: 0.9594594594594594
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9766666666666667
* cf_filler_resample_rate_given_orig_correct: 0.972972972972973
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.2966666666666667
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.21666666666666667
* cf_value_edit_rate_given_orig_correct: 0.36486486486486486
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.24666666666666667

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.403 | 0.349 | 0.460 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.950 | 0.919 | 0.969 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.977 | 0.953 | 0.989 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.297 | 0.248 | 0.351 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.217 | 0.174 | 0.267 | nan |
| control_evidence_removed | default | 300 | 0 | 0.027 | 0.014 | 0.052 | 10.797 |
| control_in_distribution | default | 300 | 0 | 0.247 | 0.201 | 0.298 | 1.335 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.247 | 0.201 | 0.298 | 1.335 |
| in_format | n_queries=4 | 400 | 0 | 0.323 | 0.279 | 0.370 | 1.317 |
