import pygame
import random
import colorsys

from settings import *


class Snake(pygame.sprite.Sprite):

    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

    def new(self):
        self.can_move_in_tick = True
        self.alive = True
        self.length = SNAKE_LENGTH_STARTING
        # Randomise the snake's starting direction
        start_direction = random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))
        self.direction = pygame.math.Vector2(start_direction)
        # Start the snake in the middle of the screen
        start_position = (TILE_WIDTH // 2, TILE_HEIGHT // 2)
        self.parts = [pygame.math.Vector2(start_position)]

    def update(self):
        # Calculate next snake-head position
        next_x = self.parts[0].x + self.direction.x
        next_y = self.parts[0].y + self.direction.y

        # Add segments to the snake as it gets longer
        self.parts.insert(0, pygame.math.Vector2(next_x, next_y))
        if len(self.parts) > self.length:
            self.parts.pop()
        
        head = self.parts[0]
        # Check if the snake goes outside of the screen
        if head.x not in range(1, TILE_WIDTH) or head.y not in range(1, TILE_HEIGHT):
            self.alive = False

        # Check if the snake collides with itself
        elif head in self.parts[1:-1]:
            self.alive = False

        # Check for the snake eating food
        elif self.parts[0] == self.game.food.position:
            self.game.food.destroy()
            self.length += SNAKE_LENGTH_INCREMENT
            self.game.score += SNAKE_SCORE_INCREMENT
            self.game.highscore = max(self.game.score, self.game.highscore)

    def draw(self, screen):
        for i, part in enumerate(self.parts):
            # Calculate the rainbow colour for this part of the snake
            rgb = colorsys.hsv_to_rgb(i / len(self.parts) * 0.9, 1, 1)
            colour = tuple(round(i * 255) for i in rgb)
            pygame.draw.rect(screen,
                             colour,
                             ((part.x - 1) * TILE_SIZE,
                              (part.y - 1) * TILE_SIZE,
                              TILE_SIZE,
                              TILE_SIZE))
