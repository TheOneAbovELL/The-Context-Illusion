# Run none_s0_3b095ef5

* study: `main_pe`  variant: `none`  seed: 0
* positional method: `none`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 570s, final train loss 2.1007, final in-distribution val acc 0.191
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.23
* evidence_removed_acc: 0.035
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.49
* cf_distractor_edit_rate_given_orig_correct: 0.717391304347826
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.9525
* cf_evidence_move_rate_given_orig_correct: 0.967391304347826
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.905
* cf_filler_resample_rate_given_orig_correct: 0.9347826086956522
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.1825
* cf_key_swap_rate_given_orig_correct: 0.010869565217391304
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.0725
* cf_value_edit_rate_given_orig_correct: 0.08695652173913043
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.23
* pos_offset_64_acc: 0.23
* pos_offset_192_acc: 0.23

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.490 | 0.441 | 0.539 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.953 | 0.927 | 0.969 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.905 | 0.872 | 0.930 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.182 | 0.148 | 0.223 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.072 | 0.051 | 0.102 | nan |
| control_evidence_removed | default | 400 | 0 | 0.035 | 0.021 | 0.058 | 6.150 |
| control_in_distribution | default | 400 | 0 | 0.230 | 0.191 | 0.274 | 2.081 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.230 | 0.191 | 0.274 | 2.081 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.230 | 0.191 | 0.274 | 2.081 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.230 | 0.191 | 0.274 | 2.081 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.645 | 0.577 | 0.708 | 1.008 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.214 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.387 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.335 | 0.273 | 0.403 | 1.553 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.065 | 0.038 | 0.108 | 3.840 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.114 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.110 | 0.074 | 0.161 | 2.789 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.675 | 0.607 | 0.736 | 0.833 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.090 | 0.058 | 0.138 | 3.144 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.411 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.375 | 0.311 | 0.444 | 1.434 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 3.822 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.106 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.125 | 0.086 | 0.178 | 2.764 |
| length | seq_len=128 | 300 | 0 | 0.223 | 0.180 | 0.274 | 2.110 |
| length | seq_len=192 | 300 | 0 | 0.207 | 0.165 | 0.256 | 2.166 |
| length | seq_len=256 | 300 | 0 | 0.187 | 0.147 | 0.235 | 2.247 |
| length | seq_len=32 | 300 | 0 | 0.187 | 0.147 | 0.235 | 2.115 |
| length | seq_len=48 | 300 | 0 | 0.207 | 0.165 | 0.256 | 2.096 |
| length | seq_len=64 | 300 | 0 | 0.233 | 0.189 | 0.284 | 2.102 |
| length | seq_len=96 | 300 | 0 | 0.250 | 0.204 | 0.302 | 2.087 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.118 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.088 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.162 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.314 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.274 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.175 | 0.129 | 0.234 | 2.398 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.052 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.038 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.088 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.210 | 0.159 | 0.272 | 1.998 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.014 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.017 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.049 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.110 | 0.074 | 0.161 | 2.964 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.157 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.175 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.176 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.190 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.100 | 0.066 | 0.149 | 3.226 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.235 | 0.182 | 0.298 | 1.976 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.240 | 0.186 | 0.304 | 1.978 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.240 | 0.186 | 0.304 | 1.986 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.230 | 0.177 | 0.293 | 1.989 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.815 |
