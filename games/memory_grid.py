import pygame
import random

memory_grid = []
highlighted_cells = []
selected_cells = []
showing_highlight = True
highlight_timer = 0
game_round = 0
difficulty = "hard"  # Can be "easy", "medium", or "hard"

def init_memory_grid():
    """Initialize the memory grid game"""
    global memory_grid, highlighted_cells, selected_cells, showing_highlight, highlight_timer, game_round
    
    # Generate a new grid
    memory_grid = generate_grid()
    
    # Select random cells to highlight based on difficulty
    num_to_highlight = 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
    highlighted_cells = select_random_cells(num_to_highlight)
    
    selected_cells = []
    showing_highlight = True
    highlight_timer = 120  # 2 seconds at 60 FPS
    game_round += 1

def generate_grid():
    """Generate a 3x4 grid of cells"""
    grid = []
    
    for row in range(3):
        grid_row = []
        for col in range(4):
            grid_row.append({
                "x": 0,
                "y": 0,
                "size": 0,
                "highlighted": False,
                "selected": False
            })
        
        grid.append(grid_row)
    
    return grid

def select_random_cells(num):
    """Select a specified number of random cells"""
    cells = []
    
    while len(cells) < num:
        row = random.randint(0, 2)
        col = random.randint(0, 3)
        
        cell = (row, col)
        if cell not in cells:
            cells.append(cell)
    
    return cells

def draw_memory_grid(screen, font_medium, game_data):
    """Draw the memory grid game"""
    global memory_grid, highlighted_cells, selected_cells, showing_highlight, highlight_timer
    
    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    
    # Calculate grid position and size
    grid_width = screen_width * 0.8
    grid_height = screen_height * 0.6
    cell_width = grid_width // 4
    cell_height = grid_height // 3
    grid_x = (screen_width - grid_width) // 2
    grid_y = (screen_height - grid_height) // 2 + 30
    
    # Update grid cells
    for row in range(3):
        for col in range(4):
            memory_grid[row][col]["x"] = grid_x + col * cell_width
            memory_grid[row][col]["y"] = grid_y + row * cell_height
            memory_grid[row][col]["width"] = cell_width
            memory_grid[row][col]["height"] = cell_height
    
    # Draw instruction
    if showing_highlight:
        inst_text = font_medium.render("Remember the highlighted squares", True, (0, 0, 0))
    else:
        inst_text = font_medium.render("Select the squares you saw highlighted", True, (0, 0, 0))
    
    inst_rect = inst_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(inst_text, inst_rect)
    
    # Draw grid cells
    for row in range(3):
        for col in range(4):
            cell = memory_grid[row][col]
            x = cell["x"]
            y = cell["y"]
            
            # Draw cell background
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, (240, 240, 240), cell_rect)
            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 2)
            
            # Draw highlight if showing highlights
            if showing_highlight and (row, col) in highlighted_cells:
                highlight_rect = pygame.Rect(x + 5, y + 5, cell_width - 10, cell_height - 10)
                pygame.draw.rect(screen, (255, 255, 0), highlight_rect)
            
            # Draw selection if not showing highlights
            if not showing_highlight and (row, col) in selected_cells:
                select_rect = pygame.Rect(x + 5, y + 5, cell_width - 10, cell_height - 10)
                pygame.draw.rect(screen, (0, 0, 255), select_rect)
    
    # Update highlight timer
    if showing_highlight and highlight_timer > 0:
        highlight_timer -= 1
        
        if highlight_timer == 0:
            showing_highlight = False

def handle_memory_grid_events(event, game_data):
    """Handle events for the memory grid game"""
    global memory_grid, selected_cells, showing_highlight
    
    # Only handle events if not showing highlights
    if not showing_highlight:
        # Handle mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check which cell was clicked
            for row in range(3):
                for col in range(4):
                    cell = memory_grid[row][col]
                    cell_rect = pygame.Rect(cell["x"], cell["y"], cell["width"], cell["height"])
                    
                    if cell_rect.collidepoint(mouse_pos):
                        toggle_cell_selection(row, col, game_data)
                        break
        
        # Handle keyboard
        elif event.type == pygame.KEYDOWN:
            # Number keys 1-12 correspond to grid positions
            if pygame.K_1 <= event.key <= pygame.K_9:
                key_num = event.key - pygame.K_1
                row = key_num // 4
                col = key_num % 4
                
                if 0 <= row < 3 and 0 <= col < 4:
                    toggle_cell_selection(row, col, game_data)
            elif event.key == pygame.K_0:
                # 0 key corresponds to the 10th position
                toggle_cell_selection(2, 1, game_data)
            elif event.key == pygame.K_MINUS:
                # - key corresponds to the 11th position
                toggle_cell_selection(2, 2, game_data)
            elif event.key == pygame.K_EQUALS:
                # = key corresponds to the 12th position
                toggle_cell_selection(2, 3, game_data)
            elif event.key == pygame.K_RETURN:
                # Submit selection
                check_selection(game_data)

def toggle_cell_selection(row, col, game_data):
    """Toggle the selection state of a cell"""
    global selected_cells
    
    cell = (row, col)
    
    if cell in selected_cells:
        selected_cells.remove(cell)
    else:
        selected_cells.append(cell)

def check_selection(game_data):
    """Check if the selected cells match the highlighted cells and update score"""
    global highlighted_cells, selected_cells
    
    # Calculate correct and incorrect selections
    correct = 0
    incorrect = 0
    
    for cell in selected_cells:
        if cell in highlighted_cells:
            correct += 1
        else:
            incorrect += 1
    
    for cell in highlighted_cells:
        if cell not in selected_cells:
            # Missed a highlighted cell
            pass
    
    # Update score
    game_data["score"] += correct * 5
    game_data["score"] -= incorrect * 2
    
    # Play sound
    from main import play_sound
    play_sound(correct > 0)
    
    # Show feedback and start a new round
    show_feedback_and_restart()

def show_feedback_and_restart():
    """Show feedback and start a new round"""
    global memory_grid, highlighted_cells, selected_cells, showing_highlight, highlight_timer
    
    # Generate a new grid
    memory_grid = generate_grid()
    
    # Select new cells to highlight
    num_to_highlight = 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
    highlighted_cells = select_random_cells(num_to_highlight)
    
    selected_cells = []
    showing_highlight = True
    highlight_timer = 120  # 2 seconds at 60 FPS