import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from tank import Tank
from enemies import enemy
from menu import show_menu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Game")
clock = pygame.time.Clock()

menu_action = show_menu(screen)
if menu_action == "quit":
    pygame.quit()
    sys.exit()

tank = Tank(100, 100)
enemy1 = enemy(400, 300)

running = True
while running:
    clock.tick(FPS)   #fps lock

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_SPACE:
            tank.player_shoot()

    keys = pygame.key.get_pressed()

    tank.update(keys)
    enemy1.update(tank.pos)
    for bullet in tank.bullets:
        if bullet.get_rect().colliderect(enemy1.get_rect()):
            enemy1.on_hit()

# Удаление мёртвых пуль
    tank.bullets = [b for b in tank.bullets if b.alive]

    screen.fill((100, 100, 100))
    tank.draw(screen)
    enemy1.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
