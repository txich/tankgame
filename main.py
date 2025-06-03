import pygame
import sys
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from tank import Tank
from enemies import enemy
from menu import show_menu

def spawn_enemy_outside_screen():
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2
    screen_diagonal = math.hypot(SCREEN_WIDTH, SCREEN_HEIGHT)
    spawn_radius = screen_diagonal / 2 + 100
    angle = random.uniform(0, 2 * math.pi)
    x = center_x + math.cos(angle) * spawn_radius
    y = center_y + math.sin(angle) * spawn_radius
    return enemy(x, y)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Game")
clock = pygame.time.Clock()

menu_action = show_menu(screen)
if menu_action == "quit":
    pygame.quit()
    sys.exit()

tank = Tank(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# list of enemies
enemies = []
enemy_spawn_delay = 3000
last_spawn_time = pygame.time.get_ticks()

# kill counter
kill_count = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
    dt = clock.tick(FPS) # fps lock

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            tank.player_shoot()

    keys = pygame.key.get_pressed()
    tank.update(keys)

    # enemy spawn
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > enemy_spawn_delay:
        enemies.append(spawn_enemy_outside_screen())
        last_spawn_time = current_time

    # enemy update cycle
    for e in enemies:
        e.update(tank.pos)
        # bullet update (check for hits)
        for bullet in tank.bullets:
            if bullet.get_rect().colliderect(e.get_rect()) and e.speed != 0:
                e.on_hit()
                kill_count += 1

    # enemies alive checker
    enemies = [e for e in enemies if e.speed != 0]

    # draw
    screen.fill((100, 100, 100))
    tank.draw(screen)
    for e in enemies:
        e.draw(screen)

    # kill counter render
    kill_text = font.render(f"Kills: {kill_count}", True, (255, 255, 255))
    screen.blit(kill_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
