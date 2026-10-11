# Run t5_relative_s2_6b7d8280

* study: `main_pe`  variant: `t5_relative`  seed: 2
* positional method: `t5_relative`; layers=2, d_model=64, heads=2; parameters=116800 (positional: 64)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 379s, final train loss 1.7214, final in-distribution val acc 0.279
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.3125
* evidence_removed_acc: 0.0275
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.4675
* cf_distractor_edit_rate_given_orig_correct: 0.592
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.7325
* cf_evidence_move_rate_given_orig_correct: 0.656
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9175
* cf_filler_resample_rate_given_orig_correct: 0.912
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.2275
* cf_key_swap_rate_given_orig_correct: 0.016
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.2225
* cf_value_edit_rate_given_orig_correct: 0.344
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.3125
* pos_offset_64_acc: 0.3125
* pos_offset_192_acc: 0.3125

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.468 | 0.419 | 0.516 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.733 | 0.687 | 0.774 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.917 | 0.886 | 0.941 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.228 | 0.189 | 0.271 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.223 | 0.184 | 0.266 | nan |
| control_evidence_removed | default | 400 | 0 | 0.028 | 0.015 | 0.049 | 6.902 |
| control_in_distribution | default | 400 | 0 | 0.312 | 0.269 | 0.360 | 1.660 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.312 | 0.269 | 0.360 | 1.660 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.312 | 0.269 | 0.360 | 1.660 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.312 | 0.269 | 0.360 | 1.660 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.740 | 0.675 | 0.796 | 1.136 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.402 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.075 | 0.046 | 0.120 | 4.222 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.430 | 0.363 | 0.499 | 2.113 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.045 | 0.024 | 0.083 | 5.710 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.265 | 0.209 | 0.330 | 2.474 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.145 | 0.103 | 0.200 | 3.023 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.176 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.080 | 0.050 | 0.126 | 3.462 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.055 | 0.031 | 0.096 | 4.552 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.485 | 0.417 | 0.554 | 0.939 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.050 | 0.027 | 0.090 | 6.710 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.310 | 0.250 | 0.377 | 1.667 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.135 | 0.094 | 0.189 | 2.784 |
| length | seq_len=128 | 300 | 0 | 0.257 | 0.211 | 0.309 | 2.559 |
| length | seq_len=192 | 300 | 0 | 0.220 | 0.177 | 0.270 | 3.344 |
| length | seq_len=256 | 300 | 0 | 0.193 | 0.153 | 0.242 | 3.930 |
| length | seq_len=32 | 300 | 0 | 0.270 | 0.223 | 0.323 | 1.808 |
| length | seq_len=48 | 300 | 0 | 0.250 | 0.204 | 0.302 | 1.753 |
| length | seq_len=64 | 300 | 0 | 0.300 | 0.251 | 0.354 | 1.698 |
| length | seq_len=96 | 300 | 0 | 0.243 | 0.198 | 0.295 | 1.991 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.045 | 0.024 | 0.083 | 3.943 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.065 | 0.038 | 0.108 | 2.996 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.065 | 0.038 | 0.108 | 4.254 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.080 | 0.050 | 0.126 | 5.294 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.080 | 0.050 | 0.126 | 5.204 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.070 | 0.042 | 0.114 | 5.345 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.644 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.325 | 0.264 | 0.393 | 1.586 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.295 | 0.236 | 0.362 | 1.681 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.425 | 0.359 | 0.494 | 1.348 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.415 | 0.349 | 0.484 | 1.319 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.054 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.065 | 0.038 | 0.108 | 3.747 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.095 | 0.062 | 0.144 | 3.548 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.620 | 0.551 | 0.684 | 1.074 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.320 | 0.259 | 0.388 | 1.736 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.095 | 0.062 | 0.144 | 4.108 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.090 | 0.058 | 0.138 | 4.795 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.035 | 0.017 | 0.070 | 5.068 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.160 | 0.116 | 0.217 | 1.863 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.275 | 0.218 | 0.341 | 1.625 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.230 | 0.177 | 0.293 | 1.686 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.245 | 0.191 | 0.309 | 1.689 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.400 | 0.335 | 0.469 | 1.834 |
