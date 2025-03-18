#include <ncurses.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define WIDTH 30
#define HEIGHT 20
#define DELAY 100000 // Vitesse du jeu (en microsecondes)

typedef struct
{
    int x, y;
} Point;

typedef struct
{
    Point body[100]; // Corps du serpent
    int length;
    int dx, dy; // Direction
} Snake;

Point food;
Snake snake;

// Initialisation du jeu
void init_game()
{
    initscr();
    noecho();
    curs_set(FALSE);
    keypad(stdscr, TRUE);
    timeout(100); // Attente input

    // Initialiser le serpent
    snake.length = 3;
    snake.body[0] = (Point){WIDTH / 2, HEIGHT / 2};
    snake.body[1] = (Point){WIDTH / 2 - 1, HEIGHT / 2};
    snake.body[2] = (Point){WIDTH / 2 - 2, HEIGHT / 2};
    snake.dx = 1;
    snake.dy = 0;

    // Placer la nourriture
    srand(time(0));
    food.x = rand() % WIDTH;
    food.y = rand() % HEIGHT;
}

// Affichage du jeu
void draw_game()
{
    clear();

    // Dessiner le serpent
    for (int i = 0; i < snake.length; i++)
    {
        mvprintw(snake.body[i].y, snake.body[i].x, "O");
    }

    // Dessiner la nourriture
    mvprintw(food.y, food.x, "X");

    refresh();
}

// Vérifier collision
int check_collision()
{
    // Collision avec le mur
    if (snake.body[0].x < 0 || snake.body[0].x >= WIDTH ||
        snake.body[0].y < 0 || snake.body[0].y >= HEIGHT)
    {
        return 1;
    }

    // Collision avec lui-même
    for (int i = 1; i < snake.length; i++)
    {
        if (snake.body[0].x == snake.body[i].x &&
            snake.body[0].y == snake.body[i].y)
        {
            return 1;
        }
    }
    return 0;
}

// Mise à jour du jeu
void update_game()
{
    // Déplacement du serpent
    for (int i = snake.length - 1; i > 0; i--)
    {
        snake.body[i] = snake.body[i - 1];
    }

    snake.body[0].x += snake.dx;
    snake.body[0].y += snake.dy;

    // Vérifier si le serpent mange la nourriture
    if (snake.body[0].x == food.x && snake.body[0].y == food.y)
    {
        snake.length++;
        food.x = rand() % WIDTH;
        food.y = rand() % HEIGHT;
    }
}

// Lire les entrées du joueur
void handle_input()
{
    int ch = getch();
    switch (ch)
    {
    case 'z':
        snake.dx = 0;
        snake.dy = -1;
        break;
    case 's':
        snake.dx = 0;
        snake.dy = 1;
        break;
    case 'q':
        snake.dx = -1;
        snake.dy = 0;
        break;
    case 'd':
        snake.dx = 1;
        snake.dy = 0;
        break;
    }
}

// Boucle principale du jeu
void game_loop()
{
    while (1)
    {
        draw_game();
        handle_input();
        update_game();

        if (check_collision())
        {
            break; // Fin du jeu
        }

        usleep(DELAY);
    }
}

int main()
{
    init_game();
    game_loop();

    // Fin du jeu
    endwin();
    printf("Game Over !\n");

    return 0;
}
