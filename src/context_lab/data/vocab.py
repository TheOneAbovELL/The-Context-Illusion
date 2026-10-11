"""A single fixed vocabulary shared by every task, so that all models have the
same embedding/unembedding size regardless of the task they were trained on.

Layout (default sizes):
    0..5      specials  <pad> <bos> <qry> <ans> -> <nxt>
    6..21     fillers   F0..F15   (irrelevant noise tokens)
    22..53    keys      K0..K31
    54..85    values    V0..V31
    86..133   entities  E0..E47   (multi-hop: an entity is both a key and a value)
"""

from __future__ import annotations

from dataclasses import dataclass

SPECIALS = ("<pad>", "<bos>", "<qry>", "<ans>", "->", "<nxt>")
PAD, BOS, QRY, ANS, ARROW, NXT = range(len(SPECIALS))


@dataclass(frozen=True)
class Vocab:
    n_fillers: int = 16
    n_keys: int = 32
    n_values: int = 32
    n_entities: int = 48

    @property
    def filler_start(self) -> int:
        return len(SPECIALS)

    @property
    def key_start(self) -> int:
        return self.filler_start + self.n_fillers

    @property
    def value_start(self) -> int:
        return self.key_start + self.n_keys

    @property
    def entity_start(self) -> int:
        return self.value_start + self.n_values

    @property
    def size(self) -> int:
        return self.entity_start + self.n_entities

    def fillers(self) -> range:
        return range(self.filler_start, self.key_start)

    def keys(self) -> range:
        return range(self.key_start, self.value_start)

    def values(self) -> range:
        return range(self.value_start, self.entity_start)

    def entities(self) -> range:
        return range(self.entity_start, self.size)

    def kind(self, i: int) -> str:
        if i < self.filler_start:
            return "special"
        if i < self.key_start:
            return "filler"
        if i < self.value_start:
            return "key"
        if i < self.entity_start:
            return "value"
        if i < self.size:
            return "entity"
        raise ValueError(f"token id {i} outside vocab of size {self.size}")

    def token_str(self, i: int) -> str:
        k = self.kind(i)
        if k == "special":
            return SPECIALS[i]
        prefix, start = {"filler": ("F", self.filler_start), "key": ("K", self.key_start),
                         "value": ("V", self.value_start), "entity": ("E", self.entity_start)}[k]
        return f"{prefix}{i - start}"

    def decode(self, ids, sep: str = " ") -> str:
        return sep.join(self.token_str(int(i)) for i in ids)


DEFAULT_VOCAB = Vocab()
