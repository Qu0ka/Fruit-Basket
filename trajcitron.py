"""
Hugo Pallard                                                                                                                                                                   13/05/2020
Léo Toggenburger

-------------------------------------------------------------------------------- Fruit Basket ------------------------------------------------------------------------------------------------

Bonjour,

Vous vous trouvez dans le fichier trajcitron.py de notre projet.
Ce fichier est commun pour chacun des fruits. Nous avons fait ce choix car cela est plus simple pour gérer séparemment les paramètres de chacun des fruits.
Dans le cas contraire, nous aurions dû utiliser le_nombre_de_fruits * le nombre de paramètres de chaques fruits variables différentes, soit un total d'environ 80 variables.
Ce fichier contrôle la trajectoire du fruit à l'aide de la méthode move_fruit() ligne 48, rend possible la suppresion d'un sprite avec la méthode remove() ligne 45
Ici, on peut tester si le fruit est rentré dans le panier avec la méthode panier_fruit() en fonction de sa propre tolérance, calculée experimentalement.

Ce fichier étant commun pour chacun des fruits, nous avons commenté que celui la par commodité, les autres fonctionnement sur le même principe.

Cordialement.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""


import pygame
import numpy as N
import scipy.integrate as SI




class Trajcitron(pygame.sprite.Sprite):
    """ Cette classe s'occupe de la gestion du fruit qui lui est associé, exemple ici, le citron"""
    def __init__(self, player):
        self.panier = False
        super().__init__()                                              # On charge la classe de sprite.Sprite de pygame
        self.player = player                                            # On récupère ici le joueur initialisé dans Position_x() dans positions.py
        self.image = pygame.image.load('citron_blank.png')              # Afichage du citron, transformation de l'image, et placement du citron aux coords du joueur
        self.image = pygame.transform.scale(self.image, (200, 150))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 110
        self.rect.y = player.rect.y + 10
        self.x_init = player.rect.x - 20
        self.y_init = player.rect.y - 365
        self.mass = 6                                                 # On applique une masse au citron

    def remove(self):
        """Fonction qui supprime le sprite en cours"""
        self.player.citron.remove(self)

    def move_citron(self, x, y, i):
        """Fonction qui gère le déplacement du citron"""

        # self.i = i

        if self.panier is False :                                       # Si l'on à pas mis de panier alors...
            self.rect.x = x                                             # ... Le citron est déplacé selon y et x, à partir de la trajectoire calculée
            self.rect.y = y

            if self.rect.x > 1080 or self.rect.y > 720 or i == 499:     # Si le citron est sorti de la fenêtre...
                self.remove()                                           # ... On le supprime, et
                lancer_citron_possible = True                           # On permet à l'utilisateur de relancer un nouveau citron
                return lancer_citron_possible

    def panier_citron(self, angle):
        """Fonction qui détecte si un panier a été marqué"""
        centre_citron_x = self.rect.x - 100                             # Calcul des coordonnées du centre du citron
        centre_citron_y = self.rect.y - 75

        if 778 < centre_citron_x < 835 and 140 < centre_citron_y < 170 and angle > 50:
            self.panier = True
            self.remove()
            return True
        return False

    def traj(self, angle, V0):
        """Fonction qui calcule la trajectoire selon les équations différentielle du mouvement, à partir des conditions initiales calculées dans Position_x de positions.py"""
        g = 9.81                                                            # Pesanteur [m/s2]
        cx = 0.45                                                           # Coefficient de frottement d'une sphère
        rhoAir = 1.2                                                        # Masse volumique de l'air [kg/m3] au niveau de la mer, T=20°C
        rad = 0.05/2                                                       # Rayon du citron [m]
        mass = self.mass
        # rho = mass / (4./3.*N.pi*rad**3)                                    # masse volumique
        alpha = 0.5*cx*rhoAir*N.pi*rad**2 / mass                            # Coefficient de frottement par unité de masse

        #Conditions initiales
        v0 = V0*0.95                                                             # Vitesse initiale [m/s]
        alt = angle                                                         # Inclinaison du canon [deg]
        alt *= N.pi / 180.                                                  # Inclinaison [rad]
        z0 = (self.x_init, self.y_init, v0 * N.cos(alt), v0 * N.sin(alt))   # (x0, y0, vx0, vy0)

        #Temps caractéristique
        tc = N.sqrt(mass / (g * alpha))

        t = N.linspace(0, tc, 500)

        def zdot(z, t):

            """Calcul de la dérivée de z=(x, y, vx, vy) à l'instant t."""

            x, y, vx, vy = z
            alphav = alpha * N.hypot(vx, vy)

            return vx, vy, -alphav * vx, -g - alphav * vy  # dz/dt = (vx,vy,x..,y..)

        zs = SI.odeint(zdot, z0, t)                                         # On résout l'équation différentielle
        X = zs[:,0].astype(int)                                             # avec odeint( fonction, valeurs_initiales, temps).
        Y = zs[:,1].astype(int)
        ypos = zs[:, 1] >= 0
        return X, Y


