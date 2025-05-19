import pygame
import math

class Tank:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0         # угол корпуса в градусах
        self.turret_angle = 0  # угол башни относительно корпуса

        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.rotation_speed = 3  # градусы за кадр

        # Размеры танка (для отрисовки)
        self.width = 60
        self.height = 40

        # Заглушки для изображения
        self.body_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.body_surf.fill((0, 100, 0))
        self.turret_surf = pygame.Surface((self.width // 2, self.height // 3), pygame.SRCALPHA)
        self.turret_surf.fill((50, 50, 50))

    def update(self, keys):
        # Поворот корпуса (A/D)
        if keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if keys[pygame.K_d]:
            self.angle -= self.rotation_speed

        # Ускорение (W/S)
        if keys[pygame.K_w]:
            self.speed += self.acceleration
        elif keys[pygame.K_s]:
            self.speed -= self.acceleration
        else:
            # Плавное замедление
            if self.speed > 0:
                self.speed -= self.acceleration / 2
            elif self.speed < 0:
                self.speed += self.acceleration / 2

        # Ограничение скорости
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed / 2:
            self.speed = -self.max_speed / 2  # Задний ход медленнее

        # Перемещение по направлению корпуса
        rad = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(rad), -math.sin(rad))
        self.pos += direction * self.speed

        # Поворот башни (стрелки ← →)
        if keys[pygame.K_LEFT]:
            self.turret_angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.turret_angle -= self.rotation_speed

        # Ограничение угла башни
        self.turret_angle %= 360

    def draw(self, screen):
        # Поворачиваем корпус
        rotated_body = pygame.transform.rotate(self.body_surf, self.angle)
        body_rect = rotated_body.get_rect(center=self.pos)

        # Поворачиваем башню с учётом корпуса (башня поворачивается относительно корпуса)
        total_turret_angle = self.angle + self.turret_angle
        rotated_turret = pygame.transform.rotate(self.turret_surf, total_turret_angle)
        turret_rect = rotated_turret.get_rect(center=self.pos)

        # Рисуем корпус и башню
        screen.blit(rotated_body, body_rect)
        screen.blit(rotated_turret, turret_rect)