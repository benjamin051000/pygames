import random
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
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
        self.surf = pygame.Surface((15, 15))
        self.rect = self.surf.get_rect(
            center=(WIDTH/2, HEIGHT/2)
            # topleft=(10,10)
        )
        self.vx = 4 * random.choice([-1, 1])
        self.vy = 3 * random.choice([-1, 1])
        # Only draw the circle once
        self.surf.fill(Colors.WHITE)
        # pygame.draw.circle(self.surf, Colors.WHITE, self.rect.center, 10)

    def update(self, wall_group):
        # Check for collisions
        if pygame.sprite.spritecollideany(self, wall_group):
            self.vx *= -1  # TODO edge case where Ball hits top/bottom of Paddle
            
        # Check walls
        if self.rect.top <= 0:
            self.vy *= -1
        if self.rect.bottom >= HEIGHT:
            self.vy *= -1

        self.rect.move_ip(self.vx, self.vy)

    def display(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_position, up_key, down_key):
        super().__init__()
        self.surf = pygame.Surface((15, 100))
        self.surf.fill(Colors.WHITE)
        self.rect = self.surf.get_rect(center=(x_position, HEIGHT / 2))
        self.speed = 5
        # Keys for Paddle movement
        self.up_key = up_key
        self.down_key = down_key

    def update(self, pressed_keys):
        """ Update Paddle location using 
        keyboard input (used for human players) """
        if pressed_keys[self.up_key]:
            self.rect.move_ip(0, -1 * self.speed)
        elif pressed_keys[self.down_key]:
            self.rect.move_ip(0, 1 * self.speed)

        # Constrain paddle to top and bottom of screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def display(self, surf: pygame.Surface):
        surf.blit(self.surf, self.rect)

class PaddleAI(Paddle):
    def __init__(self, x_position):
        super().__init__(x_position, None, None)
        self.speed = 3
        
    def update(self, pressed_keys):
        raise NotImplementedError('AI Paddles should use update_ai(), not update().')

    def update_ai(self, ball):
        """ Update the Paddle location using
        an AI algorithm (for computer players)"""
        # If the ball is below the Paddle, move it down.
        if ball.rect.center[1] > self.rect.center[1]:
            self.rect.move_ip(0, self.speed)
        
        # If the ball is above the Paddle, move it up.
        elif ball.rect.center[1] < self.rect.center[1]:
            self.rect.move_ip(0, -1 * self.speed)
        
        # If they're the same height, do nothing.

        # Constrain paddle to top and bottom of screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        

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


    player1 = Paddle(10, K_UP, K_DOWN)
    player2 = PaddleAI(WIDTH - 10)

    paddle_group = pygame.sprite.Group()
    paddle_group.add(player1, player2)

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

        # Move the Paddles
        player1.update(pressed_keys)
        player2.update_ai(ball)

        # Reset screen
        screen.fill(Colors.BLACK)

        ball.display(screen)
        player1.display(screen)
        player2.display(screen)

        pygame.display.update()

        clock.tick(60)

        


if __name__ == "__main__":
    main()
