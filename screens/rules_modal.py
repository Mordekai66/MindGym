import pygame

# Game rules
GAME_RULES = {
    "two_choice": [
        "Two items will appear on screen",
        "Click or use LEFT/RIGHT arrows to select the larger one",
        "Correct: +10 points, Wrong: -5 points",
        "Game lasts for 30 seconds"
    ],
    "shape_grid": [
        "A 3x3 grid of shapes will appear",
        "Find the shape that matches the description",
        "Correct: +15 points, Wrong: -5 points",
        "Game lasts for 30 seconds"
    ],
    "memory_grid": [
        "A 3x4 grid will highlight some squares",
        "Remember which squares were highlighted",
        "After 2 seconds, select the squares you saw",
        "Correct: +5 points, Wrong: -2 points",
        "Game lasts for 30 seconds"
    ]
}

def draw_rules_modal(screen, font_medium, font_small, game):
    """Draw the rules modal overlay"""
    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Draw modal box
    box_width, box_height = 600, 400
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2
    
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 2)
    
    # Draw title
    title_text = font_medium.render("Read the rules", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen_width // 2, box_y + 40))
    screen.blit(title_text, title_rect)
    
    # Draw game name
    game_names = {
        "two_choice": "Pick the Bigger",
        "shape_grid": "Find the Shape",
        "memory_grid": "Memory Recall"
    }
    
    game_name_text = font_medium.render(game_names[game], True, (0, 0, 200))
    game_name_rect = game_name_text.get_rect(center=(screen_width // 2, box_y + 80))
    screen.blit(game_name_text, game_name_rect)
    
    # Draw rules
    rules = GAME_RULES[game]
    for i, rule in enumerate(rules):
        rule_text = font_small.render(f"• {rule}", True, (0, 0, 0))
        screen.blit(rule_text, (box_x + 50, box_y + 130 + i * 40))
    
    # Draw buttons
    start_button = pygame.Rect(box_x + 100, box_y + box_height - 70, 150, 50)
    back_button = pygame.Rect(box_x + box_width - 250, box_y + box_height - 70, 150, 50)
    
    pygame.draw.rect(screen, (0, 200, 0), start_button)
    pygame.draw.rect(screen, (200, 0, 0), back_button)
    
    pygame.draw.rect(screen, (0, 0, 0), start_button, 2)
    pygame.draw.rect(screen, (0, 0, 0), back_button, 2)
    
    start_text = font_medium.render("Start", True, (255, 255, 255))
    back_text = font_medium.render("Back", True, (255, 255, 255))
    
    start_text_rect = start_text.get_rect(center=start_button.center)
    back_text_rect = back_text.get_rect(center=back_button.center)
    
    screen.blit(start_text, start_text_rect)
    screen.blit(back_text, back_text_rect)
    
    return start_button, back_button

def handle_rules_modal_events(event):
    """Handle events for the rules modal"""
    # Draw buttons to get their positions
    screen_width, screen_height = 800, 600  # Default size
    box_width, box_height = 600, 400
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2
    
    start_button = pygame.Rect(box_x + 100, box_y + box_height - 70, 150, 50)
    back_button = pygame.Rect(box_x + box_width - 250, box_y + box_height - 70, 150, 50)
    
    # Handle mouse click
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        
        if start_button.collidepoint(mouse_pos):
            return "start"
        elif back_button.collidepoint(mouse_pos):
            return "back"
    
    # Handle keyboard
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            return "start"
        elif event.key == pygame.K_ESCAPE:
            return "back"
    
    return None