import pygame
import random
import math

# Game variables
shape_grid = []
target_shape = ""
target_color = ""
selected_cell = None
feedback_timer = 0
feedback_correct = False
shake_amount = 0
target_text = ""

# Shape types
SHAPES = ["circle", "square", "triangle", "star", "diamond"]
COLORS = ["red", "blue", "green", "yellow", "purple"]

def init_shape_grid():
    """Initialize the shape grid game"""
    global shape_grid, target_shape, target_color, selected_cell, feedback_timer, feedback_correct, shake_amount, target_text
    
    # Generate a new grid
    shape_grid = generate_grid()
    
    # Select a random shape and color from the grid as target
    target_shape, target_color = select_target_from_grid()
    
    # Create target text
    target_text = f"Find: {target_shape.capitalize()}"
    if random.random() < 0.5:  # 50% chance to include color
        target_text += f" ({target_color.capitalize()})"
    
    selected_cell = None
    feedback_timer = 0
    feedback_correct = False
    shake_amount = 0

def generate_grid():
    """Generate a 3x3 grid of random shapes"""
    grid = []
    
    for row in range(3):
        grid_row = []
        for col in range(3):
            # Random shape and color
            shape = random.choice(SHAPES)
            color = random.choice(COLORS)
            
            # Random rotation (0, 90, 180, 270 degrees)
            rotation = random.choice([0, 90, 180, 270])
            
            grid_row.append({
                "shape": shape,
                "color": color,
                "rotation": rotation,
                "x": 0,
                "y": 0,
                "size": 0,
                "highlighted": False
            })
        
        grid.append(grid_row)
    
    return grid

def select_target_from_grid():
    """Select a random shape and color from the grid as target"""
    global shape_grid
    
    # Flatten the grid to get all cells
    all_cells = []
    for row in shape_grid:
        for cell in row:
            all_cells.append(cell)
    
    # Select a random cell from the grid
    target_cell = random.choice(all_cells)
    
    # Return the shape and color of the selected cell
    return target_cell["shape"], target_cell["color"]

