# Run alibi_s2_58a1d391

* study: `main_pe`  variant: `alibi`  seed: 2
* positional method: `alibi`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 389s, final train loss 2.5063, final in-distribution val acc 0.174
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.18
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.485
* cf_distractor_edit_rate_given_orig_correct: 0.5555555555555556
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.8275
* cf_evidence_move_rate_given_orig_correct: 0.8611111111111112
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.8475
* cf_filler_resample_rate_given_orig_correct: 0.9166666666666666
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.1475
* cf_key_swap_rate_given_orig_correct: 0.041666666666666664
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.115
* cf_value_edit_rate_given_orig_correct: 0.1527777777777778
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.18
* pos_offset_64_acc: 0.18
* pos_offset_192_acc: 0.18

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.485 | 0.436 | 0.534 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.828 | 0.787 | 0.861 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.848 | 0.809 | 0.879 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.147 | 0.116 | 0.186 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.115 | 0.087 | 0.150 | nan |
| control_evidence_removed | default | 400 | 0 | 0.030 | 0.017 | 0.052 | 5.298 |
| control_in_distribution | default | 400 | 0 | 0.180 | 0.145 | 0.221 | 2.499 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.180 | 0.145 | 0.221 | 2.499 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.180 | 0.145 | 0.221 | 2.499 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.180 | 0.145 | 0.221 | 2.499 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.565 | 0.496 | 0.632 | 1.581 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.571 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.055 | 0.031 | 0.096 | 3.718 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.320 | 0.259 | 0.388 | 2.002 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 3.992 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.150 | 0.107 | 0.206 | 2.543 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.065 | 0.038 | 0.108 | 3.148 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.570 | 0.501 | 0.637 | 1.495 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.593 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.827 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.315 | 0.255 | 0.382 | 1.957 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.045 | 0.024 | 0.083 | 3.952 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.519 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.114 |
| length | seq_len=128 | 300 | 0 | 0.170 | 0.132 | 0.217 | 2.528 |
| length | seq_len=192 | 300 | 0 | 0.173 | 0.135 | 0.220 | 2.621 |
| length | seq_len=256 | 300 | 0 | 0.167 | 0.129 | 0.213 | 2.818 |
| length | seq_len=32 | 300 | 0 | 0.193 | 0.153 | 0.242 | 2.478 |
| length | seq_len=48 | 300 | 0 | 0.170 | 0.132 | 0.217 | 2.472 |
| length | seq_len=64 | 300 | 0 | 0.163 | 0.126 | 0.209 | 2.443 |
| length | seq_len=96 | 300 | 0 | 0.167 | 0.129 | 0.213 | 2.473 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.280 | 0.222 | 0.346 | 2.209 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.309 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.378 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.295 | 0.236 | 0.362 | 2.248 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.255 | 0.200 | 0.320 | 2.279 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.260 | 0.204 | 0.325 | 2.375 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.231 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.150 | 0.107 | 0.206 | 2.481 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.367 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.095 | 0.062 | 0.144 | 2.978 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.726 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.430 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.288 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.110 | 0.074 | 0.161 | 3.291 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.427 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.135 | 0.094 | 0.189 | 3.120 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.140 | 0.099 | 0.195 | 2.658 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.346 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.145 | 0.103 | 0.200 | 3.329 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.105 | 0.070 | 0.155 | 2.604 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.485 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.353 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.350 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.269 |
