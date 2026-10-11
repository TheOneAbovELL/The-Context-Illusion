# Mathematics guide

Every equation below is implemented in `src/context_lab`; file and symbol
names are given so the derivation can be checked against the code.

Notation: batch `B`, sequence length `T`, model width `D`, heads `H`,
head width `d_h = D/H`, vocabulary `V`. Positions are integers
`0..T-1` (plus an optional global `pos_offset`, used only for diagnostics).

---

## 1. Decoder-only Transformer (`models/transformer.py`)

Pre-LayerNorm residual architecture (Xiong et al., 2020):

```
x⁰_t   = E[w_t] (+ P(t) for additive schemes)                 E ∈ R^{V×D}
a      = LN₁(xˡ)
xˡ'    = xˡ + Attn(a)
xˡ⁺¹   = xˡ' + W₂ GELU(W₁ LN₂(xˡ') + b₁) + b₂                 W₁ ∈ R^{D×4D}
logits = LN_f(x^L) W_U                                        W_U ∈ R^{D×V}
```

`LN(z) = γ ⊙ (z − μ(z)) / sqrt(σ²(z) + ε) + β`.

### 1.1 Scaled dot-product attention

For head `h`:

```
q_t = W_Q^h a_t,  k_s = W_K^h a_s,  v_s = W_V^h a_s            ∈ R^{d_h}
S_{t,s} = q_t·k_s / sqrt(d_h) + b_h(t, s)                      (b = 0 unless relative bias)
A_{t,s} = exp(S_{t,s}) / Σ_{s'≤t} exp(S_{t,s'})                (softmax over allowed keys)
z_t     = Σ_s A_{t,s} v_s
Attn(a)_t = W_O [z_t^1; …; z_t^H]
```

The `1/sqrt(d_h)` factor keeps the variance of `q·k` at O(1) when the
components of `q` and `k` have unit variance: `Var(q·k) = d_h`.

### 1.2 Causal masking

`S_{t,s} = −∞` for `s > t` (code: `causal_mask = ones(T,T).triu(1)`,
`masked_fill(..., -inf)`), hence `A_{t,s} = 0` for `s > t` and every row still
sums to one because the diagonal `s = t` is always allowed. Consequently the
output at position `t` is a function of tokens `0..t` only. Tests:
`test_causal_mask` (perturbing future tokens leaves earlier logits unchanged),
`test_attention_probabilities_are_causal_and_normalised`, and a per-run
`mask_check` on every trained model.

### 1.3 Softmax dilution (why length can hurt even with perfect matching)

Suppose a head assigns score `σ_e` to the evidence and `σ_j` to `n` competing
positions. Then

```
A_e = 1 / (1 + Σ_j exp(σ_j − σ_e)).
```

If every competitor sits at a fixed gap `Δ = σ_e − σ_j`, `A_e = 1/(1 + n e^{−Δ})`:
attention to the evidence **decays with the number of competitors at a fixed
score gap**. Keeping `A_e` constant as `n` grows requires `Δ` to grow like
`log n`. This motivates the diagnostic `score_gap` reported by
`diagnostics.attention_role_profile`, which separates "the match got worse"
(smaller `Δ`) from "the same match is diluted by more tokens" (larger `n`).

### 1.4 Training objective

For the retrieval tasks the loss is the cross-entropy of the answer token at
the final `<ans>` position(s):

```
L = −(1/|A|) Σ_{(b,t)∈A} log softmax(logits_{b,t})[y_{b,t}]
```

where `A` contains the scored `<ans>` position of each sequence plus any
auxiliary training-query positions (§5 of `datasets.md`).
`Transformer.lm_loss` implements the ordinary next-token loss over all
positions for completeness.

---

## 2. Positional representations (`positional/`)

All schemes implement one interface (`PositionalScheme`) with three hooks:
an additive input embedding, a rotation of `(q, k)`, and an additive attention
bias. The attention code is identical for every scheme.

### 2.1 Learned absolute (`absolute.py: LearnedAbsolute`)

