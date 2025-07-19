"""Choose the locally optimal that maximizes the chance of success."""

from __future__ import annotations

from collections import Counter

import numpy as np

from hot_pile_sim.strategy.base import BasePlayer
from hot_pile_sim.util.card_counter import CardCounter


class GreedyPlayer(BasePlayer):
    greater_than_count = np.array([4 * (12 - i) for i in range(13)])
    less_than_count = np.array([4 * i for i in range(13)])

    def play(
        self: GreedyPlayer,
        seen_cards: CardCounter,
        piles: Counter[int],
        hot_pile: int | None,  # noqa: ARG002
    ) -> tuple[int, bool]:
        card_count = np.array(seen_cards)
        seen_leq_count = np.cumsum(card_count)
        remaining_less_than_count = GreedyPlayer.less_than_count - (seen_leq_count - card_count)
        remaining_greater_than_count = GreedyPlayer.greater_than_count - (np.sum(card_count) - seen_leq_count)

        max_so_far = -1
        best_so_far = (-1, True)

        for pile in piles:
            if remaining_greater_than_count[pile - 2] > max_so_far:
                max_so_far = remaining_greater_than_count[pile - 2]
                best_so_far = (pile, True)

            if remaining_less_than_count[pile - 2] > max_so_far:
                max_so_far = remaining_less_than_count[pile - 2]
                best_so_far = (pile, False)

        return best_so_far
