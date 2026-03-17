import pygame
import sys
import math
from game import GameState
from card import Card

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlackWhack")

try:
    # Monospace fonts give a more 'pixely' / retro look
    font = pygame.font.SysFont("Consolas", 22)
    large_font = pygame.font.SysFont("Consolas", 32, bold=True)
    title_font = pygame.font.SysFont("Consolas", 64, bold=True)
    small_font = pygame.font.SysFont("Consolas", 18)
except:
    font = pygame.font.SysFont("monospace", 22)
    large_font = pygame.font.SysFont("monospace", 32, bold=True)
    title_font = pygame.font.SysFont("monospace", 56, bold=True)
    small_font = pygame.font.SysFont("monospace", 18)

WHITE = (250, 250, 250)
BLACK = (20, 20, 20)
RED = (220, 55, 55)
GREEN = (50, 180, 90)
DARK_GREEN = (25, 100, 50)
GRAY = (200, 200, 200)
DARK_GRAY = (70, 70, 70)
BLUE = (50, 100, 200)
LIGHT_BLUE = (100, 150, 250)
GOLD = (255, 215, 0)
CARD_BG = (245, 240, 230)
STAR_BG = (255, 240, 150)

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, text_font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = text_font or large_font

    def draw(self, surface):
        col = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, col, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        img = self.font.render(self.text, True, WHITE)
        surface.blit(img, img.get_rect(center=self.rect.center))

    def update(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def clicked(self, pos, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(pos))

def text_center(surface, text, fnt, color, x, y):
    img = fnt.render(text, True, color)
    surface.blit(img, img.get_rect(center=(x, y)))

def text_left(surface, text, fnt, color, x, y):
    surface.blit(fnt.render(text, True, color), (x, y))

def draw_card(surface, x, y, card: Card, hidden=False):
    rect = pygame.Rect(x, y, 65, 95)
    if hidden:
        pygame.draw.rect(surface, BLUE, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)
        pygame.draw.circle(surface, LIGHT_BLUE, rect.center, 14)
    else:
        # Star card gets a special golden background
        bg = STAR_BG if card.color == "Star" else CARD_BG
        pygame.draw.rect(surface, bg, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)
        
        if card.color == "Star":
            col = GOLD
        elif card.color == "Red":
            col = RED
        else:
            col = BLACK
        
        val = str(card)
        surface.blit(large_font.render(val, True, col), (x + 8, y + 6))
        
        if card.color == "Star":
            # Draw a manual 5-pointed star using polygons
            cx, cy = x + 32, y + 55
            points = []
            for i in range(10):
                angle = math.radians(i * 36) - math.pi / 2
                radius = 20 if i % 2 == 0 else 8
                points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
            pygame.draw.polygon(surface, GOLD, points)
            pygame.draw.polygon(surface, BLACK, points, 2)

def draw_hand(surface, player, x, y, is_human, show_all):
    text_left(surface, f"{player.name}  (Score: {player.score})", font, WHITE, x, y - 30)
    cx = x
    for c in player.cards:
        hidden = not show_all and not is_human and c not in player.revealed_cards
        draw_card(surface, cx, y, c, hidden)
        cx += 75

def main():
    clock = pygame.time.Clock()
    game = None
    state = "START"  # START, HTP, PEEK, GUESS1, GUESS2, OVER, GAMEOVER
    input_text = ""
    guess_alice = 0

    btn_easy = Button(WIDTH//2 - 110, 340, 220, 50, "EASY", DARK_GRAY, GREEN)
    btn_med  = Button(WIDTH//2 - 110, 410, 220, 50, "MEDIUM", DARK_GRAY, BLUE)
    btn_hard = Button(WIDTH//2 - 110, 480, 220, 50, "HARD", DARK_GRAY, RED)
    btn_htp  = Button(WIDTH//2 - 110, 570, 220, 50, "How to Play", DARK_GRAY, GOLD, font)
    btn_back = Button(WIDTH//2 - 100, 520, 200, 50, "Back", DARK_GRAY, RED, font)

    btn_peek1 = Button(WIDTH//2 - 260, 290, 170, 45, "Peek Alice", DARK_GRAY, BLUE, font)
    btn_peek2 = Button(WIDTH//2 + 90,  290, 170, 45, "Peek Bob",   DARK_GRAY, BLUE, font)
    btn_skip  = Button(WIDTH//2 - 85,  350, 170, 45, "Skip",       DARK_GRAY, RED, font)

    btn_submit = Button(WIDTH//2 + 140, 370, 110, 50, "Submit", DARK_GRAY, GREEN, font)
    btn_next = Button(WIDTH//2 - 110, 600, 220, 50, "Next Round", DARK_GRAY, GREEN, font)
    btn_restart = Button(WIDTH//2 - 110, 480, 220, 55, "Play Again", DARK_GRAY, GREEN)

    running = True
    while running:
        screen.fill(DARK_GREEN)
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

            if state == "START":
                for b in [btn_easy, btn_med, btn_hard, btn_htp]:
                    b.update(mouse)
                diff = None
                if btn_easy.clicked(mouse, ev): diff = "EASY"
                if btn_med.clicked(mouse, ev):  diff = "MEDIUM"
                if btn_hard.clicked(mouse, ev): diff = "HARD"
                if diff:
                    game = GameState(diff)
                    game.start_round()
                    state = "PEEK" if game.peeking else "GUESS1"
                    input_text = ""
                if btn_htp.clicked(mouse, ev):
                    state = "HTP"

            elif state == "HTP":
                btn_back.update(mouse)
                if btn_back.clicked(mouse, ev):
                    state = "START"

            elif state == "PEEK":
                for b in [btn_peek1, btn_peek2, btn_skip]:
                    b.update(mouse)
                if btn_peek1.clicked(mouse, ev):
                    game.submit_peek(1); state = "GUESS1"
                elif btn_peek2.clicked(mouse, ev):
                    game.submit_peek(2); state = "GUESS1"
                elif btn_skip.clicked(mouse, ev):
                    game.peeking = False; state = "GUESS1"

            elif state == "GUESS1":
                btn_submit.update(mouse)
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN and input_text.isdigit():
                        guess_alice = int(input_text)
                        input_text = ""
                        state = "GUESS2"
                    elif ev.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif ev.unicode.isdigit() and len(input_text) < 3:
                        input_text += ev.unicode
                if btn_submit.clicked(mouse, ev) and input_text.isdigit():
                    guess_alice = int(input_text)
                    input_text = ""
                    state = "GUESS2"

            elif state == "GUESS2":
                btn_submit.update(mouse)
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN and input_text.isdigit():
                        game.resolve_round(guess_alice, int(input_text))
                        input_text = ""
                        state = "GAMEOVER" if game.game_over else "OVER"
                    elif ev.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif ev.unicode.isdigit() and len(input_text) < 3:
                        input_text += ev.unicode
                if btn_submit.clicked(mouse, ev) and input_text.isdigit():
                    game.resolve_round(guess_alice, int(input_text))
                    input_text = ""
                    state = "GAMEOVER" if game.game_over else "OVER"

            elif state == "OVER":
                btn_next.update(mouse)
                if btn_next.clicked(mouse, ev):
                    game.start_round()
                    state = "PEEK" if game.peeking else "GUESS1"
                    input_text = ""

            elif state == "GAMEOVER":
                btn_restart.update(mouse)
                if btn_restart.clicked(mouse, ev):
                    game = None
                    state = "START"
                    input_text = ""

        # ═══════════ RENDERING ═══════════
        if state == "START":
            text_center(screen, "BLACKWHACK", title_font, BLACK, WIDTH//2, 120)
            text_center(screen, "Select Difficulty", large_font, GRAY, WIDTH//2, 260)
            for b in [btn_easy, btn_med, btn_hard, btn_htp]:
                b.draw(screen)

        elif state == "HTP":
            # How to Play popup - wider box
            overlay_w = 750
            overlay = pygame.Surface((overlay_w, 420))
            overlay.set_alpha(245)
            overlay.fill((10, 10, 10))
            screen.blit(overlay, (WIDTH//2 - overlay_w//2, 110))

            text_center(screen, "HOW TO PLAY", title_font, GOLD, WIDTH//2, 160)
            rules = [
                "27 cards: values 2-14 in Red & Black + one Star card (worth 16)",
                "",
                "3 rounds — each round 3 cards dealt per player, 1 revealed.",
                "You guess the TOTAL card sum of each opponent (Alice & Bob).",
                "They guess yours and each other's too!",
                "",
                "50% chance each round to PEEK at one extra hidden card.",
                "Score = sum of your guess errors. Lowest score after 3 rounds wins!",
            ]
            y = 240
            for line in rules:
                text_center(screen, line, small_font, WHITE, WIDTH//2, y)
                y += 25

            btn_back.draw(screen)

        elif state == "GAMEOVER" and game:
            # Final game over screen
            text_center(screen, "GAME OVER", title_font, WHITE, WIDTH//2, 120)
            
            # Last round results
            y = 180
            for p in game.players:
                guesses_list = game.all_guesses.get(p, [])
                parts = []
                for target, guess, actual in guesses_list:
                    parts.append(f"{target.name}: {guess}/{actual}")
                err = game.round_scores.get(p, 0)
                line = f"{p.name}  →  " + "  |  ".join(parts) + f"  |  Error: {err}"
                text_center(screen, line, small_font, WHITE, WIDTH//2, y)
                y += 25

            y += 20
            text_center(screen, "FINAL SCORES", large_font, GOLD, WIDTH//2, y)
            y += 40
            for p in sorted(game.players, key=lambda p: p.score):
                text_center(screen, f"{p.name}:  {p.score}", large_font, WHITE, WIDTH//2, y)
                y += 40

            overall = game.get_game_winner()
            y += 10
            text_center(screen, f"WINNER:  {overall.name}", title_font, GOLD, WIDTH//2, y)

            btn_restart.draw(screen)

        elif game:
            show_all = (state == "OVER")
            # Round indicator
            text_center(screen, f"Round {game.round_num} / 3", font, GRAY, WIDTH//2, 20)
            
            draw_hand(screen, game.ai1, 60, 70, False, show_all)
            draw_hand(screen, game.ai2, WIDTH - 300, 70, False, show_all)
            draw_hand(screen, game.human, WIDTH//2 - 115, HEIGHT - 160, True, True)

            if state == "PEEK":
                text_center(screen, "PEEK ABILITY!  Reveal one extra card:", large_font, GOLD, WIDTH//2, 240)
                for b in [btn_peek1, btn_peek2, btn_skip]:
                    b.draw(screen)

            elif state in ("GUESS1", "GUESS2"):
                target_name = "Alice" if state == "GUESS1" else "Bob"
                text_center(screen, f"Guess TOTAL card value of {target_name}", large_font, WHITE, WIDTH//2, 300)
                text_center(screen, "(revealed + hidden)", small_font, GRAY, WIDTH//2, 330)

                box = pygame.Rect(WIDTH//2 - 120, 360, 240, 50)
                pygame.draw.rect(screen, WHITE, box)
                pygame.draw.rect(screen, BLACK, box, 2)
                text_center(screen, input_text, large_font, BLACK, box.centerx, box.centery)
                btn_submit.draw(screen)

                if state == "GUESS2":
                    text_center(screen, f"(Alice guess locked: {guess_alice})", small_font, GOLD, WIDTH//2, 430)

            elif state == "OVER":
                overlay = pygame.Surface((700, 380))
                overlay.set_alpha(230)
                overlay.fill((15, 15, 15))
                screen.blit(overlay, (WIDTH//2 - 350, 200))

                text_center(screen, f"ROUND {game.round_num} RESULTS", title_font, WHITE, WIDTH//2, 240)

                y = 290
                for p in game.players:
                    guesses_list = game.all_guesses.get(p, [])
                    parts = []
                    for target, guess, actual in guesses_list:
                        parts.append(f"{target.name}: {guess}/{actual}")
                    err = game.round_scores.get(p, 0)
                    line = f"{p.name}  →  " + "  |  ".join(parts) + f"  |  Error: {err}"
                    text_center(screen, line, small_font, WHITE, WIDTH//2, y)
                    y += 28

                y += 10
                win = game.winner
                text_center(screen, f"Round Winner:  {win.name}", large_font, GOLD, WIDTH//2, y)
                y += 35
                text_center(screen, f"Total  —  You: {game.human.score}  |  Alice: {game.ai1.score}  |  Bob: {game.ai2.score}",
                            font, GRAY, WIDTH//2, y)

                btn_next.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
