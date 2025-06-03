import pygame
from settings import calc_distance

class enemy():
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.color = (255, 0, 0)
        self.size = 40
        self.speed = 2

    def update(self, player_pos):
            direction = (player_pos - self.pos).normalize()
            self.pos += direction * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, self.size, self.size))
    
    def get_rect(self):
        return pygame.Rect(self.pos.x-2, self.pos.y-2, self.size+4, self.size+4)

    def on_hit(self):
        self.color = (0, 0, 0)
        self.speed = 0