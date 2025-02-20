# Space Invaders

A Python implementation of the classic Space Invaders arcade game using Pygame.

## Features

- **Player Mechanics**
  - Move with arrow keys
  - Shoot with spacebar
  - Multiple lives system
  - Power-up system with increased firepower

- **Enemy System**
  - Multiple waves of enemies
  - Progressive difficulty
  - Enemy shooting mechanics
  - Random enemy attack patterns

- **Power-ups**
  - Collect yellow orbs for power-ups
  - Three power levels:
    - Level 1: Single shot
    - Level 2: Double shot
    - Level 3: Triple shot
  - 10-second duration
  - 10% spawn chance from destroyed enemies

- **Visual Effects**
  - Dynamic starfield background
  - Twinkling stars with varying colors and sizes
  - Player invincibility animation
  - Score and lives display
  - Wave counter
  - Power level indicator

- **Audio System**
  - Background music
  - Shooting sound effects
  - Power-up collection sounds
  - Game over sound
  - Volume-balanced audio

## Controls

- **Arrow Keys**: Move player ship
- **Spacebar**: Shoot
- **Up/Down**: Move vertically (limited to lower half of screen)
- **Left/Right**: Move horizontally

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
```bash
git clone git@github.com:toledo-labs/space_invaders.git
cd space-invaders
```

2. Install Pygame:
```bash
pip install pygame
```

3. Run the game:
```bash
python3 main.py
```

## Game Rules

- Destroy enemy ships to score points
- Each enemy destroyed gives 10 points
- Collect power-ups to increase firepower
- Avoid enemy bullets
- Game ends when player loses all lives
- New wave starts when all enemies are destroyed
- Difficulty increases with each wave

## Project Structure

```
space-invaders/
├── main.py              # Main game loop and initialization
├── assets/             # Game assets
│   ├── player_ship.png
│   ├── enemy_ship.png
│   ├── background.wav
│   ├── shoot.wav
│   ├── powerup.wav
│   ├── game_over.wav
│   └── explosion.wav
└── entities/           # Game entities
    ├── player.py      # Player ship logic
    ├── enemy.py       # Enemy ship logic
    ├── bullet.py      # Projectile logic
    └── powerup.py     # Power-up system
```

## License

This project is open source and available under the MIT License.
