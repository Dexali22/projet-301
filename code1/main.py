import pygame
from game import Game
from tool import resource_path

pygame.init()

if __name__ == "__main__":
    game: Game = Game()
    game.run()
