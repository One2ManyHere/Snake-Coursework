# Made with 1920x1080 resolution.
# from tkinter import Tk, Canvas, Label, Button, PhotoImage, Style
from tkinter import *
import random
import os.path
import time

# Global Variables
direction = ""
score = 0
scores_names = []
scores = []
game_speed = 90
split_scores = []
walls_enabled = False
paused = False
boosted = False
colours = []
lives = 1


def get_settings():

    if os.path.isfile("settings.txt"):  # If they have saved settings
        try:
            file = open("settings.txt", "r")
            all_lines = file.readlines()

            for i in range(len(all_lines)):
                all_lines[i] = all_lines[i].replace("\n", "")
            saved_colours = [all_lines[2], all_lines[3], all_lines[4],
                             all_lines[5], all_lines[6]]

            if all_lines[1] == "True":
                keys = True
            else:
                keys = False

            file.close()
            return (int(all_lines[0]), keys, saved_colours)

        except:
            return (30, True,
                    ["red", "purple", "#00ff00", "steel blue", "blue"])
    else:
        # Returns default values. Size: ArrowKeys, Colours
        return (30, True, ["red", "purple", "#00ff00", "steel blue", "blue"])


def rules():

    def play():

        rules_screen.destroy()
        play_game()

    def display_cheats():

        cheats = []
        cheats_button.destroy()
        cheats_border = Frame(rules_screen, highlightbackground="black",
                              highlightthickness=2, bd=3,
                              relief="solid", bg="gold")

        cheats.append(Label(cheats_border, text="'1': Extra Life      "))
        cheats.append(Label(cheats_border, text="'2': Decrease Speed"))
        cheats.append(Label(cheats_border, text="'3': Increase Speed"))

        for i in range(len(cheats)):
            cheats[i].config(font=("Arial", 15), bg="gold", fg="white",)
            cheats[i].grid(row=i+1, column=1)
        cheats_border.grid(row=1, column=1)

    def create_labels():

        directions = []
        direction_border = Frame(rules_screen, highlightbackground="black",
                                 highlightthickness=2, bd=3, relief="solid")

        title_label = Label(rules_screen, text="Rules", font=("Arial", 25),
                            relief="solid", bd=4)
        title_label.grid(row=0, column=1, pady=10)

        if arrow_keys:
            directions.append(Label(direction_border, text="↑: Turn Up"))
            directions.append(Label(direction_border, text="↓: Turn Down"))
            directions.append(Label(direction_border, text="←: Turn Left"))
            directions.append(Label(direction_border, text="→: Turn Right"))
        else:
            directions.append(Label(direction_border, text="W: Turn Up"))
            directions.append(Label(direction_border, text="S: Turn Down"))
            directions.append(Label(direction_border, text="A: Turn Left"))
            directions.append(Label(direction_border, text="D: Turn Right"))

        for i in range(len(directions)):
            directions[i].config(font=("Arial", 15), padx=20, pady=10)
            directions[i].grid(row=i+1, column=0)
        direction_border.grid(row=1, column=0, padx=20)

        special_keys = []
        special_border = Frame(rules_screen, highlightbackground="black",
                               highlightthickness=2, bd=3, relief="solid")
        special_keys.append(Label(special_border, text="<Escape>: Pause"))
        special_keys.append(Label(special_border, text="<B>: Boss Key"))
        special_keys.append(Label(special_border, text="<Space>: Boost!"))

        for i in range(len(special_keys)):
            special_keys[i].config(font=("Arial", 15), padx=20, pady=10)
            special_keys[i].grid(row=i+1, column=2)
        special_border.grid(row=1, column=2, padx=20)

    rules_screen = Tk()
    rules_screen.title("Rules")

    width = int(rules_screen.winfo_screenwidth() / 1.5)
    height = int(rules_screen.winfo_screenheight() / 1.5)
    rules_screen.geometry(f"{width}x{height}")
    rules_screen.config(bg="#00ff00")

    cheats_button = Button(rules_screen, padx=width/4, bg="#00ff00", bd=0,
                           relief="sunken", command=display_cheats)
    cheats_button.grid(row=1, column=1)

    create_labels()

    play_button = Button(rules_screen, text="Play Game",
                         padx=width / 4, pady=height / 25,
                         bg="#ff0080", fg="white",
                         font=("Arial", 15), command=play)
    play_button.grid(row=5, column=1, pady=20)


