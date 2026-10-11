# Research references

Every entry was checked on 2026-10-11 against arXiv's official records
(`export.arxiv.org` API, equivalent to the `arxiv.org/abs/<id>` page), the
publisher page, or Crossref. Venues are listed only where the arXiv record
states them. The "used for" column says how this project relies on the work;
it does not claim that the paper establishes our findings.

## Positional representations

| # | reference | used for |
|---|---|---|
| 1 | Vaswani, Shazeer, Parmar et al. (2017). *Attention Is All You Need.* arXiv:1706.03762 | Transformer, scaled dot-product attention, sinusoidal encoding |
| 2 | Shaw, Uszkoreit, Vaswani (2018). *Self-Attention with Relative Position Representations.* NAACL 2018. arXiv:1803.02155 | relative-position attention (background) |
| 3 | Raffel, Shazeer, Roberts et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer.* arXiv:1910.10683 | T5 bucketed relative position bias (our relative method) |
| 4 | Su, Lu, Pan et al. (2021). *RoFormer: Enhanced Transformer with Rotary Position Embedding.* arXiv:2104.09864 | RoPE; relative-position property of rotated q·k |
| 5 | Press, Smith, Lewis (2021). *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation.* arXiv:2108.12409 | ALiBi and its slope recipe |
| 6 | Haviv, Ram, Press et al. (2022). *Transformer Language Models without Positional Encodings Still Learn Positional Information.* Findings of EMNLP 2022. arXiv:2203.16634 | NoPE control; causal mask as implicit position signal |
| 7 | Kazemnejad, Padhi, Natesan Ramamurthy et al. (2023). *The Impact of Positional Encoding on Length Generalization in Transformers.* NeurIPS 2023. arXiv:2305.19466 | prior comparison of NoPE/APE/T5/ALiBi/RoPE on length generalisation (their tasks differ from ours) |
| 8 | Chen, Wong, Chen et al. (2023). *Extending Context Window of Large Language Models via Positional Interpolation.* arXiv:2306.15595 | `rope_scale` option (implemented, not used in experiments) |

## Long-context retrieval and associative recall

| # | reference | used for |
|---|---|---|
| 9 | Liu, Lin, Hewitt et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL (accepted). arXiv:2307.03172 | motivation for position-controlled evaluation (large pretrained LMs; we test small models trained from scratch) |
| 10 | Hsieh, Sun, Kriman et al. (2024). *RULER: What's the Real Context Size of Your Long-Context Language Models?* COLM 2024. arXiv:2404.06654 | synthetic long-context evaluation beyond single-needle retrieval (background) |
| 11 | Graves, Wayne, Danihelka (2014). *Neural Turing Machines.* arXiv:1410.5401 | associative recall as a synthetic task |
| 12 | Ba, Hinton, Mnih et al. (2016). *Using Fast Weights to Attend to the Recent Past.* arXiv:1610.06258 | associative retrieval task (background) |
| 13 | Arora, Eyuboglu, Timalsina et al. (2023). *Zoology: Measuring and Improving Recall in Efficient Language Models.* arXiv:2312.04927 | multi-query associative recall; motivates auxiliary training queries |
| 14 | Press, Zhang, Min et al. (2022). *Measuring and Narrowing the Compositionality Gap in Language Models.* Findings of EMNLP 2023. arXiv:2210.03350 | "compositionality gap" notion behind our composition control |

## Mechanistic interpretability and interventions

| # | reference | used for |
|---|---|---|
| 15 | Elhage, Nanda, Olsson et al. (2021). *A Mathematical Framework for Transformer Circuits.* Transformer Circuits Thread. https://transformer-circuits.pub/2021/framework/index.html | QK/OV decomposition; induction heads need ≥ 2 layers |
| 16 | Olsson, Elhage, Nanda et al. (2022). *In-context Learning and Induction Heads.* arXiv:2209.11895 | induction heads ([A][B] … [A] → [B]) as the expected retrieval mechanism |
| 17 | Meng, Bau, Andonian et al. (2022). *Locating and Editing Factual Associations in GPT.* NeurIPS 2022. arXiv:2202.05262 | causal tracing / clean–corrupt restoration |
| 18 | Vig, Gehrmann, Belinkov et al. (2020). *Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias.* arXiv:2004.12265 | intervention-based attribution (background) |
| 19 | Zhang, Nanda (2023). *Towards Best Practices of Activation Patching in Language Models: Metrics and Methods.* ICLR 2024. arXiv:2309.16042 | logit-difference metric; corruption choice matters |
| 20 | Heimersheim, Nanda (2024). *How to use and interpret activation patching.* arXiv:2404.15255 | interpretation caveats for patching |
| 21 | Jain, Wallace (2019). *Attention is not Explanation.* NAACL 2019. arXiv:1902.10186 | caution: attention weights ≠ explanation |
| 22 | Wiegreffe, Pinter (2019). *Attention is not not Explanation.* EMNLP 2019. arXiv:1908.04626 | counterpoint: depends on the definition of explanation |

## Architecture, optimisation, statistics

| # | reference | used for |
|---|---|---|
| 23 | Xiong, Yang, He et al. (2020). *On Layer Normalization in the Transformer Architecture.* ICML 2020. arXiv:2002.04745 | pre-LN blocks |
| 24 | Ba, Kiros, Hinton (2016). *Layer Normalization.* arXiv:1607.06450 | LayerNorm |
| 25 | Hendrycks, Gimpel (2016). *Gaussian Error Linear Units (GELUs).* arXiv:1606.08415 | MLP activation |
| 26 | Loshchilov, Hutter (2017). *Decoupled Weight Decay Regularization.* ICLR 2019. arXiv:1711.05101 | AdamW |
| 27 | Wilson, E. B. (1927). *Probable Inference, the Law of Succession, and Statistical Inference.* JASA 22(158):209–212. doi:10.1080/01621459.1927.10502953 | Wilson score interval |

## Software documentation

* PyTorch (`torch` 2.10, CPU build) — https://pytorch.org/docs/stable/
* NumPy random `SeedSequence` / `Generator` — https://numpy.org/doc/stable/reference/random/
* Streamlit — https://docs.streamlit.io/
