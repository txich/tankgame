import pygame
from settings import SCREEN_WIDTH

def show_menu(screen):
    font = pygame.font.SysFont("arial", 50)
    title_text = font.render("TANK GAME", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (200, 200, 200))

    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

        clock.tick(60)