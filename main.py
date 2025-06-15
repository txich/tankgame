import pygame
import sys
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from tank import Tank
from enemies import enemy
from menu import show_menu, show_settings


current_resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
current_fps = FPS

def spawn_enemy_outside_screen():
    center_x = current_resolution[0] / 2
    center_y = current_resolution[1] / 2
    screen_diagonal = math.hypot(current_resolution[0], current_resolution[1])
    spawn_radius = screen_diagonal / 2 + 100
    angle = random.uniform(0, 2 * math.pi)
    x = center_x + math.cos(angle) * spawn_radius
    y = center_y + math.sin(angle) * spawn_radius
    base_speed = 1.5
    speed = base_speed + kill_count // 10  # increase speed with kills
    return enemy(x, y, speed)

def show_game_over(screen, kill_count):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)
    options = ["Restart", "Main Menu", "Quit"]
    selected = 0

    clock = pygame.time.Clock()
    while True:
        screen.fill((30, 0, 0))
        over_text = font.render("GAME OVER", True, (255, 50, 50))
        kills_text = small_font.render(f"Kills: {kill_count}", True, (255, 255, 255))
        screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, 150))
        screen.blit(kills_text, (SCREEN_WIDTH // 2 - kills_text.get_width() // 2, 250))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option_text = small_font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 350 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return options[selected].lower()

        clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Game")
clock = pygame.time.Clock()

# load background image and scale to screen size
background = pygame.image.load("./assets/background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

menu_action = show_menu(screen)
if menu_action == "quit":
    pygame.quit()
    sys.exit()

tank = Tank(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# list of enemies
enemies = []
enemy_spawn_delay = 3000
min_spawn_delay = 1500
last_spawn_time = pygame.time.get_ticks()

# kill counter
kill_count = 0

lives = 3


font = pygame.font.SysFont(None, 36)

# screen resolution and FPS settings

while True:
    menu_action = show_menu(screen)
    if menu_action == "quit":
        pygame.quit()
        sys.exit()
    elif menu_action == "settings":
        _, new_res, new_fps = show_settings(screen)
        current_resolution = new_res
        current_fps = new_fps
        screen = pygame.display.set_mode(current_resolution)
        continue
    elif menu_action == "start":
        # start the game loop
        while True:
            tank = Tank(current_resolution[0] /2 , current_resolution[1] / 2)
            enemies = []
            last_spawn_time = pygame.time.get_ticks()
            kill_count = 0
            lives = 3
            running = True


            while running:
                dt = clock.tick(60) # fps lock

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        tank.player_shoot()

                keys = pygame.key.get_pressed()
                tank.update(keys)

                # enemy spawn
                current_time = pygame.time.get_ticks()
                spawn_delay = max(min_spawn_delay, enemy_spawn_delay - kill_count * 30)
                if current_time - last_spawn_time > spawn_delay:
                    enemies.append(spawn_enemy_outside_screen())
                    last_spawn_time = current_time

                tank_rect = pygame.Rect(
                    tank.pos.x - tank.width // 2,
                    tank.pos.y - tank.height // 2,
                    tank.width,
                    tank.height
                )

                # enemy update cycle
                for e in enemies:
                    e.update(tank.pos)
                    # bullet update (check for hits)
                    for bullet in tank.bullets:
                        if bullet.get_rect().colliderect(e.get_rect()) and e.speed != 0:
                            e.on_hit()
                            kill_count += 1

                for e in enemies:
                    if e.get_rect().colliderect(tank_rect) and e.speed != 0:
                        e.on_hit()
                        lives -= 1
                        if lives <= 0:
                            running = False

                # draw
                screen.blit(background, (0, 0))
                tank.draw(screen)
                for e in enemies:
                    e.draw(screen)

                kill_text = font.render(f"Kills: {kill_count}", True, (255, 255, 255))
                screen.blit(kill_text, (10, 10))

                lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
                screen.blit(lives_text, (10, 50))

                pygame.display.flip()


                current_time = pygame.time.get_ticks()
                enemies = [
                    e for e in enemies
                    if not (e.exploding and current_time - e.explosion_start > e.explosion_duration)
                ]

            # after game over
            action = show_game_over(screen, kill_count)
            if action == "restart":
                continue  # restart the game loop
            elif action == "main menu":
                break  # return to the main menu
            elif action == "quit":
                pygame.quit()
                sys.exit()
