import pygame
import sys
import json
import os
import random
from screens.menu import draw_menu, handle_menu_events
from screens.rules_modal import draw_rules_modal, handle_rules_modal_events
from games.two_choice import draw_two_choice, handle_two_choice_events, init_two_choice, handle_new_items as handle_two_choice_new_items
from games.shape_grid import draw_shape_grid, handle_shape_grid_events, init_shape_grid, handle_new_grid as handle_shape_grid_new_grid
from games.memory_grid import draw_memory_grid, handle_memory_grid_events, init_memory_grid
from utils.timer import Timer

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

# Game states
STATE_MENU = "menu"
STATE_RULES = "rules"
STATE_TWO_CHOICE = "two_choice"
STATE_SHAPE_GRID = "shape_grid"
STATE_MEMORY_GRID = "memory_grid"
STATE_GAME_OVER = "game_over"

screen = None
clock = None
font_small = None
font_medium = None
font_large = None
current_state = STATE_MENU
selected_game = None
game_data = {}
timer = None
highscores = {}
sound_enabled = True
difficulty = "hard"

try:
    sound_success = pygame.mixer.Sound("assets/sound_success.wav")
    sound_fail = pygame.mixer.Sound("assets/sound_fail.wav")
except:
    sound_success = None
    sound_fail = None

def load_highscores():
    """Load high scores from JSON file"""
    global highscores
    try:
        if os.path.exists("data/highscores.json"):
            with open("data/highscores.json", "r") as f:
                highscores = json.load(f)
        else:
            # Create default highscores
            highscores = {
                "two_choice": 0,
                "shape_grid": 0,
                "memory_grid": 0
            }
            save_highscores()
    except:
        highscores = {
            "two_choice": 0,
            "shape_grid": 0,
            "memory_grid": 0
        }

def save_highscores():
    """Save high scores to JSON file"""
    global highscores
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/highscores.json", "w") as f:
            json.dump(highscores, f)
    except:
        pass

def update_highscore(game, score):
    """Update high score if current score is higher"""
    global highscores
    if score > highscores.get(game, 0):
        highscores[game] = score
        save_highscores()

def play_sound(success):
    """Play success or fail sound if enabled"""
    global sound_enabled, sound_success, sound_fail
    if sound_enabled:
        try:
            if success and sound_success:
                sound_success.play()
            elif not success and sound_fail:
                sound_fail.play()
        except:
            pass

