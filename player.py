import random
from typing import List, Optional
from card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards: List[Card] = []
        self.revealed_cards: List[Card] = []
        self.score = 0
        self.is_ai = False
        
    def add_cards(self, cards: List[Card]):
        self.cards.extend(cards)

    def reveal_random(self) -> Optional[Card]:
        hidden = [c for c in self.cards if c not in self.revealed_cards]
        if hidden:
            c = random.choice(hidden)
            self.revealed_cards.append(c)
            return c
        return None

    def get_hidden_cards(self) -> List[Card]:
        return [c for c in self.cards if c not in self.revealed_cards]
        
    def total_value(self) -> int:
        return sum(c.value for c in self.cards)

    def reset_round(self):
        self.cards = []
        self.revealed_cards = []


class AIPlayer(Player):
    def __init__(self, name: str, difficulty: str, personality: str = "neutral"):
        super().__init__(name)
        self.is_ai = True
        self.difficulty = difficulty
        self.personality = personality  # "overshoot" for Alice, "undershoot" for Bob

    def guess_target(self, target: Player, all_known_cards: List[Card]) -> int:
        """Guess the TOTAL card value (revealed + hidden) of a target player."""
        revealed_sum = sum(c.value for c in target.revealed_cards)
        num_hidden = len(target.get_hidden_cards())
        
        if num_hidden == 0:
            return revealed_sum
            
        if self.difficulty == "EASY":
            # Predictable personality-based guessing
            avg_revealed = revealed_sum / max(len(target.revealed_cards), 1)
            
            if self.personality == "overshoot":
                # Alice: sees high revealed → assumes hidden are high too
                if avg_revealed >= 10:
                    per_card = random.randint(10, 13)
                elif avg_revealed >= 7:
                    per_card = random.randint(8, 11)
                else:
                    per_card = random.randint(7, 9)
            else:
                # Bob: sees high revealed → assumes hidden are low (contrarian)
                if avg_revealed >= 10:
                    per_card = random.randint(3, 6)
                elif avg_revealed >= 7:
                    per_card = random.randint(5, 7)
                else:
                    per_card = random.randint(6, 9)
            
            return revealed_sum + per_card * num_hidden
            
        elif self.difficulty == "MEDIUM":
            # Fixed EV of 7.5 per hidden card
            hidden_guess = int(round(7.5 * num_hidden))
            return revealed_sum + hidden_guess
            
        elif self.difficulty == "HARD":
            # Dynamic EV based on remaining cards in the 27-card deck
            all_values = [v for v in range(2, 15)] * 2  # 26 normal cards
            all_values.append(16)  # Star card
            for c in all_known_cards:
                if c.value in all_values:
                    all_values.remove(c.value)
            
            if not all_values:
                avg_value = 7.5
            else:
                avg_value = sum(all_values) / len(all_values)
                
            hidden_guess = int(round(avg_value * num_hidden))
            return revealed_sum + hidden_guess
        
        return revealed_sum + 8 * num_hidden
