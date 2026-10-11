# Run learned_s2_448772ac

* study: `main_pe`  variant: `learned`  seed: 2
* positional method: `learned`; layers=2, d_model=64, heads=2; parameters=149504 (positional: 32768)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 374s, final train loss 2.0761, final in-distribution val acc 0.178
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.185
* evidence_removed_acc: 0.0275
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4975
* cf_distractor_edit_rate_given_orig_correct: 0.7162162162162162
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.825
* cf_evidence_move_rate_given_orig_correct: 0.7972972972972973
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.8525
* cf_filler_resample_rate_given_orig_correct: 0.8378378378378378
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.17
* cf_key_swap_rate_given_orig_correct: 0.02702702702702703
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1275
* cf_value_edit_rate_given_orig_correct: 0.1891891891891892
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.185
* pos_offset_64_acc: 0.1875
* pos_offset_192_acc: 0.1875

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.497 | 0.449 | 0.546 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.825 | 0.785 | 0.859 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.853 | 0.814 | 0.884 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.170 | 0.136 | 0.210 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.128 | 0.098 | 0.164 | nan |
| control_evidence_removed | default | 400 | 0 | 0.028 | 0.015 | 0.049 | 5.984 |
| control_in_distribution | default | 400 | 0 | 0.185 | 0.150 | 0.226 | 2.066 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.185 | 0.150 | 0.226 | 2.066 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.188 | 0.152 | 0.229 | 2.232 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.188 | 0.152 | 0.229 | 2.227 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.605 | 0.536 | 0.670 | 1.456 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.110 | 0.074 | 0.161 | 3.310 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.935 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.300 | 0.241 | 0.367 | 2.139 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.075 | 0.046 | 0.120 | 5.237 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.400 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.115 | 0.078 | 0.167 | 3.035 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.725 | 0.659 | 0.782 | 0.851 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.395 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.060 | 0.035 | 0.102 | 4.013 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.573 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 4.597 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.158 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.846 |
| length | seq_len=128 | 300 | 0 | 0.200 | 0.159 | 0.249 | 2.482 |
| length | seq_len=192 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.972 |
| length | seq_len=256 | 300 | 0 | 0.157 | 0.120 | 0.202 | 3.089 |
| length | seq_len=32 | 300 | 0 | 0.200 | 0.159 | 0.249 | 2.110 |
| length | seq_len=48 | 300 | 0 | 0.210 | 0.168 | 0.260 | 2.073 |
| length | seq_len=64 | 300 | 0 | 0.210 | 0.168 | 0.260 | 2.144 |
| length | seq_len=96 | 300 | 0 | 0.170 | 0.132 | 0.217 | 2.390 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.125 | 0.086 | 0.178 | 2.923 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.719 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.100 | 0.066 | 0.149 | 2.929 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.742 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.701 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.095 | 0.062 | 0.144 | 3.727 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.220 | 0.168 | 0.282 | 1.964 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.067 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.095 | 0.062 | 0.144 | 2.472 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.275 | 0.218 | 0.341 | 1.997 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.255 | 0.200 | 0.320 | 2.073 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.499 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.735 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.135 | 0.094 | 0.189 | 3.517 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.350 | 0.287 | 0.418 | 1.773 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.971 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.135 | 0.094 | 0.189 | 3.327 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.586 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.130 | 0.090 | 0.184 | 3.900 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.295 | 0.236 | 0.362 | 1.951 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.270 | 0.213 | 0.335 | 1.966 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.270 | 0.213 | 0.335 | 1.933 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.265 | 0.209 | 0.330 | 1.943 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.965 |
