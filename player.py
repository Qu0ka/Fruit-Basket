import pygame

from trajcitron import Trajcitron
from trajframb import Trajframb
from trajmelon import Trajmelon
from trajananas import Trajananas
from trajbanane import Trajbanane
from trajpomme import Trajpomme
from trajfraise import Trajfraise
from trajkiwi import Trajkiwi

gameDisplay = pygame.display.set_mode((1080, 720))
height = 720
black = (0, 0, 0)
width = 1080
size = width, height
red = (150, 0, 0)
bright_red = (255, 0, 0)
green = (0, 150, 0)
bright_green = (0, 255, 0)
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, size)
pygame.display.set_caption("Fruit Basket")
# panier = pygame.image.load('Panier.png')
# panier = pygame.transform.scale(panier, (600, 725))
panier_y = 60
panier_x = 690
white = (255, 255, 255)
clock = pygame.time.Clock()
pause = False


class Player(pygame.sprite.Sprite):  # Création de la classe du joueur:

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('basket_player.png')  # Chargement de l'image du joueur
        self.image = pygame.transform.scale(self.image, (200, 250))  # On adapte la taille de l'image du joueur
        self.citron = pygame.sprite.Group()  # On créé un groupe de sprite que l'on nomme citron
        self.framb = pygame.sprite.Group()  # ...
        self.melon = pygame.sprite.Group()
        self.ananas = pygame.sprite.Group()
        self.banane = pygame.sprite.Group()
        self.pomme = pygame.sprite.Group()
        self.fraise = pygame.sprite.Group()
        self.kiwi = pygame.sprite.Group()  # ...
        self.rect = self.image.get_rect()  # L'attribut get_rect() créé un rectangle invisible autour de l'image
        # du joueur, ce qui permet de le déplacer plus facilement

        self.rect.x = 0  # Initialisation des coordonnées
        self.rect.y = 475

    def move_Position_1(self):  # Méthode déplaçant le joueur à la coordonnée voulue
        self.rect.x = 500

    def move_Position_2(self):
        self.rect.x = 375

    def move_Position_3(self):
        self.rect.x = 200

    def move_Position_4(self):
        self.rect.x = 0

    def ajout_citron(self):  # On appelle la classe Trajcitron() cela créer un projectile citron
        # On ajoute le projectile créé au groupe projectile_citron

        self.citron.add(Trajcitron(self))

    def ajout_framb(self):
        self.framb.add(Trajframb(self))

    def ajout_melon(self):
        self.melon.add(Trajmelon(self))

    def ajout_ananas(self):
        self.ananas.add(Trajananas(self))

    def ajout_banane(self):
        self.banane.add(Trajbanane(self))

    def ajout_pomme(self):
        self.pomme.add(Trajpomme(self))

    def ajout_fraise(self):
        self.fraise.add(Trajfraise(self))

    def ajout_kiwi(self):
        self.kiwi.add(Trajkiwi(self))
