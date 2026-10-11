# Run rope_s1_fdbe0427

* study: `main_pe`  variant: `rope`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 6000 steps, 1107s, final train loss 1.2638, final in-distribution val acc 0.658
* steps to val acc 0.5/0.9/0.99: 3000/None/None

## Controls (measured)

* in_distribution_acc: 0.27
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.455
* cf_distractor_edit_rate_given_orig_correct: 0.6296296296296297
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.83
* cf_evidence_move_rate_given_orig_correct: 0.8148148148148148
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9625
* cf_filler_resample_rate_given_orig_correct: 0.9722222222222222
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.2781954887218045
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 399
* cf_key_swap_shortcut_reference: 0.24794724907506863
* cf_value_edit_rate: 0.2325
* cf_value_edit_rate_given_orig_correct: 0.37962962962962965
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.24857738095238094
* pos_offset_0_acc: 0.27
* pos_offset_64_acc: 0.27
* pos_offset_192_acc: 0.27

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.455 | 0.407 | 0.504 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.830 | 0.790 | 0.864 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.963 | 0.939 | 0.977 | nan |
| control_counterfactual | key_swap | 399 | 0 | 0.278 | 0.237 | 0.324 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.233 | 0.194 | 0.276 | nan |
| control_evidence_removed | default | 400 | 0 | 0.030 | 0.017 | 0.052 | 8.702 |
| control_in_distribution | default | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.489 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.489 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.489 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.489 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.930 | 0.886 | 0.958 | 0.286 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.140 | 0.099 | 0.195 | 3.043 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.219 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.520 | 0.451 | 0.588 | 1.694 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.100 | 0.066 | 0.149 | 3.567 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.255 | 0.200 | 0.320 | 2.500 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.760 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.140 | 0.099 | 0.195 | 2.440 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.095 | 0.062 | 0.144 | 2.740 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.520 | 0.451 | 0.588 | 0.702 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.201 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.265 | 0.209 | 0.330 | 1.462 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.058 |
| length | seq_len=128 | 300 | 0 | 0.313 | 0.263 | 0.368 | 2.334 |
| length | seq_len=192 | 300 | 0 | 0.247 | 0.201 | 0.298 | 3.380 |
| length | seq_len=256 | 300 | 0 | 0.147 | 0.111 | 0.191 | 5.817 |
| length | seq_len=32 | 300 | 0 | 0.310 | 0.260 | 0.364 | 1.493 |
| length | seq_len=48 | 300 | 0 | 0.293 | 0.245 | 0.347 | 1.485 |
| length | seq_len=64 | 300 | 0 | 0.323 | 0.273 | 0.378 | 1.504 |
| length | seq_len=96 | 300 | 0 | 0.290 | 0.242 | 0.344 | 1.781 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.210 | 0.159 | 0.272 | 3.222 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.335 | 0.273 | 0.403 | 1.797 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 3.386 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.160 | 0.116 | 0.217 | 6.769 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.160 | 0.116 | 0.217 | 6.851 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.165 | 0.120 | 0.223 | 6.444 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.345 | 0.283 | 0.413 | 1.422 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.245 | 0.191 | 0.309 | 1.535 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.275 | 0.218 | 0.341 | 1.527 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.295 | 0.236 | 0.362 | 1.992 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.365 | 0.301 | 0.434 | 1.854 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.450 | 0.383 | 0.519 | 1.497 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.868 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.160 | 0.116 | 0.217 | 3.493 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.385 | 0.320 | 0.454 | 2.977 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.170 | 0.124 | 0.228 | 4.318 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.120 | 0.082 | 0.172 | 7.304 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.140 | 0.099 | 0.195 | 7.417 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.130 | 0.090 | 0.184 | 7.302 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.215 | 0.164 | 0.277 | 1.552 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.442 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.355 | 0.292 | 0.423 | 1.408 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.350 | 0.287 | 0.418 | 1.432 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.265 | 0.209 | 0.330 | 1.589 |
| lures | n_lures=0 | 300 | 0 | 0.223 | 0.180 | 0.274 | 1.765 |
| lures | n_lures=1 | 300 | 0 | 0.253 | 0.207 | 0.305 | 1.741 |
| lures | n_lures=2 | 300 | 0 | 0.197 | 0.156 | 0.245 | 1.802 |
| lures | n_lures=4 | 300 | 0 | 0.213 | 0.171 | 0.263 | 1.835 |
| repeated_keys | repeat_distractor_keys=False | 300 | 0 | 0.163 | 0.126 | 0.209 | 2.694 |
| repeated_keys | repeat_distractor_keys=True | 300 | 0 | 0.100 | 0.071 | 0.139 | 2.752 |
