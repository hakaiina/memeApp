import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from screens.main_screen import MainScreen
from db.database import Database
from screens.quiz_screen import QuizScreen
from screens.registr_screen import RegisterScreen


def main():
    db = Database()
    db.init_db()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Мемография: ГИА по мемам")

    clock = pygame.time.Clock()

    # switch screens
    current_screen = None

    def screen_switch(new_screen):
        nonlocal current_screen
        current_screen = new_screen

    # current_screen = RegisterScreen(screen, db, screen_switch)
    current_screen = QuizScreen(screen, db, screen_switch, "name")

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

    db.close()
    pygame.quit()

if __name__ == "__main__":
    main()