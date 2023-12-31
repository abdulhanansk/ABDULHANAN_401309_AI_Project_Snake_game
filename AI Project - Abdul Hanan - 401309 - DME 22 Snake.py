import tkinter as tk
import random

# Constants
GAME_SCREEN_WIDTH = 500
GAME_SCREEN_HEIGHT = 500
SNAKE_SPEED = 200
BOX_SPACE_SIZE = 20
SNAKE_BODY_SIZE = 3
COLOR_SNAKE = "#00FF00"
COLOR_FOOD = "red"
COLOR_BACKGROUND = "#000000"

score = 0
direction = 'down'
canvas = None
snake = None
food = None
label = None
label_length_of_snake = None


class Snake:
    def __init__(self):
        self.body_size = SNAKE_BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, SNAKE_BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + BOX_SPACE_SIZE, y + BOX_SPACE_SIZE, fill=COLOR_SNAKE,
                                             tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        self.coordinates = []
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, (GAME_SCREEN_WIDTH - BOX_SPACE_SIZE) // BOX_SPACE_SIZE) * BOX_SPACE_SIZE
        y = random.randint(0, (GAME_SCREEN_HEIGHT - BOX_SPACE_SIZE) // BOX_SPACE_SIZE) * BOX_SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + BOX_SPACE_SIZE, y + BOX_SPACE_SIZE, fill=COLOR_FOOD, tag="food")


def next_turn():
    global direction, score, snake, food

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= BOX_SPACE_SIZE
    elif direction == "down":
        y += BOX_SPACE_SIZE
    elif direction == "left":
        x -= BOX_SPACE_SIZE
    elif direction == "right":
        x += BOX_SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + BOX_SPACE_SIZE, y + BOX_SPACE_SIZE, fill=COLOR_SNAKE)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Points:{}".format(score))
        label_length_of_snake.config(text="Length of Snake:{}".format(score + 3))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SNAKE_SPEED, next_turn)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_SCREEN_WIDTH:
        return True
    elif y < 0 or y >= GAME_SCREEN_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    restart_button = tk.Button(window, text="Restart", command=restart_game)
    restart_button.pack(pady=20)


def restart_game():
    global score, direction, snake, food

    score = 0
    direction = 'down'

    canvas.delete("all")
    snake = Snake()
    food = Food()

    label.config(text="Points:{}".format(score))
    label.pack()
    label_length_of_snake.config(text="Length of Snake:{}".format(score + 3))

    next_turn()


def main():
    global canvas, snake, food, label, label_length_of_snake, direction, window

    window = tk.Tk()

    label = tk.Label(window, text="Points:{}".format(score), font=('Comic Sans', 20))
    label.pack()

    label_length_of_snake = tk.Label(window, text="Length of Snake:{}".format(score + 3), font=('Comic Sans', 20))
    label_length_of_snake.pack()

    canvas = tk.Canvas(window, bg=COLOR_BACKGROUND, height=GAME_SCREEN_HEIGHT, width=GAME_SCREEN_WIDTH)
    canvas.pack()

    window.title("Snake game")
    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind("<KeyPress>", change_direction)
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    snake = Snake()
    food = Food()

    direction = 'down'

    next_turn()

    window.mainloop()


if __name__ == "__main__":
    main()
