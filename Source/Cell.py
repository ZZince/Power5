from __future__ import annotations
from Position import Position
from random import uniform, randint
from Player import Player
from Objet import Objet
import pygame


class Cell:
    sprite_path: str = "Sprites/normal.png"

    def __new__(cls, **kwargs):
        random_float = uniform(0, 1)
        if random_float >= 0.94:
            instance = super(Cell, cls).__new__(Lave)
        elif random_float >= 0.85 and random_float < 0.9:
            instance = super(Cell, cls).__new__(TrouBlanc)
        elif random_float >= 0.74 and random_float < 0.8:
            instance = super(Cell, cls).__new__(TrouNoir)
        elif random_float >= 0.65 and random_float < 0.7:
            instance = super(Cell, cls).__new__(Sable)
        else:
            instance = super(Cell, cls).__new__(Normal)

        return instance

    def __init__(
        self: Cell,
        position: Position = Position(),
        color: int = 0,
        dict_piece: dict = {},
    ):
        self.__position: Position = position
        self.__color: int = color
        self.__dict_piece: dict = {}
        self.__objet: Objet | None = None
        self.__occupied: bool = False

    def __repr__(self: Cell) -> str:
        if self.color != 0:
            return f"Cell {type(self)}: {self.__position} | occupied : {self.__occupied} | color : {self.__color} | dict_piece : {self.__dict_piece} | objet : {self.__objet}"
        else:
            return ""
        
    @property
    def position(self: Cell) -> Position:
        return self.__position

    @property
    def occupied(self: Cell) -> bool:
        return self.__occupied

    @property
    def color(self: Cell) -> int:
        return self.__color

    @property
    def dict_piece(self: Cell) -> dict:
        return self.__dict_piece

    @property
    def objet(self) -> Objet | None:
        return self.__objet

    @position.setter
    def position(self: Cell, position: Position):
        self.__position = position

    @occupied.setter
    def occupied(self: Cell, occupied: bool):
        self.__occupied = occupied

    @color.setter
    def color(self: Cell, color: int):
        self.__color = color

    @dict_piece.setter
    def dict_piece(self: Cell, dict_piece: dict):
        self.__dict_piece = dict_piece

    @objet.setter
    def objet(self, objet: Objet | None):
        self.__objet = objet

    def draw(self: Cell, screen: pygame.Surface) -> None:
        """Dessine la cellule

        Args:
            self (Cell): Cellule à dessiner
            screen (pygame.Surface): Ecran pygame à dessiner
        """
        image = pygame.image.load(self.sprite_path)
        new_size = (90, 90)
        position = (
            self.position.x * 90,
            self.position.y * 90,
        )
        screen.blit(pygame.transform.scale(image, new_size), position)
        if self.__objet: #Si la cellule à un objet
            self.__objet.draw(screen, self.position)
        if self.__color != 0: #Si la cellule à été capturé
            image = pygame.image.load(f"Sprites/drapeau{self.__color}.png")
            position = (self.position.x * 90, self.position.y * 90)
            screen.blit(image, position)
        if self.__dict_piece != {}: #Si des joueurs ont déposés des piéces sur la cellule ce tour
            temp = 0
            for elt in self.__dict_piece.values():
                if elt > temp:
                    temp = elt
            image =  pygame.image.load(f"Sprites/coins{elt if 0 < elt <= 3 else 3}.png")
            position = (self.position.x * 90 + 60, self.position.y*90 + 60)
            screen.blit(image,position)
    

    def clear_pieces_dict(self: Cell) -> None:
        """Réinitialise le dictionnaire de piéces

        Args:
            self (Cell): Cellule
        """
        self.__dict_piece = {}

    def spawn_objet(self: Cell) -> None:
        """Donne un objet à la cellule

        Args:
            self (Cell): Cellule
        """
        if not self.__occupied:
            self.__objet = Objet()
        else:
            pass

    def cellEffect(self: Cell, list_pos_available: list[Position]) -> bool|Position:
        """Effet particulié de la cellule

        Args:
            self (Cell): Cellule
            list_pos_available (list[Position]): Si la cellule à besoin de connaître une liste de position

        Returns:
            bool|Position: Booléen si la cellule accepte ou non un joueur, Position si la cellule téléporte le joueur
        """
        return True

    def player_arrived(
        self: Cell, occupied: bool, list_pos_avaible: list[Position]
    ) -> bool:
        """Occupe la cellule si le joueur est accepté

        Args:
            self (Cell): Cellule
            occupied (bool): True sur la cellule doit être occupé
            list_pos_avaible (list[Position]): Si la cellule à besoin de connaître une liste de position

        Returns:
            bool: True sur le joueur est accepté, False sinon
        """
        if self.cellEffect(list_pos_avaible):
            if self.__occupied == True and occupied == True:
                return False
            else:
                self.__occupied = occupied
            return True
        else:
            return False

    def reset(self: Cell):
        """Réinitialise certaines caractéristiques de la cellules
        """
        pass


class TrouBlanc(Cell):
    key_dict = "TrouBlanc"
    sprite_path: str = "Sprites/white_hole.png"

    def __init__(
        self: TrouBlanc,
        position: Position = ...,
        color: int = 0,
        dict_piece: dict = ...,
    ):
        super().__init__(position, color, dict_piece)

    def cellEffect(self: TrouBlanc, list_pos_available: list[Position]) -> bool:
        return False

    def spawn_objet(self: TrouBlanc):
        pass


class TrouNoir(Cell):
    key_dict = "TrouNoir"
    sprite_path: str = "Sprites/black_hole.png"

    def __init__(
        self: TrouNoir,
        position: Position = ...,
        color: int = 0,
        dict_piece: dict = ...,
    ):
        super().__init__(position, color, dict_piece)

    def cellEffect(
        self: TrouNoir, list_pos_available: list[Position]
    ) -> Position | None:
        rd: int = randint(0, len(list_pos_available) - 1)
        try:
            return list_pos_available[rd]
        except IndexError:
            return self.position

    def spawn_objet(self: TrouNoir) -> None:
        pass

    def player_arrived(
        self: TrouNoir, occupied: bool, list_pos_available: list[Position]
    ) -> bool:
        return self.cellEffect(list_pos_available)


class Normal(Cell):
    key_dict = "Normal"

    def __init__(
        self: Normal,
        position: Position = ...,
        color: int = 0,
        dict_piece: dict = ...,
    ):
        super().__init__(position, color, dict_piece)


class Lave(Cell):
    key_dict = "Lave"
    sprite_path: str = "Sprites/lava.png"

    def __init__(
        self: Lave,
        position: Position = ...,
        color: int = 0,
        dict_piece: dict = ...,
    ):
        super().__init__(position, color, dict_piece)

    def cellEffect(self: Lave, list_pos_avaible: list[Position]) -> bool:
        return False

    def spawn_objet(self: Lave) -> None:
        pass


class Sable(Cell):
    player_already_passed = False
    key_dict = "Sable"
    sprite_path: str = "Sprites/sand.png"

    def __init__(
        self: Sable,
        position: Position = ...,
        color: int = 0,
        dict_piece: dict = ...,
    ):
        super().__init__(position, color, dict_piece)

    def cellEffect(self: Sable, list_pos_available: list[Position]) -> bool:
        if not self.player_already_passed:
            self.player_already_passed = True
            return True
        else:
            return False

    def reset(self: Sable):
        self.player_already_passed = False
