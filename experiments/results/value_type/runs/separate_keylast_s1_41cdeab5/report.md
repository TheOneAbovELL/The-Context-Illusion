# Run separate_keylast_s1_41cdeab5

* study: `value_type`  variant: `separate_keylast`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 184s, final train loss 1.3283, final in-distribution val acc 0.293
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.3233333333333333
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.36666666666666664
* cf_distractor_edit_rate_given_orig_correct: 0.5154639175257731
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.9566666666666667
* cf_evidence_move_rate_given_orig_correct: 0.9484536082474226
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9766666666666667
* cf_filler_resample_rate_given_orig_correct: 0.979381443298969
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.25
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.23
* cf_value_edit_rate_given_orig_correct: 0.30927835051546393
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
| control_counterfactual | distractor_edit | 300 | 0 | 0.367 | 0.314 | 0.423 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.957 | 0.927 | 0.975 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.977 | 0.953 | 0.989 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.250 | 0.204 | 0.302 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.230 | 0.186 | 0.281 | nan |
| control_evidence_removed | default | 300 | 0 | 0.030 | 0.016 | 0.056 | 12.368 |
| control_in_distribution | default | 300 | 0 | 0.323 | 0.273 | 0.378 | 1.317 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.323 | 0.273 | 0.378 | 1.317 |
| in_format | n_queries=4 | 400 | 0 | 0.278 | 0.236 | 0.323 | 1.347 |
