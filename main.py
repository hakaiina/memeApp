import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from screens.main_screen import MainScreen
from db.database import init_db, seed_test_data



def main():
    init_db()

    seed_test_data()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Мемография: ГИА по мемам")

    clock = pygame.time.Clock()
    current_screen = MainScreen(screen)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            current_screen.handle_event(event)

        current_screen.update()
        current_screen.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()