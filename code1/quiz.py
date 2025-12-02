import pygame
import time
import random
from tool import Tool, resource_path  # ✔ resource_path ajouté

class Quiz:
    def __init__(self, banque_questions=None, nom_pnj="Professeur", nom_theme="général"):
        self.banque_questions = banque_questions
        self.nom_pnj = nom_pnj
        self.nom_theme = nom_theme
        self.reset()

    def reset(self):
        """Réinitialise le quiz et la phase d’intro."""
        if self.banque_questions is None:
            self.banque_questions = [
                {"q": "Quelle est l’unité de base du vivant ?", "choix": ["Cellule", "Organe", "Tissu"], "reponse": 0},
                {"q": "Où se trouve l’ADN dans une cellule eucaryote ?", "choix": ["Cytoplasme", "Noyau", "Mitochondrie"], "reponse": 1},
            ]

        self.questions = random.sample(self.banque_questions, min(20, len(self.banque_questions)))
        self.index = 0
        self.selection = 0
        self.score = 0
        self.termine = False
        self.end_time = None

        self.phase = "intro"  # "intro" ou "quiz"
        self.ready_choice = 0  # 0 = Oui, 1 = Non
        self.closed_by_user = False

        # Charger les images si elles existent
        for q in self.questions:
            if "image" in q:
                try:
                    q["img_surface"] = pygame.image.load(resource_path(q["image"])).convert_alpha()
                except:
                    q["img_surface"] = None
            else:
                q["img_surface"] = None

    def update(self, events):
        """Met à jour le quiz selon les événements."""
        # Gestion de la fin du quiz
        if self.termine and not self.closed_by_user:
            if self.end_time is None:
                self.end_time = time.time()
            elif time.time() - self.end_time >= 5:
                self.reset()
            return

        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.termine = True
                self.closed_by_user = True
                self.end_time = None
                return

            # Phase d'introduction
            if self.phase == "intro":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.ready_choice = max(0, self.ready_choice - 1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.ready_choice = min(1, self.ready_choice + 1)
                elif event.key == pygame.K_RETURN:
                    if self.ready_choice == 0:
                        self.phase = "quiz"
                    else:
                        self.termine = True
                        self.closed_by_user = True
                        self.end_time = None
                continue

            # Phase quiz
            if self.phase == "quiz":
                if self.index >= len(self.questions):
                    self.termine = True
                    if self.end_time is None:
                        self.end_time = time.time()
                    return

                q = self.questions[self.index]
                if event.key == pygame.K_UP:
                    self.selection = (self.selection - 1) % len(q["choix"])
                elif event.key == pygame.K_DOWN:
                    self.selection = (self.selection + 1) % len(q["choix"])
                elif event.key == pygame.K_RETURN:
                    if self.selection == q["reponse"]:
                        self.score += 1
                    self.index += 1
                    self.selection = 0
                    if self.index >= len(self.questions):
                        self.termine = True
                        if self.end_time is None:
                            self.end_time = time.time()

    def draw(self, display):
        """Dessine le quiz à l'écran."""
        if self.termine and self.closed_by_user:
            return

        font_title = pygame.font.SysFont("Arial", 20, bold=True)
        font_choice = pygame.font.SysFont("Arial", 16)

        box_width, box_height = 900, 500
        box_x = (display.get_width() - box_width) // 2
        box_y = display.get_height() - box_height - 40
        padding = 20

        # Fond dégradé
        s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        for i in range(box_height):
            alpha = 180 + int(75 * (i / box_height))
            pygame.draw.line(s, (40, 40, 60, alpha), (0, i), (box_width, i))
        display.blit(s, (box_x, box_y))

        # Ombre et bordure
        shadow = pygame.Surface((box_width + 10, box_height + 10), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        display.blit(shadow, (box_x + 5, box_y + 5))
        pygame.draw.rect(display, (255, 255, 255), (box_x, box_y, box_width, box_height), width=4, border_radius=25)

        # Phase introduction
        if self.phase == "intro":
            intro_text = f"Bonjour je suis {self.nom_pnj} et je vais te poser des questions sur {self.nom_theme}."
            prompt_text = "Es-tu prêt ?"

            def wrap_text(text, font, max_width):
                words = text.split(" ")
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if font.size(test_line)[0] <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                return lines

            intro_lines = wrap_text(intro_text, font_title, box_width - 2*padding)
            prompt_lines = wrap_text(prompt_text, font_title, box_width - 2*padding)

            total_lines = len(intro_lines) + len(prompt_lines) + 1
            start_y = box_y + (box_height - total_lines * font_title.get_linesize()) // 2

            for i, line in enumerate(intro_lines):
                line_surface = font_title.render(line, True, (255, 255, 0))
                line_rect = line_surface.get_rect(center=(box_x + box_width // 2, start_y + i*font_title.get_linesize()))
                display.blit(line_surface, line_rect)

            for i, line in enumerate(prompt_lines):
                line_surface = font_title.render(line, True, (255, 255, 0))
                line_rect = line_surface.get_rect(center=(box_x + box_width//2,
                                                          start_y + (len(intro_lines)+i)*font_title.get_linesize() + font_title.get_linesize()))
                display.blit(line_surface, line_rect)

            yes_color = (100, 180, 255) if self.ready_choice == 0 else (60, 60, 80)
            no_color = (100, 180, 255) if self.ready_choice == 1 else (60, 60, 80)
            total_button_width = 220
            start_x = box_x + (box_width - total_button_width)//2
            button_y = start_y + total_lines*font_title.get_linesize() + 10

            yes_rect = pygame.Rect(start_x, button_y, 100, 40)
            no_rect = pygame.Rect(start_x + 120, button_y, 100, 40)

            pygame.draw.rect(display, yes_color, yes_rect, border_radius=12)
            pygame.draw.rect(display, no_color, no_rect, border_radius=12)
            display.blit(font_choice.render("Oui", True, (255,255,255)),
                         font_choice.render("Oui", True, (255,255,255)).get_rect(center=yes_rect.center))
            display.blit(font_choice.render("Non", True, (255,255,255)),
                         font_choice.render("Non", True, (255,255,255)).get_rect(center=no_rect.center))

        # Phase quiz
        elif self.phase == "quiz" and self.index < len(self.questions):
            q = self.questions[self.index]

            # Question
            words = q["q"].split(" ")
            lines, current_line = [], ""
            max_width = box_width - 2*padding
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if font_title.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            y_offset = box_y + padding
            for line in lines:
                display.blit(font_title.render(line, True, (255,255,0)), (box_x + padding, y_offset))
                y_offset += font_title.get_linesize() + 5
            y_offset += 10

            # Choix
            for i, opt in enumerate(q["choix"]):
                words = opt.split(" ")
                text_lines, current_line = [], ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if font_choice.size(test_line)[0] <= max_width - 20:
                        current_line = test_line
                    else:
                        text_lines.append(current_line)
                        current_line = word
                if current_line:
                    text_lines.append(current_line)

                total_height = len(text_lines)*font_choice.get_linesize() + 20
                choice_rect = pygame.Rect(box_x + padding, y_offset, max_width, total_height)
                color = (100, 180, 255) if i == self.selection else (60, 60, 80)
                pygame.draw.rect(display, color, choice_rect, border_radius=12)

                for j, line in enumerate(text_lines):
                    line_surf = font_choice.render(line, True, (255,255,255))
                    line_rect = line_surf.get_rect(center=(choice_rect.centerx, choice_rect.y + 10 + j*font_choice.get_linesize()))
                    display.blit(line_surf, line_rect)

                y_offset += total_height + 10

            # Image si présente
            if q.get("img_surface"):
                img = q["img_surface"]
                max_img_width = max_width
                max_img_height = box_y + box_height - y_offset - padding
                scale = min(max_img_width/img.get_width(), max_img_height/img.get_height(), 1)
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                img_x = box_x + (box_width - img.get_width())//2
                img_y = y_offset
                display.blit(img, (img_x, img_y))

        # Fin
        if self.termine:
            note = round((self.score / len(self.questions))*20, 2)
            display.blit(font_title.render(f"Quiz terminé ! Note : {note}/20", True, (255,255,0)),
                         (box_x + padding, box_y + padding))
            if not self.closed_by_user:
                display.blit(font_choice.render("Le quiz redémarrera dans 5 secondes...", True, (255,255,255)),
                             (box_x + padding, box_y + 80))
