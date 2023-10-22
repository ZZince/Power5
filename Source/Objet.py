from __future__ import annotations
from random import randint
from Position import Position
import pygame


class Objet:
    def __new__(cls):
        #Création aléatoire d'objet
        random_number = randint(0, 10)

        match random_number:
            case 0:
                instance = super(Objet, cls).__new__(PieceClearer)
            case 1:
                instance = super(Objet, cls).__new__(GameBoardTurner)
            case 2:
                instance = super(Objet, cls).__new__(RunFaster)
            case 3:
                instance = super(Objet, cls).__new__(GameBoardTurner)
            case 4:
                instance = super(Objet, cls).__new__(CoinsExpensiver)
            case _:
                instance = None

        return instance

    def __init__(self: Objet):
        pass

    def use(self):
        pass

    def draw(self: Objet, screen: pygame.Surface, position: Position):
        """Dessiner l'objet sur le plateau

        Args:
            self (Objet): Objet à dessiner
            screen (pygame.Surface): Ecran pygame sur lequel dessiner
            position (Position, optional): Position de la cellule  qui appartient l'objet
        """
        image = pygame.image.load(self.sprite_path)
        new_size = (60, 60)
        position = (
            position.x * 90 + 15,
            position.y * 90 + 15,
        )
        screen.blit(pygame.transform.scale(image, new_size), position)


class PieceClearer(Objet):
    sprite_path: str = "Sprites/PieceClearer.png"

    def __init__(self: PieceClearer):
        super().__init__()

    def use(self: PieceClearer, plateau=None, player=None, player_list=[]):
        """Utilisation de l'objet

        Args:
            self (PieceClearer): Objet à utiliser
            plateau (Plateau, optional): Si l'objet à besoin de connaître le plateau. Defaults to None.
            player (Player, optional): Si l'objet à besoin de connaître le joueur. Defaults to None.
            player_list (list[Player], optional): Si l'objet à besoin de connaître la liste des joueurs. Defaults to [].
        """
        plateau.clear_all_pieces()


class GameBoardTurner(Objet):
    sprite_path: str = "Sprites/GameBoardTurner.png"

    def __init__(self: GameBoardTurner):
        super().__init__()

    def use(self: GameBoardTurner, plateau=None, player=None, player_list=[]):
        """Utilisation de l'objet

        Args:
            self (GameBoardTurner): Objet à utiliser
            plateau (Plateau, optional): Si l'objet à besoin de connaître le plateau. Defaults to None.
            player (Player, optional): Si l'objet à besoin de connaître le joueur. Defaults to None.
            player_list (list[Player], optional): Si l'objet à besoin de connaître la liste des joueurs. Defaults to [].
        """
        plateau.turn(player_list)


class RunFaster(Objet):
    sprite_path: str = "Sprites/RunFaster.png"

    def __init__(self: RunFaster):
        super().__init__()

    def use(self: RunFaster, plateau=None, player=None, player_list=[]):
        """Utilisation de l'objet

        Args:
            self (RunFaster): Objet à utiliser
            plateau (Plateau, optional): Si l'objet à besoin de connaître le plateau. Defaults to None.
            player (Player, optional): Si l'objet à besoin de connaître le joueur. Defaults to None.
            player_list (list[Player], optional): Si l'objet à besoin de connaître la liste des joueurs. Defaults to [].
        """
        player.mouvement_point += 3


class CoinsExpensiver(Objet):
    sprite_path: str = "Sprites/CoinsExpensiver.png"

    def __init__(self: CoinsExpensiver):
        super().__init__()

    def use(self: CoinsExpensiver, plateau=None, player=None, player_list=[]):
        """Utilisation de l'objet

        Args:
            self (CoinsExpensiver): Objet à utiliser
            plateau (Plateau, optional): Si l'objet à besoin de connaître le plateau. Defaults to None.
            player (Player, optional): Si l'objet à besoin de connaître le joueur. Defaults to None.
            player_list (list[Player], optional): Si l'objet à besoin de connaître la liste des joueurs. Defaults to [].
        """
        player.nb_pieces += 3
