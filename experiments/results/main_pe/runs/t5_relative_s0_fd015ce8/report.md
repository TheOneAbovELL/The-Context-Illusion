# Run t5_relative_s0_fd015ce8

* study: `main_pe`  variant: `t5_relative`  seed: 0
* positional method: `t5_relative`; layers=2, d_model=64, heads=2; parameters=116800 (positional: 64)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 369s, final train loss 1.8453, final in-distribution val acc 0.275
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.285
* evidence_removed_acc: 0.025
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.5
* cf_distractor_edit_rate_given_orig_correct: 0.631578947368421
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.7275
* cf_evidence_move_rate_given_orig_correct: 0.6666666666666666
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.915
* cf_filler_resample_rate_given_orig_correct: 0.9210526315789473
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.225
* cf_key_swap_rate_given_orig_correct: 0.02631578947368421
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.2575
* cf_value_edit_rate_given_orig_correct: 0.43859649122807015
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.285
* pos_offset_64_acc: 0.285
* pos_offset_192_acc: 0.285

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.500 | 0.451 | 0.549 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.728 | 0.682 | 0.769 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.915 | 0.884 | 0.939 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.225 | 0.187 | 0.268 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.258 | 0.217 | 0.303 | nan |
| control_evidence_removed | default | 400 | 0 | 0.025 | 0.014 | 0.045 | 6.623 |
| control_in_distribution | default | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.829 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.829 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.829 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.285 | 0.243 | 0.331 | 1.829 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.865 | 0.811 | 0.906 | 0.575 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.105 | 0.070 | 0.155 | 3.163 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.105 | 0.070 | 0.155 | 3.490 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.420 | 0.354 | 0.489 | 1.832 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.090 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.250 | 0.195 | 0.314 | 2.324 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.802 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.985 | 0.957 | 0.995 | 0.190 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.115 | 0.078 | 0.167 | 3.170 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.608 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.500 | 0.431 | 0.569 | 1.062 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.080 | 0.050 | 0.126 | 4.401 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.245 | 0.191 | 0.309 | 1.839 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.185 | 0.137 | 0.245 | 2.541 |
| length | seq_len=128 | 300 | 0 | 0.277 | 0.229 | 0.330 | 2.232 |
| length | seq_len=192 | 300 | 0 | 0.263 | 0.217 | 0.316 | 2.654 |
| length | seq_len=256 | 300 | 0 | 0.237 | 0.192 | 0.288 | 2.872 |
| length | seq_len=32 | 300 | 0 | 0.287 | 0.238 | 0.340 | 1.882 |
| length | seq_len=48 | 300 | 0 | 0.277 | 0.229 | 0.330 | 1.842 |
| length | seq_len=64 | 300 | 0 | 0.310 | 0.260 | 0.364 | 1.748 |
| length | seq_len=96 | 300 | 0 | 0.293 | 0.245 | 0.347 | 1.897 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.070 | 0.042 | 0.114 | 3.248 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.085 | 0.054 | 0.132 | 2.405 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.050 | 0.027 | 0.090 | 3.584 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.065 | 0.038 | 0.108 | 4.148 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.085 | 0.054 | 0.132 | 4.132 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.080 | 0.050 | 0.126 | 4.136 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.270 | 0.213 | 0.335 | 1.671 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.275 | 0.218 | 0.341 | 1.708 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.240 | 0.186 | 0.304 | 1.768 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.390 | 0.325 | 0.459 | 1.484 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.475 | 0.407 | 0.544 | 1.320 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.230 | 0.177 | 0.293 | 1.903 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.060 | 0.035 | 0.102 | 3.161 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.105 | 0.070 | 0.155 | 3.848 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.525 | 0.456 | 0.593 | 1.249 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.470 | 0.402 | 0.539 | 1.344 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.095 | 0.062 | 0.144 | 3.393 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.085 | 0.054 | 0.132 | 4.140 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.145 | 0.103 | 0.200 | 3.799 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.145 | 0.103 | 0.200 | 1.914 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.320 | 0.259 | 0.388 | 1.663 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.320 | 0.259 | 0.388 | 1.595 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.285 | 0.227 | 0.351 | 1.656 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.135 | 0.094 | 0.189 | 3.301 |
