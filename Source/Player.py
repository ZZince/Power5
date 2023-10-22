from __future__ import annotations
from Objet import Objet
from time import sleep
from Position import Position
import pygame


class Player:
    sprites_path: dict[int, str] = {
        1: "Sprites/Player1.png",
        2: "Sprites/Player2.png",  
        3: "Sprites/Player3.png",  
        4: "Sprites/Player4.png",  
    }

    def __init__(
        self: Player,
        color: int = 0,
        nb_reset_pieces: int = 4,
        nb_reset_mouvement_point: int = 7,
        nb_pieces: int = 0,
        mouvement_point: int = 7,
        position: Position = Position(),
    ):
        self.__color: int = color
        self.__nb_reset_pieces = nb_reset_pieces
        self.__nb_reset_mouvement_point: int = nb_reset_mouvement_point
        self.__nb_pieces: int = nb_pieces
        self.__mouvement_point: int = mouvement_point
        self.__list_objet: list[Objet] = []
        self.__position: Position = position

    def __repr__(self: Player) -> str:
        return f"Player : color = {self.__color} | max_mp = {self.__nb_reset_mouvement_point} | nb_pieces = {self.__nb_pieces} | mp = {self.__mouvement_point}"

    def __eq__(self, player: Player) -> bool:
        return self.__color == player.__color

    @property
    def color(self: Player) -> int:
        return self.__color

    @property
    def nb_reset_mouvement_point(self: Player) -> int:
        return self.__nb_reset_mouvement_point

    @property
    def nb_reset_pieces(self: Player) -> int:
        return self.__nb_reset_pieces

    @property
    def nb_pieces(self: Player) -> int:
        return self.__nb_pieces

    @property
    def mouvement_point(self: Player) -> int:
        return self.__mouvement_point

    @property
    def list_objet(self: Player) -> list[Objet]:
        return self.__list_objet

    @property
    def position(self: Player) -> Position:
        return self.__position

    @color.setter
    def color(self: Player, color: int):
        self.__color = color

    @nb_reset_mouvement_point.setter
    def nb_reset_mouvement_point(self: Player, nb_reset_mouvement_point: int):
        self.__nb_reset_mouvement_point = nb_reset_mouvement_point

    @nb_reset_pieces.setter
    def nb_reset_pieces(self: Player, nb_reset_piecesf: int):
        self.__nb_reset_pieces = nb_reset_piecesf

    @nb_pieces.setter
    def nb_pieces(self: Player, nb_pieces: int):
        self.__nb_pieces = nb_pieces

    @mouvement_point.setter
    def mouvement_point(self: Player, mouvement_point: int):
        self.__mouvement_point = mouvement_point

    @list_objet.setter
    def list_objet(self: Player, list_objet: list[Objet]):
        self.__list_objet = list_objet

    @position.setter
    def position(self: Player, position: Position):
        self.__position = position

    def draw(self: Player, screen: pygame.Surface) -> None:
        """Dessine le joueur sur le plateau

        Args:
            self (Player): Joueur à dessiner
            screen (pygame.Surface): Ecran pygame sur lequel dessiner
        """
        image = pygame.image.load(self.sprites_path[self.color])
        new_size = (60, 60)
        position = (
            self.__position.x * 90 + 15,
            self.__position.y * 90 + 15,
        )
        screen.blit(pygame.transform.scale(image, new_size), position)

    def recup_objet(self: Player, objet: Objet) -> bool:
        """Récupération ou non d'un objet par le joueur

        Args:
            self (Player): Joueur
            objet (Objet): Objet à récupérer

        Returns:
            bool: True si l''objet à été récupéré, False sinon
        """
        if len(self.__list_objet) < 3 and objet is not None:
            self.__list_objet.append(objet)
            return True
        else:
            return False

    def draw_infos(self: Player, screen) -> None:
        """Ecrit les informations du joueur sur la bande d'infomations

        Args:
            self (Player): Joueur
            screen (_type_): Ecran pygame sur lequel écrire
        """
        font = pygame.font.Font(None, 32) #Nombre de mouvements restants
        text = font.render(
            f"Nombre de déplacements: {self.mouvement_point}", True, (255, 255, 255)
        )
        screen.blit(text, (905, 250))

        font = pygame.font.Font(None, 32) #Nombre de piéces restantes
        text = font.render(f"Nombre de piéces: {self.nb_pieces}", True, (255, 255, 255))
        screen.blit(text, (905, 300))

        for i, elt in enumerate(self.__list_objet): #Dessin des objets
            image = pygame.image.load(elt.sprite_path)
            new_size = (90, 90)
            position = (925 + i * 105, 350)
            screen.blit(pygame.transform.scale(image, new_size), position)

    def effacer_infos(self: Player, screen) -> None:
        """Efface les informations précédentes sur la bande d'infomations

        Args:
            self (Player): Joueur
            screen (_type_): Ecran pygame sur lequel effacer les informations
        """
        x, y, width, height = 900, 250, 500, 300
        black_color = (0, 0, 0)

        pygame.draw.rect(screen, black_color, (x, y, width, height)) #On remplace les écritures par un rectangle noir

    def giveturn(self: Player, plateau, screen, player_list):
        """Donne le tour à un joueur

        Args:
            self (Player): Joueur
            plateau (_type_): Plateau 
            screen (_type_): Ecran pygame sur lequel dessiner
            player_list (_type_): Liste des joueurs afin de les dessiner
        """
        turn: bool = True
        self.mouvement_point = self.__nb_reset_mouvement_point
        self.nb_pieces += self.__nb_reset_pieces

        image = pygame.image.load(self.sprites_path[self.color]) #Update du sprite du joueur actuel
        new_size = (150, 150)
        position = (
            950,
            65,
        )
        screen.blit(pygame.transform.scale(image, new_size), position)
        self.effacer_infos(screen)
        self.draw_infos(screen)
        pygame.display.flip()

        while turn:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_z: #Déplacement vers le haut
                            if self.mouvement_point > 0: #Vérification de la position
                                temp_pos: Position = Position(
                                    self.position.x, self.position.y
                                )
                                temp_pos.add_y(-1) #Simulation de la prochaine position
                                return_verif_cell: bool | Position = plateau.verif_cell(
                                    temp_pos
                                ) #Réponse de la cellule  l'arriver du joueur
                                if (
                                    isinstance(return_verif_cell, bool)
                                    and return_verif_cell 
                                ): #Si la cellule renvoit un booléen vrai
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.position.y -= 1 #Update de la position du joueur
                                    self.mouvement_point -= 1 #Décrémentation du nombre dee mouvement restant au joueur
                                elif isinstance(return_verif_cell, Position): #Si la réponse de la cellule est une position
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.mouvement_point -= 1
                                    self.position.y = return_verif_cell.y #On donne au joueur la position renvoyé par la cellule
                                    self.position.x = return_verif_cell.x

                        case pygame.K_s: #Déplacement vers le bas
                            if self.mouvement_point > 0: #Vérification de la position
                                temp_pos: Position = Position(
                                    self.position.x, self.position.y
                                )
                                temp_pos.add_y(1) #Simulation de la prochaine position
                                return_verif_cell: bool | Position = plateau.verif_cell(
                                    temp_pos
                                ) #Réponse de la cellule  l'arriver du joueur
                                if (
                                    isinstance(return_verif_cell, bool)
                                    and return_verif_cell 
                                ): #Si la cellule renvoit un booléen vrai
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.position.y += 1 #Update de la position du joueur
                                    self.mouvement_point -= 1 #Décrémentation du nombre dee mouvement restant au joueur
                                elif isinstance(return_verif_cell, Position): #Si la réponse de la cellule est une position
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.mouvement_point -= 1
                                    self.position.y = return_verif_cell.y #On donne au joueur la position renvoyé par la cellule
                                    self.position.x = return_verif_cell.x

                        case pygame.K_d: #Déplacement vers la droite 
                            if self.mouvement_point > 0: #Vérification de la position
                                temp_pos: Position = Position(
                                    self.position.x, self.position.y
                                )
                                temp_pos.add_x(1) #Simulation de la prochaine position
                                return_verif_cell: bool | Position = plateau.verif_cell(
                                    temp_pos
                                ) #Réponse de la cellule  l'arriver du joueur
                                if (
                                    isinstance(return_verif_cell, bool)
                                    and return_verif_cell 
                                ): #Si la cellule renvoit un booléen vrai
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.position.x += 1 #Update de la position du joueur
                                    self.mouvement_point -= 1 #Décrémentation du nombre dee mouvement restant au joueur
                                elif isinstance(return_verif_cell, Position): #Si la réponse de la cellule est une position
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.mouvement_point -= 1
                                    self.position.y = return_verif_cell.y #On donne au joueur la position renvoyé par la cellule
                                    self.position.x = return_verif_cell.x

                        case pygame.K_q: #Déplacement vers la gauche
                            if self.mouvement_point > 0: #Vérification de la position
                                temp_pos: Position = Position(
                                    self.position.x, self.position.y
                                )
                                temp_pos.add_x(-1) #Simulation de la prochaine position
                                return_verif_cell: bool | Position = plateau.verif_cell(
                                    temp_pos
                                ) #Réponse de la cellule  l'arriver du joueur
                                if (
                                    isinstance(return_verif_cell, bool)
                                    and return_verif_cell 
                                ): #Si la cellule renvoit un booléen vrai
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.position.x -= 1 #Update de la position du joueur
                                    self.mouvement_point -= 1 #Décrémentation du nombre dee mouvement restant au joueur
                                elif isinstance(return_verif_cell, Position): #Si la réponse de la cellule est une position
                                    plateau.free_cell(self.position) #Libération de la cellule sur lequel le joueur était
                                    self.mouvement_point -= 1
                                    self.position.y = return_verif_cell.y #On donne au joueur la position renvoyé par la cellule
                                    self.position.x = return_verif_cell.x

                        case pygame.K_1: #Utilisation d'un objet en position 1
                            if len(self.__list_objet) >= 1:
                                self.__list_objet[0].use(plateau, self, player_list)
                                del self.__list_objet[0]

                        case pygame.K_2: #Utilisation d'un objet en position 2
                            if len(self.__list_objet) >= 2:
                                self.__list_objet[1].use(plateau, self, player_list)
                                del self.__list_objet[1]

                        case pygame.K_3: #Utilisation d'un objet en position 3
                            if len(self.__list_objet) >= 3:
                                self.__list_objet[2].use(plateau, self, player_list)
                                del self.__list_objet[2]

                        case pygame.K_e: #Dépôt d'une piéces sur la cellule
                            if self.nb_pieces > 0:
                                self.nb_pieces -= 1
                                plateau.coin_deposit(self.position, self.color)

                        case pygame.K_f: #Terminer le tour
                            plateau.spawn_objet()
                            plateau.reset_cells()
                            turn = False
                elif event.type == pygame.QUIT:
                    exit()

                plateau.give_objet(self) #Dons de l'objet sur la cellule du joueur (si il y en a un)

                #Update de l'affichage
                plateau.draw(screen)
                for player in player_list:
                    player.draw(screen)

                self.effacer_infos(screen)
                self.draw_infos(screen)

                pygame.display.flip()
