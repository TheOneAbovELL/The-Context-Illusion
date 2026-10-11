# Run learned_s0_b216759c

* study: `main_pe`  variant: `learned`  seed: 0
* positional method: `learned`; layers=2, d_model=64, heads=2; parameters=149504 (positional: 32768)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 369s, final train loss 2.3136, final in-distribution val acc 0.158
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.175
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.5075
* cf_distractor_edit_rate_given_orig_correct: 0.6285714285714286
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.81
* cf_evidence_move_rate_given_orig_correct: 0.8428571428571429
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.86
* cf_filler_resample_rate_given_orig_correct: 0.8857142857142857
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.145
* cf_key_swap_rate_given_orig_correct: 0.014285714285714285
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.14
* cf_value_edit_rate_given_orig_correct: 0.2
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.175
* pos_offset_64_acc: 0.195
* pos_offset_192_acc: 0.17

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.507 | 0.459 | 0.556 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.810 | 0.769 | 0.845 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.860 | 0.823 | 0.891 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.145 | 0.114 | 0.183 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.140 | 0.109 | 0.177 | nan |
| control_evidence_removed | default | 400 | 0 | 0.030 | 0.017 | 0.052 | 5.577 |
| control_in_distribution | default | 400 | 0 | 0.175 | 0.141 | 0.215 | 2.237 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.175 | 0.141 | 0.215 | 2.237 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.170 | 0.136 | 0.210 | 2.388 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.195 | 0.159 | 0.237 | 2.374 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.435 | 0.368 | 0.504 | 1.608 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.637 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.980 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.285 | 0.227 | 0.351 | 2.120 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.110 | 0.074 | 0.161 | 4.260 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.438 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.145 | 0.103 | 0.200 | 3.034 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.590 | 0.521 | 0.656 | 1.183 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.512 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.870 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.746 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.085 | 0.054 | 0.132 | 4.335 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.385 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.110 | 0.074 | 0.161 | 3.124 |
| length | seq_len=128 | 300 | 0 | 0.200 | 0.159 | 0.249 | 2.481 |
| length | seq_len=192 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.608 |
| length | seq_len=256 | 300 | 0 | 0.160 | 0.123 | 0.206 | 2.765 |
| length | seq_len=32 | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.259 |
| length | seq_len=48 | 300 | 0 | 0.193 | 0.153 | 0.242 | 2.270 |
| length | seq_len=64 | 300 | 0 | 0.217 | 0.174 | 0.267 | 2.383 |
| length | seq_len=96 | 300 | 0 | 0.210 | 0.168 | 0.260 | 2.450 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.135 | 0.094 | 0.189 | 2.642 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.505 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.878 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.953 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.863 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.160 | 0.116 | 0.217 | 3.010 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.214 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.280 | 0.222 | 0.346 | 2.164 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.060 | 0.035 | 0.102 | 3.006 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.235 | 0.182 | 0.298 | 2.174 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.230 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.415 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.532 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.115 | 0.078 | 0.167 | 3.581 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.318 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.636 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.791 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.125 | 0.086 | 0.178 | 2.852 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.948 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.275 | 0.218 | 0.341 | 2.036 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.270 | 0.213 | 0.335 | 2.041 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.245 | 0.191 | 0.309 | 2.115 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.263 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.040 | 0.020 | 0.077 | 3.971 |
