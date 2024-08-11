import pygame

from settings import *


class Food(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self.groups = (game.foods)
        self.position = pygame.math.Vector2(x, y)
        pygame.sprite.Sprite.__init__(self, self.groups)

    def destroy(self):
        self.kill()
        del self

    def draw(self, screen):
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         ((self.position.x - 1) * TILE_SIZE,
                          (self.position.y - 1) * TILE_SIZE,
                          TILE_SIZE,
                          TILE_SIZE))
