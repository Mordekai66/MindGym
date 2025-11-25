# MindGym

![Game Suite](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A collection of engaging mini-games designed to improve memory and focus skills, built with Python and Pygame.

## Games Included

### 1. Pick the Bigger
- **Objective**: Choose the larger of two items (numbers or shapes)
- **Skills**: Quick decision making, numerical comparison
- **Scoring**: +10 points for correct, -5 for incorrect

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/67aabc93-22da-45fb-bb6e-c887c838a29a" />

### 2. Find the Shape
- **Objective**: Locate the matching shape in a 3x3 grid
- **Skills**: Pattern recognition, visual discrimination
- **Scoring**: +15 points for correct, -5 for incorrect

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/ec352a82-dae6-4623-ae9e-1dd4d78e828a" />

### 3. Memory Recall
- **Objective**: Remember and recall highlighted squares in a 3x4 grid
- **Skills**: Short-term memory, spatial awareness
- **Scoring**: +5 points per correct square, -2 per incorrect

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/691380cb-43ce-484b-abd6-46d4901c3398" />

## Quick Start

### 1. Prerequisites
- Python 3.12 or higher

### 2. Clone the repository

### Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the game
```bash
python main.py
```

## How to Play
### Main Menu
The main menu provides easy access to all games with high score tracking:

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/1bde8c18-b4e7-4caf-9260-23f231fad658" />

### In-Game Controls
| Action        | Mouse     | Keyboard             |
|---------------|-----------|----------------------|
| Select        | Click     | Number Keys (1–9)    |
| Navigate      | —         | Arrow Keys           |
| Confirm       | Click     | ENTER                |
| Back to Menu  | —         | ESC                  |

### Game Features
- 30-second timer for each session
- Real-time score tracking
- Sound effects
- Rules accessible during gameplay
- Persistent high score storage

### Difficulty Settings
The Memory Recall game offers three difficulty levels:

| Difficulty | No. shapes     |
|------------|----------------|
| Easy       | 3 squares      |
| Medium     | 5 squares      |
| Hard       | 7 squares      |

To change difficulty, modify the difficulty variable in games/memory_grid.py ln.10

## Project Structure
```bash
MindGym/
├── main.py                 # Main game loop & state management
├── screens/
│   ├── menu.py             # Main menu interface
│   └── rules_modal.py      # Game rules display
├── games/
│   ├── two_choice.py       # Pick the Bigger game
│   ├── shape_grid.py       # Find the Shape game
│   └── memory_grid.py      # Memory Recall game
├── utils/
│   └── timer.py            # Timer utility class
├── assets/
│   └── icon.ico            # App icon
│   └── sound_success.wav   # success sound
│   └── sound_fail.wav      # fail sound
├── data/
│   └── highscores.json     # High score storage
├── screenshots/            # Game screenshots
│   ├── main-menu.png
│   ├── pick-the-bigger.png
│   ├── find-the-shape.png
│   └── rules-screen.png
│   └── game-over-screen.png
└── requirements.txt        # Dependencies
```
## Gameplay Overview
### Rules Screen
Before each game, players can review the rules and objectives:

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/48af0c55-f6f8-4752-9c2b-155a8f455431" />

### Game Over Screen
After each session, view your score and compare with your best:

<img width="700" height="525" alt="image" src="https://github.com/user-attachments/assets/e52e6a7b-dd23-4ff0-acf9-c48491097d82" />

## Development
### Adding New Games
To extend the suite with new mini-games:

1. Create a new python file in the games/ directory

2. Implement required functions:
   
   - init_game() - Initialize game state
   - draw_game() - Render game visuals
   - handle_game_events() - Process user input
   - Update menu and rules in respective screen files
   - Integrate into main game loop in main.py

### Example Game Template
```python
def init_your_game():
    """Initialize your game state"""
    pass

def draw_your_game(screen, font, game_data):
    """Draw your game to the screen"""
    pass

def handle_your_game_events(event, game_data):
    """Handle events for your game"""
    pass
```
## Future Enhancements
- Additional mini-games
- Multi-language support
- Mobile compatibility

## Contributing
We welcome contributions! Please feel free to submit pull requests for:
- New mini-games
- UI/UX improvements
- Bug fixes
- Performance optimizations

## License
This project is licensed under the MIT License - see the LICENSE file for details.
