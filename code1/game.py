import pygame
import os
import sys

from keylistener import KeyListener
from map import Map
from player import Player
from screen import Screen


def resource_path(relative_path: str) -> str:
    """
    Chemin compatible PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Game:
    def __init__(self):
        self.running: bool = True
        self.screen: Screen = Screen()
        self.map: Map = Map(self.screen)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.keylistener, self.screen, 408, 550)

        # Ajouter le joueur à la map
        self.map.add_player(self.player)

    def run(self) -> None:
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()

    def handle_input(self) -> None:
        events = pygame.event.get()
        for event in events:

            # Fermeture de la fenêtre
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False

            # Touche enfoncée
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)

                # 👉 Interaction (touche E)
                if event.key == pygame.K_e:
                    for npc in self.map.npcs:
                        if self.player.rect.colliderect(npc.rect):
                            npc.talk()

            # Touche relâchée
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)

        # 👉 transmettre les events au quiz si un PNJ parle
        for npc in self.map.npcs:
            if npc.is_talking:
                npc.quiz.update(events)
