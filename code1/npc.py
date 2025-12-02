import pygame
from quiz import Quiz
from entity import Entity
from tool import Tool, resource_path  # 🔹 ajouter resource_path
import json
import os

class PNJ(Entity):
    def __init__(self, keylistener, screen, x, y, skin_path, banque_path):
        super().__init__(keylistener, screen, x, y)

        # Charger le sprite du PNJ avec resource_path
        self.spritesheet = pygame.image.load(resource_path(skin_path))
        self.image = Tool.split_image(self.spritesheet, 0, 0, 24, 32)
        self.all_images = self.get_all_images(self.spritesheet)

        # Charger la banque de questions spécifique avec resource_path
        with open(resource_path(banque_path), "r", encoding="utf-8") as f:
            questions = json.load(f)

        # 🔹 Extraire le nom du PNJ et du thème depuis les chemins
        nom_pnj = os.path.splitext(os.path.basename(skin_path))[0]
        nom_theme = os.path.splitext(os.path.basename(banque_path))[0]

        # 🔹 Créer le quiz avec ces informations
        self.quiz = Quiz(
            banque_questions=questions,
            nom_pnj=nom_pnj,
            nom_theme=nom_theme
        )

        self.is_talking = False
        self.can_move = False  # Le PNJ reste immobile par défaut

    def talk(self):
        """Active le dialogue ou le quiz"""
        self.is_talking = True

        # Si le quiz est fini, on le réinitialise
        if self.quiz.termine:
            self.quiz.reset()

        # 🔹 On remet toujours la phase sur "intro" pour relancer la présentation
        self.quiz.phase = "intro"
        self.quiz.ready_choice = 0

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
                all_images[key].append(
                    Tool.split_image(spritesheet, i * width, j * height, 24, 32)
                )
        return all_images
