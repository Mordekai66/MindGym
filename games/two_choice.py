import pygame
import random
import math

# Game variables
two_choice_items = []
selected_item = None
feedback_timer = 0
feedback_correct = False

def init_two_choice():
    """Initialize the two choice game"""
    global two_choice_items, selected_item, feedback_timer
    
    # Generate two random items
    two_choice_items = generate_items()
    selected_item = None
    feedback_timer = 0

def generate_items():
    """Generate two random items for the player to choose from"""
    items = []
    
    # Decide whether to use numbers or shapes
    use_numbers = True
    
    if use_numbers:
        # Generate two numbers
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        
        # Create items with numbers
        items.append({
            "type": "number",
            "value": num1,
            "display": str(num1),
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0
        })
        
        items.append({
            "type": "number",
            "value": num2,
            "display": str(num2),
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0
        })
    return items

def draw_two_choice(screen, font_medium, game_data):
    """Draw the two choice game"""
    global two_choice_items, selected_item, feedback_timer, feedback_correct
    
    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    
    # Calculate positions
    box_width, box_height = 200, 200
    box_y = 150
    
    # Left box
    left_x = screen_width // 2 - box_width - 50
    left_rect = pygame.Rect(left_x, box_y, box_width, box_height)
    
    # Right box
    right_x = screen_width // 2 + 50
    right_rect = pygame.Rect(right_x, box_y, box_width, box_height)
    
    # Update item positions
    two_choice_items[0]["x"] = left_x
    two_choice_items[0]["y"] = box_y
    two_choice_items[0]["width"] = box_width
    two_choice_items[0]["height"] = box_height
    
    two_choice_items[1]["x"] = right_x
    two_choice_items[1]["y"] = box_y
    two_choice_items[1]["width"] = box_width
    two_choice_items[1]["height"] = box_height
    
    # Draw boxes
    pygame.draw.rect(screen, (240, 240, 240), left_rect)
    pygame.draw.rect(screen, (0, 0, 0), left_rect, 2)
    
    pygame.draw.rect(screen, (240, 240, 240), right_rect)
    pygame.draw.rect(screen, (0, 0, 0), right_rect, 2)
    
    # Draw feedback if needed
    if feedback_timer > 0:
        feedback_timer -= 1
        
        if feedback_correct:
            # Draw green overlay for correct
            overlay = pygame.Surface((box_width, box_height))
            overlay.fill((0, 200, 0))
            
            if selected_item == 0:
                screen.blit(overlay, (left_x, box_y))
            else:
                screen.blit(overlay, (right_x, box_y))
        else:
            # Draw red overlay for incorrect
            overlay = pygame.Surface((box_width, box_height))
            overlay.fill((200, 0, 0))
            
            if selected_item == 0:
                screen.blit(overlay, (left_x, box_y))
            else:
                screen.blit(overlay, (right_x, box_y))
    
    # Draw items
    for i, item in enumerate(two_choice_items):
        if item["type"] == "number":
            # Draw number
            text = font_medium.render(item["display"], True, (0, 0, 0))
            text_rect = text.get_rect(center=(item["x"] + item["width"] // 2, item["y"] + item["height"] // 2))
            screen.blit(text, text_rect)
        else:
            # Draw shape
            center_x = item["x"] + item["width"] // 2
            center_y = item["y"] + item["height"] // 2
            
            if item["shape"] == "circle":
                pygame.draw.circle(screen, (0, 0, 200), (center_x, center_y), item["size"] // 2)
            elif item["shape"] == "square":
                rect = pygame.Rect(center_x - item["size"] // 2, center_y - item["size"] // 2, item["size"], item["size"])
                pygame.draw.rect(screen, (200, 0, 0), rect)
            elif item["shape"] == "triangle":
                points = [
                    (center_x, center_y - item["size"] // 2),
                    (center_x - item["size"] // 2, center_y + item["size"] // 2),
                    (center_x + item["size"] // 2, center_y + item["size"] // 2)
                ]
                pygame.draw.polygon(screen, (0, 200, 0), points)
            
            # Draw shape name
            text = font_medium.render(item["display"], True, (0, 0, 0))
            text_rect = text.get_rect(center=(center_x, item["y"] + item["height"] - 30))
            screen.blit(text, text_rect)
    
    # Draw instruction
    inst_text = font_medium.render("Select the larger item", True, (0, 0, 0))
    inst_rect = inst_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(inst_text, inst_rect)
    
    # Draw keyboard hint
    hint_text = font_medium.render("Use LEFT/RIGHT arrows or click to select", True, (100, 100, 100))
    hint_rect = hint_text.get_rect(center=(screen_width // 2, 400))
    screen.blit(hint_text, hint_rect)

def handle_two_choice_events(event, game_data):
    """Handle events for the two choice game"""
    global two_choice_items, selected_item, feedback_timer, feedback_correct
    
    # Handle mouse click
    if event.type == pygame.MOUSEBUTTONDOWN and feedback_timer == 0:
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if left item was clicked
        left_rect = pygame.Rect(two_choice_items[0]["x"], two_choice_items[0]["y"], 
                               two_choice_items[0]["width"], two_choice_items[0]["height"])
        
        # Check if right item was clicked
        right_rect = pygame.Rect(two_choice_items[1]["x"], two_choice_items[1]["y"], 
                                two_choice_items[1]["width"], two_choice_items[1]["height"])
        
        if left_rect.collidepoint(mouse_pos):
            selected_item = 0
            check_selection(game_data)
        elif right_rect.collidepoint(mouse_pos):
            selected_item = 1
            check_selection(game_data)
    
    # Handle keyboard
    elif event.type == pygame.KEYDOWN and feedback_timer == 0:
        if event.key == pygame.K_LEFT:
            selected_item = 0
            check_selection(game_data)
        elif event.key == pygame.K_RIGHT:
            selected_item = 1
            check_selection(game_data)

def check_selection(game_data):
    """Check if the selected item is correct and update score"""
    global two_choice_items, selected_item, feedback_timer, feedback_correct
    
    # Get values of the two items
    value1 = two_choice_items[0]["value"]
    value2 = two_choice_items[1]["value"]
    
    # Determine which item is larger
    larger_item = 0 if value1 > value2 else 1
    
    # Check if selection is correct
    if selected_item == larger_item:
        # Correct selection
        game_data["score"] += 10
        feedback_correct = True
        init_two_choice()
	
    else:
        # Incorrect selection
        game_data["score"] -= 5
        feedback_correct = False
        init_two_choice()
    
    # Set feedback timer
    feedback_timer = 30  # 0.5 seconds at 60 FPS
    
    # Play sound
    from main import play_sound
    play_sound(feedback_correct)
    
    # Generate new items after a short delay
    import pygame
    pygame.time.set_timer(pygame.USEREVENT + 1, 500)

def handle_new_items():
    """Generate new items for the next round"""
    global two_choice_items, selected_item
    
    two_choice_items = generate_items()
    selected_item = None