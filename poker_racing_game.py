import random
import time
import os
import pygame
import sys
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
CARD_WIDTH = 70
CARD_HEIGHT = 100
GRID_MARGIN = 40
GRID_TOP = 180
GRID_LEFT = 300
GRID_SPACING = 100
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GREEN = (0, 100, 0)

class Card:
    def __init__(self, suit):
        self.suit = suit
        self.symbol = self.get_symbol()
        self.color = self.get_color()
        
    def get_symbol(self):
        if self.suit == "club":
            return "♣"
        elif self.suit == "heart":
            return "♥"
        elif self.suit == "spade":
            return "♠"
        elif self.suit == "diamond":
            return "♦"
        elif self.suit == "joker":
            return "J"  # Changed from emoji to a simple letter
        return "?"
    
    def get_color(self):
        if self.suit in ["heart", "diamond"]:
            return RED
        elif self.suit == "joker":
            return (128, 0, 128)  # Purple for Joker
        else:
            return BLACK
    
    def __str__(self):
        if self.suit == "joker":
            return "Joker"
        return self.symbol
    
    def draw(self, surface, x, y, hidden=False):
        # Draw card background with rounded edges
        pygame.draw.rect(surface, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=10)
        pygame.draw.rect(surface, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=10)
        
        if hidden:
            # Draw a classic card back design like in the image
            card_color = (30, 90, 180)  # Blue like in the image
            pygame.draw.rect(surface, card_color, (x + 2, y + 2, CARD_WIDTH - 4, CARD_HEIGHT - 4), border_radius=8)
            
            # Border pattern
            border_width = 6
            inner_rect = pygame.Rect(x + border_width, y + border_width, 
                                    CARD_WIDTH - 2*border_width, CARD_HEIGHT - 2*border_width)
            pygame.draw.rect(surface, card_color, inner_rect, border_radius=8)
            
            # Draw ornate border pattern
            for i in range(border_width, 0, -1):
                border_color = (255, 255, 255) if i % 2 == 0 else card_color
                pygame.draw.rect(surface, border_color, 
                               (x + i, y + i, CARD_WIDTH - 2*i, CARD_HEIGHT - 2*i), 1, border_radius=8)
            
            # Draw vertical stripe on left and right sides
            stripe_width = 10
            left_stripe = pygame.Rect(x + border_width + 4, y + border_width + 4, 
                                     stripe_width, CARD_HEIGHT - 2*(border_width + 4))
            right_stripe = pygame.Rect(x + CARD_WIDTH - border_width - 4 - stripe_width, 
                                      y + border_width + 4, 
                                      stripe_width, CARD_HEIGHT - 2*(border_width + 4))
            
            pygame.draw.rect(surface, (255, 255, 255), left_stripe, 1)
            pygame.draw.rect(surface, (255, 255, 255), right_stripe, 1)
            
            # Draw central pattern
            center_x = x + CARD_WIDTH // 2
            center_y = y + CARD_HEIGHT // 2
            
            # Outer circle
            radius = min(CARD_WIDTH, CARD_HEIGHT) // 5
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), radius, 1)
            
            # Inner circle
            inner_radius = radius - 4
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), inner_radius, 1)
            
            # Draw ornate pattern inside the circle
            points = 8
            for i in range(points):
                angle = 2 * math.pi * i / points
                
                # Outer points
                outer_x = center_x + int(radius * 0.8 * math.cos(angle))
                outer_y = center_y + int(radius * 0.8 * math.sin(angle))
                
                # Draw lines from center to points
                pygame.draw.line(surface, (255, 255, 255), 
                                (center_x, center_y), 
                                (outer_x, outer_y), 1)
            
            # Draw small patterns in the four corners
            corner_size = 10
            corner_margin = border_width + 8
            
            # Top-left corner pattern
            pygame.draw.circle(surface, (255, 255, 255), 
                              (x + corner_margin, y + corner_margin), corner_size, 1)
            
            # Top-right corner pattern
            pygame.draw.circle(surface, (255, 255, 255), 
                              (x + CARD_WIDTH - corner_margin, y + corner_margin), corner_size, 1)
            
            # Bottom-left corner pattern
            pygame.draw.circle(surface, (255, 255, 255), 
                              (x + corner_margin, y + CARD_HEIGHT - corner_margin), corner_size, 1)
            
            # Bottom-right corner pattern
            pygame.draw.circle(surface, (255, 255, 255), 
                              (x + CARD_WIDTH - corner_margin, y + CARD_HEIGHT - corner_margin), corner_size, 1)
            
            # Add small dots pattern throughout the card
            dot_spacing = 12
            for dot_x in range(x + border_width + 15, x + CARD_WIDTH - border_width - 15, dot_spacing):
                for dot_y in range(y + border_width + 15, y + CARD_HEIGHT - border_width - 15, dot_spacing):
                    # Skip dots in the center area
                    distance_to_center = math.sqrt((dot_x - center_x)**2 + (dot_y - center_y)**2)
                    if distance_to_center > radius + 5:
                        pygame.draw.circle(surface, (255, 255, 255), (dot_x, dot_y), 1)
        else:
            # Draw card symbol
            if self.suit == "joker":
                # Create a bright yellow background for the joker card
                pygame.draw.rect(surface, (255, 255, 100), (x + 2, y + 2, CARD_WIDTH - 4, CARD_HEIGHT - 4), border_radius=8)
                
                # Get center coordinates
                center_x = x + CARD_WIDTH // 2
                center_y = y + CARD_HEIGHT // 2
                
                # Load and draw the joker image if available
                try:
                    joker_image = pygame.image.load("image.png")
                    joker_image = pygame.transform.scale(joker_image, (40, 40))  # Smaller size
                    image_rect = joker_image.get_rect(center=(center_x, center_y))
                    surface.blit(joker_image, image_rect)
                except Exception as e:
                    print(f"Failed to load Joker image: {e}")
                    # Fallback: Draw a simple jester icon
                    pygame.draw.circle(surface, WHITE, (center_x, center_y), 20)
                
                # Draw "JOKER" text vertically on both diagonal corners
                font = pygame.font.SysFont('arial', 8, bold=True)  # Smaller and bold font
                
                # Bottom-left corner
                for i, letter in enumerate("JOKER"):
                    letter_text = font.render(letter, True, BLACK)
                    text_rect = letter_text.get_rect(center=(x + 15, y + CARD_HEIGHT - 15 - i * 7))  # Closer spacing
                    surface.blit(letter_text, text_rect)
                
                # Top-right corner
                for i, letter in enumerate("JOKER"):
                    letter_text = font.render(letter, True, BLACK)
                    text_rect = letter_text.get_rect(center=(x + CARD_WIDTH - 15, y + 5 + i * 7))  # Closer spacing
                    surface.blit(letter_text, text_rect)
            else:
                # Regular card drawing
                font = pygame.font.SysFont('arial', 36)
                text = font.render(self.symbol, True, self.color)
                text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
                surface.blit(text, text_rect)
                
                # Draw small symbols in corners
                small_font = pygame.font.SysFont('arial', 20)
                small_text = small_font.render(self.symbol, True, self.color)
                surface.blit(small_text, (x + 5, y + 5))
                surface.blit(small_text, (x + CARD_WIDTH - 20, y + CARD_HEIGHT - 25))

