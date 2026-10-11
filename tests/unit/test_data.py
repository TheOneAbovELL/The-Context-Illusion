import pytest

from context_lab.data import (DEFAULT_VOCAB, TaskConfig, TaskSampler, check_example, collate, corrupt_query,
                              make_dataset, make_rng, move_evidence, multihop_query_variant, naive_induction,
                              oracle, overlap_count, remove_evidence)
from context_lab.data.tasks import layout_context
from context_lab.data.validate import AmbiguousExample
from context_lab.data.vocab import ANS, ARROW, BOS, NXT, QRY

CONFIGS = {
    "recall": TaskConfig(),
    "lures_repeat": TaskConfig(n_lures=(0, 3), repeat_distractor_keys=True),
    "dense": TaskConfig(fill_pairs=True, seq_len=(16, 64)),
    "position": TaskConfig(evidence_pos=0.3, seq_len=96),
    "distance": TaskConfig(evidence_distance=17, seq_len=(40, 100)),
    "compound": TaskConfig(key_len=2, near_miss_frac=0.7, n_pairs=(4, 8)),
    "aux_queries": TaskConfig(n_queries=(1, 4)),
    "multihop": TaskConfig(task="multihop", hops=(1, 3), query_types=("end", "next"), seq_len=(48, 96)),
    "multihop_gap": TaskConfig(task="multihop", hops=2, hop_gap=9, link_order="forward", seq_len=64),
    "marker_recall": TaskConfig(query_format="ans_marker", n_queries=(1, 3), n_lures=(0, 2)),
    "marker_compound": TaskConfig(query_format="ans_marker", key_len=2, near_miss_frac=0.5),
    "marker_multihop": TaskConfig(task="multihop", query_format="ans_marker", hops=(1, 3),
                                  query_types=("end", "next"), seq_len=(48, 96)),
}


@pytest.mark.parametrize("name", list(CONFIGS))
def test_invariants_hold(name):
    exs = make_dataset(CONFIGS[name], 300, seed=3, stream="test")
    bad = [(i, e) for i, ex in enumerate(exs) for e in check_example(ex)]
    assert bad == []
    assert all(oracle(ex) == ex.answer for ex in exs)


def test_exact_length_and_format():
    for L in (12, 33, 200):
        ex = TaskSampler(TaskConfig(seq_len=L), 0).example()
        assert len(ex.tokens) == L and ex.tokens[0] == BOS and ex.tokens[-2] == QRY
        assert ex.tokens[-1] == ex.meta["_target_key"][0]          # key_last: predict at the key
        mk = TaskSampler(TaskConfig(seq_len=L, query_format="ans_marker"), 0).example()
        assert len(mk.tokens) == L and mk.tokens[-1] == ANS and mk.tokens[-3] == QRY


def test_evidence_position_placement_exact_when_fillers_available():
    for p in (0.0, 0.25, 0.5, 0.75, 1.0):
        exs = make_dataset(TaskConfig(seq_len=128, n_pairs=6, evidence_pos=p), 50, 0, f"p{p}")
        for ex in exs:
            assert ex.meta["evidence_offset"] == ex.meta["evidence_offset_requested"]
            assert abs(ex.meta["evidence_norm_pos"] - p) < 0.01


def test_dense_context_snaps_and_records_actual_position():
    exs = make_dataset(TaskConfig(seq_len=41, fill_pairs=True, evidence_pos=0.5), 50, 0, "dense")
    for ex in exs:
        assert ex.meta["n_fillers"] in (0, 1)
        assert abs(ex.meta["evidence_offset"] - ex.meta["evidence_offset_requested"]) <= 1
        assert check_example(ex) == []


def test_distance_control_is_exact_across_lengths():
    for L in (40, 64, 128, 256):
        exs = make_dataset(TaskConfig(seq_len=L, evidence_distance=20), 20, 0, f"d{L}")
        assert {e.meta["distance"] for e in exs} == {20}
        assert {e.meta["evidence_value_pos"] for e in exs} == {L - 1 - 20}


def test_infeasible_distance_raises():
    with pytest.raises(ValueError):
        TaskSampler(TaskConfig(seq_len=30, evidence_distance=40), 0).example()


def test_position_independent_of_distractor_count_and_length():
    """Changing the evidence position must not change the distractor/length distributions."""
    stats = {}
    for p in (0.0, 0.5, 1.0):
        exs = make_dataset(TaskConfig(seq_len=96, n_pairs=(2, 8), evidence_pos=p), 400, 0, "indep")
        stats[p] = ([(e.meta["n_pairs"], e.answer, tuple(e.meta["_target_key"])) for e in exs],
                    {len(e.tokens) for e in exs})
    # same stream & seed -> identical content per example (paired cells); only placement differs
    assert stats[0.0][0] == stats[0.5][0] == stats[1.0][0]
    assert stats[0.0][1] == stats[1.0][1] == {96}


