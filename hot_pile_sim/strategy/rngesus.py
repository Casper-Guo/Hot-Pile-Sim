from __future__ import annotations

from collections import Counter
from random import choice, randint

from hot_pile_sim.strategy.base import BasePlayer
from hot_pile_sim.util.card_counter import CardCounter


class RandomPlayer(BasePlayer):
    def play(
        self: RandomPlayer,
        seen_cards: CardCounter,  # noqa: ARG002
        piles: Counter[int],
        hot_pile: int | None,  # noqa: ARG002
    ) -> tuple[int, bool]:
        return choice(list(piles.elements())), bool(randint(0, 1))
