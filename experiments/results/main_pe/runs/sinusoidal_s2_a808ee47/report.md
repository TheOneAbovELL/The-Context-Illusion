# Run sinusoidal_s2_a808ee47

* study: `main_pe`  variant: `sinusoidal`  seed: 2
* positional method: `sinusoidal`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 397s, final train loss 2.0816, final in-distribution val acc 0.158
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.215
* evidence_removed_acc: 0.035
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4875
* cf_distractor_edit_rate_given_orig_correct: 0.7209302325581395
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.895
* cf_evidence_move_rate_given_orig_correct: 0.9302325581395349
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.895
* cf_filler_resample_rate_given_orig_correct: 0.9418604651162791
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.19
* cf_key_swap_rate_given_orig_correct: 0.011627906976744186
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1075
* cf_value_edit_rate_given_orig_correct: 0.1511627906976744
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.215
* pos_offset_64_acc: 0.2025
* pos_offset_192_acc: 0.2125

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.487 | 0.439 | 0.536 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.895 | 0.861 | 0.921 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.895 | 0.861 | 0.921 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.190 | 0.155 | 0.231 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.107 | 0.081 | 0.142 | nan |
| control_evidence_removed | default | 400 | 0 | 0.035 | 0.021 | 0.058 | 6.316 |
| control_in_distribution | default | 400 | 0 | 0.215 | 0.178 | 0.258 | 2.025 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.215 | 0.178 | 0.258 | 2.025 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.212 | 0.175 | 0.255 | 2.144 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.203 | 0.166 | 0.245 | 2.108 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.580 | 0.511 | 0.646 | 1.308 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.214 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.055 | 0.031 | 0.096 | 3.673 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.605 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.085 | 0.054 | 0.132 | 4.263 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.250 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.090 | 0.058 | 0.138 | 2.843 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.720 | 0.654 | 0.778 | 0.857 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.105 | 0.070 | 0.155 | 3.175 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.620 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.370 | 0.306 | 0.439 | 1.421 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.065 | 0.038 | 0.108 | 4.188 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.119 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.115 | 0.078 | 0.167 | 2.758 |
| length | seq_len=128 | 300 | 0 | 0.180 | 0.141 | 0.227 | 2.177 |
| length | seq_len=192 | 300 | 0 | 0.213 | 0.171 | 0.263 | 2.258 |
| length | seq_len=256 | 300 | 0 | 0.187 | 0.147 | 0.235 | 2.447 |
| length | seq_len=32 | 300 | 0 | 0.173 | 0.135 | 0.220 | 2.059 |
| length | seq_len=48 | 300 | 0 | 0.180 | 0.141 | 0.227 | 2.079 |
| length | seq_len=64 | 300 | 0 | 0.193 | 0.153 | 0.242 | 2.095 |
| length | seq_len=96 | 300 | 0 | 0.177 | 0.138 | 0.224 | 2.122 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.150 | 0.107 | 0.206 | 2.243 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.164 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.135 | 0.094 | 0.189 | 2.324 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.150 | 0.107 | 0.206 | 2.628 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.590 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.781 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.042 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.049 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.140 | 0.099 | 0.195 | 2.215 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.230 | 0.177 | 0.293 | 2.142 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.106 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.172 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.138 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.988 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.389 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.403 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.371 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.477 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.316 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.123 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.255 | 0.200 | 0.320 | 2.005 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.060 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.147 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.110 | 0.074 | 0.161 | 2.896 |
