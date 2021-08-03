"""
Hugo Pallard                                                                                                                                                                   13/05/2020
Léo Toggenburger

-------------------------------------------------------------------------------- Fruit Basket ------------------------------------------------------------------------------------------------

Bonjour,

Vous vous trouvez dans le fichier trajframb.py de notre projet.
Ce fichier est commun pour chacun des fruits. Nous avons fait ce choix car cela est plus simple pour gérer séparemment les paramètres de chacun des fruits.
Dans le cas contraire, nous aurions dû utiliser le_nombre_de_fruits * le nombre de paramètres de chaques fruits variables différentes, soit un total d'environ 80 variables.
Ce fichier contrôle la trajectoire du fruit à l'aide de la méthode move_fruit() ligne 48, rend possible la suppresion d'un sprite avec la méthode remove() ligne 45
Ici, on peut tester si le fruit est rentré dans le panier avec la méthode panier_fruit() en fonction de sa propre tolérance, calculée experimentalement.

Ce fichier étant commun pour chacun des fruits, nous avons commenté que le fichier trajcitron par commodité, les autres fonctionnement sur le même principe.

Cordialement.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""

import pygame
import numpy as N
import scipy.integrate as SI


class Trajframb(pygame.sprite.Sprite):
    """ Cette classe s'occupe de la gestion du fruit qui lui est associé"""
    def __init__(self, player):
        self.panier = False
        super().__init__()
        self.player = player
        self.image = pygame.image.load('framb_blank.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 150
        self.rect.y = player.rect.y + 15
        self.x_init = player.rect.x + 25
        self.y_init = player.rect.y - 390
        self.mass = 6

    def remove(self):
        """Fonction qui supprime le sprite en cours"""
        self.player.framb.remove(self)

    def move_framb(self, x, y, i):
        """Fonction qui gère le déplacement de la framboise"""
        self.i = i

        if self.panier is False:
            self.rect.x = x
            self.rect.y = y
            if self.rect.x > 1080 or self.rect.y > 720 or i == 499:
                self.remove()
                lancer_framb_possible = True
                return lancer_framb_possible

    def panier_framb(self, angle):
        """Fonction qui détecte si un panier a été marqué"""
        centre_framb_x = self.rect.x - 100
        centre_framb_y = self.rect.y - 75
        if 830 < centre_framb_x < 895 and 160 < centre_framb_y < 180 and angle > 50:
            self.panier = True
            self.remove()
            return True
        return False

    def traj(self, angle, V0):
        """Fonction qui calcule la trajectoire selon les équations différentielle du mouvement, à partir des conditions initiales calculées dans Position_x de positions.py"""
        g = 9.81
        cx = 0.45
        rhoAir = 1.2
        rad = 0.05 / 2
        mass = self.mass
        rho = mass / (4. / 3. * N.pi * rad ** 3)
        alpha = 0.5 * cx * rhoAir * N.pi * rad ** 2 / mass

        v0 = V0
        alt = angle
        alt *= N.pi / 180.
        z0 = (self.x_init, self.y_init, v0 * N.cos(alt), v0 * N.sin(alt))

        tc = N.sqrt(mass / (g * alpha))
        t = N.linspace(0, tc, 500)

        def zdot(z, t):

            """Calcul de la dérivée de z=(x, y, vx, vy) à l'instant t."""

            x, y, vx, vy = z
            alphav = alpha * N.hypot(vx, vy)

            return vx, vy, -alphav * vx, -g - alphav * vy

        zs = SI.odeint(zdot, z0, t)

        X = zs[:, 0].astype(int)
        Y = zs[:, 1].astype(int)
        ypos = zs[:, 1] >= 0
        return X, Y
