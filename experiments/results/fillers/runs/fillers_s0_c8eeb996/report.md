# Run fillers_s0_c8eeb996

* study: `fillers`  variant: `fillers`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (48, 48)
* training: 3000 steps, 592s, final train loss 1.3280, final in-distribution val acc 0.359
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.28
* evidence_removed_acc: 0.043333333333333335
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.39666666666666667
* cf_distractor_edit_rate_given_orig_correct: 0.5238095238095238
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.92
* cf_evidence_move_rate_given_orig_correct: 0.9166666666666666
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9733333333333334
* cf_filler_resample_rate_given_orig_correct: 0.9761904761904762
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.24
* cf_key_swap_rate_given_orig_correct: 0.011904761904761904
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.19333333333333333
* cf_value_edit_rate_given_orig_correct: 0.2976190476190476
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.28

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.397 | 0.343 | 0.453 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.920 | 0.884 | 0.946 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.973 | 0.948 | 0.986 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.240 | 0.195 | 0.291 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.193 | 0.153 | 0.242 | nan |
| control_evidence_removed | default | 300 | 0 | 0.043 | 0.025 | 0.073 | 10.778 |
| control_in_distribution | default | 300 | 0 | 0.280 | 0.232 | 0.333 | 1.324 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.280 | 0.232 | 0.333 | 1.324 |
| in_format | n_queries=4 | 400 | 0 | 0.275 | 0.234 | 0.321 | 1.326 |
