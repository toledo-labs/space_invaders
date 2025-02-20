# entities/enemy.py
import pygame
import os

# Constants
WIDTH = 800
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ASSET_DIR = 'assets'
ENEMY_SHIP_IMG = os.path.join(ASSET_DIR, 'enemy_ship.png')
EXPLOSION_SOUND = os.path.join(ASSET_DIR, 'explosion.wav')

def load_sound(path, default_volume=0.5):
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(default_volume)
        return sound
    except:
        return None

explosion_sound = load_sound(EXPLOSION_SOUND)

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(ENEMY_SHIP_IMG, (40, 30), RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 20

    def kill(self):
        if explosion_sound:
            explosion_sound.play()
        super().kill()
