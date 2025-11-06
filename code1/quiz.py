import pygame
import time
import random



class Quiz:
    def __init__(self):
        self.reset()

    def reset(self):
        import random
        self.banque_questions = [
            # 1-10 : Cellules et génétique
            {"q": "Quelle est l’unité de base du vivant ?", "choix": ["Cellule", "Organe", "Tissu"], "reponse": 0},
            {"q": "Où se trouve l’ADN dans une cellule eucaryote ?", "choix": ["Cytoplasme", "Noyau", "Mitochondrie"],
             "reponse": 1},
            {"q": "Quel organite produit l’énergie de la cellule ?", "choix": ["Lysosome", "Mitochondrie", "Ribosome"],
             "reponse": 1},
            {"q": "Quelle molécule porte l’information génétique ?", "choix": ["ARN", "Protéine", "ADN"], "reponse": 2},
            {"q": "Comment s’appelle la division cellulaire qui produit 2 cellules identiques ?",
             "choix": ["Méiose", "Mitose", "Fission"], "reponse": 1},
            {"q": "Quel organite synthétise les protéines ?", "choix": ["Ribosome", "Mitochondrie", "Noyau"],
             "reponse": 0},
            {"q": "Comment s’appellent les filaments qui forment le squelette de la cellule ?",
             "choix": ["Microtubules", "Chromosomes", "Ribosomes"], "reponse": 0},
            {"q": "Quel type de cellule possède un noyau ?", "choix": ["Procaryote", "Eucaryote", "Virus"],
             "reponse": 1},
            {"q": "Quel est le rôle des lysosomes ?",
             "choix": ["Digérer les déchets", "Produire l’ATP", "Synthétiser les protéines"], "reponse": 0},
            {"q": "Quelle structure protège le noyau ?",
             "choix": ["Membrane plasmique", "Membrane nucléaire", "Paroi cellulaire"], "reponse": 1},

            # 11-20 : Anatomie humaine
            {"q": "Quel organe pompe le sang ?", "choix": ["Foie", "Cœur", "Poumon"], "reponse": 1},
            {"q": "Où se situe le diaphragme ?",
             "choix": ["Entre le thorax et l’abdomen", "Entre le cœur et les poumons", "Dans la tête"], "reponse": 0},
            {"q": "Combien d’os possède un adulte ?", "choix": ["206", "205", "210"], "reponse": 0},
            {"q": "Quelle cellule transporte l’oxygène ?", "choix": ["Globule blanc", "Globule rouge", "Plaquette"],
             "reponse": 1},
            {"q": "Quel organe filtre le sang ?", "choix": ["Rein", "Foie", "Estomac"], "reponse": 0},
            {"q": "Quel muscle permet la respiration ?", "choix": ["Biceps", "Diaphragme", "Quadriceps"], "reponse": 1},
            {"q": "Quel organe stocke la bile ?", "choix": ["Foie", "Vésicule biliaire", "Estomac"], "reponse": 1},
            {"q": "Quel système contrôle les hormones ?", "choix": ["Nerveux", "Endocrinien", "Digestif"],
             "reponse": 1},
            {"q": "Où se trouve la moelle épinière ?", "choix": ["Cerveau", "Colonne vertébrale", "Cœur"],
             "reponse": 1},
            {"q": "Quel organe élimine les déchets azotés ?", "choix": ["Reins", "Foie", "Poumons"], "reponse": 0},

            # 21-30 : Écologie et évolution
            {"q": "Qui produit de l’oxygène ?", "choix": ["Plantes", "Champignons", "Bactéries"], "reponse": 0},
            {"q": "Quel gaz est responsable de l’effet de serre ?", "choix": ["Oxygène", "Dioxyde de carbone", "Azote"],
             "reponse": 1},
            {"q": "Comment s’appelle le processus d’adaptation au milieu ?",
             "choix": ["Évolution", "Photosynthèse", "Respiration"], "reponse": 0},
            {"q": "Qu’est-ce qu’un écosystème ?",
             "choix": ["Ensemble d’êtres vivants et leur milieu", "Une seule espèce", "Un continent"], "reponse": 0},
            {"q": "Quel rôle ont les producteurs primaires ?",
             "choix": ["Fabriquer la matière organique", "Décomposer", "Prédater"], "reponse": 0},
            {"q": "Qu’est-ce qu’une espèce ?",
             "choix": ["Ensemble d’individus capables de se reproduire", "Une population d’animaux", "Un gène"],
             "reponse": 0},
            {"q": "Comment s’appelle la sélection naturelle ?",
             "choix": ["Survie du plus faible", "Survie du plus apte", "Mutation aléatoire"], "reponse": 1},
            {"q": "Qu’est-ce qu’un biome ?",
             "choix": ["Grand type de milieu avec sa faune et sa flore", "Un organe animal", "Une cellule"],
             "reponse": 0},
            {"q": "Qui décompose la matière morte ?", "choix": ["Prédateurs", "Décomposeurs", "Producteurs"],
             "reponse": 1},
            {"q": "Quel est l’effet des polluants sur un écosystème ?",
             "choix": ["Aucun", "Déséquilibre écologique", "Amélioration"], "reponse": 1},

            # 31-40 : Divers biologiques
            {"q": "Quel est le plus grand organe du corps humain ?", "choix": ["Cœur", "Peau", "Foie"], "reponse": 1},
            {"q": "Quel élément est essentiel à la photosynthèse ?", "choix": ["CO2", "O2", "Azote"], "reponse": 0},
            {"q": "Quel sucre est produit par la photosynthèse ?", "choix": ["Glucose", "Fructose", "Saccharose"],
             "reponse": 0},
            {"q": "Quel est le rôle des chloroplastes ?", "choix": ["Stocker l’eau", "Photosynthèse", "Respiration"],
             "reponse": 1},
            {"q": "Quel type de reproduction produit des clones ?", "choix": ["Sexuée", "Asexuée", "Méiose"],
             "reponse": 1},
            {"q": "Comment s’appelle la transformation d’une larve en adulte ?",
             "choix": ["Métamorphose", "Division cellulaire", "Évolution"], "reponse": 0},
            {"q": "Qu’est-ce que l’ADN code ?", "choix": ["Protéines", "Glucides", "Lipides"], "reponse": 0},
            {"q": "Quel est le rôle des globules blancs ?",
             "choix": ["Transporter l’oxygène", "Défendre l’organisme", "Coaguler le sang"], "reponse": 1},
            {"q": "Quel organite contient de l’ADN mitochondrial ?", "choix": ["Noyau", "Mitochondrie", "Ribosome"],
             "reponse": 1},
            {"q": "Quel est le rôle des stomates chez les plantes ?",
             "choix": ["Échanger les gaz", "Stocker l’eau", "Produire des fleurs"], "reponse": 0},

            {"q": "Quel organite contient de l’ADN mitochondrial ?",
             "choix": ["Noyau", "Mitochondrie", "Ribosome"],
             "reponse": 1},

            {"q": "Quel est ce processus représenté ?",
             "choix": ["Réplication de l’ADN", "Transcription", "Traduction"],
             "reponse": 0,
             "image": "../assets/image/transcription.webp"},  # chemin vers ton image

            {"q": "Où se déroule la traduction ?",
             "choix": ["Ribosome", "Noyau", "Mitochondrie"],
             "reponse": 0}


        ]
        self.questions = random.sample(self.banque_questions, min(20, len(self.banque_questions)))
        self.index = 0
        self.selection = 0
        self.score = 0
        self.termine = False
        self.end_time = None  # ⚠️ temps où le quiz s’est terminé

    def update(self, events):
        if self.termine:
            # Vérifie si 15s sont écoulées
            if self.end_time and (time.time() - self.end_time >= 15):
                self.reset()
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selection = (self.selection - 1) % len(self.questions[self.index]["choix"])
                elif event.key == pygame.K_DOWN:
                    self.selection = (self.selection + 1) % len(self.questions[self.index]["choix"])
                elif event.key == pygame.K_RETURN:
                    if self.selection == self.questions[self.index]["reponse"]:
                        self.score += 1
                    self.index += 1
                    self.selection = 0

                    if self.index >= len(self.questions):
                        self.termine = True
                        self.end_time = time.time()  # ⚠️ démarre le chrono
