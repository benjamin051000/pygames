import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from colors import Colors
pygame.init()

# Constants
SCREENSIZE = WIDTH, HEIGHT = 400, 400

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(
            topleft=(10, 10)
        )
        pygame.draw.circle(self.surf, Colors.WHITE, self.rect.center, 10)
    
    def update(self):
        self.rect.move_ip(1, 1)

    def display(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect)


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, 80))
        self.surf.fill(Colors.WHITE)
        self.rect = self.surf.get_rect(center=(self.surf.get_width() / 2, HEIGHT / 2))
        self.speed = 5
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1 * self.speed)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1 * self.speed)

        # Constrain paddle to top and bottom of screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def display(self, surf: pygame.Surface):
        surf.blit(self.surf, self.rect)



def main():

    screen = pygame.display.set_mode(SCREENSIZE)

    clock = pygame.time.Clock()

    ball = Ball()

    player1 = Paddle()
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        ball.update()

        pressed_keys = pygame.key.get_pressed()

        player1.update(pressed_keys)

        # Reset screen
        screen.fill(Colors.BLACK)

        ball.display(screen)
        player1.display(screen)

        pygame.display.update()

        clock.tick(60)

        


if __name__ == "__main__":
    main()