"""
Hugo Pallard                                                                                                                                                                   13/05/2020
Léo Toggenburger

-------------------------------------------------------------------------------- Fruit Basket ------------------------------------------------------------------------------------------------

Bonjour,

Vous vous trouvez dans le fichier positions.py de notre projet.
C'est ici que se déroule le gros de notre projet. Ici on gère le score et son affichage, les fonctions pause() et unpause(), et le plus important les fonctions Position_x()
Nous avons choisi de faire une fonction par position, bien que celle ci se ressemblent beaucoup.
Les fonctions Position_x() gèrent l'affichage des fruits à l'instant t, les évènements de l'utilisateur, le déplacement des fruits, l'affichage et calcul de la trajectoire...

Ces fonctions ayant des points commun, nous avons décidé de commenter uniquement la fonction Position_1() car les suivantes fonctionnent sur le même principe.


Cordialement.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""

import pygame
from trajcitron import Trajcitron
from trajframb import Trajframb
from trajmelon import Trajmelon
from trajananas import Trajananas
from trajbanane import Trajbanane
from trajpomme import Trajpomme
from trajfraise import Trajfraise
from trajkiwi import Trajkiwi

import math as M

from player import Player

from datetime import timedelta
from datetime import datetime, date, time

position1 = True
score = 0
position2 = True
position3 = True
position4 = True
lancer_citron_possiblePos1 = True
lancer_framb_possiblePos1 = True
lancer_melon_possiblePos1 = True
white = (255, 255, 255)
red = (150, 0, 0)
bright_red = (255, 0, 0)
green = (0, 150, 0)
bright_green = (0, 255, 0)
black = (0, 0, 0)
gameDisplay = pygame.display.set_mode((1080, 720))
height = 720
pause = False


def Score(score):
    """ Fonction qui gère l'affichage du score, pris en argument"""

    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Score  " + str(score), True, black)
    gameDisplay.blit(text, (0, 0))


def Affichage(lim):
    """Fonction qui affiche le chronomètre, le temps restant"""
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Time  " + str(lim), True, black)
    gameDisplay.blit(text, (900, 0))


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
        if click[0] == 1 and action != None:
            if action == "Quitter":
                pygame.quit()
                quit()
            if action == "Continue":
                unpaused()
    else:
        pygame.draw.rect(gameDisplay, darkcolor, (x_button, y_button, widht_button, height_button))
        font_bouton1_text = pygame.font.Font("freesansbold.ttf", 20)
        bouton1_textSurf, bouton1_textRect = text_objects(msg_button, font_bouton1_text)
        bouton1_textRect.center = (x_button + (widht_button / 2)), (y_button + (height_button / 2))
        gameDisplay.blit(bouton1_textSurf, bouton1_textRect)


