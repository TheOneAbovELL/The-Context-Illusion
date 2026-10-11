# Run rope_s1_5e00cee4

* study: `main_pe`  variant: `rope`  seed: 1
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 471s, final train loss 1.6771, final in-distribution val acc 0.299
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.29
* evidence_removed_acc: 0.03
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.3325
* cf_distractor_edit_rate_given_orig_correct: 0.5258620689655172
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.8125
* cf_evidence_move_rate_given_orig_correct: 0.7844827586206896
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.96
* cf_filler_resample_rate_given_orig_correct: 0.9655172413793104
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.2625
* cf_key_swap_rate_given_orig_correct: 0.008620689655172414
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.27
* cf_value_edit_rate_given_orig_correct: 0.4051724137931034
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.29
* pos_offset_64_acc: 0.29
* pos_offset_192_acc: 0.29

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.333 | 0.288 | 0.380 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.812 | 0.771 | 0.848 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.960 | 0.936 | 0.975 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.263 | 0.222 | 0.308 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.270 | 0.229 | 0.316 | nan |
| control_evidence_removed | default | 400 | 0 | 0.030 | 0.017 | 0.052 | 6.191 |
| control_in_distribution | default | 400 | 0 | 0.290 | 0.248 | 0.336 | 1.658 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.290 | 0.248 | 0.336 | 1.658 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.290 | 0.248 | 0.336 | 1.658 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.290 | 0.248 | 0.336 | 1.658 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.895 | 0.845 | 0.930 | 1.206 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.105 | 0.070 | 0.155 | 3.921 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.075 | 0.046 | 0.120 | 4.033 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.440 | 0.373 | 0.509 | 1.579 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.095 | 0.062 | 0.144 | 4.249 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.255 | 0.200 | 0.320 | 2.106 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.140 | 0.099 | 0.195 | 3.128 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.970 | 0.936 | 0.986 | 0.719 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.120 | 0.082 | 0.172 | 3.265 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.125 | 0.086 | 0.178 | 3.746 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.515 | 0.446 | 0.583 | 0.960 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.060 | 0.035 | 0.102 | 4.497 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.290 | 0.232 | 0.356 | 1.607 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.195 | 0.146 | 0.255 | 2.466 |
| length | seq_len=128 | 300 | 0 | 0.247 | 0.201 | 0.298 | 2.118 |
| length | seq_len=192 | 300 | 0 | 0.200 | 0.159 | 0.249 | 2.612 |
| length | seq_len=256 | 300 | 0 | 0.183 | 0.144 | 0.231 | 2.998 |
| length | seq_len=32 | 300 | 0 | 0.327 | 0.276 | 0.382 | 1.727 |
| length | seq_len=48 | 300 | 0 | 0.293 | 0.245 | 0.347 | 1.601 |
| length | seq_len=64 | 300 | 0 | 0.303 | 0.254 | 0.358 | 1.595 |
| length | seq_len=96 | 300 | 0 | 0.300 | 0.251 | 0.354 | 1.649 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.201 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.130 | 0.090 | 0.184 | 2.429 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.278 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.065 | 0.038 | 0.108 | 4.164 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.080 | 0.050 | 0.126 | 4.395 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.065 | 0.038 | 0.108 | 4.064 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.295 | 0.236 | 0.362 | 1.467 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.265 | 0.209 | 0.330 | 1.559 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.320 | 0.259 | 0.388 | 1.467 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.595 | 0.526 | 0.661 | 1.065 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.397 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.170 | 0.124 | 0.228 | 2.355 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.180 | 0.133 | 0.239 | 2.175 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.025 | 0.011 | 0.057 | 5.057 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.475 | 0.407 | 0.544 | 1.532 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.380 | 0.316 | 0.449 | 2.120 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.165 | 0.120 | 0.223 | 2.505 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.115 | 0.078 | 0.167 | 4.232 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.040 | 0.020 | 0.077 | 5.662 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.305 | 0.245 | 0.372 | 1.466 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.330 | 0.269 | 0.398 | 1.440 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.340 | 0.278 | 0.408 | 1.439 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.355 | 0.292 | 0.423 | 1.425 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.025 | 0.011 | 0.057 | 5.200 |
