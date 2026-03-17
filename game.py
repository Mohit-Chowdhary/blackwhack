import random
from player import Player, AIPlayer
from card import Deck, Card
from typing import List, Dict, Tuple

MAX_ROUNDS = 3

class GameState:
    def __init__(self, difficulty="MEDIUM"):
        self.difficulty = difficulty
        self.deck = Deck()
        self.deck.shuffle()  # shuffle once at game start
        
        self.human = Player("You")
        self.ai1 = AIPlayer("Alice", difficulty, "overshoot")
        self.ai2 = AIPlayer("Bob", difficulty, "undershoot")
        
        self.players: List[Player] = [self.human, self.ai1, self.ai2]
        
        self.round_num = 0
        self.round_started = False
        self.round_over = False
        self.game_over = False
        
        self.all_guesses: Dict[Player, List[Tuple[Player, int, int]]] = {}
        self.round_scores: Dict[Player, int] = {}
        self.winner: Player = None
        
        self.peeking = False

    def start_round(self):
        if self.round_num >= MAX_ROUNDS:
            self.game_over = True
            return
            
        self.round_num += 1
        
        # Clear round-specific card data only, keep cumulative scores
        for p in self.players:
            p.reset_round()
            p.add_cards(self.deck.deal(3))  # 3 cards each from the SAME deck
            p.reveal_random()
            
        self.round_started = True
        self.round_over = False
        self.peeking = random.random() < 0.5
        self.all_guesses = {}
        self.round_scores = {}
        self.winner = None

    def submit_peek(self, target_idx: int):
        if self.peeking:
            target = self.players[target_idx]
            target.reveal_random()
            self.peeking = False
            
    def get_all_known_cards_for(self, player: Player) -> List[Card]:
        known = list(player.cards)
        for p in self.players:
            if p != player:
                known.extend(p.revealed_cards)
        return known

    def total_card_value(self, player: Player) -> int:
        return sum(c.value for c in player.cards)

    def resolve_round(self, guess_alice: int, guess_bob: int):
        actual_alice = self.total_card_value(self.ai1)
        actual_bob = self.total_card_value(self.ai2)
        self.all_guesses[self.human] = [
            (self.ai1, guess_alice, actual_alice),
            (self.ai2, guess_bob, actual_bob),
        ]
        human_error = abs(guess_alice - actual_alice) + abs(guess_bob - actual_bob)
        self.round_scores[self.human] = human_error
        self.human.score += human_error
        
        human_total = self.total_card_value(self.human)
        
        for ai, other_ai in [(self.ai1, self.ai2), (self.ai2, self.ai1)]:
            known = self.get_all_known_cards_for(ai)
            g_human = ai.guess_target(self.human, known)
            g_other = ai.guess_target(other_ai, known)
            actual_other = self.total_card_value(other_ai)
            
            self.all_guesses[ai] = [
                (self.human, g_human, human_total),
                (other_ai, g_other, actual_other),
            ]
            
            ai_error = abs(g_human - human_total) + abs(g_other - actual_other)
            self.round_scores[ai] = ai_error
            ai.score += ai_error
                
        best_score = min(self.round_scores.values())
        winners = [p for p, s in self.round_scores.items() if s == best_score]
        self.winner = winners[0]
            
        for p in self.players:
            for c in p.get_hidden_cards():
                p.revealed_cards.append(c)
                
        self.round_over = True
        
        # Check if game is done
        if self.round_num >= MAX_ROUNDS:
            self.game_over = True

    def get_game_winner(self) -> Player:
        """Overall winner = lowest cumulative score."""
        return min(self.players, key=lambda p: p.score)
