# Dataset handbook

All data are synthetic, generated on the fly by `src/context_lab/data/tasks.py`
from seeded NumPy generators. Nothing is downloaded.

## 1. Vocabulary (`data/vocab.py`)

One fixed vocabulary of 134 tokens is shared by every task, so every model has
identical embedding and unembedding sizes:

| ids | tokens | role |
|---|---|---|
| 0–5 | `<pad> <bos> <qry> <ans> -> <nxt>` | specials |
| 6–21 | `F0..F15` | fillers (irrelevant noise) |
| 22–53 | `K0..K31` | keys |
| 54–85 | `V0..V31` | values |
| 86–133 | `E0..E47` | entities (multi-hop; both "keys" and "values") |

Token identities are shared between training and evaluation; **mappings are
not** — every example draws a fresh random key→value assignment, so a model
cannot memorise answers and must read the context. The only way an evaluation
example could be "seen" is an exact duplicate sequence, which is measured
(§7).

## 2. Sequence format

```
<bos>  [context: C tokens]  <qry> KEY            → target: VALUE   (query_format = key_last, default)
<bos>  [context: C tokens]  <qry> KEY <ans>      → target: VALUE   (query_format = ans_marker)
```

The model is scored on its next-token prediction at the final position
(`T−1`), which holds the (last) query-key token in the default format.
`seq_len` is the **total** length `T` including `<bos>` and the query block,
so the context length is `C = T − 1 − (key_len + 1)` (one more for
`ans_marker`). Multi-hop queries are `<qry> e` / `<nxt> e` (+ `<ans>`).

`ans_marker` was the original design; calibration showed models trained on
it stalled at "pick any in-context value" accuracy, so all studies use
`key_last` (the standard associative-recall layout). Both formats remain
available and validated so the comparison can be reproduced
(`docs/results.md §1`).

## 3. Units and the layout engine

The context is a concatenation of units:

| unit | tokens | meaning |
|---|---|---|
| `evidence` | `K* V*` | the association the query asks about (`K*` = query key) |
| `pair` | `K V` | distractor association (`K ≠ K*`) |
| `lure` | `K* F` | the query key in a non-key role — a misleading, non-matching pattern (never followed by a value) |
| `filler` | `F` | single irrelevant token |
| `link` / `target_link` | `A -> B` | multi-hop association |

`layout_context` places *fixed* units at exact token offsets and distributes
the *free* units over the remaining gaps (number per gap ~ Binomial with
probability proportional to gap size), then fills the rest with filler
tokens and shuffles within each gap. If an exact offset is impossible (e.g. no
fillers available), the evidence is **snapped to the nearest feasible
offset and the actual offset is recorded**; all analyses bin on actual values.

**Content vs placement RNG.** Each example first draws its *content*
(number of queries, number of pairs and lures, keys, values) from the stream
RNG, then draws one integer that seeds a private *placement* RNG used for
everything positional. Therefore changing only placement variables
(`evidence_pos`, `evidence_distance`) — or the sequence length, as long as the
requested number of pairs still fits — leaves the content of example *i*
unchanged. Evaluation grids exploit this: all cells of a grid share one content
stream, so grid cells are **paired** (tested in
`test_position_grid_is_paired_and_isolates_position`,
`test_length_cells_are_paired_in_content`).

## 4. Tasks

### Task A — single-item associative recall (`task: recall`)
`n_pairs` associations (one evidence + `n_pairs−1` distractors), keys distinct
by default, values drawn uniformly with replacement from 32 values. Metric:
exact-match accuracy of the answer token.

### Task B — position-controlled retrieval (`evidence_pos ∈ [0,1]`)
The evidence offset is `round(p · (C − m))`, `m = key_len + 1`. `p = 0` puts the
evidence immediately after `<bos>`; `p = 1` immediately before the query.
Sequence length and distractor count are set independently.

### Task C — distractor robustness
Independent knobs:
* `n_pairs` — number of distractor *associations* (at fixed length, more pairs
  = fewer fillers);
* `n_lures` / `lure_prob` — occurrences of the query key followed by a filler;
* `repeat_distractor_keys` — distractor keys may repeat among themselves (with
  different values); the query key is still unique;
* `key_len = 2` + `near_miss_frac` — compound keys; a near-miss distractor
  shares the first sub-token with the query key. This is the controlled
  notion of **distractor similarity** used here (number of shared key
  sub-tokens: 0 or 1 of 2).

