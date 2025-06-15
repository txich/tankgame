import pygame
import math

class enemy():
    def __init__(self, x, y, speed=1.5):
        self.pos = pygame.Vector2(x, y)
        self.color = (255, 0, 0)
        self.size = 50
        self.speed = speed

        # image loading
        self.image = pygame.image.load("./assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.angle = 0  # angle in degrees 

        # explosion animation (4 frames)
        self.explosion_frames = [
            pygame.transform.scale(
                pygame.image.load(f"./assets/explosion{i}.png").convert_alpha(),
                (self.size, self.size)
            ) for i in range(1, 5)
        ]
        self.exploding = False
        self.explosion_start = 0
        self.explosion_duration = 400  # ms
        self.explosion_frame_time = self.explosion_duration // len(self.explosion_frames)

    def update(self, player_pos):
        if self.exploding:
            return
        direction = (player_pos - self.pos)
        if direction.length() != 0:
            direction = direction.normalize()
            self.pos += direction * self.speed
            # angle calculation
            self.angle = -math.degrees(math.atan2(direction.y, direction.x))

    def draw(self, surface):
        if self.exploding:
            now = pygame.time.get_ticks()
            frame_idx = min(
                (now - self.explosion_start) // self.explosion_frame_time,
                len(self.explosion_frames) - 1
            )
            frame = self.explosion_frames[frame_idx]
            rect = frame.get_rect(center=(self.pos.x + self.size // 2, self.pos.y + self.size // 2))
            surface.blit(frame, rect)
        else:
            # rotate the image based on the angle
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rect = rotated_image.get_rect(center=(self.pos.x + self.size // 2, self.pos.y + self.size // 2))
            surface.blit(rotated_image, rect)
    
    def get_rect(self):
        return pygame.Rect(self.pos.x-2, self.pos.y-2, self.size+4, self.size+4)
    
    def on_hit(self):
        self.color = (0, 0, 0)
        self.speed = 0
        if not self.exploding:
            self.exploding = True
            self.explosion_start = pygame.time.get_ticks()