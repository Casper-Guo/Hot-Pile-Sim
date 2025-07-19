from __future__ import annotations


class CardCounter(list):
    """Effectively a 2-indexed list."""

    def __init__(self: CardCounter) -> None:
        super().__init__([0] * 13)

    def add(self: list[int], card: int) -> None:
        assert 2 <= card <= 14
        self[card - 2] += 1

    def get(self: list[int], card: int) -> int:
        assert 2 <= card <= 14
        return self[card - 2]

    def reset(self: list[int]) -> None:
        for i in range(13):
            self[i] = 0
