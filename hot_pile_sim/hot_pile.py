from __future__ import annotations

import logging
from collections import Counter
from random import shuffle

from hot_pile_sim.strategy.base import BasePlayer
from hot_pile_sim.util.card_counter import CardCounter

logging.basicConfig(level=logging.INFO, format="%(filename)s\t%(levelname)s\t%(message)s")
logger = logging.getLogger(__name__)


def shuffle_deck() -> list[int]:
    deck = list(range(2, 15)) * 4
    shuffle(deck)
    return deck


class HotPile:
    player: BasePlayer
    num_piles: int
    tie_allowed: bool
    # verbosity = 0: no log output
    # verbosity >= 1: basic log output for starting piles and game outcome
    # verbosity >= 2: detailed log output for every action
    verbosity: int
    seen_cards: CardCounter
    piles: Counter[int]
    deck: list[int]

    def __init__(
        self: HotPile,
        player: BasePlayer,
        num_piles: int = 9,
        tie_allowed: bool = False,
        verbosity: int = 0,
    ) -> None:
        """Verbose mode produce log for every action."""
        self.player = player
        self.num_piles = num_piles
        self.tie_allowed = tie_allowed
        self.verbosity = verbosity
        self.seen_cards = CardCounter()
        self.piles = Counter()

        self.setup_game()

    def _format_piles(self: HotPile) -> str:
        return ", ".join([str(i) for i in sorted(self.piles.elements())])

    def _discard_pile(self: HotPile, pile: int) -> None:
        """
        Decrement the count of pile and remove the key when the count reaches zero.

        The latter allow checking whether the game has ended by checking the length of self.piles.
        """
        if pile not in self.piles:
            return

        self.piles[pile] -= 1
        if not self.piles[pile]:
            del self.piles[pile]

    def setup_game(self: HotPile) -> None:
        self.deck = shuffle_deck()

        for _ in range(self.num_piles):
            drawn_card = self.deck.pop()
            self.piles[drawn_card] += 1
            self.seen_cards.add(drawn_card)

        if self.verbosity >= 1:
            logger.info("Starting piles: %s", self._format_piles())

    def on_move(self: HotPile, move_pile: int, above_below: bool, card_drawn: int) -> int | None:
        """Return the new top card if the pile is still active, None if the pile is discarded."""
        if self.verbosity >= 2:
            logger.info("Call is %s %d, %d is drawn.", "above" if above_below else "below", move_pile, card_drawn)

        self._discard_pile(move_pile)
        if (
            (card_drawn == move_pile and self.tie_allowed)
            or (above_below and card_drawn > move_pile)
            or (not above_below and card_drawn < move_pile)
        ):
            self.piles[card_drawn] += 1
            return card_drawn

        if self.verbosity >= 2:
            logger.info("Remaining piles: %s", self._format_piles())
        return None

    def sim_game(self: HotPile) -> int:
        """Return number of cards remaining when the game ended."""
        hot_pile: int | None = None
        while self.deck:
            move_pile, above_below = self.player.play(self.seen_cards, self.piles, hot_pile)
            card_drawn = self.deck.pop()
            hot_pile = self.on_move(move_pile, above_below, card_drawn)
            self.seen_cards.add(card_drawn)

            if not self.piles:
                if self.verbosity >= 1:
                    logger.info("Loss!")
                return len(self.deck)

            if self.verbosity >= 2:
                logger.info("Current piles: %s", self._format_piles())

        if self.verbosity >= 1:
            logger.info("Win!")
        return len(self.deck)

    def reset(self: HotPile) -> None:
        self.seen_cards.reset()
        self.piles.clear()
        self.setup_game()
