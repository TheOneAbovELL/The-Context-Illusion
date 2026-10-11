# Run rope_s2_7938b6b2

* study: `main_pe`  variant: `rope`  seed: 2
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 475s, final train loss 1.5366, final in-distribution val acc 0.260
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.27
* evidence_removed_acc: 0.025
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.39
* cf_distractor_edit_rate_given_orig_correct: 0.48148148148148145
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.83
* cf_evidence_move_rate_given_orig_correct: 0.8055555555555556
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.96
* cf_filler_resample_rate_given_orig_correct: 0.9722222222222222
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.2675
* cf_key_swap_rate_given_orig_correct: 0.037037037037037035
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.225
* cf_value_edit_rate_given_orig_correct: 0.2962962962962963
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.27
* pos_offset_64_acc: 0.27
* pos_offset_192_acc: 0.27

## Validity checks

* eval_examples_checked: 9700
* eval_examples_with_violations: 0
* n_train_sampled: 5000
* n_eval: 9700
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_counterfactual | distractor_edit | 400 | 0 | 0.390 | 0.343 | 0.439 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.830 | 0.790 | 0.864 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.960 | 0.936 | 0.975 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.268 | 0.226 | 0.313 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.225 | 0.187 | 0.268 | nan |
| control_evidence_removed | default | 400 | 0 | 0.025 | 0.014 | 0.045 | 6.755 |
| control_in_distribution | default | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.477 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.477 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.477 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.270 | 0.229 | 0.316 | 1.477 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.285 | 0.227 | 0.351 | 2.667 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.070 | 0.042 | 0.114 | 4.442 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.115 | 0.078 | 0.167 | 4.541 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.220 | 0.168 | 0.282 | 3.038 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.095 | 0.062 | 0.144 | 4.615 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.869 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.150 | 0.107 | 0.206 | 4.006 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.995 | 0.972 | 0.999 | 0.914 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.165 | 0.120 | 0.223 | 3.314 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.755 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.460 | 0.392 | 0.529 | 0.848 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.495 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.280 | 0.222 | 0.346 | 1.523 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.419 |
| length | seq_len=128 | 300 | 0 | 0.200 | 0.159 | 0.249 | 2.858 |
| length | seq_len=192 | 300 | 0 | 0.097 | 0.068 | 0.135 | 3.786 |
| length | seq_len=256 | 300 | 0 | 0.127 | 0.094 | 0.169 | 3.758 |
| length | seq_len=32 | 300 | 0 | 0.307 | 0.257 | 0.361 | 1.587 |
| length | seq_len=48 | 300 | 0 | 0.290 | 0.242 | 0.344 | 1.520 |
| length | seq_len=64 | 300 | 0 | 0.263 | 0.217 | 0.316 | 1.456 |
| length | seq_len=96 | 300 | 0 | 0.257 | 0.211 | 0.309 | 1.626 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 4.313 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.150 | 0.107 | 0.206 | 3.070 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.050 | 0.027 | 0.090 | 4.200 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.025 | 0.011 | 0.057 | 4.673 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.035 | 0.017 | 0.070 | 4.717 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.035 | 0.017 | 0.070 | 4.687 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.275 | 0.218 | 0.341 | 1.401 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.270 | 0.213 | 0.335 | 1.468 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.295 | 0.236 | 0.362 | 1.406 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.545 | 0.476 | 0.613 | 1.494 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.786 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.747 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.110 | 0.074 | 0.161 | 3.116 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.060 | 0.035 | 0.102 | 3.970 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.415 | 0.349 | 0.484 | 2.181 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.965 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.714 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.070 | 0.042 | 0.114 | 4.407 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.394 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.285 | 0.227 | 0.351 | 1.412 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.260 | 0.204 | 0.325 | 1.430 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.255 | 0.200 | 0.320 | 1.425 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.290 | 0.232 | 0.356 | 1.415 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.220 | 0.168 | 0.282 | 1.533 |
