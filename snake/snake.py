"""
snake.py

A snake clone written with pygame.
"""
import random
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
SCREENSIZE = WIDTH, HEIGHT = 800, 800
GRIDSIZE = 50  # Keep WIDTH and HEIGHT divisible by GRIDSIZE


class Snake(pygame.sprite.Sprite):
    """ Represents a Snake object. """

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((GRIDSIZE, GRIDSIZE))
        self.surf.fill(Colors.WHITE)
        self.rect = self.surf.get_rect()
        # Tail to hold coords to draw rectangles.
        self.tail = pygame.sprite.Group()
        self.last_key = None
        self.direction = (0, 0)

    def update(self, pressed_keys):
        """ Updates the sprite location based on its direction. """
        if pressed_keys[K_UP] and self.last_key != K_DOWN:
            self.direction = (0, -GRIDSIZE)
            self.last_key = K_UP
        elif pressed_keys[K_DOWN] and self.last_key != K_UP:
            self.direction = (0, GRIDSIZE)
            self.last_key = K_DOWN
        elif pressed_keys[K_LEFT] and self.last_key != K_RIGHT:
            self.direction = (-GRIDSIZE, 0)
            self.last_key = K_LEFT
        elif pressed_keys[K_RIGHT] and self.last_key != K_LEFT:
            self.direction = (GRIDSIZE, 0)
            self.last_key = K_RIGHT

        # We don't have to update every tail square. Just move the last square to the 2nd spot (right behind the head).
        sprite_list = self.tail.sprites()
        # for idx in range(len(sprite_list), 1, -1):
        #     sprite_list[idx].rect.move_ip(sprite_list[idx].rect.x, sprite_list[idx].rect.y)
            

        self.rect.move_ip(*self.direction)


    def grow(self):
        """ When the Snake eats an apple, grow in size. """
        tail = SnakeTail(self)
        self.tail.add(tail)

    def display(self, screen: pygame.Surface):
        """ Helper function to blit the entire length of the snake onto a surface. """
        # Display the head of the snake
        screen.blit(self.surf, self.rect)
        # Display each other sprite.
        for sprite in self.tail:
            screen.blit(sprite.surf, sprite.rect)

    def hit_anything(self):
        """ Checks if the Snake has hit itself. """
        # Check if out of bounds
        return any((
            self.rect.left < 0,
            self.rect.right > WIDTH,
            self.rect.top < 0,
            self.rect.bottom > HEIGHT,
            pygame.sprite.spritecollideany(self, self.tail)
        ))


class SnakeTail(pygame.sprite.Sprite):
    """ Represents a non-head portion of the Snake.
    Used in the snake.grow() function. """

    def __init__(self, head: Snake):
        super().__init__()
        self.surf = pygame.Surface((GRIDSIZE, GRIDSIZE))
        self.surf.fill(Colors.WHITE)
        self.rect = self.surf.get_rect(
            topleft=(
                head.rect.x,
                head.rect.y
            )
        )


class Food(pygame.sprite.Sprite):
    """ Represents the food object which the snake will . """

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((GRIDSIZE, GRIDSIZE))
        self.surf.fill(Colors.RED)
        cols = WIDTH // GRIDSIZE
        rows = HEIGHT // GRIDSIZE
        self.rect = self.surf.get_rect(
            topleft=(
                random.randint(0, cols-1) * GRIDSIZE,
                random.randint(0, rows-1) * GRIDSIZE
            )
        )


def main():
    """ Main game loop. """

    # Create screen
    screen = pygame.display.set_mode(SCREENSIZE)

    # Create clock
    clock = pygame.time.Clock()

    # Create snake
    snake = Snake()

    apple = Food()

    running = True
    ########## Main game loop ##########
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()

        snake.update(pressed_keys)

        # Check if the snake hit the wall or itself.
        if snake.hit_anything():
            print('You hit something. Game over!')
            running = False

        if apple.rect.colliderect(snake.rect):
            snake.grow()  # Add one to the length.
            apple = Food()  # Get new food location

        # Render surfaces
        screen.fill(Colors.BLACK)
        # screen.blit(snake.surf, snake.rect)
        snake.display(screen)
        screen.blit(apple.surf, apple.rect)
        pygame.display.update()

        clock.tick(10)


if __name__ == '__main__':
    main()