def play_game():

    global snake_size

    def set_dimensions(width, height):

        root = Tk()  # Initialises new game_window
        root.title("Coursework Snake Game")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()  # Gets computers screen-size

        # Calculates the center of the screen
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))

        # root.geometry('%dx%d+%d+%d' %(width, height, x, y))
        root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
        return root

    def set_special_keys():
        canvas.bind("<Escape>", pause_key)
        canvas.bind("<space>", boost_key)
        canvas.bind("b", boss_key)
        canvas.bind("1", extra_life)
        canvas.bind("2", speed_down)
        canvas.bind("3", speed_up)
        canvas.focus_set()

    def set_arrow_bindings():

        canvas.bind("<Left>", left_key)  # Sets <- key to left_key function.
        canvas.bind("<Right>", right_key)
        canvas.bind("<Up>", up_key)
        canvas.bind("<Down>", down_key)
        canvas.focus_set()

    def set_WASD_bindings():

        canvas.bind("a", left_key)  # Sets "a" key to left_key, same direction.
        canvas.bind("d", right_key)
        canvas.bind("w", up_key)
        canvas.bind("s", down_key)
        canvas.focus_set()

    def place_food():  # Places the first food block

        global food, food_x, food_y
        #  Rectangle = (x1,y1,x2,y2)
        try:
            food = canvas.create_rectangle(0, 0, snake_size, snake_size,
                                           fill=colours[4])
        except:  # Default value for colours if file is wrong.
            food = canvas.create_rectangle(0, 0, snake_size, snake_size,
                                           fill="steel blue")

        food_x = random.randint(0, width-snake_size)
        food_y = random.randint(0, height-snake_size)  # Generates X,Y coords
        canvas.move(food, food_x, food_y)  # Places food on canvas.

    def left_key(event):

        global direction
        direction = "left"

    def right_key(event):

        global direction
        direction = "right"

    def up_key(event):

        global direction
        direction = "up"

    def down_key(event):

        global direction
        direction = "down"

    def pause_key(event):

        global colours
        global paused
        paused = True

        def unpause(event):

            global paused
            paused = False
            canvas.delete("pause_info")
            canvas.bind("<Escape>", pause_key)  # Back to normal

        canvas.bind("<Escape>", unpause)  # Rebinds pause button to unpause
        canvas.focus_set()
        try:
            canvas.create_text(width/2, height/2,
                               text="Paused...\nPress ESC to unpause",
                               font=("Arial", 15), fill=colours[3],
                               tag="pause_info")  # Tag = specific deletion.
        except:
            canvas.create_text(width/2, height/2,
                               text="Paused...\nPress ESC to unpause",
                               font=("Arial", 15),
                               fill="blue", tag="pause_info",)

    def boost_key(event):
        global boosted
        boosted = True

    def boss_key(event):

        def unboss(event):
            global paused
            paused = False
            boss = False
            bosscanvas.destroy()
            canvas.bind("b", boss_key)

        global paused
        paused = True
        boss = True
        picture = PhotoImage(file="document.png")

        canvas.bind("b", unboss)
        canvas.focus_set()

        if paused is True and boss is True:
            bosscanvas = Canvas(width=1920, height=1025, bg="black")
            bosscanvas.place(x=0, y=0)
            picture = PhotoImage(file="document.png")
            bosscanvas.create_image(0, 0, image=picture, anchor=NW)
            bosscanvas.mainloop()  # Runs new canvas on top.

    def extra_life(event):

        global colours
        global lives

        lives += 1

        canvas.delete("lives_text")
        try:

            canvas.create_text(width/5, 10, fill=colours[3],
                               text=f"Lives Remaining: {lives}",
                               font=("Arial", 20), tag="lives_text")
        except:
            canvas.create_text(width/5, 10, fill="blue",
                               text=f"Lives Remaining: {lives}",
                               font=("Arial", 20), tag="lives_text")

    def speed_down(event):

        global game_speed
        game_speed += 5

    def speed_up(event):

        global game_speed
        if game_speed > 5:
            game_speed -= 5

    def grow_snake():

        final_body = len(snake)-1
        #  Will be 2 coordinates (x1,y1)(x2,y2)
        final_body_pos = canvas.coords(snake[final_body])

        try:
            snake.append(canvas.create_rectangle(0, 0,
                                                 snake_size, snake_size,
                                                 fill=colours[1]))
            # Creates a new snake block (not placed on snake)

        except:
            snake.append(canvas.create_rectangle(0, 0,
                                                 snake_size, snake_size,
                                                 fill="red"))

        if direction == "left":  # Placed to right of last body part
            canvas.coords(snake[final_body+1],
                          final_body_pos[0] + snake_size,
                          final_body_pos[1],
                          final_body_pos[2] + snake_size,
                          final_body_pos[3])

        elif direction == "right":  # Placed to the left of last body piece
            canvas.coords(snake[final_body+1],
                          final_body_pos[0] - snake_size,
                          final_body_pos[1],
                          final_body_pos[2] - snake_size,
                          final_body_pos[3])

        elif direction == "up":  # Placed to bottom of last body piece
            canvas.coords(snake[final_body+1],
                          final_body_pos[0],
                          final_body_pos[1] + snake_size,
                          final_body_pos[2],
                          final_body_pos[3] + snake_size)

        elif direction == "down":  # Placed to top of last body piece
            canvas.coords(snake[final_body+1],
                          final_body_pos[0],
                          final_body_pos[1] - snake_size,
                          final_body_pos[2],
                          final_body_pos[3] - snake_size)

    # The canvas works so tranlsation from (0,0) to (15,15)
    # Involves moving 15 to the right and 15 downwards.

    def move_food():  # Places food after snake eats it.

        global food, food_x, food_y
        canvas.move(food, food_x * (-1), food_y * (-1))
        food_x = random.randint(0, width-snake_size)
        food_y = random.randint(0, height-snake_size)
        canvas.move(food, food_x, food_y)

        # Incrementing Score:
        global score
        score += 1
        txt = "Score:" + str(score)
        canvas.itemconfigure(scoreText, text=txt,)

        # Increasing Speed
        global game_speed

        if game_speed > 60:
            game_speed -= 1  # Allows gradual speedup,

    def overlapping(a, b):  # Collision Checking Positions[a] and Positions[b]
        if a[0] < b[2] and a[1] < b[3] and a[2] > b[0] and a[3] > b[1]:
            return True
        return False

    def move_snake():

        global lives
        global direction

        def follow_head(positions, snake):

            if not paused:
                for i in range(1, len(snake)):
                    positions.append(canvas.coords(snake[i]))  # All coords.

                for i in range(len(snake)-1):  # Allows body to follow the head
                    canvas.coords(snake[i+1],
                                  positions[i][0],
                                  positions[i][1],
                                  positions[i][2],
                                  positions[i][3])

        def constant_movement():

            if paused:
                canvas.move(snake[0], 0, 0)
            elif direction == "left":
                canvas.move(snake[0], -snake_size, 0)
            elif direction == "right":
                canvas.move(snake[0], snake_size, 0)
            elif direction == "up":
                canvas.move(snake[0], 0, -snake_size)
            elif direction == "down":
                canvas.move(snake[0], 0, snake_size)

        def check_boundary(game_over):

                if positions[0][0] < 0:  # Left Wall

                    if not walls_enabled:
                        canvas.coords(snake[0], width, positions[0][1],
                                      width-snake_size, positions[0][3])
                    else:
                        game_over = True

                elif positions[0][2] > width:  # Right Wall

                    if not walls_enabled:
                        canvas.coords(snake[0], 0-snake_size, positions[0][1],
                                      0, positions[0][3])  # Appears L wall.
                    else:
                        game_over = True

                elif positions[0][3] > height:  # Top wall

                    if not walls_enabled:
                        canvas.coords(snake[0], positions[0][0], 0-snake_size,
                                      positions[0][2], 0)  # Appears bottom.
                    else:
                        game_over = True

                elif positions[0][1] < 0:  # Bottom Wall

                    if not walls_enabled:
                        canvas.coords(snake[0], positions[0][0], height,
                                      positions[0][2], height-snake_size)
                    else:
                        game_over = True

        def display_game_over():

            def text():

                text = ""
                for i in range(int(width / 40)):
                    text += " "
                    space_filler_text = text
                    space_filler = Label(game_over_screen,
                                         text=space_filler_text,
                                         bg="#00ff00")
                    space_filler.grid(row=0, column=0)

                    text2 = (f"Your final score was {score}!")
                    score_label = Label(game_over_screen, text=text2,
                                        font=("Arial", 25), pady=height / 40,
                                        relief="solid", borderwidth=2)

                    score_label.grid(row=0, column=1, pady=height / 30)

            def return_to_menu():
                global game_speed
                game_speed = 90   # Resets speed value which was last game.

                game_over_screen.destroy()
                game_window.destroy()
                menu()

            def save_scores():

                def save_to_file():

                    global score
                    name = save_to_file.get_name.get().strip()

                    if (len(name) > 15):
                        save_scores.label1.config(text="Name too long!")
                    else:
                        name_score = [name, score]

                        if (len(scores_names) == 1):
                            file = open("Leaderboard.txt", "a")
                            file.write(f"{name_score[0]},{name_score[1]}\n")
                            file.close()
                        else:
                            for i in range(0, len(split_scores)):
                                # If new score > current pos score
                                # Insert the new score at this position.
                                if name_score[1] >= int(split_scores[i][1]):
                                    split_scores.insert(i, name_score)

                                    congrats_label = Label(game_over_screen,
                                                           text=f"That is " +
                                                           f"{i+1} " +
                                                           "on the " +
                                                           "leaderboard.",
                                                           pady=height / 10,
                                                           font=("Arial", 25),
                                                           bg="white",
                                                           fg="green")

                                    congrats_label.grid(row=4, column=1)
                                    break
                            # If lowest score, still adds.
                            if name_score not in split_scores:
                                split_scores.append(name_score)

                            file = open("Leaderboard.txt", "w")
                            file.write("Leaderboards:\n")
                            for i in range(0, len(split_scores)):
                                file.write(f"{split_scores[i][0]}," +
                                           f"{split_scores[i][1]}\n")
                            file.close()

                save_scores.label1 = Label(game_over_screen,
                                           borderwidth="3", relief="solid",
                                           text="Enter Name:")
                save_scores.label1.grid(row=3, pady=10)

                save_to_file.get_name = Entry(game_over_screen)
                save_to_file.get_name.grid(row=3, column=1, pady=10)

                save_button = Button(game_over_screen, text="Save",
                                     command=save_to_file)
                save_button.grid(row=3, column=2, pady=10)

            def create_buttons():

                button_border = Frame(game_over_screen,
                                      highlightbackground="black",
                                      highlightthickness=2,
                                      bd=3, relief="solid")

                save_score_button = Button(button_border, text="Save Score?",
                                           padx=width / 3, pady=height / 25,
                                           font=("Arial", 20), fg="white",
                                           bg="#002700", command=save_scores)
                save_score_button.grid(row=1, column=1)

                return_button = Button(button_border, text="Return to Menu",
                                       padx=width / 3 - 15,
                                       pady=height / 25,
                                       font=("Arial", 20),
                                       fg="white", bg="#002700",
                                       command=return_to_menu)
                return_button.grid(row=2, column=1)
                button_border.grid(row=1, column=1)

            time.sleep(1)
            game_over_screen = Tk()
            game_over_screen.title("Game Over")
            game_over_screen.config(bg="#00ff00")
            width = int(game_over_screen.winfo_screenwidth() / 1.5)
            height = int(game_over_screen.winfo_screenheight() / 1.5)

            game_over_screen.geometry(f"{width}x{height}")

            text()
            create_buttons()

        game_over = False

        canvas.pack()
        positions = []
        positions.append(canvas.coords(snake[0]))  # Pos Head(x1,y1)(x2,y2)

        check_boundary(game_over)

        positions.clear()
        positions.append(canvas.coords(snake[0]))

        constant_movement()

        head_position = canvas.coords(snake[0])
        food_position = canvas.coords(food)

        if overlapping(head_position, food_position):  # == True
            move_food()
            grow_snake()

        for i in range(1, len(snake)):
            next_body = canvas.coords(snake[i])

            # If head collides with body:
            if overlapping(head_position, next_body):
                lives -= 1

                canvas.coords(snake[0], 0, 0, snake_size, snake_size)
                direction = "right"

                canvas.delete("lives_text")
                try:  # Updates lives
                    canvas.create_text(width / 5, 10, fill=colours[3],
                                       text=f"Lives Remaining: {lives}",
                                       font=("Arial", 20),
                                       tag="lives_text")
                except:
                    canvas.create_text(width / 5, 10, fill="blue",
                                       text=f"Lives Remaining: {lives}",
                                       font=("Arial", 20),
                                       tag="lives_text")

            if lives == 0:
                game_over = True
                canvas.create_text(width / 2, height / 2,
                                   fill="white",
                                   font="Times 20 italic bold",
                                   text="Game Over!")
                canvas.config(bg="red")

        follow_head(positions, snake)

        global boosted

        if not game_over and not boosted:
            game_window.after(game_speed, move_snake)
        elif boosted:
            game_window.after(int(game_speed / 2), move_snake)  # 2x Speed

            boosted = False  # Means boost must be held
        else:
            display_game_over()
            lives = 1

    width = 1920  # Dimensions of game_window.
    height = 1025
    game_window = set_dimensions(width, height)

    # Sets property width to variable width
    try:
        canvas = Canvas(game_window, bg=colours[2],
                        width=width, height=height)
    except:
        canvas = Canvas(game_window, bg="white",
                        width=width, height=height)

    snake = []

    # Creates the head of the snake     Point (15,15) size (30,30)
    try:
        snake.append(canvas.create_rectangle(snake_size, snake_size,
                                             snake_size * 2,
                                             snake_size * 2,
                                             fill=colours[0]))
    except:
        snake.append(canvas.create_rectangle(snake_size, snake_size,
                                             snake_size * 2,
                                             snake_size * 2,
                                             fill="blue"))

    # Score Text
    global score
    score = 0
    text = "Score:" + str(score)

    try:
        scoreText = canvas.create_text(width / 2, 15,
                                       fill=colours[3],
                                       font=("Arial", 25),
                                       text=text,)  # Dislplays current score

        canvas.create_text(width / 5, 10, fill=colours[2],  # Cheat text.
                           text=f"Lives Remaining: {lives}",
                           font=("Arial", 20), tag="lives_text")
    except:

        scoreText = canvas.create_text(width / 2, 15,
                                       fill="blue",
                                       font=("Arial", 25),
                                       text=text,)  # Displays current score

        canvas.create_text(width / 5, 10, fill="blue",  # Cheat Text
                           text=f"Lives Remaining: {lives}",
                           font=("Arial", 20), tag="lives_text")

    set_special_keys()

    if arrow_keys:  # Uses Global variable, assigned in Settings
        set_arrow_bindings()
    else:
        set_WASD_bindings()

    global direction
    direction = "right"  # Initial Direction

    place_food()
    move_snake()

    game_window.mainloop()  # Waits for events in game_window


