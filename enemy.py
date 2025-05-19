import pygame
from settings import calc_distance

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.color = (255, 0, 0)
        self.size = 40

    def update(self, player_pos):
        direction = (player_pos - self.pos).normalize()
        self.pos += direction * 2

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.size, self.size))
