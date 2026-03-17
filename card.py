import random
from typing import List

class Card:
    def __init__(self, value: int, color: str):
        self.value = value
        self.color = color  # "Red", "Black", or "Star"

    def __repr__(self):
        if self.color == "Star":
            return "S16"
        val_str = str(self.value)
        if self.value == 11: val_str = "J"
        elif self.value == 12: val_str = "Q"
        elif self.value == 13: val_str = "K"
        elif self.value == 14: val_str = "A"
        return val_str

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self._build()

    def _build(self):
        self.cards = []
        for color in ["Red", "Black"]:
            for value in range(2, 15):  # 2-14, 13 each = 26
                self.cards.append(Card(value, color))
        # Add the Star card (value 16)
        self.cards.append(Card(16, "Star"))
        # Total: 27 cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num: int) -> List[Card]:
        dealt = []
        for _ in range(num):
            if self.cards:
                dealt.append(self.cards.pop())
        return dealt

    def remaining(self) -> int:
        return len(self.cards)