def display_settings():

    def space_filler():  # Allows text in grid to be centered.

        text = ""
        for i in range(int(width / 33)):
            text += " "
        space_filler_text = text
        space_filler = Label(settings, text=space_filler_text,
                             bg="#00b300")
        space_filler.grid(row=0, column=0)

    def return_to_menu():

        def save_settings():

            global snake_size, arrow_keys, colours

            file = open("settings.txt", "w")  # Overwrites old settings
            file.write(f"{snake_size}\n{arrow_keys}\n")
            for i in range(len(colours)):
                file.write(f"{colours[i]}\n")

        save_settings()
        settings.destroy()  # Closes current Window, Opens Menu
        menu()

    def change_size():  # Allows user to configure how large the canvas is.

        global snake_size

        if snake_size == 45:  # Bigger snake_size = Smaller Game size.
            snake_size = 38
            create_buttons.game_size_button.config(text="Map Size: Small",
                                                   padx=width / 3)
        elif snake_size == 38:
            snake_size = 30
            create_buttons.game_size_button.config(text="Map Size: Normal",
                                                   padx=width / 3 - 12)

        elif snake_size == 30:
            snake_size = 20
            create_buttons.game_size_button.config(text="Map Size: Big",
                                                   padx=width / 3 + 8)

        elif snake_size == 20:
            snake_size = 10
            create_buttons.game_size_button.config(text="Map Size: Very Big",
                                                   padx=width / 3 - 15)

        else:
            snake_size = 45
            create_buttons.game_size_button.config(text="Map Size: Very Small",
                                                   padx=width / 3 - 25)

    def change_keybinds():  # Where WASD/Arrows are chosen

        global arrow_keys
        arrow_keys = not arrow_keys
        if arrow_keys:
            create_buttons.controls_button.config(text="Controls: Arrow Keys")
        else:
            #  Changes label text to signify to user what they chose.
            create_buttons.controls_button.config(text="Controls: WASD Keys")

    def change_colours():

        def save_colours(colours_num):

            global colours
            # Copies all entry values into array
            for i in range(0, colours_num):
                colours[i] = entries[i].get()

            colour_window.destroy()

        colour_window = Tk()
        colour_window.title("Colour Configuration")
        colour_window.config(bg="White")
        width = int(colour_window.winfo_screenwidth() / 4)
        height = int(colour_window.winfo_screenheight() / 4)

        colour_window.geometry(f"{width}x{height}")

        title_label = Label(colour_window, text="Colour Config ",
                            font=("Arial", 25), relief="solid",
                            borderwidth=2,)
        title_label.grid(row=0, column=0, pady=height / 25,)

        colour_choices = []
        descriptions = []
        entries = []

        border = Frame(colour_window, bd=2, highlightbackground="black",
                       relief="solid",)

        descriptions.append(Label(border, text="Snake head colour: ",
                                  font=("Arial", 15), fg="red"))
        descriptions.append(Label(border, text="Snake body colour: ",
                                  font=("Arial", 15), fg="red"))
        descriptions.append(Label(border, text="Game canvas colour: ",
                                  font=("Arial", 15), fg="red"))
        descriptions.append(Label(border, text="Score label colour: ",
                                  font=("Arial", 15), fg="red"))
        descriptions.append(Label(border, text="Food colour",
                                  font=("Arial", 15), fg="red"))

        border.grid(row=1, column=0, padx=50)

        for i in range(len(descriptions)):
            descriptions[i].grid(row=i+1, column=0,)
            entries.append(Entry(border))  # Creates an entry for each
            entries[i].grid(row=i+1, column=1)

        submit_colours_button = Button(border, text="Submit Colours",
                                       command=lambda:
                                       (save_colours(len(descriptions))))
        submit_colours_button.grid(row=len(descriptions) + 1, column=0)

    def create_buttons():

        # Create_buttons."name" allows access in other functions.
        # Grid system allows them to be placed well.

        button_border = Frame(settings, highlightbackground="black",
                              highlightthickness=2, bd=3, relief="solid")
        button_border.grid(row=1, column=1)

        create_buttons.game_size_button = Button(button_border,
                                                 text="Map Size:",
                                                 padx=width / 3 + 23,
                                                 pady=height/25,
                                                 bg="#ff0080", fg="white",
                                                 font=("Arial", 15),
                                                 command=change_size)
        create_buttons.game_size_button.grid(row=1, column=1)

        if arrow_keys:
            create_buttons.controls_button = Button(button_border,
                                                    text="Controls: Arrow " +
                                                         "Keys",
                                                    padx=width / 3 - 25,
                                                    pady=height / 25,
                                                    bg="#ff0080", fg="white",
                                                    font=("Arial", 15),
                                                    command=change_keybinds)
        else:
            create_buttons.controls_button = Button(button_border,
                                                    text="Controls: WASD Keys",
                                                    padx=width / 3 - 30,
                                                    pady=height / 25,
                                                    bg="#ff0080", fg="white",
                                                    font=("Arial", 15),
                                                    command=change_keybinds)

        create_buttons.controls_button.grid(row=2, column=1)

        colours_button = Button(button_border,
                                text="Colours",
                                padx=width / 3 + 35,
                                pady=height / 25,
                                bg="#ff0080", fg="white",
                                font=("Arial", 15),
                                command=change_colours)
        colours_button.grid(row=3, column=1)

        return_button = Button(button_border,
                               text="Return to Menu",
                               padx=width / 3 - 1,
                               pady=height / 25,
                               bg="#ff0080", fg="white",
                               font=("Arial", 15),
                               command=return_to_menu)
        return_button.grid(row=5, column=1)

    settings = Tk()
    settings.config(bg="#00b300")
    settings.title("Settings")
    width = settings.winfo_screenwidth()
    height = settings.winfo_screenheight()

    settings.geometry(f"{width}x{height}")

    space_filler()
    title_label = Label(settings, text="Settings", font=("Arial", 25),
                        borderwidth=5, relief="solid",
                        pady=height / 25, padx=width / 25)
    title_label.grid(row=0, column=1, pady=20)
    create_buttons()

    settings.mainloop()


