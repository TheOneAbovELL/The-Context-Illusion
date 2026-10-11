# Run rope_s2_562ec0e7

* study: `main_pe`  variant: `rope`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 6000 steps, 1107s, final train loss 1.2419, final in-distribution val acc 0.645
* steps to val acc 0.5/0.9/0.99: 1750/None/None

## Controls (measured)

* in_distribution_acc: 0.285
* evidence_removed_acc: 0.02
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.48
* cf_distractor_edit_rate_given_orig_correct: 0.6052631578947368
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.895
* cf_evidence_move_rate_given_orig_correct: 0.9122807017543859
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9325
* cf_filler_resample_rate_given_orig_correct: 0.9122807017543859
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.2857142857142857
* cf_key_swap_rate_given_orig_correct: 0.017699115044247787
* cf_key_swap_n: 399
* cf_key_swap_shortcut_reference: 0.24794724907506863
* cf_value_edit_rate: 0.255
* cf_value_edit_rate_given_orig_correct: 0.41228070175438597
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.24857738095238094
* pos_offset_0_acc: 0.285
* pos_offset_64_acc: 0.285
* pos_offset_192_acc: 0.285

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.480 | 0.431 | 0.529 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.895 | 0.861 | 0.921 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.932 | 0.904 | 0.953 | nan |
| control_counterfactual | key_swap | 399 | 0 | 0.286 | 0.244 | 0.332 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.255 | 0.215 | 0.300 | nan |
| control_evidence_removed | default | 400 | 0 | 0.020 | 0.010 | 0.039 | 8.317 |
| control_in_distribution | default | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.520 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.520 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.520 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.520 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.840 | 0.783 | 0.884 | 0.761 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.170 | 0.124 | 0.228 | 3.227 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.115 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.510 | 0.441 | 0.578 | 2.244 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.418 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.335 | 0.273 | 0.403 | 2.580 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.986 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.002 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.449 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.095 | 0.062 | 0.144 | 2.694 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.475 | 0.407 | 0.544 | 0.720 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.120 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.285 | 0.227 | 0.351 | 1.388 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.036 |
| length | seq_len=128 | 300 | 0 | 0.257 | 0.211 | 0.309 | 2.752 |
| length | seq_len=192 | 300 | 0 | 0.250 | 0.204 | 0.302 | 4.215 |
| length | seq_len=256 | 300 | 0 | 0.250 | 0.204 | 0.302 | 4.845 |
| length | seq_len=32 | 300 | 0 | 0.330 | 0.279 | 0.385 | 1.491 |
| length | seq_len=48 | 300 | 0 | 0.340 | 0.289 | 0.395 | 1.482 |
| length | seq_len=64 | 300 | 0 | 0.307 | 0.257 | 0.361 | 1.489 |
| length | seq_len=96 | 300 | 0 | 0.300 | 0.251 | 0.354 | 1.819 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.205 | 0.155 | 0.266 | 4.274 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.310 | 0.250 | 0.377 | 1.920 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 4.945 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.135 | 0.094 | 0.189 | 6.696 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.120 | 0.082 | 0.172 | 6.538 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.125 | 0.086 | 0.178 | 6.866 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.315 | 0.255 | 0.382 | 1.443 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.255 | 0.200 | 0.320 | 1.543 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.305 | 0.245 | 0.372 | 1.482 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.335 | 0.273 | 0.403 | 1.859 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.335 | 0.273 | 0.403 | 1.956 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.410 | 0.344 | 0.479 | 1.729 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.225 | 0.173 | 0.288 | 3.131 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.110 | 0.074 | 0.161 | 4.875 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.340 | 0.278 | 0.408 | 2.744 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.360 | 0.297 | 0.429 | 2.982 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.175 | 0.129 | 0.234 | 5.136 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.155 | 0.111 | 0.212 | 6.084 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.165 | 0.120 | 0.223 | 6.465 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.240 | 0.186 | 0.304 | 1.583 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.305 | 0.245 | 0.372 | 1.506 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.300 | 0.241 | 0.367 | 1.463 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.340 | 0.278 | 0.408 | 1.471 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.255 | 0.200 | 0.320 | 1.645 |
| lures | n_lures=0 | 300 | 0 | 0.217 | 0.174 | 0.267 | 1.828 |
| lures | n_lures=1 | 300 | 0 | 0.240 | 0.195 | 0.291 | 1.776 |
| lures | n_lures=2 | 300 | 0 | 0.240 | 0.195 | 0.291 | 1.794 |
| lures | n_lures=4 | 300 | 0 | 0.193 | 0.153 | 0.242 | 1.782 |
| repeated_keys | repeat_distractor_keys=False | 300 | 0 | 0.127 | 0.094 | 0.169 | 2.673 |
| repeated_keys | repeat_distractor_keys=True | 300 | 0 | 0.107 | 0.077 | 0.147 | 2.692 |