def draw_shape_grid(screen, font_medium, game_data):
    """Draw the shape grid game"""
    global shape_grid, target_shape, target_color, selected_cell, feedback_timer, feedback_correct, shake_amount, target_text
    
    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    
    # Calculate grid position and size
    grid_size = min(screen_width, screen_height) * 0.6
    cell_size = grid_size // 3
    grid_x = (screen_width - grid_size) // 2
    grid_y = (screen_height - grid_size) // 2 + 30
    
    # Apply shake effect if needed
    shake_x = 0
    shake_y = 0
    if shake_amount > 0:
        shake_x = random.randint(-shake_amount, shake_amount)
        shake_y = random.randint(-shake_amount, shake_amount)
        shake_amount = max(0, shake_amount - 1)  # Ensure it doesn't go negative
    
    # Draw target description
    text = font_medium.render(target_text, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, 90))
    screen.blit(text, text_rect)
    
    # Draw grid cells
    for row in range(3):
        for col in range(3):
            # Calculate cell position
            x = grid_x + col * cell_size + shake_x
            y = grid_y + row * cell_size + shake_y
            
            # Update cell position
            shape_grid[row][col]["x"] = x
            shape_grid[row][col]["y"] = y
            shape_grid[row][col]["size"] = cell_size
            
            # Draw cell background
            cell_rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, (240, 240, 240), cell_rect)
            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)
            
            # Draw feedback if needed
            if feedback_timer > 0 and selected_cell == (row, col):
                if feedback_correct:
                    # Draw green overlay for correct
                    overlay = pygame.Surface((cell_size, cell_size))
                    overlay.set_alpha(100)
                    overlay.fill((0, 200, 0))
                    screen.blit(overlay, (x, y))
                else:
                    # Draw red overlay for incorrect
                    overlay = pygame.Surface((cell_size, cell_size))
                    overlay.set_alpha(100)
                    overlay.fill((200, 0, 0))
                    screen.blit(overlay, (x, y))
            
            # Draw shape
            draw_shape(screen, shape_grid[row][col], x + cell_size // 2, y + cell_size // 2, cell_size * 0.6)
    
    # Decrease feedback timer after drawing
    if feedback_timer > 0:
        feedback_timer -= 1
        # Only generate new grid when feedback is done
        if feedback_timer == 0:
            handle_new_grid()
    
    # Draw instruction
    inst_text = font_medium.render("Click on the matching shape", True, (0, 0, 0))
    inst_rect = inst_text.get_rect(center=(screen_width // 2, 135))
    screen.blit(inst_text, inst_rect)

def draw_shape(screen, shape_data, center_x, center_y, size):
    """Draw a shape at the specified position"""
    shape = shape_data["shape"]
    color_name = shape_data["color"]
    rotation = shape_data["rotation"]
    
    # Map color names to RGB values
    color_map = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "purple": (128, 0, 128)
    }
    
    color = color_map.get(color_name, (0, 0, 0))
    
    # Create a surface for the shape
    shape_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Draw the shape based on its type
    if shape == "circle":
        pygame.draw.circle(shape_surface, color, (size // 2, size // 2), size // 2)
    elif shape == "square":
        rect = pygame.Rect(0, 0, size, size)
        pygame.draw.rect(shape_surface, color, rect)
    elif shape == "triangle":
        points = [
            (size // 2, 0),
            (0, size),
            (size, size)
        ]
        pygame.draw.polygon(shape_surface, color, points)
    elif shape == "star":
        # Draw a simple 5-pointed star
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                # Outer point
                r = size // 2
            else:
                # Inner point
                r = size // 4
            x = size // 2 + r * math.sin(angle)
            y = size // 2 - r * math.cos(angle)
            points.append((x, y))
        pygame.draw.polygon(shape_surface, color, points)
    elif shape == "diamond":
        points = [
            (size // 2, 0),
            (size, size // 2),
            (size // 2, size),
            (0, size // 2)
        ]
        pygame.draw.polygon(shape_surface, color, points)
    
    # Rotate the shape if needed
    if rotation != 0:
        shape_surface = pygame.transform.rotate(shape_surface, -rotation)
    
    # Draw the shape on the screen
    shape_rect = shape_surface.get_rect(center=(center_x, center_y))
    screen.blit(shape_surface, shape_rect)

def handle_shape_grid_events(event, game_data):
    """Handle events for the shape grid game"""
    global shape_grid, selected_cell, feedback_timer, feedback_correct, shake_amount, target_text
    
    # Only handle clicks if no feedback is showing
    if feedback_timer > 0:
        return
    
    # Handle mouse click
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        
        # Check which cell was clicked
        for row in range(3):
            for col in range(3):
                cell = shape_grid[row][col]
                cell_rect = pygame.Rect(cell["x"], cell["y"], cell["size"], cell["size"])
                
                if cell_rect.collidepoint(mouse_pos):
                    selected_cell = (row, col)
                    check_selection(row, col, game_data)
                    return
    
    # Handle keyboard
    elif event.type == pygame.KEYDOWN:
        # Number keys 1-9 correspond to grid positions
        if pygame.K_1 <= event.key <= pygame.K_9:
            key_num = event.key - pygame.K_1
            row = key_num // 3
            col = key_num % 3
            
            selected_cell = (row, col)
            check_selection(row, col, game_data)

def check_selection(row, col, game_data):
    """Check if the selected cell matches the target and update score"""
    global shape_grid, target_shape, target_color, feedback_timer, feedback_correct, shake_amount, target_text
    
    # Get the selected cell
    cell = shape_grid[row][col]
    
    # Check if the cell matches the target
    shape_match = cell["shape"] == target_shape
    color_match = cell["color"] == target_color
    
    # Determine if the selection is correct
    # If the target description includes color, both must match
    # Otherwise, only the shape must match
    if "(" in target_text and ")" in target_text:
        # Target includes color
        correct = shape_match and color_match
    else:
        # Target only includes shape
        correct = shape_match
    
    if correct:
        # Correct selection
        game_data["score"] += 15
        feedback_correct = True
    else:
        # Incorrect selection
        game_data["score"] = max(0, game_data["score"] - 5)  # Prevent negative score
        feedback_correct = False
        shake_amount = 10  # Shake effect
    
    # Set feedback timer
    feedback_timer = 48  # 0.8 seconds at 60 FPS
    
    # Play sound
    try:
        from main import play_sound
        play_sound(feedback_correct)
    except ImportError:
        pass  # Skip if sound module not available

def handle_new_grid():
    """Generate a new grid and target for the next round"""
    global shape_grid, target_shape, target_color, selected_cell, target_text
    
    # Generate a new grid
    shape_grid = generate_grid()
    
    # Select a random shape and color from the new grid as target
    target_shape, target_color = select_target_from_grid()
    
    # Create target text
    target_text = f"Find: {target_shape.capitalize()}"
    if random.random() < 0.5:  # 50% chance to include color
        target_text += f" ({target_color.capitalize()})"
    
    selected_cell = None