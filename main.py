import pygame
import random
import sys

from settings import *
from snake import Snake
from food import Food


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(WIN_TITLE)
        self.font = pygame.font.SysFont("Arial", 32)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.snake_area = pygame.Surface((WIN_WIDTH, WIN_HEIGHT - 40))
        self.clock = pygame.time.Clock()
        self.foods = pygame.sprite.Group()

    def new(self):
        self.score = 0
        self.highscore = 0
        self.food_count = 0
        self.tick = 0
        self.running = True
        self.snake = Snake(self)
        self.snake.new()

    def run(self):
        while self.running:
            self.clock.tick(WIN_FPS)
            self.events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.snake.can_move_in_tick:
                    if event.key in [pygame.K_UP, pygame.K_w] and self.snake.direction.y != 1:
                        self.snake.direction.update(0, -1)
                        self.snake.can_move_in_tick = False

                    elif event.key in [pygame.K_DOWN, pygame.K_s] and self.snake.direction.y != -1:
                        self.snake.direction.update(0, 1)
                        self.snake.can_move_in_tick = False

                    elif event.key in [pygame.K_LEFT, pygame.K_a] and self.snake.direction.x != 1:
                        self.snake.direction.update(-1, 0)
                        self.snake.can_move_in_tick = False

                    elif event.key in [pygame.K_RIGHT, pygame.K_d] and self.snake.direction.x != -1:
                        self.snake.direction.update(1, 0)
                        self.snake.can_move_in_tick = False

    def update(self):
        # Reset game if snake is dead
        if not self.snake.alive:
            self.new()
            return

        # Spawn a new food if there are currently none
        if len(self.foods) < 1:
            random_x = random.randint(2, TILE_WIDTH - 2)
            random_y = random.randint(2, TILE_HEIGHT - 2)
            self.food = Food(self, random_x, random_y)

        # Limit how often the snake can move using a tick system
        if self.tick >= SNAKE_MOVE_TICK:
            self.snake.update()
            self.snake.can_move_in_tick = True
            self.tick = 0

        self.food.update()
        self.tick += 1

    def draw(self):
        self.screen.fill((32, 32, 32))
        self.snake_area.fill((0, 0, 0))

        self.food.draw(self.snake_area)
        self.snake.draw(self.snake_area)
        self.screen.blit(self.snake_area, (0, 40))
        
        # Draw score texts on screen
        score = self.font.render("Score: " + str(self.score), False, (255, 255, 255))
        lives = self.font.render("Highscore: " + str(self.highscore), False, (255, 255, 255))
        self.screen.blit(score, (12, 2))
        self.screen.blit(lives, (WIN_WIDTH - lives.get_rect().width - 12, 2))

        pygame.display.flip()
        

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
