# Do irrelevant filler tokens slow the learning of retrieval? (controlled)

*Study id:* `fillers`  
*Spec:* ``

## Design

**Research question.** Holding the number of associations (4), the number of supervised queries (4, one per association) and the query format fixed, does adding irrelevant filler tokens to the context change how quickly and how well the model learns retrieval?


**Hypothesis.** If fillers are an obstacle, the filler condition reaches 90% later (or not at all) and ends lower than the packed condition. The earlier Q1/Q2 pilot could not test this because it changed the number of pairs (and hence chance level) together with the fillers.


**Independent variables:** filler count (0 vs 24)  
**Controlled variables:** 4 associations per sequence, all 4 queried (3 auxiliary + 1 scored), <ans> query format, model (RoPE, 2 heads, d_model 64, 2 layers), optimiser, steps, batch size, seeds, evaluation format identical to the training format; chance = 1/32, random-in-context = 1/4, UNAVOIDABLE CONFOUND: fillers add length (24 vs 48 tokens) and spread the pairs apart  
**Primary metric:** steps to 90% validation accuracy and final validation accuracy  
**Seeds:** [0, 1, 2]  
**Evaluation seed (shared by all runs):** 20261016

**Expected failure modes:** neither condition learns within budget (then the comparison is inconclusive); length and distance effects are confounded with filler count

## Runs (measured)

| run_id | variant | seed | pos_method | status | elapsed_s | final_val_acc | final_train_loss | steps | n_params |
|---|---|---|---|---|---|---|---|---|---|
| fillers_s0_06f531b3 | fillers | 0 | rope | completed | 501.710 | 1.000 | 0.818 | 3000 | 116736 |
| fillers_s1_588de66b | fillers | 1 | rope | completed | 499.441 | 1.000 | 0.808 | 3000 | 116736 |
| fillers_s2_85c1c382 | fillers | 2 | rope | completed | 501.164 | 0.914 | 0.937 | 3000 | 116736 |
| packed_s0_9b274764 | packed | 0 | rope | completed | 258.487 | 1.000 | 0.818 | 3000 | 116736 |
| packed_s1_7391834c | packed | 1 | rope | completed | 258.556 | 1.000 | 0.810 | 3000 | 116736 |
| packed_s2_d76748a3 | packed | 2 | rope | completed | 258.592 | 1.000 | 0.824 | 3000 | 116736 |

## Validity flags

* none raised

## Controls (mean, min and max over seeds)

| grid | cell | variant | n_seeds | mean | min | max |
|---|---|---|---|---|---|---|
| control_evidence_removed | default | fillers | 3 | 0.031 | 0.027 | 0.037 |
| control_evidence_removed | default | packed | 3 | 0.033 | 0.030 | 0.040 |
| control_in_distribution | default | fillers | 3 | 0.980 | 0.940 | 1.000 |
| control_in_distribution | default | packed | 3 | 1.000 | 1.000 | 1.000 |
| control_position_offset | pos_offset=0 | fillers | 3 | 0.980 | 0.940 | 1.000 |
| control_position_offset | pos_offset=0 | packed | 3 | 1.000 | 1.000 | 1.000 |

## Control metrics per run (measured)

`composition_end_given_both_hops` = accuracy on the chain end among contexts where both single hops were answered correctly (multi-hop only).

| run_id | variant | seed | in_distribution_acc | evidence_removed_acc | chance_acc | pos_offset_0_acc |
|---|---|---|---|---|---|---|
| fillers_s0_06f531b3 | fillers | 0 | 1.000 | 0.030 | 0.031 | 1.000 |
| fillers_s1_588de66b | fillers | 1 | 1.000 | 0.027 | 0.031 | 1.000 |
| fillers_s2_85c1c382 | fillers | 2 | 0.940 | 0.037 | 0.031 | 0.940 |
| packed_s0_9b274764 | packed | 0 | 1.000 | 0.030 | 0.031 | 1.000 |
| packed_s1_7391834c | packed | 1 | 1.000 | 0.040 | 0.031 | 1.000 |
| packed_s2_d76748a3 | packed | 2 | 1.000 | 0.030 | 0.031 | 1.000 |

## Grid `in_format` (derived: mean across seeds; t-interval over seeds)

| grid | variant | cell_n_queries | n_seeds | n_per_seed | mean | std | min | max | t_lo | t_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| in_format | fillers | 4 | 3 | 400 | 0.973 | 0.048 | 0.917 | 1.000 | 0.854 | 1.091 |
| in_format | packed | 4 | 3 | 400 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Baselines on the identical examples (reference):

| cell_n_queries | oracle | naive_induction | last_value | random_context | chance | best_fixed_offset | best_fixed_offset_d |
|---|---|---|---|---|---|---|---|
| 4 | 1.000 | 1.000 | 0.158 | 0.275 | 0.031 | 0.352 | 21 |

## Paired differences vs `packed` (per-seed differences on identical examples)

| grid | cell_n_queries | a | b | mean_diff | t_lo | t_hi | n_seeds | seeds_a_better | seeds_b_better |
|---|---|---|---|---|---|---|---|---|---|
| in_format | 4 | fillers | packed | -0.028 | -0.146 | 0.091 | 3 | 0 | 1 |

## Figures

![fig_in_format](fig_in_format.png)
![fig_training_curves](fig_training_curves.png)

## Reading guide

* Per-seed Wilson intervals (in `per_seed_cells.csv`) capture example sampling only; the across-seed t-interval captures training variability but is very wide with 3 seeds.
* Interpretation and conclusions are written separately in `docs/results.md`; this report is generated mechanically from the measured tables above.