def display_leaderboards():

    def space_filler():

        text = ""
        for i in range(int(width / 33)):
            text += " "
        space_filler_text = text
        space_filler = Label(leaderboard, text=space_filler_text, bg="#00e600")
        space_filler.grid(row=0, column=0)

    def show_top_five():

        global scores_names
        labels = []
        positions = []

        top_five_border = Frame(leaderboard, highlightbackground="black",
                                highlightthickness=2, bd=1, bg="gold")

        if (len(scores_names) == 1):  # If no scores saved (just "leaderboard")
            no_scores = Label(top_five_border, text="No saved scores!")
            no_scores.grid(row=1, column=1)

        else:

            if len(scores_names) <= 5:
                z = len(scores_names) - 1  # Avoids index error.

            else:
                z = 5

            for i in range(1, z+1):  # 1 as 0 would be "Leaderboards, \n"
                positions.append(Label(top_five_border, text=f"{i}: ",
                                       font=("Arial", 30), bg="gold",))
                positions[i-1].grid(row=i, column=0)  # Makes 1. 2. 3. etc

                labels.append(Label(top_five_border, text=f"{scores_names[i]}",
                                    font=("Arial", 25), anchor="s", bg="gold"))
                labels[i-1].grid(row=i, column=1)
                top_five_border.grid(row=i, column=1, pady=50)

    def return_to_menu():
        leaderboard.destroy()
        menu()

    leaderboard = Tk()
    leaderboard.title("Leaderboard")
    leaderboard.config(bg="#00e600")
    width = leaderboard.winfo_screenwidth()
    height = leaderboard.winfo_screenheight()

    leaderboard.geometry(f"{width}x{height}")

    title_label = Label(leaderboard, text="Leaderboard", font=("Arial", 25),
                        relief="solid", borderwidth=2, pady=height / 25)
    title_label.grid(row=0, column=1, pady=height / 50)

    return_button = Button(leaderboard, text="Return to Menu",
                           padx=width / 3 - 1, pady=height / 50, bg="#ff0080",
                           font=("Arial", 20), fg="white",
                           command=return_to_menu)
    return_button.grid(row=6, column=1)

    space_filler()
    show_top_five()

    leaderboard.mainloop()


