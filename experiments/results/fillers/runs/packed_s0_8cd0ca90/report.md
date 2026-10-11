# Run packed_s0_8cd0ca90

* study: `fillers`  variant: `packed`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 577s, final train loss 1.3276, final in-distribution val acc 0.281
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2733333333333333
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.43
* cf_distractor_edit_rate_given_orig_correct: 0.6707317073170732
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.8933333333333333
* cf_evidence_move_rate_given_orig_correct: 0.8536585365853658
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.9666666666666667
* cf_filler_resample_rate_given_orig_correct: 0.975609756097561
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.29333333333333333
* cf_key_swap_rate_given_orig_correct: 0.012195121951219513
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.19
* cf_value_edit_rate_given_orig_correct: 0.32926829268292684
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.2733333333333333

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.430 | 0.375 | 0.487 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.893 | 0.853 | 0.923 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.967 | 0.940 | 0.982 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.293 | 0.245 | 0.347 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.190 | 0.150 | 0.238 | nan |
| control_evidence_removed | default | 300 | 0 | 0.030 | 0.016 | 0.056 | 10.640 |
| control_in_distribution | default | 300 | 0 | 0.273 | 0.226 | 0.326 | 1.333 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.273 | 0.226 | 0.326 | 1.333 |
| in_format | n_queries=4 | 400 | 0 | 0.335 | 0.291 | 0.383 | 1.317 |