def paused(Fps_clock, background_pause):
    """Fonction qui créer le menu pause"""
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(background_pause, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Pause", font)
        TextRect.center = (1080 / 2, 720 / 3)
        gameDisplay.blit(TextSurf, TextRect)
        button("Continue", 150, 550, 150, 75, green, bright_green, "Continue")
        button("Quitter", 780, 550, 150, 75, red, bright_red, "Quitter")
        pygame.display.update()

        Fps_clock = pygame.time.Clock()

    return Fps_clock


def unpaused():
    """Fonction qui relance le jeu"""
    global pause
    pause = False


# def AffichagePanier(background, panier, panier_x, panier_y):
#     """Fonction pour afficher le panier de basket"""
#     background.blit(panier, (panier_x, panier_y))


def AffichageBackground(gameDisplay, background):
    """Fonction pour afficher l'arrière plan"""
    gameDisplay.blit(background, (0, 0))


def Position_1(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono, Fps_clock):
    """Fonction Position_x qui gère le déplacement des fruits, les évènements de l'utilisateur et le dessin / calcul des conditions initiales de la trajectoire"""
    global pause, X, Y, angle, trajectoire, V0
    global position1

    niveau1 = Niveau1
    niveau2 = Niveau2
    niveau3 = Niveau3

    if niveau1:
        scoremax = 16
        score = 0
    if niveau2:
        scoremax = 122
        score = 98
    if niveau3:
        scoremax = 258
        score = 228

    black = (0, 0, 0)

    lancer_citron_possible = True
    lancer_framb_possible = False
    lancer_melon_possible = False
    lancer_fraise_possible = False
    lancer_kiwi_possible = False

    player = Player()
    player.move_Position_1()

    background = pygame.image.load('bg.jpg')
    background = pygame.transform.scale(background, (1080, 720))
    background_pause = pygame.image.load('bg_pause.jpg')
    background_pause = pygame.transform.scale(background_pause, (1080, 720))
    # background.blit(panier, (panier_x, panier_y))
    # background.blit(panier, (panier_x, panier_y))  # Appliquer l'image du panier de basket

    trajcitron = Trajcitron(player)
    trajframb = Trajframb(player)
    trajmelon = Trajmelon(player)
    trajfraise = Trajfraise(player)
    trajkiwi = Trajkiwi(player)

    i = 1
    espace = False

    while position1 is True and score <= scoremax:
        player.move_Position_1()

        # background.blit(panier, (panier_x, panier_y))
        background.blit(player.image, player.rect)  # Appliquer l'image du joueur
        AffichageBackground(gameDisplay, background)  # On applique l'arrière plan
        # AffichagePanier(background, panier, panier_x, panier_y)
        player.citron.draw(gameDisplay)
        player.framb.draw(gameDisplay)  # Appliquer l'ensemble des framboises lancés
        player.melon.draw(gameDisplay)  # Appliquer l'ensemble des melons lancés
        player.fraise.draw(gameDisplay)
        player.kiwi.draw(gameDisplay)

        Score(score)  # Appel de la fonction Score()

        chrono = Chrono
        fps_clock = Fps_clock
        dt = fps_clock.tick(120)
        chrono -= timedelta(milliseconds=dt)
        time = chrono.strftime("%S")
        lim = int(time)
        if lim == 0:
            return score, lim

        Chrono = chrono

        Affichage(lim)

        for trajcitron in player.citron:  # Parcours des instances de la classe trajcitron contenue dans le groupe de sprite player.citron
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_citron_possible = trajcitron.move_citron(x, y, i)  # Déplacement du citron

            if trajcitron.panier_citron(
                    angle) and angle > 50:  # On teste s'il y a eu un panier, et avec un angle suffisant (le panier ne doit pas être marqué d'en dessous)

                lancer_citron_possible = False  # Dans ce cas, on empêche le joueur de lancer un nouveau citron
                player.citron.empty()  # On vide le groupe de sprite player.citron
                score += 3  # On ajoute le score correspondant au panier

                lancer_framb_possible = True  # On permet le lancer du fruit suivant
                trajectoire = False

        if espace and i < 499:  # Ici, on parcours le tableau contenant les coordonées du calcul de la trajectoire
            i += 1

        for trajframb in player.framb:  # Cette boucle for marche du même principe que la précédente
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_framb_possible = trajframb.move_framb(x, y, i)
            if trajframb.panier_framb(angle):
                lancer_framb_possible = False
                player.framb.empty()
                score += 4
                lancer_melon_possible = True
                trajectoire = False

        for trajmelon in player.melon:  # Cette boucle for marche du même principe que la précédente
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_melon_possible = trajmelon.move_melon(x, y, i)

            if trajmelon.panier_melon(angle):
                lancer_melon_possible = False
                if niveau2 or niveau3:
                    lancer_fraise_possible = True
                player.melon.empty()
                score += 9

        for trajfraise in player.fraise:  # Cette boucle for marche du même principe que la précédente
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_fraise_possible = trajfraise.move_fraise(x, y, i)

            if trajfraise.panier_fraise(angle):
                lancer_fraise_possible = False
                if niveau3:
                    lancer_kiwi_possible = True
                player.fraise.empty()
                score += 8

        for trajkiwi in player.kiwi:  # Cette boucle for marche du même principe que la précédente
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_kiwi_possible = trajkiwi.move_kiwi(x, y, i)

            if trajkiwi.panier_kiwi(angle):
                lancer_kiwi_possible = False
                player.kiwi.empty()
                score += 6

        for event in pygame.event.get():  # On parcours la liste des évènements de pygame
            if event.type == pygame.QUIT:  # Si l'evement est fermeture de fenetre
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and lancer_citron_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement du citron
                    player.ajout_citron()  # On ajoute le fruit créé au groupe de sprite player.citron
                    X, Y = trajcitron.traj(angle, V0)  # LEO COMMENTE ICI
                    i = 1
                    espace = True
                    lancer_citron_possible = False  # On empêche le joueur de lancer un citron tant qu'un citron est lancé

                if event.key == pygame.K_SPACE and lancer_framb_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement de la framboise
                    player.ajout_framb()
                    X, Y = trajframb.traj(angle, V0)
                    i = 1
                    lancer_framb_possible = False
                if event.key == pygame.K_SPACE and lancer_melon_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement du melon
                    player.ajout_melon()
                    X, Y = trajmelon.traj(angle, V0)
                    i = 1
                    lancer_melon_possible = False
                if event.key == pygame.K_SPACE and lancer_fraise_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement de la fraise
                    player.ajout_fraise()
                    X, Y = trajfraise.traj(angle, V0)
                    i = 1
                    lancer_fraise_possible = False
                if event.key == pygame.K_SPACE and lancer_kiwi_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement du kiwi
                    player.ajout_kiwi()
                    X, Y = trajkiwi.traj(angle, V0)
                    i = 1
                    lancer_kiwi_possible = False

                if event.key == pygame.K_ESCAPE:  # Lorsque la touche ESCAPE, on met le jeu en pause
                    pause = True
                    Fps_clock = paused(Fps_clock, background_pause)



            elif event.type == pygame.MOUSEBUTTONDOWN:  # Lorsque le joueur clique avec sa souris, on...

                background = pygame.image.load('bg.jpg')  # Actualise les images du jeu
                background = pygame.transform.scale(background, (1080, 720))
                AffichageBackground(gameDisplay, background)
                background.blit(player.image, player.rect)
                # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

                mx, my = pygame.mouse.get_pos()  # Récupère les coordonnées du clique
                tailleTraj = (M.sqrt((mx - (player.rect.x + 195)) ** 2 + (my - (
                            player.rect.y + 80)) ** 2) * 0.3)  # On calcule la taille du segment créé plus bas avec pygame.draw.line

                V0 = tailleTraj  # On défini la vitesse du lancer comme la taille du segment

                tailleNormale = (M.sqrt(
                    (mx - (player.rect.x + 195)) ** 2) * 0.3)  # On calcule la taille de la normale à la trajectoire

                cosTraj = (tailleNormale / tailleTraj)  # Cosinus de cette taille
                angle = M.degrees(M.acos(cosTraj))  # On converti en degrés
                trajectoire = True
                pygame.draw.line(background, black, (player.rect.x + 195, player.rect.y + 80), (mx, my),
                                 3)  # On dessine la ligne

        if score >= scoremax:  # On teste si le score est égal au score max
            return score, lim

        pygame.display.flip()  # On actualise l'affichage


def Position_2(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono, Fps_clock):
    """Fonction Position_x qui gère le déplacement des fruits, les évènements de l'utilisateur et le dessin / calcul des conditions initiales de la trajectoire"""
    black = (0, 0, 0)

    niveau1 = Niveau1
    niveau2 = Niveau2
    niveau3 = Niveau3

    if niveau1:
        scoremax = 39
        score = 16
    if niveau2:
        scoremax = 153
        score = 122
    if niveau3:
        scoremax = 295
        score = 258

    global pause, X, Y, angle, trajectoire, V0

    lancer_citron_possible = True
    lancer_framb_possible = False
    lancer_melon_possible = False
    lancer_fraise_possible = False
    lancer_ananas_possible = False
    lancer_kiwi_possible = False

    player = Player()
    player.move_Position_2()

    background = pygame.image.load('bg.jpg')
    background = pygame.transform.scale(background, (1080, 720))
    background_pause = pygame.image.load('bg_pause.jpg')
    background_pause = pygame.transform.scale(background_pause, (1080, 720))
    # background.blit(panier, (panier_x, panier_y))

    trajcitron = Trajcitron(player)
    trajframb = Trajframb(player)
    trajmelon = Trajmelon(player)
    trajananas = Trajananas(player)
    trajfraise = Trajfraise(player)
    trajkiwi = Trajkiwi(player)

    i = 1
    espace = False

    while position2 is True and score <= scoremax:
        player.move_Position_2()

        background.blit(player.image, player.rect)
        AffichageBackground(gameDisplay, background)
        # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

        player.citron.draw(gameDisplay)
        player.framb.draw(gameDisplay)
        player.melon.draw(gameDisplay)
        player.ananas.draw(gameDisplay)
        player.fraise.draw(gameDisplay)
        player.kiwi.draw(gameDisplay)
        Score(score)

        chrono = Chrono
        fps_clock = Fps_clock
        dt = fps_clock.tick(200)
        chrono -= timedelta(milliseconds=dt)
        time = chrono.strftime("%S")
        lim = int(time)
        if lim == 0:
            return score, lim
        Chrono = chrono
        Affichage(lim)

        for trajcitron in player.citron:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_citron_possible = trajcitron.move_citron(x, y, i)
            if trajcitron.panier_citron(angle):
                lancer_citron_possible = False
                player.citron.empty()
                score += 3
                lancer_framb_possible = True
                trajectoire = False

        if espace and i < 499:
            i += 1

        for trajframb in player.framb:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_framb_possible = trajframb.move_framb(x, y, i)
            if trajframb.panier_framb(angle):
                lancer_framb_possible = False
                player.framb.empty()
                score += 4
                lancer_melon_possible = True
                trajectoire = False

        for trajmelon in player.melon:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_melon_possible = trajmelon.move_melon(x, y, i)
            if trajmelon.panier_melon(angle):
                lancer_melon_possible = False
                lancer_ananas_possible = True
                if niveau2 or niveau3:
                    lancer_fraise_possible = True
                    lancer_ananas_possible = False
                player.melon.empty()
                score += 9

        for trajfraise in player.fraise:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_fraise_possible = trajfraise.move_fraise(x, y, i)

            if trajfraise.panier_fraise(angle):
                lancer_fraise_possible = False
                lancer_ananas_possible = True
                if niveau3:
                    lancer_kiwi_possible = True
                    lancer_ananas_possible = False
                player.fraise.empty()
                score += 8

        for trajkiwi in player.kiwi:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_kiwi_possible = trajkiwi.move_kiwi(x, y, i)

            if trajkiwi.panier_kiwi(angle):
                lancer_kiwi_possible = False
                lancer_ananas_possible = True
                player.kiwi.empty()
                score += 6

        for trajananas in player.ananas:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_ananas_possible = trajananas.move_ananas(x, y, i)
            if trajananas.panier_ananas(angle):
                lancer_ananas_possible = False
                player.ananas.empty()
                score += 7
                trajectoire = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and lancer_citron_possible is True and trajectoire is True:
                    player.ajout_citron()
                    X, Y = trajcitron.traj(angle, V0)
                    i = 1
                    espace = True
                    lancer_citron_possible = False
                if event.key == pygame.K_SPACE and lancer_framb_possible is True and trajectoire is True:
                    player.ajout_framb()
                    X, Y = trajframb.traj(angle, V0)
                    i = 1
                    lancer_framb_possible = False
                if event.key == pygame.K_SPACE and lancer_melon_possible is True and trajectoire is True:
                    player.ajout_melon()
                    X, Y = trajmelon.traj(angle, V0)
                    i = 1
                    lancer_melon_possible = False
                if event.key == pygame.K_SPACE and lancer_fraise_possible is True and trajectoire is True:
                    player.ajout_fraise()
                    X, Y = trajfraise.traj(angle, V0)
                    i = 1
                    lancer_fraise_possible = False
                if event.key == pygame.K_SPACE and lancer_kiwi_possible is True and trajectoire is True:
                    player.ajout_kiwi()
                    X, Y = trajkiwi.traj(angle, V0)
                    i = 1
                    lancer_kiwi_possible = False
                if event.key == pygame.K_SPACE and lancer_ananas_possible is True and trajectoire is True:
                    player.ajout_ananas()
                    X, Y = trajananas.traj(angle, V0)
                    i = 1
                    lancer_ananas_possible = True
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    Fps_clock = paused(Fps_clock)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                background = pygame.image.load('bg.jpg')
                background = pygame.transform.scale(background, (1080, 720))
                AffichageBackground(gameDisplay, background)
                background.blit(player.image, player.rect)
                # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

                mx, my = pygame.mouse.get_pos()

                tailleTraj = (M.sqrt((mx - (player.rect.x + 195)) ** 2 + (my - (player.rect.y + 80)) ** 2) * 0.3)
                V0 = tailleTraj
                tailleNormale = (M.sqrt((mx - (player.rect.x + 195)) ** 2) * 0.3)
                cosTraj = (tailleNormale / tailleTraj)
                angle = M.degrees(M.acos(cosTraj))
                trajectoire = True
                pygame.draw.line(background, black, (player.rect.x + 195, player.rect.y + 80), (mx, my), 3)

        if score >= scoremax:
            return score, lim
        pygame.display.flip()


def Position_3(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono, Fps_clock):
    """Fonction Position_x qui gère le déplacement des fruits, les évènements de l'utilisateur et le dessin / calcul des conditions initiales de la trajectoire"""
    black = (0, 0, 0)

    niveau1 = Niveau1
    niveau2 = Niveau2
    niveau3 = Niveau3

    if niveau1:
        scoremax = 66
        score = 39
    if niveau2:
        scoremax = 188
        score = 153
    if niveau3:
        scoremax = 336
        score = 295

    global pause, trajectoire, V0, X, angle, Y
    lancer_citron_possible = True
    lancer_framb_possible = False
    lancer_melon_possible = False
    lancer_ananas_possible = False
    lancer_banane_possible = False
    lancer_fraise_possible = False
    lancer_kiwi_possible = False

    player = Player()
    player.move_Position_3()

    background = pygame.image.load('bg.jpg')
    background = pygame.transform.scale(background, (1080, 720))
    background_pause = pygame.image.load('bg_pause.jpg')
    background_pause = pygame.transform.scale(background_pause, (1080, 720))
    # background.blit(panier, (panier_x, panier_y))

    trajcitron = Trajcitron(player)
    trajframb = Trajframb(player)
    trajmelon = Trajmelon(player)
    trajfraise = Trajfraise(player)
    trajananas = Trajananas(player)
    trajbanane = Trajbanane(player)
    trajkiwi = Trajkiwi(player)

    i = 1
    espace = False

    while position3 is True and score <= scoremax:
        player.move_Position_3()

        background.blit(player.image, player.rect)
        AffichageBackground(gameDisplay, background)
        # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

        player.citron.draw(gameDisplay)
        player.framb.draw(gameDisplay)
        player.melon.draw(gameDisplay)
        player.ananas.draw(gameDisplay)
        player.banane.draw(gameDisplay)
        player.fraise.draw(gameDisplay)
        player.kiwi.draw(gameDisplay)
        Score(score)

        chrono = Chrono
        fps_clock = Fps_clock
        dt = fps_clock.tick(120)
        chrono -= timedelta(milliseconds=dt)
        time = chrono.strftime("%S")
        lim = int(time)
        if lim == 0:
            return score, lim
        Chrono = chrono
        Affichage(lim)

        for trajcitron in player.citron:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_citron_possible = trajcitron.move_citron(x, y, i)
            if trajcitron.panier_citron(angle):
                lancer_citron_possible = False
                player.citron.empty()
                score += 3
                lancer_framb_possible = True
                trajectoire = False

        if espace and i < 499:
            i += 1

        for trajframb in player.framb:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_framb_possible = trajframb.move_framb(x, y, i)
            if trajframb.panier_framb(angle):
                lancer_framb_possible = False
                player.framb.empty()
                score += 4
                lancer_melon_possible = True
                trajectoire = False

        for trajmelon in player.melon:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_melon_possible = trajmelon.move_melon(x, y, i)
            if trajmelon.panier_melon(angle):
                lancer_melon_possible = False

                lancer_ananas_possible = True
                if niveau2 or niveau3:
                    lancer_fraise_possible = True
                    lancer_ananas_possible = False
                trajectoire = False
                player.melon.empty()
                score += 9

        for trajfraise in player.fraise:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_fraise_possible = trajfraise.move_fraise(x, y, i)

            if trajfraise.panier_fraise(angle):
                lancer_fraise_possible = False
                lancer_ananas_possible = True
                if niveau3:
                    lancer_kiwi_possible = True
                    lancer_ananas_possible = False
                player.fraise.empty()
                score += 8

        for trajkiwi in player.kiwi:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_kiwi_possible = trajkiwi.move_kiwi(x, y, i)

            if trajkiwi.panier_kiwi(angle):
                lancer_kiwi_possible = False
                lancer_ananas_possible = True
                player.kiwi.empty()
                score += 6

        for trajananas in player.ananas:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_ananas_possible = trajananas.move_ananas(x, y, i)
            if trajananas.panier_ananas(angle):
                lancer_ananas_possible = False
                lancer_banane_possible = True
                player.ananas.empty()
                score += 7
                trajectoire = False

        for trajbanane in player.banane:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_banane_possible = trajbanane.move_banane(x, y, i)
            if trajbanane.panier_banane(angle):
                lancer_banane_possible = False
                player.banane.empty()
                score += 4
                trajectoire = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and lancer_citron_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement du citron
                    player.ajout_citron()
                    X, Y = trajcitron.traj(angle, V0)
                    i = 1
                    espace = True
                    lancer_citron_possible = False
                if event.key == pygame.K_SPACE and lancer_framb_possible is True and trajectoire is True:  # Détecter si la touche espace est enclenchée = lancement de la framboise
                    player.ajout_framb()
                    X, Y = trajframb.traj(angle, V0)
                    i = 1
                    lancer_framb_possible = False
                if event.key == pygame.K_SPACE and lancer_melon_possible is True and trajectoire is True:
                    player.ajout_melon()
                    X, Y = trajmelon.traj(angle, V0)
                    i = 1
                    lancer_melon_possible = False
                if event.key == pygame.K_SPACE and lancer_fraise_possible is True and trajectoire is True:
                    player.ajout_fraise()
                    X, Y = trajfraise.traj(angle, V0)
                    i = 1
                    lancer_fraise_possible = False
                if event.key == pygame.K_SPACE and lancer_kiwi_possible is True and trajectoire is True:
                    player.ajout_kiwi()
                    X, Y = trajkiwi.traj(angle, V0)
                    i = 1
                    lancer_kiwi_possible = False
                if event.key == pygame.K_SPACE and lancer_ananas_possible is True and trajectoire is True:
                    player.ajout_ananas()
                    X, Y = trajananas.traj(angle, V0)
                    i = 1
                    lancer_ananas_possible = False
                if event.key == pygame.K_SPACE and lancer_banane_possible is True and trajectoire is True:
                    player.ajout_banane()
                    X, Y = trajbanane.traj(angle, V0)
                    i = 1
                    lancer_banane_possible = False
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    Fps_clock = paused(Fps_clock)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                background = pygame.image.load('bg.jpg')
                background = pygame.transform.scale(background, (1080, 720))
                AffichageBackground(gameDisplay, background)
                background.blit(player.image, player.rect)
                # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

                mx, my = pygame.mouse.get_pos()

                tailleTraj = (M.sqrt((mx - (player.rect.x + 195)) ** 2 + (my - (player.rect.y + 80)) ** 2) * 0.3)
                V0 = tailleTraj

                tailleNormale = (M.sqrt((mx - (player.rect.x + 195)) ** 2) * 0.3)

                cosTraj = (tailleNormale / tailleTraj)
                angle = M.degrees(M.acos(cosTraj))
                trajectoire = True
                pygame.draw.line(background, black, (player.rect.x + 195, player.rect.y + 80), (mx, my), 3)

        if score >= scoremax:
            return score, lim
        pygame.display.flip()


def Position_4(gameDisplay, Niveau1, Niveau2, Niveau3, Chrono, Fps_clock):
    """Fonction Position_x qui gère le déplacement des fruits, les évènements de l'utilisateur et le dessin / calcul des conditions initiales de la trajectoire"""
    black = (0, 0, 0)

    niveau1 = Niveau1
    niveau2 = Niveau2
    niveau3 = Niveau3
    if niveau1:
        scoremax = 98
        score = 66
    if niveau2:
        scoremax = 228
        score = 188
    if niveau3:
        scoremax = 382
        score = 336

    global pause, trajectoirePossible, V0, X, Y, angle

    lancer_citron_possible = True
    lancer_framb_possible = False
    lancer_melon_possible = False
    lancer_ananas_possible = False
    lancer_banane_possible = False
    lancer_pomme_possible = False
    lancer_kiwi_possible = False
    lancer_fraise_possible = False

    player = Player()
    player.move_Position_4()

    background = pygame.image.load('bg.jpg')
    background = pygame.transform.scale(background, (1080, 720))
    background_pause = pygame.image.load('bg_pause.jpg')
    background_pause = pygame.transform.scale(background_pause, (1080, 720))
    # background.blit(panier, (panier_x, panier_y))

    trajcitron = Trajcitron(player)
    trajframb = Trajframb(player)
    trajmelon = Trajmelon(player)
    trajananas = Trajananas(player)
    trajbanane = Trajbanane(player)
    trajpomme = Trajpomme(player)
    trajkiwi = Trajkiwi(player)
    trajfraise = Trajfraise(player)

    i = 1
    espace = False

    while position4 is True and score <= scoremax:
        player.move_Position_4()

        background.blit(player.image, player.rect)
        AffichageBackground(gameDisplay, background)
        # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

        player.citron.draw(gameDisplay)
        player.framb.draw(gameDisplay)
        player.melon.draw(gameDisplay)
        player.ananas.draw(gameDisplay)
        player.banane.draw(gameDisplay)
        player.pomme.draw(gameDisplay)
        player.kiwi.draw(gameDisplay)
        player.fraise.draw(gameDisplay)
        Score(score)

        chrono = Chrono
        fps_clock = Fps_clock
        dt = fps_clock.tick(120)
        chrono -= timedelta(milliseconds=dt)
        time = chrono.strftime("%S")
        lim = int(time)

        if lim == 0:
            return score, lim
        Chrono = chrono
        Affichage(lim)

        for trajcitron in player.citron:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_citron_possible = trajcitron.move_citron(x, y, i)
            if trajcitron.panier_citron(angle):
                lancer_citron_possible = False
                player.citron.empty()
                score += 3
                lancer_framb_possible = True
                trajectoirePossible = False

        if espace and i < 499:
            i += 1

        for trajframb in player.framb:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_framb_possible = trajframb.move_framb(x, y, i)
            if trajframb.panier_framb(angle):
                lancer_framb_possible = False
                player.framb.empty()
                score += 4
                lancer_melon_possible = True
                trajectoirePossible = False

        for trajmelon in player.melon:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_melon_possible = trajmelon.move_melon(x, y, i)
            if trajmelon.panier_melon(angle):
                lancer_melon_possible = False
                lancer_ananas_possible = True
                if niveau2 or niveau3:
                    lancer_fraise_possible = True
                    lancer_ananas_possible = False
                trajectoirePossible = False
                player.melon.empty()
                score += 9

        for trajfraise in player.fraise:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_fraise_possible = trajfraise.move_fraise(x, y, i)

            if trajfraise.panier_fraise(angle):
                lancer_fraise_possible = False
                lancer_ananas_possible = True
                if niveau3:
                    lancer_kiwi_possible = True
                    lancer_ananas_possible = False
                player.fraise.empty()
                score += 8

        for trajkiwi in player.kiwi:
            x = X[i] + 120
            y = -1 * Y[i] + 600
            lancer_kiwi_possible = trajkiwi.move_kiwi(x, y, i)

            if trajkiwi.panier_kiwi(angle):
                lancer_kiwi_possible = False
                lancer_ananas_possible = True
                player.kiwi.empty()
                score += 6

        for trajananas in player.ananas:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_ananas_possible = trajananas.move_ananas(x, y, i)
            if trajananas.panier_ananas(angle):
                lancer_ananas_possible = False
                lancer_banane_possible = True
                player.ananas.empty()
                score += 7
                trajectoirePossible = False

        for trajbanane in player.banane:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_banane_possible = trajbanane.move_banane(x, y, i)
            if trajbanane.panier_banane(angle):
                lancer_banane_possible = False
                lancer_pomme_possible = True
                player.banane.empty()
                score += 4
                trajectoirePossible = False

        for trajpomme in player.pomme:
            x = X[i] + 120
            y = -1 * Y[i] + 600

            lancer_pomme_possible = trajpomme.move_pomme(x, y, i)
            if trajpomme.panier_pomme(angle):
                lancer_pomme_possible = False

                player.pomme.empty()
                score += 5
                trajectoirePossible = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and lancer_citron_possible is True and trajectoirePossible is True:
                    player.ajout_citron()
                    X, Y = trajcitron.traj(angle, V0)
                    i = 1
                    espace = True
                    lancer_citron_possible = False
                if event.key == pygame.K_SPACE and lancer_framb_possible is True and trajectoirePossible is True:
                    player.ajout_framb()
                    X, Y = trajframb.traj(angle, V0)
                    i = 1
                    lancer_framb_possible = False
                if event.key == pygame.K_SPACE and lancer_melon_possible is True and trajectoirePossible is True:
                    player.ajout_melon()
                    X, Y = trajmelon.traj(angle, V0)
                    i = 1
                    lancer_melon_possible = False
                if event.key == pygame.K_SPACE and lancer_fraise_possible is True and trajectoirePossible is True:
                    player.ajout_fraise()
                    X, Y = trajfraise.traj(angle, V0)
                    i = 1
                    lancer_fraise_possible = False
                if event.key == pygame.K_SPACE and lancer_kiwi_possible is True and trajectoirePossible is True:
                    player.ajout_kiwi()
                    X, Y = trajkiwi.traj(angle, V0)
                    i = 1
                    lancer_kiwi_possible = False
                if event.key == pygame.K_SPACE and lancer_ananas_possible is True and trajectoirePossible is True:
                    player.ajout_ananas()
                    X, Y = trajananas.traj(angle, V0)
                    i = 1
                    lancer_ananas_possible = False
                if event.key == pygame.K_SPACE and lancer_banane_possible is True and trajectoirePossible is True:
                    player.ajout_banane()
                    X, Y = trajbanane.traj(angle, V0)
                    i = 1
                    lancer_banane_possible = False
                if event.key == pygame.K_SPACE and lancer_pomme_possible is True and trajectoirePossible is True:
                    player.ajout_pomme()
                    X, Y = trajpomme.traj(angle, V0)
                    i = 1
                    lancer_pomme_possible = False
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    Fps_clock = paused(Fps_clock)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                background = pygame.image.load('bg.jpg')
                background = pygame.transform.scale(background, (1080, 720))
                AffichageBackground(gameDisplay, background)
                background.blit(player.image, player.rect)
                # AffichagePanier(gameDisplay, panier, panier_x, panier_y)

                mx, my = pygame.mouse.get_pos()

                tailleTraj = (M.sqrt((mx - (player.rect.x + 195)) ** 2 + (my - (player.rect.y + 80)) ** 2) * 0.3)

                V0 = tailleTraj

                tailleNormale = (M.sqrt((mx - (player.rect.x + 195)) ** 2) * 0.3)

                cosTraj = (tailleNormale / tailleTraj)
                angle = M.degrees(M.acos(cosTraj))
                trajectoirePossible = True
                pygame.draw.line(background, black, (player.rect.x + 195, player.rect.y + 80), (mx, my), 3)

        if score >= scoremax:
            return scoremax, lim
        pygame.display.flip()
