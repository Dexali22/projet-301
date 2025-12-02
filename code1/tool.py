import pygame
import sys, os

def resource_path(relative_path: str) -> str:
    """ Retourne le bon chemin, compatible PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Tool:
    @staticmethod
    def split_image(spritesheet: pygame.Surface, x: int, y: int, witdh: int, height: int):
        return spritesheet.subsurface(pygame.Rect(x, y, witdh, height))
