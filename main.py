import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from tank import Tank
from enemy import Enemy
from menu import show_menu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Game")
clock = pygame.time.Clock()

menu_action = show_menu(screen)
if menu_action == "quit":
    pygame.quit()
    sys.exit()

# В дальнейшем сюда можно добавить обработку "settings"

tank = Tank(100, 100)
enemy = Enemy(400, 300)

running = True
while running:
    clock.tick(FPS)   #fps lock

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tank.update()
    enemy.update(tank.pos)

    screen.fill((30, 30, 30))
    tank.draw(screen)
    enemy.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
