"""
Hugo Pallard                                                                                                                                                                   13/05/2020
Léo Toggenburger

-------------------------------------------------------------------------------- Fruit Basket ------------------------------------------------------------------------------------------------

Vous vous trouvez dans le fichier main de notre projet.
C'est ici que le jeu est lancé, grâce à notre main_loop running contenue dans main().
Dans ce fichier se trouve également une fonction réalisant un menu d'accueil pour le jeu, game_intro()

Nous nous sommes amusés à implenter des fonctionnalités supplémentaires au niveau du GUI; comme la fonction décrite ci-dessus, ou encore une fonction pause (paused) située dans
positions.py. Le temps étant vraiment cours pour tenter de finir la partie, cette fonction était nécessaire.

Notre principe:
Nous avons créé un jeu de Basket suivant le cahier des charges. Il fonctionne par positions, au nombre de 4 qui sont regroupées par niveaux. Chaque position fait l'objet d'une fonction
différente mais fonctionnant sur le même principe. L'ajout d'un fruit est la seule différence entre les différentes fonctions.
Tous les objets graphiques (fruits, joueur...) sont gérés à l'aide de la méthode pygame.sprite.
On passe au niveau suivant lorsque la fonction Position_1 (2,3 ou 4) retourne le score nécessaire. Le passage aux différents niveaux est géré à l'aide de la fonction Niveaux().
Chaque fruit possède son propre fichier de trajectoire. Cela n'est pas très optimisé, mais seul moyen que nous avons trouvé pour attribuer les différents paramètres de chaque fruit.

Bonne partie et bon courage pour la lecture !

Cordialement.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""

import pygame
from pygame.locals import *
from positions import Position_1, Position_2, Position_3, Position_4
from datetime import datetime, date, time
from sauv import Sauvegarde

pygame.init()           # Initialisation de PyGame

width = 1080            # Initialisation des images, des différentes variables simples
height = 720
size = width, height
red = (150, 0, 0)
bright_red = (255, 0, 0)
green = (0, 150, 0)
bright_green = (0, 255, 0)
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, size)
pygame.display.set_caption("Fruit Basket")
gameDisplay = pygame.display.set_mode((1080, 720))
# # panier = pygame.image.load('Panier.png')
# panier = pygame.transform.scale(panier, (600, 725))
panier_y = 60
panier_x = 690
panier = 2

white = (255, 255, 255)
black = (0, 0, 0)
clock = pygame.time.Clock()

Chrono = datetime.combine(date.today(), time(0, 0, 55))     # Initialisation du chronomètre

music = pygame.mixer.Sound("music.wav")


def text_objects(text, font):
    """Fonction qui affiche un texte à l'écran"""
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg_button, x_button, y_button, widht_button, height_button, darkcolor, brightcolor, action=None):
    """Fonction qui gère les boutons des menus pause et game_intro"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x_button + widht_button > mouse[0] > x_button and y_button + height > mouse[1] > y_button:
        pygame.draw.rect(gameDisplay, brightcolor, (x_button, y_button, widht_button, height_button))
        if click[0] == 1 and action is not None:
            if action == "Jouer":
                main()
            elif action == "Rejouer":
                main()
            elif action == "Quitter":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, darkcolor, (x_button, y_button, widht_button, height_button))
        font_bouton1_text = pygame.font.Font("freesansbold.ttf", 20)
        bouton1_textSurf, bouton1_textRect = text_objects(msg_button, font_bouton1_text)
        bouton1_textRect.center = (x_button + (widht_button / 2)), (y_button + (height_button / 2))
        gameDisplay.blit(bouton1_textSurf, bouton1_textRect)


def game_intro():  # Fonction qui gère l'introduction à notre jeu
    """ Fonction qui créer un menu d'introduction à notre jeu"""
    intro = True

    while intro:
        for event in pygame.event.get():                                    # On parcours les évènements utilisateurs de PyGame
            if event.type == pygame.QUIT:                                   # On teste si le joueur ferme le jeu
                pygame.quit()
                quit()
        gameDisplay.fill(white)                                               # Création du menu d'introduction du jeu
        font = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Jouer à Fruit Basket ?", font)
        TextRect.center = (1080 / 2, 720 / 2)
        gameDisplay.blit(TextSurf, TextRect)

        button("Jouer", 150, 550, 150, 75, green, bright_green, "Jouer")      # On appelle la fonction button
        button("Quitter", 780, 550, 150, 75, red, bright_red, "Quitter")

        pygame.display.update()


