# Run alibi_s1_48cfd5ce

* study: `main_pe`  variant: `alibi`  seed: 1
* positional method: `alibi`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 377s, final train loss 1.9043, final in-distribution val acc 0.381
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.4575
* evidence_removed_acc: 0.035
* chance_acc: 0.03125
* cf_distractor_edit_rate: 0.6125
* cf_distractor_edit_rate_given_orig_correct: 0.7868852459016393
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 0.6025
* cf_evidence_move_rate_given_orig_correct: 0.6502732240437158
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.8575
* cf_filler_resample_rate_given_orig_correct: 0.9016393442622951
* cf_filler_resample_n: 400
* cf_key_swap_rate: 0.4275
* cf_key_swap_rate_given_orig_correct: 0.47540983606557374
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 0.375
* cf_value_edit_rate_given_orig_correct: 0.5683060109289617
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 0.4575
* pos_offset_64_acc: 0.4575
* pos_offset_192_acc: 0.4575

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
| control_counterfactual | distractor_edit | 400 | 0 | 0.613 | 0.564 | 0.659 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 0.603 | 0.554 | 0.649 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.858 | 0.820 | 0.888 | nan |
| control_counterfactual | key_swap | 400 | 0 | 0.427 | 0.380 | 0.476 | nan |
| control_counterfactual | value_edit | 400 | 0 | 0.375 | 0.329 | 0.423 | nan |
| control_evidence_removed | default | 400 | 0 | 0.035 | 0.021 | 0.058 | 6.199 |
| control_in_distribution | default | 400 | 0 | 0.458 | 0.409 | 0.506 | 1.829 |
| control_position_offset | pos_offset=0 | 400 | 0 | 0.458 | 0.409 | 0.506 | 1.829 |
| control_position_offset | pos_offset=192 | 400 | 0 | 0.458 | 0.409 | 0.506 | 1.829 |
| control_position_offset | pos_offset=64 | 400 | 0 | 0.458 | 0.409 | 0.506 | 1.829 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.865 | 0.811 | 0.906 | 0.642 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.220 | 0.168 | 0.282 | 3.339 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.170 | 0.124 | 0.228 | 3.284 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.615 | 0.546 | 0.680 | 1.259 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.100 | 0.066 | 0.149 | 3.755 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.410 | 0.344 | 0.479 | 1.960 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.260 | 0.204 | 0.325 | 2.455 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 0.920 | 0.874 | 0.950 | 0.453 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.110 | 0.074 | 0.161 | 3.193 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.115 | 0.078 | 0.167 | 3.367 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 0.675 | 0.607 | 0.736 | 1.086 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.095 | 0.062 | 0.144 | 3.799 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 0.395 | 0.330 | 0.464 | 1.732 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.270 | 0.213 | 0.335 | 2.578 |
| length | seq_len=128 | 300 | 0 | 0.403 | 0.349 | 0.460 | 2.032 |
| length | seq_len=192 | 300 | 0 | 0.397 | 0.343 | 0.453 | 2.200 |
| length | seq_len=256 | 300 | 0 | 0.370 | 0.317 | 0.426 | 2.353 |
| length | seq_len=32 | 300 | 0 | 0.360 | 0.308 | 0.416 | 1.973 |
| length | seq_len=48 | 300 | 0 | 0.363 | 0.311 | 0.419 | 1.887 |
| length | seq_len=64 | 300 | 0 | 0.440 | 0.385 | 0.497 | 1.819 |
| length | seq_len=96 | 300 | 0 | 0.377 | 0.324 | 0.433 | 1.947 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.480 | 0.412 | 0.549 | 1.637 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.420 | 0.354 | 0.489 | 1.854 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.465 | 0.397 | 0.534 | 1.756 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.450 | 0.383 | 0.519 | 1.830 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.455 | 0.387 | 0.524 | 1.827 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.455 | 0.387 | 0.524 | 1.805 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 0.500 | 0.431 | 0.569 | 1.620 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 0.480 | 0.412 | 0.549 | 1.644 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 0.465 | 0.397 | 0.534 | 1.711 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.435 | 0.368 | 0.504 | 2.010 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.410 | 0.344 | 0.479 | 2.069 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.425 | 0.359 | 0.494 | 1.915 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.510 | 0.441 | 0.578 | 1.639 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.230 | 0.177 | 0.293 | 2.729 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.335 | 0.273 | 0.403 | 2.765 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.315 | 0.255 | 0.382 | 2.771 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.380 | 0.316 | 0.449 | 2.277 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.470 | 0.402 | 0.539 | 1.855 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.200 | 0.150 | 0.261 | 2.853 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.485 | 0.417 | 0.554 | 1.632 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 0.400 | 0.335 | 0.469 | 1.864 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.430 | 0.363 | 0.499 | 1.725 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 0.450 | 0.383 | 0.519 | 1.707 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.190 | 0.142 | 0.250 | 2.900 |
