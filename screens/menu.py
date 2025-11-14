import pygame

# Game descriptions
GAME_DESCRIPTIONS = {
    "two_choice": "Pick the larger of two items",
    "shape_grid": "Find the matching shape in a grid",
    "memory_grid": "Remember and recall highlighted squares"
}

def draw_menu(screen, font_medium, font_small, highscores):
    """Draw the main menu screen"""
    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    
    # Draw title
    title_text = font_medium.render("Memory & Focus Mini-Games", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(title_text, title_rect)
    
    # Draw game options
    games = ["two_choice", "shape_grid", "memory_grid"]
    game_names = {
        "two_choice": "Pick the Bigger",
        "shape_grid": "Find the Shape",
        "memory_grid": "Memory Recall"
    }
    
    menu_items = []
    for i, game in enumerate(games):
        # Calculate position
        y_pos = 200 + i * 120
        
        # Draw game box
        box_width, box_height = 600, 100
        box_x = (screen_width - box_width) // 2
        
        pygame.draw.rect(screen, (240, 240, 240), (box_x, y_pos, box_width, box_height))
        pygame.draw.rect(screen, (0, 0, 0), (box_x, y_pos, box_width, box_height), 2)
        
        # Draw game name
        name_text = font_medium.render(game_names[game], True, (0, 0, 0))
        screen.blit(name_text, (box_x + 20, y_pos + 20))
        
        # Draw game description
        desc_text = font_small.render(GAME_DESCRIPTIONS[game], True, (100, 100, 100))
        screen.blit(desc_text, (box_x + 20, y_pos + 60))
        
        # Draw high score badge
        highscore = highscores.get(game, 0)
        badge_text = font_small.render(f"Best: {highscore}", True, (255, 255, 255))
        badge_width = badge_text.get_width() + 20
        badge_height = 30
        
        pygame.draw.rect(screen, (0, 100, 200), (box_x + box_width - badge_width - 20, y_pos + 35, badge_width, badge_height))
        screen.blit(badge_text, (box_x + box_width - badge_width - 10, y_pos + 40))
        
        # Store menu item rect for click detection
        menu_items.append((game, pygame.Rect(box_x, y_pos, box_width, box_height)))
    
    # Draw instructions
    inst_text = font_small.render("Use UP/DOWN arrows to navigate and ENTER to select, or click with mouse", True, (100, 100, 100))
    inst_rect = inst_text.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(inst_text, inst_rect)
    
    return menu_items

def handle_menu_events(event, highscores):
    """Handle events for the menu screen"""
    # Get menu items
    menu_items = []
    games = ["two_choice", "shape_grid", "memory_grid"]
    game_names = {
        "two_choice": "Pick the Bigger",
        "shape_grid": "Find the Shape",
        "memory_grid": "Memory Recall"
    }
    
    screen_width = 800  # Default width
    for i, game in enumerate(games):
        y_pos = 200 + i * 120
        box_width, box_height = 600, 100
        box_x = (screen_width - box_width) // 2
        menu_items.append((game, pygame.Rect(box_x, y_pos, box_width, box_height)))
    
    # Handle mouse click
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        
        for game, rect in menu_items:
            if rect.collidepoint(mouse_pos):
                return game
    
    # Handle keyboard navigation
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            # Navigate up (not implemented in this simple version)
            pass
        elif event.key == pygame.K_DOWN:
            # Navigate down (not implemented in this simple version)
            pass
        elif event.key == pygame.K_RETURN:
            # Select first game by default
            return games[0]
    
    return None