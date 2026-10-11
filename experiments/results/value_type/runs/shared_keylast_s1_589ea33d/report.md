# Run shared_keylast_s1_589ea33d

* study: `value_type`  variant: `shared_keylast`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 616s, final train loss 0.0071, final in-distribution val acc 1.000
* steps to val acc 0.5/0.9/0.99: 300/500/1000

## Controls (measured)

* in_distribution_acc: 1.0
* evidence_removed_acc: 0.04
* chance_acc: 0.03125
* cf_distractor_edit_rate: 1.0
* cf_distractor_edit_rate_given_orig_correct: 1.0
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 1.0
* cf_evidence_move_rate_given_orig_correct: 1.0
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 1.0
* cf_filler_resample_rate_given_orig_correct: 1.0
* cf_filler_resample_n: 300
* cf_key_swap_rate: 1.0
* cf_key_swap_rate_given_orig_correct: 1.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 1.0
* cf_value_edit_rate_given_orig_correct: 1.0
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 1.0

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
| control_counterfactual | evidence_move | 300 | 0 | 1.000 | 0.987 | 1.000 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 1.000 | 0.987 | 1.000 | nan |
| control_counterfactual | key_swap | 300 | 0 | 1.000 | 0.987 | 1.000 | nan |
| control_counterfactual | value_edit | 300 | 0 | 1.000 | 0.987 | 1.000 | nan |
| control_evidence_removed | default | 300 | 0 | 0.040 | 0.023 | 0.069 | 11.663 |
| control_in_distribution | default | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| control_position_offset | pos_offset=0 | 300 | 0 | 1.000 | 0.987 | 1.000 | 0.000 |
| in_format | n_queries=4 | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.003 |