`x⁰_t = E[w_t] + P_t` with a trainable table `P ∈ R^{N_max×D}`. Positions
`≥ N_max` raise `PositionOverflowError` — the code never clamps or wraps.
Rows that never occur in training receive **zero gradient** (verified in
`test_gradient_flow`) and are excluded from weight decay, so they remain at
their random initialisation `N(0, σ_P²)`. Evaluating at such positions feeds
the network inputs drawn from a distribution it was never trained on.

### 2.2 Sinusoidal (`absolute.py: Sinusoidal`)

```
PE(t)_{2i}   = sin(t · ω_i),   PE(t)_{2i+1} = cos(t · ω_i),   ω_i = 10000^{−2i/D}
```

Properties used in the analysis:

* **Defined for every t**, so there is no overflow, but large `t` still yields
  vectors never seen in training (unseen phase combinations of the slow
  frequencies).
* **Linear relative shift.** For each frequency, `[sin((t+k)ω), cos((t+k)ω)]`
  is a fixed rotation `R(kω)` of `[sin(tω), cos(tω)]`, so `PE(t+k) = M_k PE(t)`
  for a block-diagonal orthogonal `M_k` independent of `t`. This makes
  relative offsets *linearly accessible* — it does not make the model
  translation invariant, because `PE(t)` is added to the content and passes
  through LayerNorm and the nonlinear network.
* **Norm.** `‖PE(t)‖² = D/2` for every `t` (each pair contributes
  `sin²+cos²=1`), i.e. RMS 1/√2 per dimension. Token embeddings are initialised
  with σ = 0.02, so an unscaled sinusoid would dominate the token signal by a
  factor ≈ 35. We therefore multiply PE by `s = 0.02·√2` (`sinusoidal_scale`),
  giving the same per-dimension RMS as the token embeddings and the learned
  table (σ_P = 0.02) at initialisation. This is a fairness choice; other scales
  are possible and would change sinusoidal results.

### 2.3 Rotary position embedding (`rope.py`)

Split `q, k ∈ R^{d_h}` into `d_h/2` planes. Plane `i` at position `m` is rotated
by angle `m θ_i`, `θ_i = b^{−2i/d_h}` (`b = 10000`):

```
R_m = diag(R(mθ_0), …, R(mθ_{d_h/2−1})),   R(φ) = [[cos φ, −sin φ], [sin φ, cos φ]]
q'_m = R_m q,   k'_n = R_n k.
```

Because each `R(φ)` is orthogonal and `R(α)ᵀR(β) = R(β − α)`:

```
q'_m · k'_n = qᵀ R_mᵀ R_n k = qᵀ R_{n−m} k.
```

The logit depends on positions **only through `n − m`**. Values are not
rotated, so no positional signal enters the residual stream directly.
Code layout: "rotate-half" (`plane i = dims (i, i + d_h/2)`):
`x' = x ⊙ cos + rotate_half(x) ⊙ sin` with `rotate_half([x₁, x₂]) = [−x₂, x₁]`.
This is the interleaved formulation of the RoFormer paper under a fixed
permutation of dimensions, which `W_Q`, `W_K` absorb. Shapes: `q, k: (B,H,T,d_h)`,
`cos, sin: (T, d_h)` broadcast over `B, H`.

Verified numerically (`test_rope_preserves_norm_and_is_relative`,
`test_rope_attention_scores_depend_only_on_relative_position`): norms are
preserved to 1e-5, scores at `(3,1)` and `(103,101)` agree to 1e-4, and all
attention logits of a model are unchanged by a global `pos_offset` of 77.

**Long-term decay.** For random `q = k`, `E[q·R_d k]` oscillates and decays in
`d` (`positional_structure` plots it). This is a property of the expected
inner product at initialisation; trained `W_Q, W_K` can concentrate on low
frequencies and need not decay.

**Numerical note.** Angles `mθ_0 = m` radians for the fastest plane; we
compute `cos/sin` in float32 from `positions.float()`; for the lengths used
here (`≤ 1024`) the absolute error is far below 1e-4.

Only plain RoPE is used in experiments. The code accepts a `rope_scale` (<1
gives linear position interpolation, Chen et al. 2023) but no experiment
relies on it.

### 2.4 Relative position: T5 bucketed bias (`relative.py: T5RelativeBias`)

This is the relative method selected for the main comparison. With
`n = t − s ≥ 0` (query minus key position, the only non-masked case):

