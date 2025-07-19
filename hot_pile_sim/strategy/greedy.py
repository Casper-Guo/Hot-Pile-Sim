"""Choose the locally optimal that maximizes the chance of success."""

from __future__ import annotations

from collections import Counter

import numpy as np

from hot_pile_sim.strategy.base import BasePlayer
from hot_pile_sim.util.card_counter import CardCounter


class GreedyPlayer(BasePlayer):
    def play(
        self: GreedyPlayer,
        seen_cards: CardCounter,
        piles: Counter[int],
        hot_pile: int | None,  # noqa: ARG002
    ) -> tuple[int, bool]:
        card_count = np.array(seen_cards)
        seen_leq_count = np.cumsum(card_count)
        seen_geq_count = np.sum(card_count) - seen_leq_count + card_count
        # print(np.stack((card_count, seen_leq_count, seen_geq_count)))

        min_so_far = 100
        best_so_far = (-1, True)

        for pile in piles:
            if seen_leq_count[pile - 2] < min_so_far:
                min_so_far = seen_leq_count[pile - 2]
                best_so_far = (pile, True)

            if seen_geq_count[pile - 2] < min_so_far:
                min_so_far = seen_geq_count[pile - 2]
                best_so_far = (pile, False)

        return best_so_far
