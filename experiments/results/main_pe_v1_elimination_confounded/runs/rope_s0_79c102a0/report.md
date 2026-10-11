# Run rope_s0_79c102a0

* study: `main_pe`  variant: `rope`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 6000 steps, 1107s, final train loss 1.3072, final in-distribution val acc 0.604
* steps to val acc 0.5/0.9/0.99: 3750/None/None

## Controls (measured)

* in_distribution_acc: 0.2725
* evidence_removed_acc: 0.0275
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.465
* cf_distractor_edit_rate_given_orig_correct: 0.6422018348623854
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.8875
* cf_evidence_move_rate_given_orig_correct: 0.8256880733944955
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9325
* cf_filler_resample_rate_given_orig_correct: 0.9724770642201835
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.2531328320802005
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 399
* cf_key_swap_shortcut_reference: 0.24794724907506863
* cf_value_edit_rate: 0.21
* cf_value_edit_rate_given_orig_correct: 0.3486238532110092
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.24857738095238094
* pos_offset_0_acc: 0.2725
* pos_offset_64_acc: 0.2725
* pos_offset_192_acc: 0.2725

## Validity checks

* eval_examples_checked: 11500
* eval_examples_with_violations: 0
* n_train_sampled: 5000
* n_eval: 11500
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_counterfactual | distractor_edit | 400 | 0 | 0.465 | 0.417 | 0.514 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.887 | 0.853 | 0.915 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.932 | 0.904 | 0.953 | nan |
| control_counterfactual | key_swap | 399 | 0 | 0.253 | 0.213 | 0.298 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.210 | 0.173 | 0.253 | nan |
| control_evidence_removed | default | 400 | 0 | 0.028 | 0.015 | 0.049 | 8.692 |
| control_in_distribution | default | 400 | 0 | 0.273 | 0.231 | 0.318 | 1.550 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.273 | 0.231 | 0.318 | 1.550 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.273 | 0.231 | 0.318 | 1.550 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.273 | 0.231 | 0.318 | 1.550 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.550 | 0.481 | 0.617 | 2.268 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.150 | 0.107 | 0.206 | 3.373 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.130 | 0.090 | 0.184 | 3.406 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.415 | 0.349 | 0.484 | 3.386 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.808 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.300 | 0.241 | 0.367 | 4.049 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.185 | 0.137 | 0.245 | 3.744 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.140 | 0.099 | 0.195 | 2.452 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.717 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.550 | 0.481 | 0.617 | 0.738 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.110 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.260 | 0.204 | 0.325 | 1.409 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.052 |
| length | seq_len=128 | 300 | 0 | 0.273 | 0.226 | 0.326 | 3.808 |
| length | seq_len=192 | 300 | 0 | 0.167 | 0.129 | 0.213 | 4.745 |
| length | seq_len=256 | 300 | 0 | 0.113 | 0.082 | 0.154 | 4.813 |
| length | seq_len=32 | 300 | 0 | 0.317 | 0.267 | 0.371 | 1.503 |
| length | seq_len=48 | 300 | 0 | 0.283 | 0.235 | 0.337 | 1.513 |
| length | seq_len=64 | 300 | 0 | 0.290 | 0.242 | 0.344 | 1.524 |
| length | seq_len=96 | 300 | 0 | 0.293 | 0.245 | 0.347 | 2.209 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.340 | 0.278 | 0.408 | 3.626 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.270 | 0.213 | 0.335 | 2.967 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.315 | 0.255 | 0.382 | 4.011 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.145 | 0.103 | 0.200 | 4.780 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.150 | 0.107 | 0.206 | 4.814 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.185 | 0.137 | 0.245 | 4.708 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.448 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.265 | 0.209 | 0.330 | 1.555 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.290 | 0.232 | 0.356 | 1.503 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.170 | 0.124 | 0.228 | 4.419 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.240 | 0.186 | 0.304 | 4.309 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.305 | 0.245 | 0.372 | 3.025 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.325 | 0.264 | 0.393 | 3.756 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.335 | 0.273 | 0.403 | 4.185 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.240 | 0.186 | 0.304 | 3.736 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.165 | 0.120 | 0.223 | 4.284 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.065 | 0.038 | 0.108 | 5.269 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.195 | 0.146 | 0.255 | 4.552 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.220 | 0.168 | 0.282 | 4.423 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.240 | 0.186 | 0.304 | 1.627 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.290 | 0.232 | 0.356 | 1.493 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.320 | 0.259 | 0.388 | 1.469 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.350 | 0.287 | 0.418 | 1.413 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.220 | 0.168 | 0.282 | 1.653 |
| lures | n_lures=0 | 300 | 0 | 0.230 | 0.186 | 0.281 | 1.776 |
| lures | n_lures=1 | 300 | 0 | 0.177 | 0.138 | 0.224 | 1.820 |
| lures | n_lures=2 | 300 | 0 | 0.193 | 0.153 | 0.242 | 1.836 |
| lures | n_lures=4 | 300 | 0 | 0.237 | 0.192 | 0.288 | 1.823 |
| repeated_keys | repeat_distractor_keys=False | 300 | 0 | 0.147 | 0.111 | 0.191 | 2.681 |
| repeated_keys | repeat_distractor_keys=True | 300 | 0 | 0.123 | 0.091 | 0.165 | 2.695 |
