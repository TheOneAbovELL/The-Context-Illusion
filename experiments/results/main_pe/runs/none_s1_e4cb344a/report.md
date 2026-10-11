# Run none_s1_e4cb344a

* study: `main_pe`  variant: `none`  seed: 1
* positional method: `none`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 570s, final train loss 2.1427, final in-distribution val acc 0.184
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.22
* evidence_removed_acc: 0.0225
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4775
* cf_distractor_edit_rate_given_orig_correct: 0.6363636363636364
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.955
* cf_evidence_move_rate_given_orig_correct: 0.9659090909090909
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.91
* cf_filler_resample_rate_given_orig_correct: 0.9545454545454546
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.17
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1125
* cf_value_edit_rate_given_orig_correct: 0.17045454545454544
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.22
* pos_offset_64_acc: 0.22
* pos_offset_192_acc: 0.22

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.477 | 0.429 | 0.526 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.955 | 0.930 | 0.971 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.910 | 0.878 | 0.934 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.170 | 0.136 | 0.210 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.113 | 0.085 | 0.147 | nan |
| control_evidence_removed | default | 400 | 0 | 0.022 | 0.012 | 0.042 | 5.998 |
| control_in_distribution | default | 400 | 0 | 0.220 | 0.182 | 0.263 | 2.098 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.220 | 0.182 | 0.263 | 2.098 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.220 | 0.182 | 0.263 | 2.098 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.220 | 0.182 | 0.263 | 2.098 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.595 | 0.526 | 0.661 | 1.127 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.105 | 0.070 | 0.155 | 3.221 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.065 | 0.038 | 0.108 | 3.592 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.300 | 0.241 | 0.367 | 1.725 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.969 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.223 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.135 | 0.094 | 0.189 | 2.765 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.600 | 0.531 | 0.665 | 0.944 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.189 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.065 | 0.038 | 0.108 | 3.551 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.300 | 0.241 | 0.367 | 1.521 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.969 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.120 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.710 |
| length | seq_len=128 | 300 | 0 | 0.160 | 0.123 | 0.206 | 2.222 |
| length | seq_len=192 | 300 | 0 | 0.163 | 0.126 | 0.209 | 2.410 |
| length | seq_len=256 | 300 | 0 | 0.170 | 0.132 | 0.217 | 2.572 |
| length | seq_len=32 | 300 | 0 | 0.220 | 0.177 | 0.270 | 2.111 |
| length | seq_len=48 | 300 | 0 | 0.197 | 0.156 | 0.245 | 2.116 |
| length | seq_len=64 | 300 | 0 | 0.203 | 0.162 | 0.252 | 2.145 |
| length | seq_len=96 | 300 | 0 | 0.167 | 0.129 | 0.213 | 2.139 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.223 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.200 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.257 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.645 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.622 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.678 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.045 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.052 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.078 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.178 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.179 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.192 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.191 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.140 | 0.099 | 0.195 | 3.091 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.489 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.483 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.487 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.490 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.140 | 0.099 | 0.195 | 3.521 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.044 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.051 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.052 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.054 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.140 | 0.099 | 0.195 | 2.805 |
