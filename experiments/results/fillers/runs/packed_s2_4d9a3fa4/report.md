# Run packed_s2_4d9a3fa4

* study: `fillers`  variant: `packed`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 24)
* training: 3000 steps, 334s, final train loss 1.3245, final in-distribution val acc 0.273
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.30666666666666664
* evidence_removed_acc: 0.03666666666666667
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.41
* cf_distractor_edit_rate_given_orig_correct: 0.5760869565217391
* cf_distractor_edit_n: 300
* cf_evidence_move_rate: 0.9066666666666666
* cf_evidence_move_rate_given_orig_correct: 0.8695652173913043
* cf_evidence_move_n: 300
* cf_filler_resample_rate: 0.97
* cf_filler_resample_rate_given_orig_correct: 0.9456521739130435
* cf_filler_resample_n: 300
* cf_key_swap_rate: 0.25333333333333335
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 300
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.24
* cf_value_edit_rate_given_orig_correct: 0.358695652173913
* cf_value_edit_n: 300
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.30666666666666664

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
| control_counterfactual | distractor_edit | 300 | 0 | 0.410 | 0.356 | 0.466 | nan |
| control_counterfactual | evidence_move | 300 | 0 | 0.907 | 0.868 | 0.935 | nan |
| control_counterfactual | filler_resample | 300 | 0 | 0.970 | 0.944 | 0.984 | nan |
| control_counterfactual | key_swap | 300 | 0 | 0.253 | 0.207 | 0.305 | nan |
| control_counterfactual | value_edit | 300 | 0 | 0.240 | 0.195 | 0.291 | nan |
| control_evidence_removed | default | 300 | 0 | 0.037 | 0.021 | 0.064 | 10.667 |
| control_in_distribution | default | 300 | 0 | 0.307 | 0.257 | 0.361 | 1.329 |
| control_position_offset | pos_offset=0 | 300 | 0 | 0.307 | 0.257 | 0.361 | 1.329 |
| in_format | n_queries=4 | 400 | 0 | 0.312 | 0.269 | 0.360 | 1.319 |
