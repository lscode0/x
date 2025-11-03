
import tkinter as tk
import random

# Game constants
WIDTH = 500
HEIGHT = 500
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    if x < 0:
        x = WIDTH - SPACE_SIZE
    elif x >= WIDTH:
        x = 0
    if y < 0:
        y = HEIGHT - SPACE_SIZE
    elif y >= HEIGHT:
        y = 0

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def show_high_scores():
    global high_scores_window
    try:
        with open("C:\\Users\\L\\Desktop\\gierka\\snake_game\\high_scores.txt", "r") as file:
            scores = file.readlines()
    except FileNotFoundError:
        scores = []

    scores = [score.strip().split(",") for score in scores]
    scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)

    if high_scores_window is None or not high_scores_window.winfo_exists():
        high_scores_window = tk.Toplevel(window)
        high_scores_window.title("High Scores")
        high_scores_window.resizable(False, False)
    else:
        for widget in high_scores_window.winfo_children():
            widget.destroy()

    high_scores_label = tk.Label(high_scores_window, text="High Scores", font=('consolas', 30))
    high_scores_label.pack()

    for i, (name, score) in enumerate(scores[:10]):
        score_label = tk.Label(high_scores_window, text=f"{i+1}. {name}: {score}", font=('consolas', 20))
        score_label.pack()

def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 100,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    name_label = tk.Label(window, text="Enter your name:", font=('consolas', 20))
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 - 20, window=name_label)

    name_entry = tk.Entry(window, font=('consolas', 20))
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 20, window=name_entry)

    save_button = tk.Button(window, text="Save Score", font=('consolas', 20), command=lambda: save_score(name_entry.get()))
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 70, window=save_button)

    play_again_button = tk.Button(window, text="Play Again", font=('consolas', 20), command=restart_game)
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 120, window=play_again_button)

def save_score(name):
    with open("C:\\Users\\L\\Desktop\\gierka\\snake_game\\high_scores.txt", "a") as file:
        file.write(f"{name},{score}\n")
    show_high_scores()

def restart_game():
    global score, direction, snake, food
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    canvas.delete(tk.ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)

window = tk.Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'
high_scores_window = None

label = tk.Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

def change_speed(speed):
    global SPEED
    SPEED = 210 - int(speed) * 10

speed_slider = tk.Scale(window, from_=1, to=20, orient=tk.HORIZONTAL, label="Speed", command=change_speed)
speed_slider.set(10)
speed_slider.pack()

high_scores_button = tk.Button(window, text="High Scores", font=('consolas', 20), command=show_high_scores)
high_scores_button.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

global snake, food
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
