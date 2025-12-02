import pygame
from keylistener import KeyListener
from map import Map
from player import Player
from screen import Screen


class Game:
    def __init__(self):
        self.running: bool = True
        self.screen: Screen = Screen()
        self.map: Map = Map(self.screen)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.keylistener, self.screen, 408, 550)
        self.map.add_player(self.player)

    def run(self) -> None:
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()

    def handle_input(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)

                # 👉 Appui sur E = interaction
                if event.key == pygame.K_e:
                    for npc in self.map.npcs:
                        # Vérifie si le joueur touche le PNJ
                        if self.player.rect.colliderect(npc.rect):
                            npc.talk()

            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)

        # ⚠️ important : transmettre les events au quiz si un PNJ parle
        for npc in self.map.npcs:
            if npc.is_talking:
                npc.quiz.update(events)
