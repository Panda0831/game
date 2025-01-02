import pygame
import time
import random

pygame.init()


blanc = (255, 255, 255)
jaune = (255, 255, 102)
noir = (0, 0, 0)
rouge = (213, 50, 80)
vert = (0, 255, 0)
bleu = (50, 153, 213)


largeur = 300
hauteur = 200


fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption('Snake Game')


horloge = pygame.time.Clock()
vitesse_snake = 8


taille_snake = 10


police_score = pygame.font.SysFont("bahnschrift", 35)
police_message = pygame.font.SysFont("comicsansms", 50)

def score(score):
    valeur = police_score.render("Score: " + str(score), True, noir)
    fenetre.blit(valeur, [0, 0])

def notre_snake(taille_snake, liste_snake):
    for x in liste_snake:
        pygame.draw.rect(fenetre, noir, [x[0], x[1], taille_snake, taille_snake])

def message(msg, couleur):
    mesg = police_message.render(msg, True, couleur)
    fenetre.blit(mesg, [largeur / 6, hauteur / 3])

def jeu():
    game_over = False
    game_close = False

    x1 = largeur / 2
    y1 = hauteur / 2

    x1_change = 0
    y1_change = 0

    liste_snake = []
    longueur_snake = 1

    nourriturex = round(random.randrange(0, largeur - taille_snake) / 10.0) * 10.0
    nourriturey = round(random.randrange(0, hauteur - taille_snake) / 10.0) * 10.0

    while not game_over:

        while game_close:
            fenetre.fill(blanc)
            message("You Lost! Press Q-Quit or C-Play Again", rouge)
            score(longueur_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        jeu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -taille_snake
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = taille_snake
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -taille_snake
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = taille_snake
                    x1_change = 0

        if x1 >= largeur or x1 < 0 or y1 >= hauteur or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        fenetre.fill(bleu)
        pygame.draw.rect(fenetre, vert, [nourriturex, nourriturey, taille_snake, taille_snake])
        notre_snake(taille_snake, liste_snake)
        score(longueur_snake - 1)

        liste_snake.append([x1, y1])
        if len(liste_snake) > longueur_snake:
            del liste_snake[0]

        for x in liste_snake[:-1]:
            if x == [x1, y1]:
                game_close = True

        pygame.display.update()

        if x1 == nourriturex and y1 == nourriturey:
            nourriturex = round(random.randrange(0, largeur - taille_snake) / 10.0) * 10.0
            nourriturey = round(random.randrange(0, hauteur - taille_snake) / 10.0) * 10.0
            longueur_snake += 1

        horloge.tick(vitesse_snake)

    pygame.quit()
    quit()

jeu()
