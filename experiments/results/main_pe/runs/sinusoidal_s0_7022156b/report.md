# Run sinusoidal_s0_7022156b

* study: `main_pe`  variant: `sinusoidal`  seed: 0
* positional method: `sinusoidal`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 392s, final train loss 2.2102, final in-distribution val acc 0.203
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2
* evidence_removed_acc: 0.0325
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.5
* cf_distractor_edit_rate_given_orig_correct: 0.65
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.8025
* cf_evidence_move_rate_given_orig_correct: 0.8
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.8675
* cf_filler_resample_rate_given_orig_correct: 0.9
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.1575
* cf_key_swap_rate_given_orig_correct: 0.0375
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1075
* cf_value_edit_rate_given_orig_correct: 0.15
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.2
* pos_offset_64_acc: 0.195
* pos_offset_192_acc: 0.2025

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.500 | 0.451 | 0.549 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.802 | 0.761 | 0.839 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.868 | 0.831 | 0.897 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.158 | 0.125 | 0.196 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.107 | 0.081 | 0.142 | nan |
| control_evidence_removed | default | 400 | 0 | 0.033 | 0.019 | 0.055 | 5.791 |
| control_in_distribution | default | 400 | 0 | 0.200 | 0.164 | 0.242 | 2.183 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.200 | 0.164 | 0.242 | 2.183 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.203 | 0.166 | 0.245 | 2.245 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.195 | 0.159 | 0.237 | 2.212 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.610 | 0.541 | 0.675 | 1.081 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.100 | 0.066 | 0.149 | 3.422 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.660 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.325 | 0.264 | 0.393 | 1.590 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 4.087 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.233 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.100 | 0.066 | 0.149 | 2.863 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.645 | 0.577 | 0.708 | 0.892 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.387 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.654 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.514 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.015 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.197 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.110 | 0.074 | 0.161 | 2.850 |
| length | seq_len=128 | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.195 |
| length | seq_len=192 | 300 | 0 | 0.177 | 0.138 | 0.224 | 2.271 |
| length | seq_len=256 | 300 | 0 | 0.180 | 0.141 | 0.227 | 2.348 |
| length | seq_len=32 | 300 | 0 | 0.217 | 0.174 | 0.267 | 2.136 |
| length | seq_len=48 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.155 |
| length | seq_len=64 | 300 | 0 | 0.223 | 0.180 | 0.274 | 2.162 |
| length | seq_len=96 | 300 | 0 | 0.223 | 0.180 | 0.274 | 2.146 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.100 | 0.066 | 0.149 | 2.374 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.272 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.100 | 0.066 | 0.149 | 2.491 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.080 | 0.050 | 0.126 | 2.798 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.115 | 0.078 | 0.167 | 2.601 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.074 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.113 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.300 | 0.241 | 0.367 | 2.068 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.534 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.145 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.086 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.244 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.273 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.149 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.245 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.296 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.396 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.573 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.518 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.186 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.050 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.104 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.242 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.065 | 0.038 | 0.108 | 3.017 |
