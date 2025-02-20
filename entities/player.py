# entities/player.py
import pygame
import os

# Constants
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 8
PLAYER_LIVES = 3
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ASSET_DIR = 'assets'
PLAYER_SHIP_IMG = os.path.join(ASSET_DIR, 'player_ship.png')
SHOOT_SOUND = os.path.join(ASSET_DIR, 'shoot.wav')
POWERUP_SOUND = os.path.join(ASSET_DIR, 'powerup.wav')

def load_sound(path, default_volume=0.5):
    try:
        if not os.path.exists(path):
            print(f"Sound file not found: {path}")
            return None
        sound = pygame.mixer.Sound(path)
        sound.set_volume(default_volume)
        print(f"Successfully loaded sound: {path}")
        return sound
    except Exception as e:
        print(f"Error loading sound {path}: {str(e)}")
        return None

def create_default_ship(color, size):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    if color == GREEN:
        points = [(size[0]//2, 0), (size[0], size[1]), (0, size[1])]
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
        pygame.draw.circle(surface, WHITE, (size[0]//2, size[1]//2), size[0]//4)
    return surface

def load_image(path, size, default_color):
    try:
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)
        return create_default_ship(default_color, size)
    except:
        return create_default_ship(default_color, size)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load sounds
        self.shoot_sound = load_sound(SHOOT_SOUND)
        self.powerup_sound = load_sound(POWERUP_SOUND)
        
        self.image = load_image(PLAYER_SHIP_IMG, (50, 40), GREEN)
        self.original_image = self.image
        self.rect = self.image.get_rect(centerx=WIDTH//2, bottom=HEIGHT-10)
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES
        self.invincible = False
        self.invincible_timer = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.power_level = 1
        self.power_timer = 0

    def update(self):
        # Manage power-up timer
        if self.power_level > 1 and pygame.time.get_ticks() - self.power_timer > 10000:
            self.power_level = 1

        # Manage invincibility
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer > 2000:
                self.invincible = False
                self.image = self.original_image
            else:
                alpha = 255 if (current_time // 200) % 2 else 128
                self.image = self.original_image.copy()
                self.image.set_alpha(alpha)

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > HEIGHT//2:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        from entities.bullet import Bullet
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets = []
            if self.power_level == 1:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, True))
            elif self.power_level == 2:
                bullets.extend([
                    Bullet(self.rect.centerx - 10, self.rect.top, True),
                    Bullet(self.rect.centerx + 10, self.rect.top, True)
                ])
            elif self.power_level == 3:
                bullets.extend([
                    Bullet(self.rect.centerx - 15, self.rect.top, True),
                    Bullet(self.rect.centerx, self.rect.top, True),
                    Bullet(self.rect.centerx + 15, self.rect.top, True)
                ])
            if self.shoot_sound:
                self.shoot_sound.play()
            return bullets
        return []

    def hit(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()
            return True
        return False

    def power_up(self):
        self.power_level = min(self.power_level + 1, 3)
        self.power_timer = pygame.time.get_ticks()
        if self.powerup_sound:
            self.powerup_sound.play()
