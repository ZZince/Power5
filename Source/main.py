import pygame
from Plateau import Plateau
from Position import Position
from Player import Player

pygame.init()

screen = pygame.display.set_mode((1250, 900))
pygame.display.set_caption("Power5")

gagnant = None
font = pygame.font.Font(None, 36)

white = (255, 255, 255)
black = (0, 0, 0)

options = [2, 3, 4]
selected_option = options[0]

button_positions = [(500, 400), (600, 400), (700, 400)]

text = font.render(f"Choisissez le nombre de joueurs :", True, white)
text_rect = text.get_rect(center=(635, 375))
screen.blit(text, text_rect)

for i, (x, y) in enumerate(button_positions):  #Préparation de l'écran titre
    pygame.draw.rect(screen, white, (x, y, 50, 50))
    button_text = font.render(str(options[i]), True, black)
    button_text_rect = button_text.get_rect(center=(x + 25, y + 25))
    screen.blit(button_text, button_text_rect)


running = True
while running:  #Affichage de l'écran titre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            for i, (x, y) in enumerate(button_positions):
                if x < event.pos[0] < x + 50 and y < event.pos[1] < y + 50:
                    selected_option = options[i]
                    running = False

    pygame.display.flip()

plateau: Plateau = Plateau() #Création aléatoire du plateau
player_list: list[Player] = []
for i in range(selected_option): #Création des joueurs
    player_list.append(Player(i + 1, position=Position()))

for player in player_list:
    for cell in plateau.list_cell:
        if cell.position == player.position:
            cell.player_arrived(True, plateau._list_pos_trou_blanc) #Initialisation des cellules occupées par les joueurs
            break

font = pygame.font.Font(None, 36)
text = font.render("Tour actuel: ", True, (255, 255, 255))  #Texte fixe 
screen.blit(text, (950, 15))

plateau.spawn_objet() #Premiére création des objets
plateau.draw(screen) #Dessiner le plateau
for player in player_list: #Dessiner les joueurs
    player.draw(screen)
pygame.display.flip()

while True:
    for player in player_list: #Donner le tour à chaque joueur
        player.giveturn(plateau, screen, player_list)

    plateau.update_color() #Calcul des captures de cases
    pygame.display.flip()
    gagnant = plateau.verif_gagnant() #Vérification du gagnant
    plateau.clear_all_pieces() #Reset des piéces sur les cases
    plateau.draw(screen)
    for player in player_list:
        player.draw(screen)
    if gagnant is not None:
        break

while True:
    for event in pygame.event.get(): #Si on a un gagnant, on change de boucle pour bloquer le jeu
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
    text = font.render(f"Le joueur {gagnant} à gagné !", True, white) #Affichage du joueur gagnant
    text_rect = text.get_rect(center=(1050, 500))
    screen.blit(text, text_rect)
    pygame.display.flip()
