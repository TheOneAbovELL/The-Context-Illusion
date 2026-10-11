# Run learned_s0_6718f8d8

* study: `smoke`  variant: `learned`  seed: 0
* positional method: `learned`; layers=2, d_model=32, heads=2; parameters=29568 (positional: 4096)
* task: `recall`, training lengths (16, 32)
* training: 60 steps, 11s, final train loss 4.7832, final in-distribution val acc 0.000
* steps to val acc 0.5/0.9/0.99: None/None/None

## Controls (measured)

* in_distribution_acc: 0.03125
* evidence_removed_acc: 0.03125
* chance_acc: 0.03125
* pos_offset_0_acc: 0.03125
* pos_offset_32_acc: 0.03125

## Validity checks

* eval_examples_checked: 240
* eval_examples_with_violations: 0
* n_train_sampled: 500
* n_eval: 240
* n_eval_in_train_sample: 0
* mask_check_max_abs_diff: 0.0
* position_overflow_rows: 0

## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)

| grid | cell | n | n_unsupported | acc | ci_lo | ci_hi | mean_loss |
|---|---|---|---|---|---|---|---|
| control_evidence_removed | default | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.686 |
| control_in_distribution | default | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.686 |
| control_position_offset | pos_offset=0 | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.686 |
| control_position_offset | pos_offset=32 | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.682 |
| length | seq_len=16 | 40 | 0 | 0.050 | 0.014 | 0.165 | 4.679 |
| length | seq_len=32 | 40 | 0 | 0.025 | 0.004 | 0.129 | 4.654 |
| length | seq_len=64 | 40 | 0 | 0.050 | 0.014 | 0.165 | 4.659 |
| position | evidence_pos=0.0 | 40 | 0 | 0.000 | 0.000 | 0.088 | 4.688 |
| position | evidence_pos=0.5 | 40 | 0 | 0.025 | 0.004 | 0.129 | 4.699 |
| position | evidence_pos=1.0 | 40 | 0 | 0.050 | 0.014 | 0.165 | 4.676 |
