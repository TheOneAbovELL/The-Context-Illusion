# Run separate_keylast_s0_02877c6d

* study: `value_type`  variant: `separate_keylast`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 300s, final train loss 1.3322, final in-distribution val acc 0.324
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2866666666666667
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.3466666666666667
* cf_distractor_edit_rate_given_orig_correct: 0.5232558139534884
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.9433333333333334
* cf_evidence_move_rate_given_orig_correct: 0.9418604651162791
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9733333333333334
* cf_filler_resample_rate_given_orig_correct: 0.9651162790697675
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.27
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.26
* cf_value_edit_rate_given_orig_correct: 0.27906976744186046
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.2866666666666667

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.347 | 0.295 | 0.402 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.943 | 0.911 | 0.964 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.973 | 0.948 | 0.986 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.270 | 0.223 | 0.323 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.260 | 0.214 | 0.312 | nan |
| control_evidence_removed | default | 300 | 0 | 0.030 | 0.016 | 0.056 | 12.406 |
| control_in_distribution | default | 300 | 0 | 0.287 | 0.238 | 0.340 | 1.332 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.287 | 0.238 | 0.340 | 1.332 |
| in_format | n_queries=4 | 400 | 0 | 0.263 | 0.222 | 0.308 | 1.350 |