class Player:
    def __init__(self, suit):
        self.suit = suit
        self.position = 0
        self.card = Card(suit)
    
    def move_forward(self):
        self.position += 1
        
    def move_backward(self):
        if self.position > 0:  # Cannot move backward from starting position
            self.position -= 1
    
    def __str__(self):
        return f"{self.card} Player"

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        font = pygame.font.SysFont('arial', 24)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class PokerRacingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Poker Racing Game")
        self.clock = pygame.time.Clock()
        
        # Load joker image
        try:
            self.joker_image = pygame.image.load("image.png")
            # Scale the image to fit nicely on the card
            self.joker_image = pygame.transform.scale(self.joker_image, (40, 40))
        except:
            # If image loading fails, we'll use a fallback drawing method
            self.joker_image = None
        
        # Adjust grid spacing for a more compact board
        self.grid_spacing_x = 70  # Reduced from 120
        self.grid_spacing_y = 100  # Reduced from 100
        
        self.suits = ["club", "heart", "spade", "diamond"]
        self.grid_height = 4
        self.players = []
        self.y_axis_cards = []
        self.deck = []
        self.message = ""
        self.message_timer = 0
        
        # Animation variables
        self.animating = False
        self.animation_frames = 0
        self.animation_type = None
        self.animation_data = None
        
        # Buttons - move draw button to the right side
        self.draw_button = Button(SCREEN_WIDTH - 200, 
                                 SCREEN_HEIGHT - 90,
                                 BUTTON_WIDTH, BUTTON_HEIGHT, 
                                 "Draw Card", GREEN)
        
        self.suit_buttons = [
            Button(100 + i * 200, 350, 150, 60, suit.capitalize(), GRAY)
            for i, suit in enumerate(self.suits)
        ]
        
        self.drawn_cards_history = []  # Keep track of previously drawn cards
        self.max_history_cards = 3     # Maximum number of cards to show in history
        
        self.drawn_card = None
        self.previous_card = None
        self.fade_alpha = 0  # For fading out previous card
        
        # Card animation variables
        self.card_rotation = 0
        self.card_scale = 1.0
        
        self.initialize_game()
    
    def initialize_game(self):
        # Create deck with all suits
        self.deck = []
        for suit in ["club", "heart", "spade", "diamond"]:
            for _ in range(13):  # 13 cards per suit in a standard deck
                self.deck.append(Card(suit))
        
        # Add two Joker cards to the deck
        self.deck.append(Card("joker"))
        self.deck.append(Card("joker"))
        
        # Shuffle the deck thoroughly
        random.shuffle(self.deck)
        random.shuffle(self.deck)  # Double shuffle for better randomness
        
        # Reset game state
        self.game_state = "setup"  # setup, player_selection, playing, game_over
        self.current_player = 0
        self.num_players = 0
        self.winner = None
        
        # Reset messages
        self.message = ""
        self.message_timer = 0
        
        # Clear any animations
        self.animating = False
        self.animation_frames = 0
        self.animation_type = None
        self.animation_data = None
        
        # Reset player list and suit buttons for new game setup
        self.players = []
        self.suits = ["club", "heart", "spade", "diamond"]
        self.suit_buttons = [
            Button(100 + i * 200, 350, 150, 60, suit.capitalize(), GRAY)
            for i, suit in enumerate(self.suits)
        ]
        
        # Y-axis cards will be set up after player selection
        self.y_axis_cards = []
        self.y_axis_revealed = [False] * self.grid_height
    
    def setup_game_after_player_selection(self):
        # Get the suits chosen by players
        chosen_suits = [player.suit for player in self.players]
        
        # For 2 or 3 player games, filter the deck to only include chosen suits
        if len(self.players) < 4:
            filtered_deck = [card for card in self.deck if card.suit in chosen_suits]
            
            # If we don't have enough cards of chosen suits, we'll need to use the full deck
            if len(filtered_deck) >= self.grid_height:
                # Set up y-axis cards (4 random cards) from chosen suits only
                random.shuffle(filtered_deck)
                self.y_axis_cards = [filtered_deck.pop() for _ in range(self.grid_height)]
                
                # Remove these cards from the main deck
                for y_card in self.y_axis_cards:
                    for i, card in enumerate(self.deck):
                        if card.suit == y_card.suit:
                            self.deck.pop(i)
                            break
            else:
                # Fallback to using the full deck if we don't have enough cards
                random.shuffle(self.deck)
                self.y_axis_cards = [self.deck.pop() for _ in range(self.grid_height)]
        else:
            # For 4 player games (all suits used), just use random cards from the deck
            random.shuffle(self.deck)
            self.y_axis_cards = [self.deck.pop() for _ in range(self.grid_height)]
        
        # Hide the y-axis cards (we'll reveal them when needed)
        self.y_axis_revealed = [False] * self.grid_height
    
    def select_player_suit(self, suit_index):
        if suit_index < len(self.suits):
            # Add the player with the selected suit
            selected_suit = self.suits.pop(suit_index)
            self.players.append(Player(selected_suit))
            
            # Remove the corresponding button
            self.suit_buttons.pop(suit_index)
            
            # Update remaining buttons positions
            for i, button in enumerate(self.suit_buttons):
                button.rect.x = 100 + i * 200
            
            # Move to next player or start game
            self.current_player += 1
            if self.current_player >= self.num_players:
                self.game_state = "playing"
                # Now that all players have been selected, set up the y-axis cards
                self.setup_game_after_player_selection()
    
    def draw_card(self):
        if not self.deck:
            self.set_message("Deck is empty! Reshuffling...")
            self.initialize_game()
        
        # Store previous card for fade effect
        self.previous_card = self.drawn_card
        self.fade_alpha = 255  # Start fully visible
        
        # Get the next card (but don't remove it from the deck yet)
        next_card = self.deck[-1]
        
        # Check if it's a close game (2+ players one step away from winning AND next card matches one of them)
        close_game = False
        potential_winners = []
        
        for player in self.players:
            if player.position == self.grid_height:  # One step away from winning
                potential_winners.append(player)
                # Check if the next card matches this player's suit
                if player.suit == next_card.suit:
                    close_game = True
        
        # Only consider it a close game if there are at least 2 players in the final row
        # AND the next card will determine a winner
        close_game = close_game and len(potential_winners) >= 2
        
        # Now actually draw the card
        card = self.deck.pop()
        
        # Set as current drawn card
        self.drawn_card = card
        
        # Animate card drawing
        start_x, start_y = 20, 85  # Deck position
        end_x, end_y = 120, 85     # Drawn card position
        
        if close_game:
            # Dramatic animation for close games
            animation_frames = 150  # Even longer animation for dramatic effect
            
            # Center of the screen for dramatic reveal
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            
            # Allocate more frames to the reveal phase
            first_phase = animation_frames // 4    # 25% - moving to center
            second_phase = animation_frames // 2   # 50% - revealing (slower fade-in)
            third_phase = animation_frames // 4    # 25% - returning to position
            
            for frame in range(animation_frames):
                progress = frame / animation_frames
                
                # First phase: card moves to center (face down)
                if frame < first_phase:
                    phase_progress = frame / first_phase
                    current_x = start_x + (center_x - start_x) * phase_progress
                    current_y = start_y + (center_y - start_y) * phase_progress
                    
                    # Card grows as it moves to center
                    scale = 1 + phase_progress * 3  # Grow to 4x size
                    
                    # Card is still face down during movement
                    hidden = True
                    
                    # Calculate background fade-in alpha (0 to 178 = 70% opacity)
                    bg_alpha = int(phase_progress * 178)
                
                # Second phase: card stays in center and flips slowly with fade-in effect
                elif frame < first_phase + second_phase:
                    phase_progress = (frame - first_phase) / second_phase
                    current_x = center_x
                    current_y = center_y
                    
                    # Card stays at maximum size
                    scale = 4.0
                    
                    # Card flips over with very slow fade-in effect
                    hidden = phase_progress < 0.3  # First 30% of this phase is still face down
                    
                    # Calculate fade-in alpha for the face-up card (only during the latter part of this phase)
                    fade_alpha = 255
                    if not hidden:  # When card is face up
                        # Map from 0.3-1.0 to 0-255 for alpha (slower fade-in)
                        reveal_progress = (phase_progress - 0.3) / 0.7  # 0 to 1
                        fade_alpha = int(reveal_progress * 255)
                    
                    # Background stays at full opacity during this phase
                    bg_alpha = 178  # 70% opacity
                
                # Third phase: card returns to position
                else:
                    phase_progress = (frame - (first_phase + second_phase)) / third_phase
                    current_x = center_x + (end_x - center_x) * phase_progress
                    current_y = center_y + (end_y - center_y) * phase_progress
                    
                    # Card shrinks back as it moves to final position
                    scale = 4 - phase_progress * 3  # Shrink from 4x to 1x
                    
                    # Card remains face up
                    hidden = False
                    fade_alpha = 255  # Fully visible
                    
                    # Background fades out quickly
                    bg_alpha = int(178 * (1 - phase_progress * 3))  # Fade out 3x faster than the card shrinks
                    bg_alpha = max(0, bg_alpha)  # Ensure it doesn't go negative
                
                # Draw the game board without the drawn card
                self.draw_game_board(skip_drawn_card=True)
                
                # Draw semi-transparent black background
                if bg_alpha > 0:
                    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    bg_surface.fill((0, 0, 0, bg_alpha))
                    self.screen.blit(bg_surface, (0, 0))
                
                # Draw the animated card
                # Save the current state
                original_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
                
                # Draw the card on the temporary surface
                card.draw(original_surface, 0, 0, hidden=hidden)
                
                # Apply fade-in effect if needed
                if not hidden and frame < first_phase + second_phase:
                    # Set alpha for fade-in effect
                    original_surface.set_alpha(fade_alpha)
                
                # Scale the surface
                scaled_width = int(CARD_WIDTH * scale)
                scaled_height = int(CARD_HEIGHT * scale)
                scaled_surface = pygame.transform.scale(original_surface, (scaled_width, scaled_height))
                
                # Get the rect for positioning (no rotation)
                scaled_rect = scaled_surface.get_rect(center=(current_x, current_y))
                
                # Draw the transformed card
                self.screen.blit(scaled_surface, scaled_rect)
                
                # Update the display
                pygame.display.flip()
                self.clock.tick(25)  # Even slower frame rate for more dramatic effect
            
            # Add a pause after the animation completes
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 700:  
                # Keep drawing the game board with the drawn card
                self.draw_game_board()
                pygame.display.flip()
                self.clock.tick(30)
                
                # Handle any quit events during the pause
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        else:
            # Regular animation with rotation, scaling, and arc movement
            total_frames = 30  # Increased for smoother animation
            
            for frame in range(total_frames, 0, -1):
                progress = 1 - (frame / total_frames)
                
                # Calculate arc path for more natural card movement
                # Card rises up and then comes down to destination
                arc_height = 50  # Maximum height of the arc
                arc_y = -math.sin(progress * math.pi) * arc_height
                
                # Calculate current position with arc
                current_x = start_x + (end_x - start_x) * progress
                current_y = start_y + (end_y - start_y) * progress - arc_y
                
                # Calculate rotation (card spins as it moves)
                rotation = 360 * progress  # Full rotation during movement
                
                # Calculate scale (card appears to get slightly larger then normal)
                scale = 1.0 + 0.2 * math.sin(progress * math.pi)  # Scale up to 1.2x in the middle
                
                # Fade out previous card
                if self.previous_card:
                    self.fade_alpha = max(0, int(255 * (1 - progress * 2)))
                
                # Draw the entire game board
                self.draw_game_board(skip_drawn_card=True)
                
                # Draw previous card with fade effect
                if self.previous_card and self.fade_alpha > 0:
                    card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
                    self.previous_card.draw(card_surface, 0, 0)
                    card_surface.set_alpha(self.fade_alpha)
                    self.screen.blit(card_surface, (end_x, end_y))
                
                # Draw the moving card with rotation and scaling
                card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
                card.draw(card_surface, 0, 0)
                
                # Scale the card
                scaled_width = int(CARD_WIDTH * scale)
                scaled_height = int(CARD_HEIGHT * scale)
                scaled_surface = pygame.transform.scale(card_surface, (scaled_width, scaled_height))
                
                # Rotate the card
                rotated_surface = pygame.transform.rotate(scaled_surface, rotation)
                
                # Get the rect for the rotated surface to center it properly
                rotated_rect = rotated_surface.get_rect(center=(int(current_x) + CARD_WIDTH//2, 
                                                               int(current_y) + CARD_HEIGHT//2))
                
                # Draw the transformed card
                self.screen.blit(rotated_surface, rotated_rect)
                
                pygame.display.flip()
                self.clock.tick(60)
        
        # Handle Joker card special effect - mirror player positions
        if card.suit == "joker":
            self.set_message("JOKER CARD! Player positions will be mirrored!")
            
            # Find the furthest and closest players
            max_position = max(player.position for player in self.players)
            min_position = min(player.position for player in self.players)
            
            # Store original positions for animation
            original_positions = {player: player.position for player in self.players}
            
            # Calculate new positions (mirrored)
            new_positions = {}
            for player in self.players:
                # Mirror the position: new_pos = max_pos - (current_pos - min_pos)
                new_positions[player] = max_position - (player.position - min_position)
            
            # Animate and update positions
            for player in self.players:
                start_pos = original_positions[player]
                end_pos = new_positions[player]
                
                # Only animate if position changed
                if start_pos != end_pos:
                    # Set the new position
                    player.position = end_pos
                    
                    # Animate the movement
                    self.animate_player_movement(player, start_pos, end_pos)
            
            return  # Skip the regular card handling
        
        # First step: Move players whose suit matches the drawn card
        moved_players = []
        for player in self.players:
            if player.suit == card.suit:
                # Store original position
                start_pos = player.position
                
                # Move player forward
                player.move_forward()
                
                # Animate the movement
                self.animate_player_movement(player, start_pos, player.position)
                
                # Add to moved players list
                moved_players.append(player)
        
        # Set message based on what happened
        if moved_players:
            if len(moved_players) == 1:
                self.set_message(f"{moved_players[0]} moves forward!")
            else:
                self.set_message(f"{len(moved_players)} players move forward!")
        else:
            self.set_message("No player moves this turn.")
        
        # Second step: Check if all players are on the same row
        if self.check_same_row():
            # Convert player position to grid row (important fix)
            # The grid is displayed from top to bottom, but positions increase from bottom to top
            # So we need to convert the position to the correct row index
            player_position = self.players[0].position
            row = self.grid_height - player_position
            
            if 0 <= row < self.grid_height and not self.y_axis_revealed[row]:
                # Reveal the card for this row
                self.reveal_row_card(row)
                while self.animating:
                    self.draw_game_board()
                    pygame.display.flip()
                    self.update_animation()
                
                # Get the revealed card
                revealed_card = self.y_axis_cards[row]
                
                # Set message about the revealed card
                self.set_message(f"All players on same row! Y-axis card revealed: {revealed_card}")
                
                # Move matching players backward
                backward_players = []
                for player in self.players:
                    if player.suit == revealed_card.suit:
                        # Store original position
                        start_pos = player.position
                        
                        # Move player backward
                        player.move_backward()
                        
                        # Animate the movement
                        self.animate_player_movement(player, start_pos, player.position)
                        
                        # Add to backward players list
                        backward_players.append(player)
                
                # Set message about backward movement
                if backward_players:
                    if len(backward_players) == 1:
                        self.set_message(f"{backward_players[0]} matches the revealed card and moves backward!")
                    else:
                        self.set_message(f"{len(backward_players)} players match the revealed card and move backward!")
        
        # Check for winner (beyond the grid)
        for player in self.players:
            if player.position > self.grid_height:
                self.winner = player
                self.game_state = "game_over"
                break
        
        return card
    
    def check_same_row(self):
        if not self.players or len(self.players) < 2:
            return False
        
        # Get the position of the first player
        position = self.players[0].position
        
        # Check if all players are on the same row and not at starting position
        return all(player.position == position for player in self.players) and position > 0
    
    def set_message(self, msg):
        self.message = msg
        self.message_timer = 180  # Show message for 3 seconds (60 frames per second)
    
    def draw_setup_screen(self):
        self.screen.fill(DARK_GREEN)
        
        # Title
        font = pygame.font.SysFont('arial', 60)
        title = font.render("Poker Racer", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Instructions
        font = pygame.font.SysFont('arial', 30)
        instructions = font.render("Select number of players:", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(instructions, instructions_rect)
        
        # Player number buttons - store them for event handling
        self.player_buttons = []
        button_width = 120
        total_width = 3 * button_width + 2 * 60  # 3 buttons with 60px spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i in range(2, 5):
            button = Button(start_x + (i-2) * (button_width + 60), 300, button_width, 60, str(i))
            self.player_buttons.append(button)
            button.check_hover(pygame.mouse.get_pos())
            button.draw(self.screen)
        
        # Add Exit button - using a direct pygame.Rect for simplicity
        exit_button_width = 120
        exit_button_height = 50
        exit_button_rect = pygame.Rect((SCREEN_WIDTH - exit_button_width) // 2, 400, exit_button_width, exit_button_height)
        
        # Check if mouse is hovering over exit button
        mouse_pos = pygame.mouse.get_pos()
        if exit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, RED, exit_button_rect)
        else:
            pygame.draw.rect(self.screen, (200, 50, 50), exit_button_rect)  # Darker red when not hovered
        
        pygame.draw.rect(self.screen, BLACK, exit_button_rect, 2)
        
        # Draw exit button text
        font = pygame.font.SysFont('arial', 24)
        exit_text = font.render("Exit", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        self.screen.blit(exit_text, exit_text_rect)
        
        # Store the exit button rect for event handling
        self.exit_button_rect = exit_button_rect
    
    def draw_player_selection_screen(self):
        self.screen.fill(DARK_GREEN)
        
        # Title
        font = pygame.font.SysFont('arial', 60)
        title = font.render("Poker Racer", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Instructions
        font = pygame.font.SysFont('arial', 30)
        instructions = font.render(f"Player {self.current_player + 1}, select your suit:", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(instructions, instructions_rect)
        
        # Player count info
        font = pygame.font.SysFont('arial', 24)
        player_info = font.render(f"Player {self.current_player + 1} of {self.num_players}", True, WHITE)
        player_info_rect = player_info.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(player_info, player_info_rect)
        
        # Suit buttons - ensure they're properly spaced based on available suits
        button_width = 150
        button_spacing = 60
        total_width = len(self.suits) * button_width + (len(self.suits) - 1) * button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.suit_buttons):
            # Update button position
            button.rect.x = start_x + i * (button_width + button_spacing)
            button.rect.y = 350
            
            button.check_hover(mouse_pos)
            button.draw(self.screen)
            
            # Draw suit symbol below button
            suit = self.suits[i]
            card = Card(suit)
            font = pygame.font.SysFont('arial', 60)
            text = font.render(card.symbol, True, card.color)
            text_rect = text.get_rect(center=(button.rect.centerx, button.rect.bottom + 50))
            self.screen.blit(text, text_rect)
    
    def draw_game_board(self, skip_drawn_card=False, animating_player=None, skip_player=None):
        self.screen.fill(DARK_GREEN)
        
        # Title - moved down to be above the finish line
        font = pygame.font.SysFont('arial', 32)
        title = font.render("Poker Racer", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, GRID_TOP -110))
        self.screen.blit(title, title_rect)
        
        # Calculate grid dimensions based on number of players
        num_players = len(self.players)
        if num_players == 0:
            return  # Nothing to draw if no players
        
        # Use the more compact grid spacing
        player_spacing = min(self.grid_spacing_x, (SCREEN_WIDTH - 300) // max(1, num_players))
        
        # Calculate total grid width
        grid_width = player_spacing * num_players
        
        # Center the grid horizontally
        grid_left = (SCREEN_WIDTH - grid_width) // 2
        
        # Draw remaining deck count
        font = pygame.font.SysFont('arial', 18)
        deck_text = font.render(f"Remaining cards: {len(self.deck)}", True, WHITE)
        self.screen.blit(deck_text, (20, 60))
        
        # Draw deck
        if self.deck:
            deck_card = Card("club")  # Just for visualization
            deck_card.draw(self.screen, 20, 85, hidden=True)
        
        # Draw current drawn card without the label text
        if not skip_drawn_card and self.drawn_card:
            # Draw only the current card
            self.drawn_card.draw(self.screen, 120, 85)
        
        # Draw finish line - centered over the grid
        pygame.draw.rect(self.screen, WHITE, (grid_left - 10, GRID_TOP - 40, grid_width + 20, 25))
        font = pygame.font.SysFont('arial', 18)
        finish_text = font.render("FINISH LINE", True, BLACK)
        finish_rect = finish_text.get_rect(center=(grid_left + grid_width // 2, GRID_TOP - 28))
        self.screen.blit(finish_text, finish_rect)
        
        # Draw grid with more compact spacing
        for row in range(self.grid_height + 1):
            y_pos = GRID_TOP + row * self.grid_spacing_y
            
            # Draw y-axis card - positioned relative to grid
            if row < self.grid_height:
                card = self.y_axis_cards[row]
                # Only show the card if it's been revealed
                is_hidden = not self.y_axis_revealed[row]
                card.draw(self.screen, grid_left - CARD_WIDTH - 20, y_pos, hidden=is_hidden)
            
            # Draw grid cells
            for col in range(num_players):
                x_pos = grid_left + col * player_spacing
                pygame.draw.rect(self.screen, WHITE, (x_pos, y_pos, CARD_WIDTH, CARD_HEIGHT), 1)
        
        # Draw players
        for player in self.players:
            if player == skip_player:
                continue  # Skip this player as it's being animated separately
            
            col = self.players.index(player)
            
            # Handle the animating player specially
            if player == animating_player and player.animation_progress is not None:
                # Calculate the animated position
                start_row = self.grid_height - player.animation_start
                end_row = self.grid_height - player.animation_end
                current_row = start_row + (end_row - start_row) * player.animation_progress
                
                x_pos = grid_left + col * player_spacing
                y_pos = GRID_TOP + current_row * self.grid_spacing_y
                player.card.draw(self.screen, x_pos, y_pos)
            else:
                # Draw player in normal position
                row = self.grid_height - player.position
                x_pos = grid_left + col * player_spacing
                y_pos = GRID_TOP + row * self.grid_spacing_y
                player.card.draw(self.screen, x_pos, y_pos)
        
        # Draw player labels below the grid (without cards) - moved further down
        for col, player in enumerate(self.players):
            x_pos = grid_left + col * player_spacing
            # Increase the y-offset to move labels further down
            y_pos = GRID_TOP + self.grid_height * self.grid_spacing_y + 120 #fixed to 120
            
            # Draw player label only, not the card
            font = pygame.font.SysFont('arial', 13)
            player_text = font.render(f"Player {col+1}", True, WHITE)
            player_rect = player_text.get_rect(center=(x_pos + CARD_WIDTH // 2, y_pos-6))
            self.screen.blit(player_text, player_rect)
        
        # Draw message
        if self.message and self.message_timer > 0:
            font = pygame.font.SysFont('arial', 18)
            message_text = font.render(self.message, True, WHITE)
            message_rect = message_text.get_rect(midleft=(20, SCREEN_HEIGHT - 50))
            self.screen.blit(message_text, message_rect)
            self.message_timer -= 1
        
        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button.check_hover(mouse_pos)
        self.draw_button.draw(self.screen)
    
    def draw_game_over_screen(self):
        self.screen.fill(DARK_GREEN)
        
        # Title
        font = pygame.font.SysFont('arial', 48)
        title = font.render("Game Over!", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Winner
        font = pygame.font.SysFont('arial', 36)
        winner_text = font.render(f"{self.winner} Wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(winner_text, winner_rect)
        
        # Draw winner's card
        self.winner.card.draw(self.screen, SCREEN_WIDTH // 2 - CARD_WIDTH // 2, 280)
        
        # Play again button
        play_again_button = Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 
                                  420, BUTTON_WIDTH, BUTTON_HEIGHT, 
                                  "Play Again", GREEN)
        
        mouse_pos = pygame.mouse.get_pos()
        play_again_button.check_hover(mouse_pos)
        play_again_button.draw(self.screen)
        
        # Check for button click
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_again_button.rect.collidepoint(mouse_pos):
                    self.players = []
                    self.suits = ["club", "heart", "spade", "diamond"]
                    self.suit_buttons = [
                        Button(100 + i * 200, 350, 150, 60, suit.capitalize(), GRAY)
                        for i, suit in enumerate(self.suits)
                    ]
                    self.initialize_game()
                    self.game_state = "setup"  # Explicitly set to setup
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_state == "setup":
                if event.type == MOUSEBUTTONDOWN:
                    # Check each player number button
                    for i, button in enumerate(self.player_buttons):
                        if button.rect.collidepoint(mouse_pos):
                            self.num_players = i + 2  # 2, 3, or 4 players
                            self.game_state = "player_selection"
                            # Reset player selection
                            self.current_player = 0
                            self.players = []
                            self.suits = ["club", "heart", "spade", "diamond"]
                            self.suit_buttons = [
                                Button(100 + j * 200, 350, 150, 60, suit.capitalize(), GRAY)
                                for j, suit in enumerate(self.suits)
                            ]
                            break
                    
                    # Check if exit button is clicked - using the rect directly
                    if hasattr(self, 'exit_button_rect') and self.exit_button_rect.collidepoint(mouse_pos):
                        print("Exit button clicked!")  # Debug print
                        # Use os._exit for a clean exit without triggering exception handling
                        pygame.quit()
                        os._exit(0)  # Force immediate exit
            
            elif self.game_state == "player_selection":
                if event.type == MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.suit_buttons):
                        if button.rect.collidepoint(mouse_pos):
                            self.select_player_suit(i)
                            break
            
            elif self.game_state == "playing":
                if event.type == MOUSEBUTTONDOWN:
                    if self.draw_button.rect.collidepoint(mouse_pos):
                        self.draw_card()
            
            elif self.game_state == "game_over":
                if event.type == MOUSEBUTTONDOWN:
                    # Check if play again button is clicked
                    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if play_again_button.collidepoint(mouse_pos):
                        self.players = []
                        self.suits = ["club", "heart", "spade", "diamond"]
                        self.suit_buttons = [
                            Button(100 + i * 200, 350, 150, 60, suit.capitalize(), GRAY)
                            for i, suit in enumerate(self.suits)
                        ]
                        self.initialize_game()
                        self.game_state = "setup"  # Explicitly set to setup
    
    def play(self):
        while True:
            if self.game_state == "setup":
                self.draw_setup_screen()
            elif self.game_state == "player_selection":
                self.draw_player_selection_screen()
            elif self.game_state == "playing":
                self.draw_game_board()
            elif self.game_state == "game_over":
                self.draw_game_over_screen()
            
            self.handle_events()
            
            pygame.display.flip()
            self.clock.tick(60)

    def display_board(self):
        self.draw_game_board()
        pygame.display.flip()

    def reveal_row_card(self, row):
        if 0 <= row < self.grid_height and not self.y_axis_revealed[row]:
            self.y_axis_revealed[row] = True
            revealed_card = self.y_axis_cards[row]
            
            # Start animation for revealing the card
            self.start_animation('reveal_card', {'row': row, 'card': revealed_card})

    def start_animation(self, animation_type, data=None, frames=15):
        self.animating = True
        self.animation_frames = frames
        self.animation_type = animation_type
        self.animation_data = data
        if animation_type == 'reveal_card':
            # Ensure the card is drawn with the correct format from the start
            card = data['card']
            row = data['row']
            x_pos = GRID_LEFT - CARD_WIDTH - 20
            y_pos = GRID_TOP + row * GRID_SPACING
            card.draw(self.screen, x_pos, y_pos, hidden=False)  # Ensure hidden=False for correct design

    def update_animation(self):
        if not self.animating:
            return False
        
        self.animation_frames -= 1
        if self.animation_frames <= 0:
            self.animating = False
            if self.animation_type == 'reveal_card':
                # Finalize the reveal
                data = self.animation_data
                card = data['card']
                row = data['row']
                x_pos = GRID_LEFT - CARD_WIDTH - 20
                y_pos = GRID_TOP + row * GRID_SPACING
                card.draw(self.screen, x_pos, y_pos, hidden=False)  # Draw with correct design
            return False
        
        if self.animation_type == 'reveal_card':
            # Continue animation with correct card design
            data = self.animation_data
            card = data['card']
            row = data['row']
            x_pos = GRID_LEFT - CARD_WIDTH - 20
            y_pos = GRID_TOP + row * GRID_SPACING
            # Apply animation effects here if needed
            card.draw(self.screen, x_pos, y_pos, hidden=False)  # Maintain correct design throughout

        return True

    def animate_player_movement(self, player, start_pos, end_pos):
        # Calculate grid dimensions based on number of players
        num_players = len(self.players)
        player_spacing = min(self.grid_spacing_x, (SCREEN_WIDTH - 200) // max(1, num_players))
        grid_width = player_spacing * num_players
        grid_left = (SCREEN_WIDTH - grid_width) // 2
        
        # Get player column
        col = self.players.index(player)
        
        # Calculate exact start and end positions
        start_row = self.grid_height - start_pos
        end_row = self.grid_height - end_pos
        
        start_x = grid_left + col * player_spacing
        start_y = GRID_TOP + start_row * self.grid_spacing_y
        
        end_x = grid_left + col * player_spacing
        end_y = GRID_TOP + end_row * self.grid_spacing_y
        
        # Animate movement
        for frame in range(15, 0, -1):
            # Calculate current position
            progress = 1 - (frame / 15)
            
            # Calculate exact current position
            current_x = start_x
            current_y = start_y + (end_y - start_y) * progress
            
            # Ensure the final frame positions the player exactly in the grid cell
            if frame == 1:
                current_x = end_x
                current_y = end_y
            
            # Draw the entire game board without the moving player
            self.draw_game_board(skip_player=player)
            
            # Draw the moving player at the exact position
            player.card.draw(self.screen, current_x, current_y)
            
            pygame.display.flip()
            self.clock.tick(60)

# Terminal-based version (kept for compatibility)
class TerminalPokerRacingGame:
    def __init__(self):
        self.suits = ["club", "heart", "spade", "diamond"]
        self.grid_height = 4
        self.players = []
        self.y_axis_cards = []
        self.deck = []
        self.initialize_game()
    
    def initialize_game(self):
        # Create deck (excluding the cards used for the y-axis)
        for suit in self.suits:
            for _ in range(13):  # 13 cards per suit in a standard deck
                self.deck.append(Card(suit))
        
        # Shuffle the deck
        random.shuffle(self.deck)
        
        # Set up y-axis cards (4 random cards)
        self.y_axis_cards = [self.deck.pop() for _ in range(self.grid_height)]
        
        # Hide the y-axis cards (we'll reveal them when needed)
        self.y_axis_revealed = [False] * self.grid_height
    
    def select_players(self, num_players):
        available_suits = self.suits.copy()
        
        for i in range(num_players):
            print(f"\nPlayer {i+1}, select your suit:")
            for j, suit in enumerate(available_suits):
                print(f"{j+1}. {suit} ({Card(suit)})")
            
            while True:
                try:
                    choice = int(input("Enter your choice (number): ")) - 1
                    if 0 <= choice < len(available_suits):
                        selected_suit = available_suits.pop(choice)
                        self.players.append(Player(selected_suit))
                        print(f"Player {i+1} selected {selected_suit} ({Card(selected_suit)})")
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a number.")
    
    def draw_card(self):
        if not self.deck:
            print("Deck is empty! Reshuffling...")
            self.initialize_game()
        
        card = self.deck.pop()
        print(f"\nDrawn card: {card} ({card.suit})")
        return card
    
    def check_same_row(self):
        if not self.players:
            return False
        
        position = self.players[0].position
        return all(player.position == position for player in self.players) and position > 0
    
    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print("POKER RACING GAME")
        print("=" * 40)
        
        # Display remaining cards in deck
        print(f"\nRemaining cards in deck: {len(self.deck)}")
        
        # Display the grid
        print("\nRace Track:")
        
        # Display finish line
        print("  " + "-" * 20)
        print("  | FINISH LINE     |")
        print("  " + "-" * 20)
        
        # Display y-axis cards and player positions
        for row in range(self.grid_height, -1, -1):
            row_str = ""
            
            # Y-axis card (if applicable)
            if row < self.grid_height:
                if self.y_axis_revealed[row]:
                    row_str += f"{self.y_axis_cards[row]} "
                else:
                    row_str += "? "
            else:
                row_str += "  "
            
            # Player positions
            for player in self.players:
                if player.position == row:
                    row_str += f"{player.card} "
                else:
                    row_str += "  "
            
            print(row_str)
        
        # Display x-axis (player suits)
        x_axis = "  "
        for player in self.players:
            x_axis += f"{player.card} "
        print(x_axis)
        
        # Display player information
        print("\nPlayers:")
        for i, player in enumerate(self.players):
            print(f"Player {i+1}: {player.card} ({player.suit})")
    
    def play(self):
        print("Welcome to Poker Racing Game!")
        
        # Get number of players
        while True:
            try:
                num_players = int(input("Enter number of players (2-4): "))
                if 2 <= num_players <= 4:
                    break
                print("Please enter a number between 2 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Select player suits
        self.select_players(num_players)
        
        # Main game loop
        game_over = False
        while not game_over:
            self.display_board()
            
            input("\nPress Enter to draw a card...")
            drawn_card = self.draw_card()
            
            # Move players whose suit matches the drawn card
            moved = False
            for player in self.players:
                if player.suit == drawn_card.suit:
                    player.move_forward()
                    print(f"{player} moves forward!")
                    moved = True
            
            if not moved:
                print("No player moves this turn.")
            
            # Check if all players are on the same row
            if self.check_same_row():
                row = self.players[0].position - 1  # Convert to 0-based index
                if 0 <= row < self.grid_height and not self.y_axis_revealed[row]:
                    self.y_axis_revealed[row] = True
                    revealed_card = self.y_axis_cards[row]
                    print(f"\nAll players on same row! Y-axis card revealed: {revealed_card} ({revealed_card.suit})")
                    
                    # Move matching players backward
                    for player in self.players:
                        if player.suit == revealed_card.suit:
                            player.move_backward()
                            print(f"{player} matches the revealed card and moves backward!")
            
            # Check for winner (beyond the grid)
            for player in self.players:
                if player.position > self.grid_height:
                    self.display_board()
                    print(f"\n{player} has reached the finish line!")
                    print(f"{player} WINS THE GAME!")
                    game_over = True
                    break
            
            if not game_over:
                time.sleep(1)  # Pause for a moment between turns

if __name__ == "__main__":
    # Check if pygame is available
    try:
        pygame.init()
        game = PokerRacingGame()
        game.play()
    except:
        print("Pygame not available or error initializing. Falling back to terminal version.")
        game = TerminalPokerRacingGame()
        game.play() 