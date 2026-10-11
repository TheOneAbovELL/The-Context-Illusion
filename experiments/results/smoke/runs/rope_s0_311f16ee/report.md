# Run rope_s0_311f16ee

* study: `smoke`  variant: `rope`  seed: 0
* positional method: `rope`; layers=2, d_model=32, heads=2; parameters=25472 (positional: 0)
* task: `recall`, training lengths (16, 32)
* training: 60 steps, 9s, final train loss 4.7272, final in-distribution val acc 0.016
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
| control_evidence_removed | default | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.602 |
| control_in_distribution | default | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.602 |
| control_position_offset | pos_offset=0 | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.602 |
| control_position_offset | pos_offset=32 | 64 | 0 | 0.031 | 0.009 | 0.107 | 4.602 |
| length | seq_len=16 | 40 | 0 | 0.000 | 0.000 | 0.088 | 4.592 |
| length | seq_len=32 | 40 | 0 | 0.025 | 0.004 | 0.129 | 4.563 |
| length | seq_len=64 | 40 | 0 | 0.025 | 0.004 | 0.129 | 4.582 |
| position | evidence_pos=0.0 | 40 | 0 | 0.025 | 0.004 | 0.129 | 4.565 |
| position | evidence_pos=0.5 | 40 | 0 | 0.025 | 0.004 | 0.129 | 4.596 |
| position | evidence_pos=1.0 | 40 | 0 | 0.075 | 0.026 | 0.199 | 4.593 |
