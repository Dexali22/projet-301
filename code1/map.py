import pygame
import pyscroll
import pytmx

from player import Player
from screen import Screen
from switch import Switch
from npc import PNJ

# Chemins des sprites
prof_skins = [
    "../assets/sprite/professor1.png",
    "../assets/sprite/professor2.png",
    "../assets/sprite/professor3.png",
    "../assets/sprite/professor4.png"
]

class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        self.player: Player | None = None
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None

        self.current_map: Switch = Switch("switch", "map_0", pygame.Rect(0, 0, 0, 0), 0)

        self.switch_map(self.current_map)
        self.npcs: list[PNJ] = []  # PNJ de la map
        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.load_pygame(f"../assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)
        self.npcs = []
        for obj in self.tmx_data.objects:
            if obj.name.startswith("npc"):  # par exemple "npc 1", "npc 2"…
                # Déterminer quel professeur / quiz selon le nom
                index = int(obj.name.split(" ")[-1]) - 1  # npc 1 -> index 0
                skin_path = prof_skins[index]  # liste des sprites
                pnj = PNJ(self.player.keylistener, self.screen, obj.x, obj.y, skin_path=skin_path)
                self.npcs.append(pnj)
                self.group.add(pnj)

        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 3
        else:
            self.map_layer.zoom = 3.75

        self.switchs = []
        self.collisions = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            type = obj.name.split(" ")[0]
            if type == "switch":
                self.switchs.append(Switch(
                    type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height),
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

    def add_player(self, player) -> None:
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
        display = self.screen.get_display()
        font = pygame.font.SysFont("Arial", 28)

        # Définir la position et taille de la boîte
        box_width, box_height = 800, 400
        box_x = (display.get_width() - box_width) // 2
        box_y = display.get_height() - box_height - 30
        padding = 10


        # Dessiner le rectangle semi-transparent
        s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        s.fill((30, 30, 30, 220))  # gris foncé transparent
        display.blit(s, (box_x, box_y))

        # Ajouter le contour blanc
        pygame.draw.rect(display, (255, 255, 255),
                         (box_x, box_y, box_width, box_height), width=4, border_radius=20)

        if not quiz.termine:
            q = quiz.questions[quiz.index]
            # Afficher la question
            texte_q = font.render(q["q"], True, (255, 255, 0))
            display.blit(texte_q, (box_x + padding, box_y + padding))
            if "image" in q:
                img = pygame.image.load(q["image"]).convert_alpha()
                img = pygame.transform.scale(img, (350, 250))  # image plus large
                # Centrage de l’image à droite
                img_x = box_x + box_width - 370
                img_y = box_y + (box_height - 250) // 2
                display.blit(img, (img_x, img_y))

            # Afficher les choix
            for i, opt in enumerate(q["choix"]):
                color = (0, 255, 0) if i == quiz.selection else (255, 255, 255)
                display.blit(font.render(opt, True, color), (box_x + 2 * padding, box_y + 60 + i * 40))
        else:
            note = round((quiz.score / len(quiz.questions)) * 20, 2)
            display.blit(font.render(f"Quiz terminé ! Note : {note}/20", True, (255, 255, 0)),
                         (box_x + padding, box_y + padding))
            display.blit(font.render("Le quiz redémarrera dans 15 secondes...", True, (255, 255, 255)),
                         (box_x + padding, box_y + 60))

    def pose_player(self, switch: Switch):
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)
