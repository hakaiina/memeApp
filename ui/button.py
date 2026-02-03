import pygame

class Button:
    def __init__(self, image, hover_image, pos, callback):
        self.image_normal = image
        self.image_hover = hover_image
        self.image = self.image_normal

        self.rect = self.image.get_rect(center=pos)
        self.callback = callback

        self.hovered = False
        self.was_hovered = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)

        self.image = self.image_hover if self.hovered else self.image_normal

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()

    def draw(self, screen):
        screen.blit(self.image, self.rect)