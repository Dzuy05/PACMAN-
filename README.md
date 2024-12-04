# PACMAN WITH HAND CONTROLL, WHY NOT??!!
WELCOM TO THE PACMAN - WHERE YOU CAN EXPERIENCE THE GAME WITH NOT JUST THE KEYBOARD BUT ALSO YOUR HAND!! 
## **OVERVIEW**
- Pac-Man is a classic video game where the player controls Pac-Man, navigating a maze to eat all the small pellets while avoiding four ghosts.  
- The goal is to eat all the pellets without being caught by the ghosts.
## Installation
### **Installation dependencies**
To get the Pacman game up and running on your local machine, make sure you have the following installed:
- Python 3
- Opencv
- Mediapipe
- Pygame
- Threading
- Numpy 

### How to run   
- Pull this repository to your computer/laptop
- Locate to the file that contain `run.py`
- Run `run.py` or use this:
```bash
py run.py
```
## USAGE
**1. How to play**
 - **Arrow Keys**: Use the arrow keys to move Pacman around the maze.
- **Objective**: Collect all the pellets while avoiding the ghosts. Eating a power pellet allows you to chase and eat ghosts for extra points.
- **Game Over**: The game ends when you either run out of lives or clear the maze of all pellets.

Enjoy playing Pacman! If you encounter any issues, feel free to open an issue on the GitHub repository.

**2. Gameplay Mechanic**
#
**OBJECTIVE**
- The main objective of the game is to navigate Pacman through the maze, collect all the pellets, and avoid the ghosts. Eating all the pellets in the maze advances you to the next level.

# 
**CONTROLS**
- **Arrow Keys**: Use the arrow keys to move Pacman up, down, left, and right.
- **Hand movements**: Use hand by rotate the wrist to change the direction of Pacman. Where the fingers point is direction of Pacman.
#
**GAME ELEMENTS**
- **Pellets**: Small dots scattered throughout the maze. Eating all pellets in a level allows you to progress to the next level.
- **Power Pellets**: Larger dots that give Pacman the temporary ability to eat ghosts.
- **Ghosts**: Enemies that roam the maze. If a ghost catches Pacman, you lose a life. After losing all lives, the game is over.
- **Fruits**: Occasionally appear in the maze and provide bonus points when eaten.
3. **Feature**
### GHOST BEHAVIOR
- **Chase Mode**: Ghosts actively chase Pacman.
- **Scatter Mode**: Ghosts move to their respective corners of the maze.
- **Frightened Mode**: Triggered by eating a power pellet, allowing Pacman to eat the ghosts for a limited time.

### SCORING
- **Pellet**: 10 points each.
- **Power Pellet**: 50 points each.
- **Ghost**: Points for eating ghosts increase with each successive ghost eaten in a single power pellet duration (200, 400, 800, 1600 points).
- **Fruit**: Points vary depending on the type of fruit.

### LEVELS
Each level increases in difficulty with faster ghosts and more complex maze layouts. The game continues until all lives are lost.

### LIVES
Pacman starts with three lives. Extra lives can be earned by reaching certain score thresholds.

Enjoy playing Pacman and aim for the highest score!

## PROJECT STRUCTURES
The project is organized into following directories and files:

- **Font Files:**
  - `PressStart2P-Regular.ttf`: The font used for the game’s text.

- **Game Logic:**
  - `main.py`: The entry point of the game, initializing the game window and managing the game loop.
  - `pacman.py`: Logic for controlling Pac-Man's movement and interactions.
  - `ghosts.py`: Defines the behavior and movement of ghosts chasing Pac-Man.
  - `direction_handler.py`: Controls direction inputs and movement.

- **Game Elements:**
  - `fruit.py`: Defines special fruit items for bonus points.
  - `pellets.py`: Manages pellets for Pac-Man to eat in the maze.
  - `mazedata.py`: Contains functions for reading and parsing maze layout files (`maze1.txt`, `maze2.txt`).
  - `modes.py`: Contains different game modes (like difficulty levels and win/lose conditions).
  
- **Sprites & Graphics:**
  - `spritesheet.png`: The standard sprite sheet for characters.
  - `spritesheet_mspacman.png`: Alternate sprite sheet for Ms. Pac-Man.
  - `spritesheet_pacman2.png`: Another version of sprite sheet for Pac-Man.

- **Utilities:**
  - `text.py`: Renders text on the screen for things like scores and messages.
  - `vector.py`: Provides vector mathematics utilities used in movement and collision.




## License
This project is licensed under the MIT License


## Contact Information

- Bui Phuong Duy 20233957 - duy.bp233957@sis.hust.edu.vn - Coder for this project.
- Bui Quang Huy 20233961 - huy.bq233961@sis.hust.edu.vn - Document maintainance.