# SUPERSEDED — elimination shortcut in the training design

These runs were trained with dense auxiliary queries of the form `<qry> K <ans> V`, which DISPLAY
each queried distractor's value. When (almost) every association is queried, the scored answer is
the only context value that has not been displayed, so it can be found by elimination without
binding keys to values. Verified on 2026-10-11: the fillers-study models score exactly the elimination
baseline when one or two unqueried decoy pairs are added (0.52/0.49/0.50 vs 0.50; 0.37/0.38/0.34 vs
0.35), and the main-study RoPE models were at the value-guessing level (0.27-0.29) in the
single-query evaluation format, with key-swap follow rate 0.00-0.02 when originally correct.

Kept unchanged as a record of the flaw (docs/book/development_log.md, docs/results.md).
The corrected studies hide auxiliary answers (`aux_show_answers: false`).
