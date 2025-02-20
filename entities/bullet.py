# entities/bullet.py
import pygame

# Constants
HEIGHT = 600
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player=True):
        super().__init__()
        if is_player:
            self.image = pygame.Surface((4, 10))
            self.image.fill(GREEN)
        else:
            self.image = pygame.Surface((4, 10))
            self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7 if is_player else 5
        self.is_player = is_player

    def update(self):
        if self.is_player:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
