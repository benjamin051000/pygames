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
SCREENSIZE = WIDTH, HEIGHT = 640, 480

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.rect = self.surf.get_rect(
            center=(WIDTH/2, HEIGHT/2)
            # topleft=(10,10)
        )
        self.x, self.y = 6, 5  # Speed
        # Only draw the circle once
        self.surf.fill(Colors.WHITE)
        # pygame.draw.circle(self.surf, Colors.WHITE, self.rect.center, 10)

    def update(self, wall_group):
        # Check for collisions
        if pygame.sprite.spritecollideany(self, wall_group):
            self.x *= -1
        
        # Check walls
        if self.rect.top <= 0:
            self.y *= -1
        if self.rect.bottom >= HEIGHT:
            self.y *= -1

        self.rect.move_ip(self.x, self.y)

    def display(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect)
    
    # def collide(self, sprite) -> bool:
    #     """ Check if this Sprite has collided with another. """
    #     return self.rect.colliderect(sprite.rect)


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

class Wall(pygame.sprite.Sprite):
    """ A wall on the right side which will always deflect the Ball. """
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, WIDTH))
        self.surf.fill(Colors.WHITE)
        self.rect = self.surf.get_rect(center=(WIDTH - self.surf.get_width() / 2, HEIGHT / 2))

    def display(self, surf: pygame.Surface):
        surf.blit(self.surf, self.rect)


def main():

    screen = pygame.display.set_mode(SCREENSIZE)

    clock = pygame.time.Clock()

    ball = Ball()


    player1 = Paddle()
    wall = Wall()
    paddle_group = pygame.sprite.Group()
    paddle_group.add(player1, wall)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # Move the ball. Check for collisions.
        ball.update(paddle_group)

        pressed_keys = pygame.key.get_pressed()

        player1.update(pressed_keys)

        # Reset screen
        screen.fill(Colors.BLACK)

        ball.display(screen)
        player1.display(screen)
        wall.display(screen)

        pygame.display.update()

        clock.tick(60)

        


if __name__ == "__main__":
    main()