def menu():

    def check_leaderboard():

        def get_scores():
            global scores
            global scores_names
            global split_scores

            file = open("Leaderboard.txt", "r")
            scores_names = file.readlines()
            file.close()

            split_scores = []

            for i in range(1, len(scores_names)):
                scores_names[i] = scores_names[i].replace("\n", "")
                split_scores.append(scores_names[i].split(","))
                # [Name][score]

            # for i in range(0,len(split_scores)-1):
            #   scores.append(split_scores[i][1])  # [score]
            #   print(scores)

            # print(scores)

        if os.path.isfile("Leaderboard.txt"):  # If the file exists.
            get_scores()
        else:
            file = open("Leaderboard.txt", "w")
            file.write("Leaderboards: \n")
            file.close()
            get_scores()

    def space_filler():

        text = ""
        for i in range(int(width / 33)):
            text += " "

        space_filler_text = text
        space_filler = Label(menu, text=space_filler_text, bg="#00ff00")
        space_filler.grid(row=0, column=0)

    def play_button_click():

        menu.destroy()
        rules()

    def leaderboards_button_click():

        menu.destroy()
        display_leaderboards()

    def settings_button_click():

        menu.destroy()
        display_settings()

    def quit_button_click():

        menu.destroy()

    def create_buttons():

        space_filler()

        button_border = Frame(menu, highlightbackground="black",
                              highlightthickness=2,
                              bd=3, relief="solid")

        play_button = Button(button_border, text="Play Game",
                             padx=width / 3 + 5, pady=height / 25,
                             bg="#ff0080", fg="white",
                             font=("Arial", 15),
                             command=play_button_click)
        play_button.grid(row=1, column=1,)

        leaderboards_button = Button(button_border, text="Leaderboards",
                                     padx=width / 3 - 8, pady=height / 25,
                                     bg="#ff0080", fg="white",
                                     font=("Arial", 15),
                                     command=leaderboards_button_click)
        leaderboards_button.grid(row=2, column=1)

        settings_button = Button(button_border, text="Settings",
                                 padx=width / 3 + 18, pady=height / 25,
                                 bg="#ff0080", fg="white",
                                 font=("Arial", 15),
                                 command=settings_button_click)
        settings_button.grid(row=3, column=1)

        exit_button = Button(button_border, text="Exit Application",
                             padx=width / 3 - 15, pady=height / 25,
                             bg="#ff0080", fg="white",
                             font=("Arial", 15),
                             command=quit_button_click)
        exit_button.grid(row=4, column=1)
        button_border.grid(row=1, column=1)

    menu = Tk()
    menu.config(bg="#00ff00")
    menu.title("Coursework Snake Game")
    width = menu.winfo_screenwidth()
    height = menu.winfo_screenheight()
    menu.geometry(f"{width}x{height}")

    title_label = Label(menu, text="Snake Game",
                        font=("Arial", 25),
                        borderwidth=5, relief="solid",
                        pady=height / 23,)

    title_label.grid(row=0, column=1, pady=20)

    check_leaderboard()

    create_buttons()

    menu.mainloop()

snake_size, arrow_keys, colours = get_settings()
menu()