def draw_top_bar():
    """Draw the top bar with game title, timer, score, mute button and rules button"""
    global screen, font_medium, font_small, timer, game_data, sound_enabled
    
    # Draw background
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, SCREEN_WIDTH, 50))
    
    # Draw game title
    if current_state in [STATE_TWO_CHOICE, STATE_SHAPE_GRID, STATE_MEMORY_GRID]:
        title = ""
        if current_state == STATE_TWO_CHOICE:
            title = "Pick the Bigger"
        elif current_state == STATE_SHAPE_GRID:
            title = "Find the Shape"
        elif current_state == STATE_MEMORY_GRID:
            title = "Memory Recall"
            
        title_text = font_medium.render(title, True, WHITE)
        screen.blit(title_text, (20, 15))
    
    # Draw timer
    if timer:
        time_left = max(0, timer.get_time_left())
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        timer_text = font_medium.render(f"{minutes:02d}:{seconds:02d}", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - 40, 15))
        
        # Draw timer progress bar
        bar_width = 200
        bar_height = 10
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 40
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        progress = time_left / 30  # 30 seconds total
        progress_width = int(bar_width * progress)
        pygame.draw.rect(screen, GREEN if progress > 0.3 else RED, (bar_x, bar_y, progress_width, bar_height))
    
    # Draw score
    if "score" in game_data:
        score_text = font_medium.render(f"Score: {game_data['score']}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 250, 15))
    
    # Draw rules button
    rules_text = "?"
    rules_button = font_medium.render(rules_text, True, WHITE)
    screen.blit(rules_button, (SCREEN_WIDTH - 100, 15))

def draw_game_over():
    """Draw game over screen with score and options"""
    global screen, font_large, font_medium, font_small, game_data, highscores
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Draw game over box
    box_width, box_height = 500, 300
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = (SCREEN_HEIGHT - box_height) // 2
    
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)
    
    # Draw title
    title_text = font_large.render("Game Over!", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 50))
    screen.blit(title_text, title_rect)
    
    # Draw score
    score_text = font_medium.render(f"Your Score: {game_data.get('score', 0)}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 100))
    screen.blit(score_text, score_rect)
    
    # Draw high score
    highscore = highscores.get(selected_game, 0)
    highscore_text = font_medium.render(f"Best Score: {highscore}", True, BLACK)
    highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 140))
    screen.blit(highscore_text, highscore_rect)
    
    # Draw tip
    tips = [
        "Tip: Focus on accuracy over speed!",
        "Tip: Take a deep breath before starting.",
        "Tip: Practice makes perfect!",
        "Tip: Stay calm and maintain focus.",
        "Tip: Try to remember patterns, not individual items."
    ]
    tip = random.choice(tips)
    tip_text = font_small.render(tip, True, DARK_GRAY)
    tip_rect = tip_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 180))
    screen.blit(tip_text, tip_rect)
    
    # Draw buttons
    replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 220, box_y + 220, 200, 50)
    menu_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, box_y + 220, 200, 50)
    
    pygame.draw.rect(screen, GREEN, replay_button)
    pygame.draw.rect(screen, BLUE, menu_button)
    
    pygame.draw.rect(screen, BLACK, replay_button, 2)
    pygame.draw.rect(screen, BLACK, menu_button, 2)
    
    replay_text = font_medium.render("Replay", True, WHITE)
    menu_text = font_medium.render("Back to Menu", True, WHITE)
    
    replay_text_rect = replay_text.get_rect(center=replay_button.center)
    menu_text_rect = menu_text.get_rect(center=menu_button.center)
    
    screen.blit(replay_text, replay_text_rect)
    screen.blit(menu_text, menu_text_rect)
    
    return replay_button, menu_button

def handle_game_over_events(event, replay_button, menu_button):
    """Handle events for game over screen"""
    global current_state, selected_game, timer
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        
        if replay_button.collidepoint(mouse_pos):
            # Start the same game again
            timer = Timer(30)  # 30 seconds timer
            game_data = {"score": 0}
            
            if selected_game == STATE_TWO_CHOICE:
                init_two_choice()
            elif selected_game == STATE_SHAPE_GRID:
                init_shape_grid()
            elif selected_game == STATE_MEMORY_GRID:
                init_memory_grid()
                
            current_state = selected_game
            
        elif menu_button.collidepoint(mouse_pos):
            # Go back to menu
            current_state = STATE_MENU
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            # Start the same game again
            timer = Timer(30)  # 30 seconds timer
            game_data = {"score": 0}
            
            if selected_game == STATE_TWO_CHOICE:
                init_two_choice()
            elif selected_game == STATE_SHAPE_GRID:
                init_shape_grid()
            elif selected_game == STATE_MEMORY_GRID:
                init_memory_grid()
                
            current_state = selected_game
            
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
            # Go back to menu
            current_state = STATE_MENU

def handle_top_bar_events(event):
    """Handle events for the top bar buttons"""
    global sound_enabled, current_state, selected_game
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        
        # Check mute button
        mute_button_rect = pygame.Rect(SCREEN_WIDTH - 50, 15, 30, 30)
        if mute_button_rect.collidepoint(mouse_pos):
            sound_enabled = not sound_enabled
            return
        
        # Check rules button
        rules_button_rect = pygame.Rect(SCREEN_WIDTH - 100, 15, 30, 30)
        if rules_button_rect.collidepoint(mouse_pos) and current_state in [STATE_TWO_CHOICE, STATE_SHAPE_GRID, STATE_MEMORY_GRID]:
            current_state = STATE_RULES
            return