def Niveaux(niveau1, niveau2, niveau3, Chrono, Fps_clock):
    """Fonction Niveaux qui se charge du passage au niveau suivant en fonction du score et du chrono"""
    gameDisplay.blit(background, (0, 0))
    Niveau1, Niveau2, Niveau3 = niveau1, niveau2, niveau3
    score = 0
    lim = 40

    if score <= 16:
        score, lim = Position_1(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono, Fps_clock)
    if score >= 16 and lim != 0:
        lim = int(lim)
        Chrono = datetime.combine(date.today(), time(0, 0, lim))
        score, lim = Position_2(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono, Fps_clock)
    if lim != 0:
        if score >= 32 or score >= 150:
            lim = int(lim)
            Chrono = datetime.combine(date.today(), time(0, 0, lim))
            score, lim = Position_3(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono,
                                    Fps_clock)
    if lim != 0:
        if score >= 66 or score >= 188:
            lim = int(lim)
            Chrono = datetime.combine(date.today(), time(0, 0, lim))
            score, lim = Position_4(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono,
                                    Fps_clock)

    for event in pygame.event.get():  # On parcours la liste des évènements de pygame
        if event.type == pygame.QUIT:  # Si l'evement est fermeture de fenetre
            pygame.quit()               # On quitte le jeu
            quit()
    if lim == 0:
        niveau1 = False
        niveau2 = False
        niveau3 = False
        return niveau1, niveau2, niveau3, score
    if score == 98 and lim != 0:
        niveau1 = False
        niveau2 = True
        niveau3 = False
        return niveau1, niveau2, niveau3, score
    if score == 228 and lim != 0:
        niveau1 = False
        niveau2 = False
        niveau3 = True
        return niveau1, niveau2, niveau3, score
    if score == 382 and lim != 0:
        niveau1 = False
        niveau2 = False
        niveau3 = True
        return niveau1, niveau2, niveau3, score


def main():
    """Notre fonction principale, qui assure l'exécution du jeu tant que le joueur ne quitte pas"""
    print("Lancement du jeu")
    running = True
    niveau1 = True
    niveau2 = False
    niveau3 = False
    Fps_clock = pygame.time.Clock()

    while running:

        music.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                running = False
                niveau1 = True
        if niveau1:
            niveau1, niveau2, niveau3, score = Niveaux(niveau1, niveau2, niveau3, Chrono, Fps_clock)
        if niveau2:
            niveau1, niveau2, niveau3, score = Niveaux(niveau1, niveau2, niveau3, Chrono, Fps_clock)
        if niveau3:
            niveau1, niveau2, niveau3, score = Niveaux(niveau1, niveau2, niveau3, Chrono, Fps_clock)
        else:
            music.stop()
            scoremax = Sauvegarde(score)
            background_end = pygame.image.load('bg_end.jpg')
            background_end = pygame.transform.scale(background_end, (1080, 720))
            gameDisplay.blit(background_end, (0, 0))
            font = pygame.font.Font('freesansbold.ttf', 50)
            font1 = pygame.font.Font('freesansbold.ttf', 80)

            TextSurf, TextRect = text_objects("Le score max est :", font)
            TextRect.center = (510, 720 / 4)
            gameDisplay.blit(TextSurf, TextRect)

            scoremaxSurf, scoremaxRect = text_objects(str(scoremax), font)
            scoremaxRect.center = (800, 720 / 4)
            gameDisplay.blit(scoremaxSurf, scoremaxRect)

            textSurf, textRect = text_objects("Votre score est :", font)
            textRect.center = (510, 720 / 2.5)
            gameDisplay.blit(textSurf, textRect)

            scoreSurf, scoreRect = text_objects(str(score), font)
            scoreRect.center = (750, 720 / 2.5)
            gameDisplay.blit(scoreSurf, scoreRect)

            gameoverSurf, gameoverRect = text_objects("GAME OVER", font1)
            gameoverRect.center = (1080 / 2, 50)
            gameDisplay.blit(gameoverSurf, gameoverRect)

            button("Rejouer", 150, 550, 150, 75, green, bright_green, "Rejouer")
            button("Quitter", 780, 550, 150, 75, red, bright_red, "Quitter")

            pygame.display.update()


game_intro()
