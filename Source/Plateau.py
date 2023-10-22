from __future__ import annotations
from Cell import Cell, TrouBlanc
from Position import Position
import pygame
from Player import Player


class Plateau:
    def __init__(self: Plateau):
        self._list_cell: list[Cell] = []
        self._list_pos_trou_blanc: list[Position] = []

        for i in range(10):
            for y in range(10):
                self._list_cell.append(Cell(position=Position(x=i, y=y)))
                if isinstance(self._list_cell[-1], TrouBlanc):
                    self._list_pos_trou_blanc.append(Position(i, y))

    @property
    def list_cell(self: Plateau) -> list[Cell]:
        return self._list_cell
    

    def clear_all_pieces(self: Plateau):
        """Clear les piéces de toutes les cellules du plateau

        Args:
            self (Plateau): Plateau de jeu
        """
        for cell in self._list_cell:
            cell.clear_pieces_dict()

    def spawn_objet(self: Plateau):
        """Fait apparaître des objets sur les cellules du plateau

        Args:
            self (Plateau): Plateau de jeu
        """
        for cell in self._list_cell:
            cell.spawn_objet()

    def draw(self: Plateau, screen: pygame.Surface,):
        """Dessiner le plateau

        Args:
            self (Plateau): Plateau de jeu
            screen (pygame.Surface): Ecran pygame sur lequel dessiner
        """
        for cell in self._list_cell:
            cell.draw(screen)

    def find_cell(self: Plateau, position: Position) -> Cell | None:
        """Cherche une cellule à une certaine position sur le plateau

        Args:
            self (Plateau): Plateau de jeu
            position (Position): Position de la cellule recherchée

        Returns:
            Cell | None: Cellule trouvée, None si aucun cellule n'a cette position
        """
        for cell in self._list_cell:
            if position == cell.position:
                return cell
        return None

    def verif_cell(self: Plateau, pos: Position) -> bool:
        """Cherche une cellule à une position précise pour lui demander si un joueur peu se déplacer dessus

        Args:
            self (Plateau): Plateau de jeu
            pos (Position): Position de la cellule

        Returns:
            bool: True sur le joueur peut se déplacer, False sinon
        """
        try:
            cell: Cell = self.find_cell(pos)
            return cell.player_arrived(True, self._list_pos_trou_blanc)
        except AttributeError:
            return False

    def free_cell(self: Plateau, pos: Position) -> None:
        """Libére une cellule d'un joueur

        Args:
            self (Plateau): Plateau de jeu
            pos (Position): Position de la cellule
        """
        cell = self.find_cell(pos)
        if cell is None:
            return
        else:
            cell.occupied = False #Libére la cellule

    def give_objet(self: Plateau, joueur: Player) -> None:
        """Donne un objet à un joueur

        Args:
            self (Plateau): Plateau de jeu
            joueur (Player): Joueur
        """
        cell = self.find_cell(joueur.position)
        if joueur.recup_objet(cell.objet):
            cell.objet = None #La cellule n'a plus d'objet

    def reset_cells(self: Plateau):
        """Réinitialise les cellules du plateau

        Args:
            self (Plateau): Plateau de jeu
        """
        for cell in self._list_cell:
            cell.reset()

    def turn(self: Plateau, player_list: list[Player] = []):
        """Retourne le plateau

        Args:
            self (Plateau): Plateau de jeu
            player_list (list[Player], optional): Liste des joueurs. Defaults to [].
        """
        for cell in self._list_cell:
            cell.position = Position(
                (10 - cell.position.y) % 10, (10 - cell.position.x) % 10 #Modification des positions des cellules
            ) 
            for player in player_list: #Libération des cellules anciennement occupées et occupations des nouvelles
                if player.position != cell.position:
                    cell.occupied = False
                else:
                    cell.occupied = True

    def update_color(self: Plateau):
        """Update des couleurs des cellules

        Args:
            self (Plateau): Plateau de jeu
        """
        for cell in self._list_cell:
            color = (0, 0)
            for elt in cell.dict_piece.keys(): #Détermination de la couleur de la cellule
                if cell.dict_piece[elt] > color[1]:
                    color = (elt, cell.dict_piece[elt])
            if color[0] != 0: #La couleur 0 est réservé par défaut
                cell.color = color[0]

    def coin_deposit(self: Plateau, position: Position, color: int, nb_coins: int = 1):
        """Dépose une piéce sur une cellule

        Args:
            self (Plateau): Plateau de jeu
            position (Position): Position de la cellule
            color (int): Couleur du joueur déposant les piéces
            nb_coins (int, optional): Nombre de piéce à déposer. Defaults to 1.
        """
        cell = self.find_cell(position)
        if color in cell.dict_piece.keys():
            cell.dict_piece[color] += nb_coins
        else:
            cell.dict_piece[color] = nb_coins

    def verif_gagnant(self: Plateau) -> int | None:
        """Vérifie si un joueur remplit la condition pour gagner

        Args:
            self (Plateau): Plateau de jeu

        Returns:
            int | None: Couleur du joueur gagnant si il y en a un
        """
        for cell in self.list_cell:
            if cell.color != 0:
                if (
                    self.check_color(
                        x=1,
                        color=cell.color,
                        position=Position(cell.position.x, cell.position.y),
                    )
                    or self.check_color(
                        x=-1,
                        color=cell.color,
                        position=Position(cell.position.x, cell.position.y),
                    )
                    or self.check_color(
                        y=1,
                        color=cell.color,
                        position=Position(cell.position.x, cell.position.y),
                    )
                    or self.check_color(
                        y=-1,
                        color=cell.color,
                        position=Position(cell.position.x, cell.position.y),
                    )
                ):
                    return cell.color
        return None

    def check_color(self: Plateau, color: int, position: Position, x: int = 0, y: int = 0):
        """Vérifie si 5 cellules de la même couleur sont alignées et côte à côte

        Args:
            self (Plateau): Plateau de jeu
            color (int): Couleur
            position (Position): Position de la cellule de base
            x (int, optional): Décalage entre les cellules. Defaults to 0.
            y (int, optional): Décalage entre les cellules. Defaults to 0.

        Returns:
            _type_: _description_
        """
        for i in range(4):
            position.x += x
            position.y += y
            cell = self.find_cell(position)
            if cell is not None:
                if cell.color != color:
                    return False
            else:
                return False
        return True