```
bucket(n) = n                                                    if n < N/2
          = min(N−1, N/2 + ⌊ log(n/(N/2)) / log(D_max/(N/2)) · (N − N/2) ⌋)  otherwise
S_{t,s} = q_t·k_s/sqrt(d_h) + β_{h, bucket(t−s)}
```

`N = 32` buckets, `D_max = 128`, one trainable scalar per (bucket, head),
shared across layers (as in T5). Which parts depend on relative position: only
the additive logit bias `β`; the content term `q·k` and the values are
position-free. Consequences:

* Every distance `≥ D_max` maps to the same bucket — beyond `D_max` the model
  **cannot distinguish distances at all** (by construction, not by training).
* Distances between `N/2` and `D_max` are bucketed logarithmically, so
  resolution coarsens with distance.
* Extra cost: one `(H, T, T)` bias gather per forward pass, i.e. O(H T²) time
  and memory, the same order as the attention matrix itself; `N·H = 128`
  parameters.

Unidirectional bucketing (all buckets spent on `n ≥ 0`) is a deliberate
adaptation to the causal setting; T5's encoder uses half the buckets for each
direction.

### 2.5 ALiBi (`relative.py: ALiBi`)

`S_{t,s} = q_t·k_s/sqrt(d_h) − m_h (t − s)` with fixed slopes
`m_h = 2^{−8h/H}` (`h = 1..H`). A head with slope `m` down-weights a key at
distance `n` by `e^{−m n}` relative to an equally matching key at distance 0;
retrieving from distance `n` against a nearby competitor therefore requires a
content-score advantage `Δ > m n`. With `H = 4` the slopes are
`1/4, 1/16, 1/64, 1/256`, so only the shallowest head can reach far.

### 2.6 NoPE (`base.py: NoPositional`)

No positional signal. Causal masking still breaks permutation symmetry: a
head that attends uniformly over the prefix produces an output whose
statistics depend on `t` (e.g. a BOS-attention fraction `≈ 1/(t+1)`), so
position can be inferred (Haviv et al., 2022). Included as a control.

---

## 3. Statistics (`evaluation/stats.py`)

**Wilson score interval** for `k` successes in `n` trials, `p̂ = k/n`,
`z = 1.96`:

```
centre = (p̂ + z²/2n) / (1 + z²/n)
half   = z sqrt(p̂(1−p̂)/n + z²/4n²) / (1 + z²/n)
```

It treats examples within a cell as i.i.d. draws from that cell's
generator; it does **not** cover variation across training seeds.

**Across seeds**: mean, sample s.d., and `mean ± t_{0.975, k−1} · s/√k`. With
`k = 3`, `t = 4.30`: intervals are wide by design.

**Paired method comparisons**: all runs of a study are evaluated on identical
examples (shared evaluation seed), so per-seed differences
`acc_A(seed) − acc_B(seed)` are paired; we report their mean, t-interval and
the number of seeds where each method is better. An exact McNemar test is
available for example-level comparisons within one seed.

---

## 4. Causal interventions (`interventions/causal.py`)

**Attention knockout.** At layer `l`, set `S_{t*,s} = −∞` for the `<ans>`
position `t*` and `s` in a chosen set, and renormalise. Comparing the
evidence set with an equal-size control set (a random distractor pair)
isolates the effect of the *direct* `<ans>`→evidence read at that layer.

**Activation patching.** For clean input `x` and corrupted input `x̃` (evidence
value `v` replaced by `v'`, so the correct answer becomes `v'`), with
`LD(·) = logit_v − logit_{v'}` at `<ans>`:

```
R(l, p) = (LD(x̃ with h_{l,p} ← h_{l,p}(x)) − LD(x̃)) / (LD(x) − LD(x̃)).
```

Built-in controls (tested in `test_patching_has_builtin_negative_and_positive_controls`):
positions strictly before the corrupted token have identical activations in
both runs, so `R = 0` exactly; patching the final residual at `<ans>` gives
`R = 1` exactly.

**Head ablation.** Replace head `h`'s output `z^h` by zeros at all positions;
report the change in accuracy. Zero-ablation moves activations off-distribution,
so it upper-bounds rather than measures a head's contribution.
