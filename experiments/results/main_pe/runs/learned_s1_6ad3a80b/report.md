# Run learned_s1_6ad3a80b

* study: `main_pe`  variant: `learned`  seed: 1
* positional method: `learned`; layers=2, d_model=64, heads=2; parameters=149504 (positional: 32768)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 370s, final train loss 2.1424, final in-distribution val acc 0.197
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.21
* evidence_removed_acc: 0.0275
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.51
* cf_distractor_edit_rate_given_orig_correct: 0.6309523809523809
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.8525
* cf_evidence_move_rate_given_orig_correct: 0.8452380952380952
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9
* cf_filler_resample_rate_given_orig_correct: 0.9047619047619048
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.195
* cf_key_swap_rate_given_orig_correct: 0.023809523809523808
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1075
* cf_value_edit_rate_given_orig_correct: 0.19047619047619047
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.21
* pos_offset_64_acc: 0.1925
* pos_offset_192_acc: 0.2075

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.510 | 0.461 | 0.559 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.853 | 0.814 | 0.884 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.900 | 0.867 | 0.926 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.195 | 0.159 | 0.237 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.107 | 0.081 | 0.142 | nan |
| control_evidence_removed | default | 400 | 0 | 0.028 | 0.015 | 0.049 | 6.090 |
| control_in_distribution | default | 400 | 0 | 0.210 | 0.173 | 0.253 | 2.117 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.210 | 0.173 | 0.253 | 2.117 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.207 | 0.171 | 0.250 | 2.231 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.193 | 0.157 | 0.234 | 2.235 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.430 | 0.363 | 0.499 | 2.006 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.537 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.090 | 0.058 | 0.138 | 4.092 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.280 | 0.222 | 0.346 | 2.300 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.105 | 0.070 | 0.155 | 4.468 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.676 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.339 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.615 | 0.546 | 0.680 | 1.022 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.493 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.055 | 0.031 | 0.096 | 3.978 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.340 | 0.278 | 0.408 | 1.582 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 4.505 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.235 | 0.182 | 0.298 | 2.312 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.115 | 0.078 | 0.167 | 3.088 |
| length | seq_len=128 | 300 | 0 | 0.217 | 0.174 | 0.267 | 2.664 |
| length | seq_len=192 | 300 | 0 | 0.210 | 0.168 | 0.260 | 3.060 |
| length | seq_len=256 | 300 | 0 | 0.163 | 0.126 | 0.209 | 3.171 |
| length | seq_len=32 | 300 | 0 | 0.227 | 0.183 | 0.277 | 2.053 |
| length | seq_len=48 | 300 | 0 | 0.213 | 0.171 | 0.263 | 2.076 |
| length | seq_len=64 | 300 | 0 | 0.217 | 0.174 | 0.267 | 2.271 |
| length | seq_len=96 | 300 | 0 | 0.227 | 0.183 | 0.277 | 2.509 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.248 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.130 | 0.090 | 0.184 | 3.235 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.115 | 0.078 | 0.167 | 3.231 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.523 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.453 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.608 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.280 | 0.222 | 0.346 | 1.968 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.275 | 0.218 | 0.341 | 1.975 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.125 | 0.086 | 0.178 | 2.645 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.355 | 0.292 | 0.423 | 1.855 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.290 | 0.232 | 0.356 | 1.954 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.848 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.975 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.127 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.430 | 0.363 | 0.499 | 1.782 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.130 | 0.090 | 0.184 | 3.188 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.306 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.110 | 0.074 | 0.161 | 3.292 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.145 | 0.103 | 0.200 | 3.259 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.255 | 0.200 | 0.320 | 1.977 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.285 | 0.227 | 0.351 | 2.041 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.280 | 0.222 | 0.346 | 1.996 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.270 | 0.213 | 0.335 | 2.038 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.045 | 0.024 | 0.083 | 4.117 |