def test_length_cells_are_paired_in_content():
    a = make_dataset(TaskConfig(seq_len=64, n_pairs=(2, 8)), 200, 0, "eval/len")
    b = make_dataset(TaskConfig(seq_len=256, n_pairs=(2, 8)), 200, 0, "eval/len")
    assert [(e.meta["n_pairs"], e.answer) for e in a] == [(e.meta["n_pairs"], e.answer) for e in b]


def test_distractor_count_control():
    for n in (1, 4, 10):
        exs = make_dataset(TaskConfig(seq_len=64, n_pairs=n), 30, 0, f"n{n}")
        assert {e.meta["n_pairs"] for e in exs} == {n}


def test_lures_counted_and_fool_naive_baseline():
    exs = make_dataset(TaskConfig(seq_len=64, n_lures=2, evidence_pos=0.0), 100, 0, "lure")
    assert {e.meta["n_lures"] for e in exs} == {2}
    # evidence first, lures later -> the last occurrence of the key is always a lure
    assert all(naive_induction(e) != e.answer for e in exs)
    assert all(oracle(e) == e.answer for e in exs)


def test_near_miss_keys_share_prefix():
    exs = make_dataset(TaskConfig(key_len=2, near_miss_frac=1.0, n_pairs=6, seq_len=64), 50, 0, "nm")
    assert all(e.meta["n_near_miss"] == 5 for e in exs)


def test_seed_determinism_and_stream_independence():
    a = make_dataset(TaskConfig(), 50, 1, "train")
    b = make_dataset(TaskConfig(), 50, 1, "train")
    c = make_dataset(TaskConfig(), 50, 1, "eval")
    d = make_dataset(TaskConfig(), 50, 2, "train")
    assert [e.tokens for e in a] == [e.tokens for e in b]
    assert [e.tokens for e in a] != [e.tokens for e in c]
    assert [e.tokens for e in a] != [e.tokens for e in d]


def test_split_integrity_no_overlap():
    train = make_dataset(TaskConfig(), 3000, 0, "train")
    ev = make_dataset(TaskConfig(), 1000, 0, "eval/x")
    assert overlap_count(train, ev) == 0


def test_layout_context_lengths():
    rng = make_rng(0, "layout")
    units, offs = layout_context(rng, 30, [(10, "evidence", [22, 60])], [("pair", [23, 61])] * 3, 22,
                                 DEFAULT_VOCAB.fillers())
    toks = [t for _, _, u in units for t in u]
    assert len(toks) == 30 and offs == [10] and toks[10:12] == [22, 60]


def test_move_evidence_preserves_content():
    ex = TaskSampler(TaskConfig(seq_len=80, n_pairs=5), 0).example()
    for target in (0, 20, 40, 70):
        mv = move_evidence(ex, target)
        assert sorted(mv.tokens) == sorted(ex.tokens)
        assert mv.answer == ex.answer and check_example(mv) == []
        assert abs(mv.meta["evidence_offset"] - target) <= 2


def test_remove_evidence_makes_answer_undetermined():
    ex = TaskSampler(TaskConfig(seq_len=64), 0).example()
    rm = remove_evidence(ex, make_rng(0, "rm"))
    with pytest.raises(AmbiguousExample):
        oracle(rm)


def test_corrupt_query_changes_answer_consistently():
    rng = make_rng(0, "cq")
    for ex in make_dataset(TaskConfig(seq_len=64, n_pairs=(3, 6)), 30, 0, "cq"):
        c = corrupt_query(ex, rng)
        assert c is not None
        assert c.tokens[-1] != ex.tokens[-1]          # a different key is queried
        assert oracle(c) == c.answer                  # (values may coincide across keys by chance)
        assert c.tokens[:-3] == ex.tokens[:-3]


def test_multihop_structure():
    exs = make_dataset(TaskConfig(task="multihop", hops=2, hop_gap=5, link_order="backward", seq_len=64), 40, 0, "m")
    for ex in exs:
        a, b = ex.meta["_link_starts"]
        assert a - b == 3 + 5        # backward: hop 0 link is after hop 1 link, gap 5
        t = ex.tokens
        assert t[a + 1] == ARROW and t[b + 1] == ARROW
    ex = exs[0]
    nxt = multihop_query_variant(ex, "next", 1)
    assert nxt.tokens[-2] == NXT and oracle(nxt) == nxt.answer == ex.meta["_chains"][0][2]
    end = multihop_query_variant(ex, "end", 0)
    assert oracle(end) == ex.answer


def test_aux_queries_positions():
    exs = make_dataset(TaskConfig(n_queries=3, seq_len=64), 30, 0, "aux")
    for ex in exs:
        for pos, ans in ex.meta["_aux"]:
            assert ex.tokens[pos - 1] == QRY and ex.tokens[pos + 1] == ans
    b = collate(exs)
    assert len(b["aux_pos"]) == sum(len(e.meta["_aux"]) for e in exs)


def test_collate_right_pads():
    exs = make_dataset(TaskConfig(seq_len=(20, 40)), 8, 0, "c")
    b = collate(exs)
    for i, e in enumerate(exs):
        assert b["tokens"][i, b["ans_pos"][i]].item() == e.tokens[-1]
        assert b["ans_pos"][i].item() == len(e.tokens) - 1
