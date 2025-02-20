# main.py
import pygame
import random
import sys
import os
import math
from pygame import time
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.powerup import PowerUp

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 8
ENEMY_ROWS = 3
ENEMY_COLS = 8
PLAYER_LIVES = 3
BASE_ENEMY_SHOT_DELAY = 1000
DIFFICULTY_INCREASE = 0.8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 20)  # Very dark blue for space

# Sound paths
BACKGROUND_MUSIC = os.path.join('assets', 'background.wav')
GAME_OVER_SOUND = os.path.join('assets', 'game_over.wav')
STAR_COLORS = [
    (255, 255, 255),    # White
    (173, 216, 230),    # Light blue
    (255, 255, 224)     # Light yellow
]

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.color = random.choice(STAR_COLORS)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.t = random.uniform(0, 2 * 3.14159)  # Random start phase
        
    def update(self):
        self.t += self.twinkle_speed
        # Make stars twinkle by varying their brightness
        brightness = abs(math.sin(self.t))
        self.current_color = tuple(int(c * brightness) for c in self.color)
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.current_color, (self.x, self.y), self.size)

def load_sound(path, volume=0.5):
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except Exception as e:
        print(f"Error loading sound {path}: {str(e)}")
        return None

def reset_game(all_sprites, enemies, player_bullets, enemy_bullets, powerups):
    # Clear all sprite groups
    all_sprites.empty()
    enemies.empty()
    player_bullets.empty()
    enemy_bullets.empty()
    powerups.empty()
    
    # Create new player
    player = Player()
    all_sprites.add(player)
    
    return player

def main():
    pygame.init()
    pygame.mixer.init()  # Initialize sound system

    # Load sounds
    background_music = load_sound(BACKGROUND_MUSIC, 0.3)  # Lower volume for background
    game_over_sound = load_sound(GAME_OVER_SOUND, 0.5)

    # Initialize display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    def init_game():
        # Create starfield
        stars = [Star() for _ in range(100)]

        # Initialize sprite groups
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # Create player
        player = Player()
        all_sprites.add(player)

        # Game variables
        score = 0
        wave_number = 0
        current_enemy_shot_delay = BASE_ENEMY_SHOT_DELAY
        game_over = False

        # Start background music
        if background_music:
            background_music.play(-1)  # -1 means loop indefinitely

        return (stars, all_sprites, enemies, player_bullets, enemy_bullets, 
                powerups, player, score, wave_number, current_enemy_shot_delay, game_over)

    # Initialize game state
    (stars, all_sprites, enemies, player_bullets, enemy_bullets, 
     powerups, player, score, wave_number, current_enemy_shot_delay, game_over) = init_game()

    def spawn_enemies():
        nonlocal wave_number, current_enemy_shot_delay
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                enemy = Enemy(100 + col * 70, 50 + row * 50)
                enemies.add(enemy)
                all_sprites.add(enemy)
        current_enemy_shot_delay = max(BASE_ENEMY_SHOT_DELAY * (DIFFICULTY_INCREASE ** wave_number), 200)
        wave_number += 1

    def spawn_powerup(x, y):
        if random.random() < 0.1:  # 10% chance
            powerup = PowerUp(x, y)
            powerups.add(powerup)
            all_sprites.add(powerup)

    spawn_enemies()

    while True:  # Main game loop
        running = True
        last_enemy_shot = pygame.time.get_ticks()
        game_over = False

        # Game loop
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not game_over:
                        bullets = player.shoot()
                        for bullet in bullets:
                            all_sprites.add(bullet)
                            player_bullets.add(bullet)
                    elif game_over:
                        if event.key == pygame.K_r:
                            # Reset game state with new initialization
                            (stars, all_sprites, enemies, player_bullets, enemy_bullets, 
                             powerups, player, score, wave_number, current_enemy_shot_delay, game_over) = init_game()
                            spawn_enemies()
                            continue
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            if not game_over:
                all_sprites.update()

                # Enemy shooting
                if current_time - last_enemy_shot > current_enemy_shot_delay:
                    if enemies:
                        shooting_enemies = random.sample(list(enemies.sprites()), 
                                                      min(3, len(enemies)))
                        for enemy in shooting_enemies:
                            bullet = Bullet(enemy.rect.centerx, enemy.rect.bottom, False)
                            all_sprites.add(bullet)
                            enemy_bullets.add(bullet)
                        last_enemy_shot = current_time

                # Collisions
                hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
                for enemy, bullets in hits.items():
                    score += 10
                    spawn_powerup(enemy.rect.centerx, enemy.rect.centery)

                if pygame.sprite.spritecollide(player, enemy_bullets, True):
                    if player.hit() and player.lives <= 0:
                        game_over = True
                        if background_music:
                            background_music.stop()
                        if game_over_sound:
                            game_over_sound.play()

                powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
                for powerup in powerup_hits:
                    player.power_up()

                if not enemies:
                    spawn_enemies()

            # Draw
            screen.fill(DARK_BLUE)  # Dark blue background
            
            # Update and draw stars
            for star in stars:
                star.update()
                star.draw(screen)
                
            all_sprites.draw(screen)
            
            # HUD
            score_text = font.render(f'Score: {score}', True, WHITE)
            lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
            wave_text = font.render(f'Wave: {wave_number}', True, WHITE)
            power_text = small_font.render(f'Power: {player.power_level}', True, YELLOW)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 120, 10))
            screen.blit(wave_text, (WIDTH//2 - 40, 10))
            screen.blit(power_text, (10, 40))

            if game_over:
                game_over_text = font.render(f'GAME OVER - Final Score: {score}', True, WHITE)
                restart_text = font.render('Press R to Restart or Q to Quit', True, WHITE)
                screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
                screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 40))

            pygame.display.flip()
            clock.tick(FPS)

        if not game_over and not running:  # Only exit if not game over and window closed
            break

if __name__ == "__main__":
    main()