Unambiguity is guaranteed by construction and re-verified by the oracle
parser: exactly one `key value` association matches the query.

### Task D — long-range dependency (`evidence_distance = d`)
Puts the evidence value exactly `d` tokens before the `<ans>` position.
Varying `seq_len` at fixed `d` changes the **absolute** position of the
evidence (`T − 1 − d`) and the amount of preceding context while the
**relative** distance stays fixed; varying `d` at fixed `seq_len` does the
opposite. Together they separate distance effects from absolute-position
effects.

### Task E — multi-hop retrieval (`task: multihop`)
Chains `e₀ -> e₁ -> … -> e_h`. Distractor chains with disjoint entities (lengths
drawn from the same `hops` range) are interleaved with fillers.
* `<qry> e₀ <ans>` → `e_h` (follow the chain to its end),
* `<nxt> e_i <ans>` → `e_{i+1}` (a single hop).
`link_order` (`forward`/`backward`/`random`) controls the order of the target
links in the context; `hop_gap` sets the exact token gap between consecutive
target links. `multihop_query_variant` re-queries the *same* context with a
different query, which lets us ask on identical inputs: does the model get
each single hop right, and does it get their composition right?

The query entity always starts its chain (no incoming link) and every entity
has at most one successor, so the chain end is unique (oracle-verified).

### Task F — length generalisation
Training draws one length per batch uniformly from `seq_len = [lo, hi]`.
Evaluation grids vary `seq_len` beyond `hi`; every evaluation row carries
`length_regime ∈ {in_range, extrapolation, shorter}`.

## 5. Auxiliary training queries (`n_queries`)

Pilot runs showed the single supervised token per sequence made learning very
slow (see `docs/results.md`, calibration). With `n_queries = [1, 4]`, a
training sequence may contain up to three extra blocks
`<qry> K V` about *distractor* pairs (distinct keys, never the target)
before the final scored query, and the loss averages over all `<ans>`
positions. Evaluation always uses `n_queries = 1`, which is inside the
training distribution (≈ ¼ of training sequences have a single query). The
final query's evidence distance therefore includes the auxiliary blocks during
training; evaluation distances are computed from actual positions.

## 6. Validation (`data/validate.py`)

* `oracle(ex)` re-derives the answer **from tokens alone** (it never reads the
  generator's metadata): recall — greedy unit parser, then unique-match
  lookup; multi-hop — successor map, follow to the end.
* `check_example` additionally verifies length, `<bos>`/`<ans>` placement, no
  padding, evidence key/value at the recorded positions, recorded distance,
  number of parsed pairs, number of lure occurrences, multi-hop link
  positions.
* Every run validates every evaluation example (`metrics.json →
  validity.eval_examples_with_violations`); tests check all task variants and
  every grid of every study config (`tests/scientific`).

## 7. Splits and leakage

| stream | seed | used for |
|---|---|---|
| `train` | run seed | training batches (infinite) |
| `val` | run seed | in-distribution validation during training |
| `eval/<grid>` | study `eval_seed` | evaluation grids (shared by all runs) |
| `eval/controls/...` | study `eval_seed` | controls |
| `analysis/...` | study `eval_seed` | mechanistic analysis sets |

Streams are independent `SeedSequence` children (`stable_hash(stream)`).
Each run samples 5,000 training examples from its actual training stream and
counts exact duplicates among its evaluation examples
(`validity.n_eval_in_train_sample`).

## 8. Baselines (`data/baselines.py`)

Computed on the identical evaluation examples and reported next to model
accuracy: `oracle` (must be 1.0), `naive_induction` (copy the token after the
last occurrence of the query key — fooled by lures; one hop only),
`last_value` (recency), `random_context` (expected accuracy of guessing among
in-context values) and `chance` (1/32 values, 1/48 entities).

## 9. Reporting actual distributions

`ctxlab gen --set ...` prints examples, invariant violations, a length
summary (min/max/mean, distinct lengths, unique sequences) and baselines.
Every evaluation row stores the realised `seq_len`, `n_pairs`, `n_lures`,
`n_fillers`, `evidence_offset` (and the requested one), `evidence_norm_pos`
and `distance`, so reported distributions are the realised ones.
