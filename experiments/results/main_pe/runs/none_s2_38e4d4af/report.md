# Run none_s2_38e4d4af

* study: `main_pe`  variant: `none`  seed: 2
* positional method: `none`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 599s, final train loss 2.1690, final in-distribution val acc 0.170
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.2325
* evidence_removed_acc: 0.0275
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4875
* cf_distractor_edit_rate_given_orig_correct: 0.6451612903225806
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 1.0
* cf_evidence_move_rate_given_orig_correct: 1.0
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.975
* cf_filler_resample_rate_given_orig_correct: 1.0
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.1675
* cf_key_swap_rate_given_orig_correct: 0.0
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.07
* cf_value_edit_rate_given_orig_correct: 0.12903225806451613
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
| control_counterfactual | distractor_edit | 400 | 0 | 0.487 | 0.439 | 0.536 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 1.000 | 0.990 | 1.000 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.975 | 0.955 | 0.986 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.168 | 0.134 | 0.207 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.070 | 0.049 | 0.099 | nan |
| control_evidence_removed | default | 400 | 0 | 0.028 | 0.015 | 0.049 | 6.110 |
| control_in_distribution | default | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.099 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.099 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.099 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.233 | 0.194 | 0.276 | 2.099 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.575 | 0.506 | 0.641 | 1.527 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.324 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.706 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.310 | 0.250 | 0.377 | 1.695 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 3.949 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.245 | 0.191 | 0.309 | 2.185 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.812 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.580 | 0.511 | 0.646 | 1.352 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.085 | 0.054 | 0.132 | 3.345 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.075 | 0.046 | 0.120 | 3.720 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.595 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.960 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.265 | 0.209 | 0.330 | 2.135 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.820 |
| length | seq_len=128 | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.158 |
| length | seq_len=192 | 300 | 0 | 0.160 | 0.123 | 0.206 | 2.206 |
| length | seq_len=256 | 300 | 0 | 0.147 | 0.111 | 0.191 | 2.265 |
| length | seq_len=32 | 300 | 0 | 0.187 | 0.147 | 0.235 | 2.129 |
| length | seq_len=48 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.129 |
| length | seq_len=64 | 300 | 0 | 0.190 | 0.150 | 0.238 | 2.132 |
| length | seq_len=96 | 300 | 0 | 0.197 | 0.156 | 0.245 | 2.142 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.084 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.210 | 0.159 | 0.272 | 2.084 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.205 | 0.155 | 0.266 | 2.091 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.157 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.156 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.157 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.230 | 0.177 | 0.293 | 2.073 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.230 | 0.177 | 0.293 | 2.073 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.230 | 0.177 | 0.293 | 2.073 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.230 | 0.177 | 0.293 | 2.098 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.098 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.098 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.098 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.225 | 0.173 | 0.288 | 2.098 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.167 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.167 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.167 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.167 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.215 | 0.164 | 0.277 | 2.167 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.240 | 0.186 | 0.304 | 2.081 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.235 | 0.182 | 0.298 | 2.080 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.235 | 0.182 | 0.298 | 2.080 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.235 | 0.182 | 0.298 | 2.080 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.235 | 0.182 | 0.298 | 2.080 |
