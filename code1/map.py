import pygame
import pyscroll
import pytmx
import sys, os

from player import Player
from screen import Screen
from switch import Switch
from npc import PNJ

# -----------------------------------------------------
# FIX : Fonction pour corriger les chemins sous PyInstaller
# -----------------------------------------------------
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Chemins des sprites (corrigés)
prof_skins = [
    resource_path("assets/sprite/Adrien.png"),
    resource_path("assets/sprite/Claire Vourch.png"),
    resource_path("assets/sprite/Mahmoud HAJJ CHEHADE.png"),
    resource_path("assets/sprite/Emmanuelle Planus.png"),
    resource_path("assets/sprite/Mohamed Benharouga.png"),
]

banque_paths = [
    resource_path("assets/dialogues/les méthodes d’exploration de la cellule.json"),
    resource_path("assets/dialogues/l'organisation de la chromatine.json"),
    resource_path("assets/dialogues/la traduction, maturation des protéines.json"),
    resource_path("assets/dialogues/le cytosquelette.json"),
    resource_path("assets/dialogues/tout ce que tu peux savoir.json"),
]


class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None

        self.player = None
        self.switchs = []
        self.collisions = []

        self.current_map: Switch = Switch("switch", "house_4", pygame.Rect(0, 0, 0, 0), 0)

        self.npcs = []

        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch) -> None:

        # ----------------------------------------------------------
        # FIX : chargement correct du fichier TMX pour l'exe
        # ----------------------------------------------------------
        tmx_path = resource_path(f"assets/map/{switch.name}.tmx")

        self.tmx_data = pytmx.load_pygame(tmx_path)

        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        self.npcs = []

        if self.player:
            for obj in self.tmx_data.objects:
                if obj.name.startswith("npc"):
                    index = int(obj.name.split(" ")[-1]) - 1

                    skin = prof_skins[index]
                    banque = banque_paths[index]

                    pnj = PNJ(self.player.keylistener, self.screen, obj.x, obj.y,
                              skin_path=skin, banque_path=banque)

                    self.npcs.append(pnj)
                    self.group.add(pnj)

        if switch.name.split("_")[0] == "house":
            self.map_layer.zoom = 3
        else:
            self.map_layer.zoom = 3.75

        self.switchs = []
        self.collisions = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            if obj.name.startswith("switch"):
                self.switchs.append(Switch(
                    "switch",
                    obj.name.split(" ")[1],
                    pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    int(obj.name.split(" ")[-1])
                ))

        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.collisions)
            self.group.add(self.player)

        self.current_map = switch

    def add_player(self, player: Player) -> None:
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)

    def update(self) -> None:
        if self.player:
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None

        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

        for npc in self.npcs:
            if npc.is_talking:
                self.draw_quiz(npc.quiz)

    def draw_quiz(self, quiz):
        quiz.draw(self.screen.get_display())

    def pose_player(self, switch: Switch):
        spawn_name = f"spawn {self.current_map.name} {switch.port}"
        position = self.tmx_data.get_object_by_name(spawn_name)
        self.player.position = pygame.math.Vector2(position.x, position.y)
