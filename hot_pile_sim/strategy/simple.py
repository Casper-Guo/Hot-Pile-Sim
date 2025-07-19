from __future__ import annotations

from collections import Counter
from random import choice, randint

from hot_pile_sim.strategy.base import BasePlayer
from hot_pile_sim.util.card_counter import CardCounter


class SimplePlayer(BasePlayer):
    def play(
        self: SimplePlayer,
        seen_cards: CardCounter,  # noqa: ARG002
        piles: Counter[int],
        hot_pile: int | None,
    ) -> tuple[int, bool]:
        if hot_pile is None:
            hot_pile = choice(list(piles.elements()))
        if hot_pile < 8:
            return hot_pile, True
        if hot_pile > 8:
            return hot_pile, False
        return hot_pile, bool(randint(0, 1))
