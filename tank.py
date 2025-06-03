import pygame
import math
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import random

class Bullet():
    def __init__(self, pos, direction):
        self.speed = 30
        self.direction = direction
        self.pos = pygame.Vector2(pos)
        self.surface = pygame.Surface((6, 6), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0)) 
        self.rect = self.surface.get_rect(center=self.pos)
        self.alive = True


    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
    

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def get_rect(self):
        return pygame.Rect(self.rect)


class Tank():
    def __init__(self, x, y):
        #tank sett
        self.shoot_delay = 400  # shoot delay in milliseconds
        self.last_shot_time = 0
        self.pos = pygame.Vector2(x, y)
        self.angle = 0         # tank angle
        self.turret_angle = 0  # gun angle 
        self.speed = 0
        self.max_speed = 4
        self.acceleration = 0.03
        self.rotation_speed = 1.5

        # tank width and height
        self.width = 60
        self.height = 40

        self.bullets = []

        # temporary
        self.body_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.body_surf.fill((0, 100, 0))
        self.turret_surf = pygame.Surface((self.width // 2, self.height // 3), pygame.SRCALPHA)
        self.turret_surf.fill((50, 50, 50))
    
    def player_shoot(self):
        current_time = pygame.time.get_ticks()  # time counter
        if current_time - self.last_shot_time >= self.shoot_delay:
            total_turret_angle = self.angle + self.turret_angle     
            rad_turret = math.radians(total_turret_angle)
            bullet_direction = pygame.Vector2(math.cos(rad_turret), -math.sin(rad_turret))
            bullet = Bullet(self.pos, bullet_direction)
            self.bullets.append(bullet)
            self.last_shot_time = current_time
        

    def update(self, keys):
        # Tank rotation
        if keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if keys[pygame.K_d]:
            self.angle -= self.rotation_speed

        # acceleration
        if keys[pygame.K_w]:
            self.speed += self.acceleration
        elif keys[pygame.K_s]:
            self.speed -= self.acceleration
        else:
            # deceleration
            if self.speed > 0:
                self.speed -= self.acceleration 
            elif self.speed < 0:
                self.speed += self.acceleration

        # max spd
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed / 2:
            self.speed = -self.max_speed / 2 

        # moving
        rad = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(rad), -math.sin(rad))
        self.pos += direction * self.speed

        # gun rotation
        if keys[pygame.K_LEFT]:
            self.turret_angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.turret_angle -= self.rotation_speed

        # idk
        self.turret_angle %= 360

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [b for b in self.bullets if 0 <= b.pos.x <= SCREEN_WIDTH and 0 <= b.pos.y <= SCREEN_HEIGHT]

    def draw(self, screen):
        # draw tank rotation
        rotated_body = pygame.transform.rotate(self.body_surf, self.angle)
        body_rect = rotated_body.get_rect(center=self.pos)

        # gun rotation with tank rotation
        total_turret_angle = self.angle + self.turret_angle
        rotated_turret = pygame.transform.rotate(self.turret_surf, total_turret_angle)
        turret_rect = rotated_turret.get_rect(center=self.pos)

        # draw tank
        screen.blit(rotated_body, body_rect)
        screen.blit(rotated_turret, turret_rect)

        # draw aiming line
        aim_length = 9000
        rad_turret = math.radians(total_turret_angle)
        aim_direction = pygame.Vector2(math.cos(rad_turret), -math.sin(rad_turret))
        start_pos = self.pos
        end_pos = self.pos + aim_direction * aim_length
        aim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        aim_color = (255, 0, 0, 50) 
        pygame.draw.line(aim_surface, aim_color, start_pos, end_pos, 2)
        screen.blit(aim_surface, (0, 0))

        # draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)