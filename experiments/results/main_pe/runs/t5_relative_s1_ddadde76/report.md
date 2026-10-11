# Run t5_relative_s1_ddadde76

* study: `main_pe`  variant: `t5_relative`  seed: 1
* positional method: `t5_relative`; layers=2, d_model=64, heads=2; parameters=116800 (positional: 64)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 370s, final train loss 2.0458, final in-distribution val acc 0.213
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2325
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.475
* cf_distractor_edit_rate_given_orig_correct: 0.6021505376344086
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.94
* cf_evidence_move_rate_given_orig_correct: 0.9247311827956989
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9825
* cf_filler_resample_rate_given_orig_correct: 0.989247311827957
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.185
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1125
* cf_value_edit_rate_given_orig_correct: 0.17204301075268819
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.2325
* pos_offset_64_acc: 0.2325
* pos_offset_192_acc: 0.2325

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.475 | 0.427 | 0.524 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.940 | 0.912 | 0.959 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.983 | 0.964 | 0.991 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.185 | 0.150 | 0.226 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.113 | 0.085 | 0.147 | nan |
| control_evidence_removed | default | 400 | 0 | 0.030 | 0.017 | 0.052 | 6.765 |
| control_in_distribution | default | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.038 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.038 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.038 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.038 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.660 | 0.592 | 0.722 | 1.187 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.188 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.045 | 0.024 | 0.083 | 4.062 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.511 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.045 | 0.024 | 0.083 | 4.355 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.245 | 0.191 | 0.309 | 2.004 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.120 | 0.082 | 0.172 | 2.778 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.710 | 0.644 | 0.768 | 0.902 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.095 | 0.062 | 0.144 | 3.242 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.041 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.350 | 0.287 | 0.418 | 1.396 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 4.379 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.009 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.774 |
| length | seq_len=128 | 300 | 0 | 0.160 | 0.123 | 0.206 | 2.079 |
| length | seq_len=192 | 300 | 0 | 0.177 | 0.138 | 0.224 | 2.109 |
| length | seq_len=256 | 300 | 0 | 0.173 | 0.135 | 0.220 | 2.149 |
| length | seq_len=32 | 300 | 0 | 0.203 | 0.162 | 0.252 | 2.080 |
| length | seq_len=48 | 300 | 0 | 0.203 | 0.162 | 0.252 | 2.060 |
| length | seq_len=64 | 300 | 0 | 0.203 | 0.162 | 0.252 | 2.049 |
| length | seq_len=96 | 300 | 0 | 0.187 | 0.147 | 0.235 | 2.074 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.029 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.038 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.041 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.123 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.123 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.130 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.029 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.034 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.024 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.020 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.021 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.092 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.250 | 0.195 | 0.314 | 1.957 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.360 | 0.297 | 0.429 | 1.943 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.087 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.085 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.082 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.163 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.295 | 0.236 | 0.362 | 2.018 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.109 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.205 | 0.155 | 0.266 | 1.962 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.230 | 0.177 | 0.293 | 1.953 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.230 | 0.177 | 0.293 | 1.964 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.365 | 0.301 | 0.434 | 1.982 |
