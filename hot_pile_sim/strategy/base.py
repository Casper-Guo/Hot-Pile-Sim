from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter

from hot_pile_sim.util.card_counter import CardCounter


class BasePlayer(ABC):
    @abstractmethod
    def play(
        self: BasePlayer,
        seen_cards: CardCounter,
        piles: Counter[int],
        hot_pile: int | None,
    ) -> tuple[int, bool]:
        """
        Return the pile to play and the above/below call.

        True for above, False for below.
        """
        ...
