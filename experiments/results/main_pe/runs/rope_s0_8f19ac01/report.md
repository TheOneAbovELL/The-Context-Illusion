# Run rope_s0_8f19ac01

* study: `main_pe`  variant: `rope`  seed: 0
* positional method: `rope`; layers=2, d_model=64, heads=2; parameters=116736 (positional: 0)
* task: `recall`, training lengths (24, 64)
* training: 3000 steps, 467s, final train loss 0.0362, final in-distribution val acc 0.994
* steps to val acc 0.5/0.9/0.99: 600/800/2800

## Controls (measured)

* in_distribution_acc: 1.0
* evidence_removed_acc: 0.0225
* chance_acc: 0.03125
* cf_distractor_edit_rate: 1.0
* cf_distractor_edit_rate_given_orig_correct: 1.0
* cf_distractor_edit_n: 400
* cf_evidence_move_rate: 1.0
* cf_evidence_move_rate_given_orig_correct: 1.0
* cf_evidence_move_n: 400
* cf_filler_resample_rate: 0.9975
* cf_filler_resample_rate_given_orig_correct: 0.9975
* cf_filler_resample_n: 400
* cf_key_swap_rate: 1.0
* cf_key_swap_rate_given_orig_correct: 1.0
* cf_key_swap_n: 400
* cf_key_swap_shortcut_reference: 0.25
* cf_value_edit_rate: 1.0
* cf_value_edit_rate_given_orig_correct: 1.0
* cf_value_edit_n: 400
* cf_value_edit_shortcut_reference: 0.25
* pos_offset_0_acc: 1.0
* pos_offset_64_acc: 1.0
* pos_offset_192_acc: 1.0

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
| control_counterfactual | distractor_edit | 400 | 0 | 1.000 | 0.990 | 1.000 | nan |
| control_counterfactual | evidence_move | 400 | 0 | 1.000 | 0.990 | 1.000 | nan |
| control_counterfactual | filler_resample | 400 | 0 | 0.998 | 0.986 | 1.000 | nan |
| control_counterfactual | key_swap | 400 | 0 | 1.000 | 0.990 | 1.000 | nan |
| control_counterfactual | value_edit | 400 | 0 | 1.000 | 0.990 | 1.000 | nan |
| control_evidence_removed | default | 400 | 0 | 0.022 | 0.012 | 0.042 | 6.072 |
| control_in_distribution | default | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.003 |
| control_position_offset | pos_offset=0 | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.003 |
| control_position_offset | pos_offset=192 | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.003 |
| control_position_offset | pos_offset=64 | 400 | 0 | 1.000 | 0.990 | 1.000 | 0.003 |
| distractors | seq_len=128,n_pairs=1 | 200 | 0 | 0.940 | 0.898 | 0.965 | 0.316 |
| distractors | seq_len=128,n_pairs=12 | 200 | 0 | 0.585 | 0.516 | 0.651 | 2.377 |
| distractors | seq_len=128,n_pairs=16 | 200 | 0 | 0.560 | 0.491 | 0.627 | 2.944 |
| distractors | seq_len=128,n_pairs=2 | 200 | 0 | 0.805 | 0.745 | 0.854 | 1.243 |
| distractors | seq_len=128,n_pairs=24 | 200 | 0 | 0.390 | 0.325 | 0.459 | 4.151 |
| distractors | seq_len=128,n_pairs=4 | 200 | 0 | 0.765 | 0.702 | 0.818 | 1.214 |
| distractors | seq_len=128,n_pairs=8 | 200 | 0 | 0.670 | 0.602 | 0.731 | 2.186 |
| distractors | seq_len=64,n_pairs=1 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| distractors | seq_len=64,n_pairs=12 | 200 | 0 | 0.940 | 0.898 | 0.965 | 0.451 |
| distractors | seq_len=64,n_pairs=16 | 200 | 0 | 0.815 | 0.755 | 0.863 | 1.242 |
| distractors | seq_len=64,n_pairs=2 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| distractors | seq_len=64,n_pairs=24 | 200 | 0 | 0.600 | 0.531 | 0.665 | 2.640 |
| distractors | seq_len=64,n_pairs=4 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| distractors | seq_len=64,n_pairs=8 | 200 | 0 | 0.975 | 0.943 | 0.989 | 0.084 |
| length | seq_len=128 | 300 | 0 | 0.797 | 0.748 | 0.838 | 1.185 |
| length | seq_len=192 | 300 | 0 | 0.650 | 0.594 | 0.702 | 2.452 |
| length | seq_len=256 | 300 | 0 | 0.373 | 0.321 | 0.429 | 4.542 |
| length | seq_len=32 | 300 | 0 | 0.990 | 0.971 | 0.997 | 0.045 |
| length | seq_len=48 | 300 | 0 | 0.983 | 0.962 | 0.993 | 0.076 |
| length | seq_len=64 | 300 | 0 | 0.997 | 0.981 | 0.999 | 0.007 |
| length | seq_len=96 | 300 | 0 | 0.920 | 0.884 | 0.946 | 0.523 |
| length_x_distance | seq_len=128,evidence_distance=24 | 200 | 0 | 0.835 | 0.777 | 0.880 | 1.036 |
| length_x_distance | seq_len=128,evidence_distance=56 | 200 | 0 | 0.780 | 0.718 | 0.832 | 1.169 |
| length_x_distance | seq_len=128,evidence_distance=8 | 200 | 0 | 0.820 | 0.761 | 0.867 | 1.159 |
| length_x_distance | seq_len=256,evidence_distance=24 | 200 | 0 | 0.260 | 0.204 | 0.325 | 5.132 |
| length_x_distance | seq_len=256,evidence_distance=56 | 200 | 0 | 0.475 | 0.407 | 0.544 | 3.781 |
| length_x_distance | seq_len=256,evidence_distance=8 | 200 | 0 | 0.285 | 0.227 | 0.351 | 4.744 |
| length_x_distance | seq_len=64,evidence_distance=24 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| length_x_distance | seq_len=64,evidence_distance=56 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.006 |
| length_x_distance | seq_len=64,evidence_distance=8 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.005 |
| length_x_position | seq_len=128,evidence_pos=0.0 | 200 | 0 | 0.840 | 0.783 | 0.884 | 0.890 |
| length_x_position | seq_len=128,evidence_pos=0.25 | 200 | 0 | 0.710 | 0.644 | 0.768 | 2.012 |
| length_x_position | seq_len=128,evidence_pos=0.5 | 200 | 0 | 0.795 | 0.734 | 0.845 | 1.052 |
| length_x_position | seq_len=128,evidence_pos=0.75 | 200 | 0 | 0.840 | 0.783 | 0.884 | 0.841 |
| length_x_position | seq_len=128,evidence_pos=1.0 | 200 | 0 | 0.835 | 0.777 | 0.880 | 1.316 |
| length_x_position | seq_len=256,evidence_pos=0.0 | 200 | 0 | 0.510 | 0.441 | 0.578 | 3.291 |
| length_x_position | seq_len=256,evidence_pos=0.25 | 200 | 0 | 0.470 | 0.402 | 0.539 | 3.398 |
| length_x_position | seq_len=256,evidence_pos=0.5 | 200 | 0 | 0.465 | 0.397 | 0.534 | 3.620 |
| length_x_position | seq_len=256,evidence_pos=0.75 | 200 | 0 | 0.395 | 0.330 | 0.464 | 3.965 |
| length_x_position | seq_len=256,evidence_pos=1.0 | 200 | 0 | 0.305 | 0.245 | 0.372 | 4.927 |
| length_x_position | seq_len=64,evidence_pos=0.0 | 200 | 0 | 0.995 | 0.972 | 0.999 | 0.042 |
| length_x_position | seq_len=64,evidence_pos=0.25 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.001 |
| length_x_position | seq_len=64,evidence_pos=0.5 | 200 | 0 | 0.990 | 0.964 | 0.997 | 0.067 |
| length_x_position | seq_len=64,evidence_pos=0.75 | 200 | 0 | 1.000 | 0.981 | 1.000 | 0.004 |
| length_x_position | seq_len=64,evidence_pos=1.0 | 200 | 0 | 0.990 | 0.964 | 0.997 | 0.019 |
