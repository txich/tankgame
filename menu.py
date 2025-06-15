import pygame
from settings import SCREEN_WIDTH

def show_menu(screen):
    font = pygame.font.SysFont("arial", 50)
    options = ["Start", "Settings", "Quit"]
    selected = 0

    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        title_text = font.render("TANK GAME", True, (255, 255, 255))
        screen.blit(title_text, (pygame.display.get_surface().get_size()[0]// 2 - title_text.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (pygame.display.get_surface().get_size()[0] // 2 - option_text.get_width() // 2, 250 + i * 70))

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

def show_settings(screen):
    font = pygame.font.SysFont("arial", 40)
    resolutions = [(1280, 720), (1600, 900), (1920, 1080)]
    fps_options = [30, 60, 120, 240]
    try:
        res_index = [r[0] for r in resolutions].index(screen.get_width())
    except ValueError:
        res_index = 1
    fps_index = 1 # Default FPS index

    options = [
        f"Resolution: {resolutions[res_index][0]}x{resolutions[res_index][1]}",
        f"FPS: {fps_options[fps_index]}",
        "Back"
    ]
    selected = 0

    clock = pygame.time.Clock()
    while True:
        width, height = screen.get_size()
        screen.fill((30, 30, 30))
        title_text = font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))

        options[0] = f"Resolution: {resolutions[res_index][0]}x{resolutions[res_index][1]}"
        options[1] = f"FPS: {fps_options[fps_index]}"
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (width // 2 - option_text.get_width() // 2, 250 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", resolutions[res_index], fps_options[fps_index]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_LEFT:
                    if selected == 0:
                        res_index = (res_index - 1) % len(resolutions)
                    if selected == 1:
                        fps_index = (fps_index - 1) % len(fps_options)
                if event.key == pygame.K_RIGHT:
                    if selected == 0:
                        res_index = (res_index + 1) % len(resolutions)
                    if selected == 1:
                        fps_index = (fps_index + 1) % len(fps_options)
                if event.key == pygame.K_RETURN:
                    if selected == 2:
                        return "back", resolutions[res_index], fps_options[fps_index]

        clock.tick(60)