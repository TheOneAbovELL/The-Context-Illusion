# Run sinusoidal_s1_98fe67d9

* study: `main_pe`  variant: `sinusoidal`  seed: 1
* positional method: `sinusoidal`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 391s, final train loss 2.1613, final in-distribution val acc 0.189
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.22
* evidence_removed_acc: 0.0275
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.5275
* cf_distractor_edit_rate_given_orig_correct: 0.6363636363636364
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.8575
* cf_evidence_move_rate_given_orig_correct: 0.8409090909090909
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9
* cf_filler_resample_rate_given_orig_correct: 0.8977272727272727
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.1825
* cf_key_swap_rate_given_orig_correct: 0.011363636363636364
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1275
* cf_value_edit_rate_given_orig_correct: 0.18181818181818182
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.22
* pos_offset_64_acc: 0.185
* pos_offset_192_acc: 0.2

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.527 | 0.479 | 0.576 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.858 | 0.820 | 0.888 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.900 | 0.867 | 0.926 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.182 | 0.148 | 0.223 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.128 | 0.098 | 0.164 | nan |
| control_evidence_removed | default | 400 | 0 | 0.028 | 0.015 | 0.049 | 6.142 |
| control_in_distribution | default | 400 | 0 | 0.220 | 0.182 | 0.263 | 2.103 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.220 | 0.182 | 0.263 | 2.103 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.200 | 0.164 | 0.242 | 2.240 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.185 | 0.150 | 0.226 | 2.195 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.690 | 0.623 | 0.750 | 1.165 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.649 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.075 | 0.046 | 0.120 | 4.297 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.285 | 0.227 | 0.351 | 1.719 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.754 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.229 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.125 | 0.086 | 0.178 | 2.906 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.755 | 0.691 | 0.809 | 0.914 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.405 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.055 | 0.031 | 0.096 | 3.995 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.315 | 0.255 | 0.382 | 1.480 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 4.482 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.132 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.150 | 0.107 | 0.206 | 2.886 |
| length | seq_len=128 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.216 |
| length | seq_len=192 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.493 |
| length | seq_len=256 | 300 | 0 | 0.187 | 0.147 | 0.235 | 2.720 |
| length | seq_len=32 | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.080 |
| length | seq_len=48 | 300 | 0 | 0.170 | 0.132 | 0.217 | 2.080 |
| length | seq_len=64 | 300 | 0 | 0.177 | 0.138 | 0.224 | 2.125 |
| length | seq_len=96 | 300 | 0 | 0.180 | 0.141 | 0.227 | 2.152 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.362 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.263 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.140 | 0.099 | 0.195 | 2.424 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.125 | 0.086 | 0.178 | 2.935 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.775 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.150 | 0.107 | 0.206 | 3.208 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.083 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.031 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.348 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.103 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.265 | 0.209 | 0.330 | 2.068 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.206 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.213 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.070 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.258 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.524 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.567 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.741 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.140 | 0.099 | 0.195 | 3.550 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.084 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.270 | 0.213 | 0.335 | 1.945 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.047 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.113 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.085 | 0.054 | 0.132 | 2.795 |
