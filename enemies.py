import pygame
import math

class enemy():
    def __init__(self, x, y, speed=1.5):
        self.pos = pygame.Vector2(x, y)
        self.color = (255, 0, 0)
        self.size = 50
        self.speed = speed

        # image loading with fallback
        self.image = pygame.image.load("./assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.angle = 0  # angle in degrees 

    def update(self, player_pos):
        direction = (player_pos - self.pos)
        if direction.length() != 0:
            direction = direction.normalize()
            self.pos += direction * self.speed
            # angle calculation
            self.angle = -math.degrees(math.atan2(direction.y, direction.x))

    def draw(self, surface):
            # rotate the image based on the angle
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rect = rotated_image.get_rect(center=(self.pos.x + self.size // 2, self.pos.y + self.size // 2))
            surface.blit(rotated_image, rect)
    
    def get_rect(self):
        return pygame.Rect(self.pos.x-2, self.pos.y-2, self.size+4, self.size+4)
    
    def on_hit(self):
        self.color = (0, 0, 0)
        self.speed = 0