import pygame
from quiz import Quiz
from entity import Entity
from tool import Tool

class PNJ(Entity):
    def __init__(self, keylistener, screen, x, y, skin_path):
        super().__init__(keylistener, screen, x, y)

        # Charger le sprite du PNJ (différent du joueur)
        self.spritesheet = pygame.image.load(skin_path)
        self.image = Tool.split_image(self.spritesheet, 0, 0, 24, 32)
        self.all_images = self.get_all_images(self.spritesheet)

        self.quiz = Quiz()          # Quiz intégré
        self.is_talking = False     # Indique si le PNJ parle

        self.can_move = False       # Le PNJ reste sur place par défaut

    def talk(self):
        """Active le dialogue ou le quiz"""
        self.is_talking = True
        # Reset le quiz si déjà terminé
        if self.quiz.termine:
            self.quiz.reset()

    def stop_talk(self):
        """Désactive le dialogue/quiz"""
        self.is_talking = False

    def update(self):
        """Met à jour l’animation même si le PNJ est immobile"""
        self.animation_sprite()
        self.rect.center = self.position
        self.image = self.all_images[self.direction][self.index_image]

    def get_all_images(self, spritesheet):
        """Découpe le spritesheet en toutes les images pour animation"""
        all_images = {"down": [], "left": [], "right": [], "up": []}
        width = spritesheet.get_width() // 4
        height = spritesheet.get_height() // 4

        for i in range(4):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(spritesheet, i * width, j * height, 24, 32))
        return all_images
