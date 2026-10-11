# Run alibi_s0_14edea8d

* study: `main_pe`  variant: `alibi`  seed: 0
* positional method: `alibi`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 378s, final train loss 2.2820, final in-distribution val acc 0.186
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.1425
* evidence_removed_acc: 0.015
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.41
* cf_distractor_edit_rate_given_orig_correct: 0.6140350877192983
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.7875
* cf_evidence_move_rate_given_orig_correct: 0.7368421052631579
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.83
* cf_filler_resample_rate_given_orig_correct: 0.9122807017543859
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.1775
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.1175
* cf_value_edit_rate_given_orig_correct: 0.12280701754385964
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.1425
* pos_offset_64_acc: 0.1425
* pos_offset_192_acc: 0.1425

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.410 | 0.363 | 0.459 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.787 | 0.745 | 0.825 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.830 | 0.790 | 0.864 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.177 | 0.143 | 0.218 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.117 | 0.090 | 0.153 | nan |
| control_evidence_removed | default | 400 | 0 | 0.015 | 0.007 | 0.032 | 5.593 |
| control_in_distribution | default | 400 | 0 | 0.142 | 0.112 | 0.180 | 2.252 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.142 | 0.112 | 0.180 | 2.252 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.142 | 0.112 | 0.180 | 2.252 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.142 | 0.112 | 0.180 | 2.252 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.645 | 0.577 | 0.708 | 0.983 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.352 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.893 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.325 | 0.264 | 0.393 | 1.534 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.851 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.261 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.013 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.655 | 0.587 | 0.717 | 0.886 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.095 | 0.062 | 0.144 | 3.396 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.717 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.355 | 0.292 | 0.423 | 1.482 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.055 | 0.031 | 0.096 | 3.910 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.213 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.100 | 0.066 | 0.149 | 2.935 |
| length | seq_len=128 | 300 | 0 | 0.177 | 0.138 | 0.224 | 2.375 |
| length | seq_len=192 | 300 | 0 | 0.147 | 0.111 | 0.191 | 2.435 |
| length | seq_len=256 | 300 | 0 | 0.180 | 0.141 | 0.227 | 2.521 |
| length | seq_len=32 | 300 | 0 | 0.227 | 0.183 | 0.277 | 2.248 |
| length | seq_len=48 | 300 | 0 | 0.203 | 0.162 | 0.252 | 2.244 |
| length | seq_len=64 | 300 | 0 | 0.213 | 0.171 | 0.263 | 2.245 |
| length | seq_len=96 | 300 | 0 | 0.173 | 0.135 | 0.220 | 2.294 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.163 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.245 | 0.191 | 0.309 | 2.143 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.361 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.314 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.245 | 0.191 | 0.309 | 2.264 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.423 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.220 | 0.168 | 0.282 | 2.156 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.360 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.243 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.115 | 0.078 | 0.167 | 2.577 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.105 | 0.070 | 0.155 | 2.404 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.135 | 0.094 | 0.189 | 2.244 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.155 | 0.111 | 0.212 | 2.156 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.100 | 0.066 | 0.149 | 3.131 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.133 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.100 | 0.066 | 0.149 | 2.734 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.145 | 0.103 | 0.200 | 2.399 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.284 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.197 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.105 | 0.070 | 0.155 | 2.387 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.135 | 0.094 | 0.189 | 2.263 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.160 | 0.116 | 0.217 | 2.181 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.155 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.058 |
