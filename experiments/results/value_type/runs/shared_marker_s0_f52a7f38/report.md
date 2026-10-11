# Run shared_marker_s0_f52a7f38

* study: `value_type`  variant: `shared_marker`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 194s, final train loss 1.7309, final in-distribution val acc 0.320
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.30333333333333334
* evidence_removed_acc: 0.02666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.49666666666666665
* cf_distractor_edit_rate_given_orig_correct: 0.6153846153846154
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.7533333333333333
* cf_evidence_move_rate_given_orig_correct: 0.6813186813186813
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.96
* cf_filler_resample_rate_given_orig_correct: 0.9560439560439561
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.27666666666666667
* cf_key_swap_rate_given_orig_correct: 0.054945054945054944
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.2866666666666667
* cf_value_edit_rate_given_orig_correct: 0.4835164835164835
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.30333333333333334

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.497 | 0.440 | 0.553 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.753 | 0.702 | 0.799 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.960 | 0.931 | 0.977 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.277 | 0.229 | 0.330 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.287 | 0.238 | 0.340 | nan |
| control_evidence_removed | default | 300 | 0 | 0.027 | 0.014 | 0.052 | 7.596 |
| control_in_distribution | default | 300 | 0 | 0.303 | 0.254 | 0.358 | 1.575 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.303 | 0.254 | 0.358 | 1.575 |
| in_format | n_queries=4 | 400 | 0 | 0.307 | 0.264 | 0.354 | 1.573 |