def main():
    """Main game loop"""
    global screen, clock, font_small, font_medium, font_large, current_state, selected_game, game_data, timer, SCREEN_WIDTH, SCREEN_HEIGHT
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("MindGym")
    pygame_icon = pygame.image.load('assets/icon.ico')
    pygame.display.set_icon(pygame_icon)
    
    # Set up the clock
    clock = pygame.time.Clock()
    
    # Set up fonts
    font_small = pygame.font.Font(None, 24)
    font_medium = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 48)
    
    # Load high scores
    load_highscores()
    
    # Initialize game data
    game_data = {}
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                
            else:
                # Handle top bar events
                handle_top_bar_events(event)
                
                # Handle state-specific events
                if current_state == STATE_MENU:
                    new_state = handle_menu_events(event, highscores)
                    if new_state and new_state != current_state:
                        selected_game = new_state
                        current_state = STATE_RULES
                        
                elif current_state == STATE_RULES:
                    new_state = handle_rules_modal_events(event)
                    if new_state and new_state != current_state:
                        if new_state == "start":
                            # Start the selected game
                            timer = Timer(30)  # 30 seconds timer
                            game_data = {"score": 0}
                            
                            if selected_game == STATE_TWO_CHOICE:
                                init_two_choice()
                            elif selected_game == STATE_SHAPE_GRID:
                                init_shape_grid()
                            elif selected_game == STATE_MEMORY_GRID:
                                init_memory_grid()
                                
                            current_state = selected_game
                        else:
                            # Go back to menu
                            current_state = STATE_MENU
                            
                elif current_state == STATE_TWO_CHOICE:
                    handle_two_choice_events(event, game_data)
                    
                elif current_state == STATE_SHAPE_GRID:
                    handle_shape_grid_events(event, game_data)
                    
                elif current_state == STATE_MEMORY_GRID:
                    handle_memory_grid_events(event, game_data)
                    
                elif current_state == STATE_GAME_OVER:
                    replay_button, menu_button = draw_game_over()
                    handle_game_over_events(event, replay_button, menu_button)
        
        # Handle custom events for game timers
        for event in pygame.event.get(pygame.USEREVENT + 1):
            if current_state == STATE_TWO_CHOICE:
                handle_two_choice_new_items()
                
        for event in pygame.event.get(pygame.USEREVENT + 2):
            if current_state == STATE_SHAPE_GRID:
                handle_shape_grid_new_grid()
        
        # Update timer
        if timer and current_state in [STATE_TWO_CHOICE, STATE_SHAPE_GRID, STATE_MEMORY_GRID]:
            timer.update()
            
            # Check if time is up
            if timer.is_expired():
                # Update high score
                update_highscore(selected_game, game_data.get("score", 0))
                
                # Switch to game over state
                current_state = STATE_GAME_OVER
        
        # Draw everything
        screen.fill(WHITE)
        
        # Draw top bar if in a game
        if current_state in [STATE_TWO_CHOICE, STATE_SHAPE_GRID, STATE_MEMORY_GRID, STATE_GAME_OVER]:
            draw_top_bar()
        
        # Draw state-specific content
        if current_state == STATE_MENU:
            draw_menu(screen, font_medium, font_small, highscores)
            
        elif current_state == STATE_RULES:
            draw_rules_modal(screen, font_medium, font_small, selected_game)
            
        elif current_state == STATE_TWO_CHOICE:
            draw_two_choice(screen, font_medium, game_data)
            
        elif current_state == STATE_SHAPE_GRID:
            draw_shape_grid(screen, font_medium, game_data)
            
        elif current_state == STATE_MEMORY_GRID:
            draw_memory_grid(screen, font_medium, game_data)
            
        elif current_state == STATE_GAME_OVER:
            draw_game_over()
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()