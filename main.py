import random
from tkinter import *  # Import tkinter for GUI components
from PIL import Image, ImageTk  # Import PIL for handling images

# Function Definitions

# Keep a list to store references to images
image_refs = []

def raise_frame(frame):
    """
    Bring the specified frame to the front of the window.
    Also resets the win/loss display.
    """
    frame.tkraise()
    win_loss_label.configure(text=" ")

def reset_game():
    """
    Resets the game state to allow for another round of play.
    """
    play_again_button.place_forget()  # Hide the 'Play Again' button
    for button in game_buttons:
        button.config(text='', state='normal')  # Reset each game button
    win_loss_label.config(text='')  # Clear the win/loss display
    start_game()  # Restart the game

def check_win():
    """
    Check if there is a win condition in the game.
    Returns 'X', 'O', or 'Tie' if a win/tie is found, otherwise False.
    """
    size = grid_size.get()  # Get the current grid size

    # Check Horizontal Win
    for row_start in range(0, size * size, size):
        if all(game_buttons[row_start + col].cget('text') == game_buttons[row_start].cget('text') != '' for col in range(size)):
            return game_buttons[row_start].cget('text')

    # Check Vertical Win
    for col_start in range(size):
        if all(game_buttons[col_start + row * size].cget('text') == game_buttons[col_start].cget('text') != '' for row in range(size)):
            return game_buttons[col_start].cget('text')

    # Check Diagonal Win
    # Top-left to bottom-right diagonal
    if all(game_buttons[i * (size + 1)].cget('text') == game_buttons[0].cget('text') != '' for i in range(size)):
        return game_buttons[0].cget('text')
    # Top-right to bottom-left diagonal
    if all(game_buttons[(i + 1) * (size - 1)].cget('text') == game_buttons[size - 1].cget('text') != '' for i in range(size)):
        return game_buttons[size - 1].cget('text')

    # Check for Tie
    if all(button.cget('text') for button in game_buttons):
        return 'Tie'

    return False

def find_winning_move(symbol):
    """
    Find a winning move for the given symbol ('X' or 'O').
    Returns the index of the winning move, or None if no winning move is found.
    """
    size = grid_size.get()
    for i in range(size ** 2):
        if game_buttons[i].cget('text') == '':
            game_buttons[i].config(text=symbol)  # Temporarily set the move
            if check_win() == symbol:
                game_buttons[i].config(text='')  # Reset the move
                return i
            game_buttons[i].config(text='')  # Reset the move
    return None

def bot_move():
    """
    Makes a move for the bot by following a strategy:
    1. Try to win.
    2. Block the opponent.
    3. Pick a random spot.
    """
    size = grid_size.get()

    # Try to win
    move = find_winning_move(bot_symbol)
    if move is not None:
        game_buttons[move].config(text=bot_symbol, fg='black')
        return True

    # Try to block the opponent
    move = find_winning_move(player_symbol)
    if move is not None:
        game_buttons[move].config(text=bot_symbol, fg='black')
        return True

    # Pick a random empty spot
    empty_buttons = [i for i in range(size ** 2) if game_buttons[i].cget('text') == '']
    if empty_buttons:
        move = random.choice(empty_buttons)
        game_buttons[move].config(text=bot_symbol, fg='black')
        return True

    return False

def handle_button_press(button):
    """
    Handles the action when a game button is pressed.
    """
    global game_over
    if button.cget('text') == '' and not game_over:  # If the button hasn't been clicked yet
        button.config(text=player_symbol, fg='black')  # Set button text to the player's symbol
        winner = check_win()
        if winner:
            end_game(winner)
            return
        # Bot's turn
        if not game_over:
            if bot_move():  # Make a bot move
                winner = check_win()
                if winner:
                    end_game(winner)

def end_game(winner):
    """
    Handles the end of the game, displaying the winner and disabling buttons.
    """
    global game_over
    win_loss_label.config(text=f'Player {winner} Wins!' if winner != 'Tie' else 'Nobody Wins!')
    game_over = True
    for btn in game_buttons:
        btn.config(state='disabled')  # Disable all buttons after a win/tie
    play_again_button.place(x=210, y=450, width=200, height=40)  # Show the 'Play Again' button

def start_game():
    """
    Initializes and starts a new game based on the selected grid size.
    """
    global game_buttons, game_over
    play_again_button.place_forget()  # Hide the 'Play Again' button
    game_buttons = []  # Initialize the game button list
    game_over = False
    size = grid_size.get()  # Get the grid size
    button_size = 300 / size

    for i in range(size ** 2):  # Create the game buttons
        btn = Button(start_frame, text="", bg="white", activebackground="white", fg="white",
                     font="Times 15 bold", borderwidth=10, command=lambda b=i: handle_button_press(game_buttons[b]))
        btn.place(x=150 + (i % size) * button_size, y=100 + (i // size) * button_size, width=button_size, height=button_size)
        game_buttons.append(btn)  # Add each button to the list
    
    raise_frame(start_frame)
    # Randomly decide who starts
    if random.choice([True, False]):
        # Bot starts first
        bot_move()

# Main Application Code

# Create the main application window
root = Tk()
root.title("Tic-Tac-Toe Project")
root.geometry('600x500')

# Global Variables
player_symbol = 'X'  # Player is always 'X'
bot_symbol = 'O'     # Bot is always 'O'
game_buttons = []  # List to hold the game buttons
grid_size = IntVar(value=3)  # Variable to hold the grid size, default to 3x3
game_over = False

# Home Frame Setup
home_frame = Frame(root)
home_frame.place(x=0, y=0, width=600, height=500)

# Home Frame Widgets
Welcome_label = Label(home_frame, text="Welcome to Tic Tac Toe!", bg="Green", font="Courier")
Welcome_label.place(x=150, y=50, width=300, height=50)

Start_button = Button(home_frame, text="Start", bg='Red', fg="black", font="Courier", command=start_game)
Start_button.place(x=250, y=150, width=110, height=50)

Options_button = Button(home_frame, text="Directions", bg='yellow', fg="black", font="Courier", command=lambda: raise_frame(options_frame))
Options_button.place(x=250, y=250, width=110, height=50)

Gamemode_button = Button(home_frame, text="Game Modes", bg='blue', fg="black", font="Courier", command=lambda: raise_frame(gamemode_frame))
Gamemode_button.place(x=250, y=200, width=110, height=50)

# Home Page Images
x_image = ImageTk.PhotoImage(Image.open("images/Players/X.png").resize((95, 95)))
image_refs.append(x_image)  # Keep a reference
home_x_label = Label(home_frame, image=x_image)
home_x_label.place(x=430, y=190)

o_image = ImageTk.PhotoImage(Image.open("images/Players/O.png").resize((150, 150)))
image_refs.append(o_image)  # Keep a reference
home_o_label = Label(home_frame, image=o_image)
home_o_label.place(x=60, y=190)

# Start Frame Setup
start_frame = Frame(root)
start_frame.place(x=0, y=0, width=600, height=500)

# Start Frame Widgets
back_to_home_button = Button(start_frame, text="Home", font="Courier", command=lambda: raise_frame(home_frame))
back_to_home_button.place(x=250, y=20, width=100, height=50)

win_loss_label = Label(start_frame, text='', font="Courier 20")
win_loss_label.place(x=162, y=405, width=300)

play_again_button = Button(start_frame, text='Play again', font='Courier', state='normal', command=reset_game)

# Gamemode Frame Setup
gamemode_frame = Frame(root)
gamemode_frame.place(x=0, y=0, width=600, height=500)

# Adding the Home Button to the Game Modes Frame
home_button_gamemode = Button(gamemode_frame, text="Home", font="Courier", command=lambda: raise_frame(home_frame))
home_button_gamemode.place(x=250, y=20, width=100, height=50)

# Updated Game Mode Label
gamemode_label = Label(
    gamemode_frame, 
    text="Select any of the game modes to play with a new grid!", 
    font="Courier 12",  # Consistent font size
    bg="green",  # Green background
    fg="white"  # White text for contrast
)
gamemode_label.place(x=30, y=400, width=540, height=50)  # Adjusted placement

# Automate Grid Mode Setup
grid_images = ["3x3.png", "4x4.png", "5x5.png"]
grid_sizes = [3, 4, 5]
grid_positions = [(47, 190), (255, 190), (463, 185)]
grid_radiobutton_positions = [(15, 225), (220, 225), (435, 225)]

for idx, (image, size, position, radio_position) in enumerate(zip(grid_images, grid_sizes, grid_positions, grid_radiobutton_positions)):
    img = ImageTk.PhotoImage(Image.open(f"images/Grids/{image}").resize((90 + idx*5, 90 + idx*5)))
    image_refs.append(img)  # Keep a reference
    Label(gamemode_frame, image=img).place(x=position[0], y=position[1])
    Radiobutton(gamemode_frame, variable=grid_size, value=size).place(x=radio_position[0], y=radio_position[1])

# Instructions Frame Setup
options_frame = Frame(root)
options_frame.place(x=0, y=0, width=600, height=500)

# Updated Instructions Label
instructions_text = (
    "Instructions:\n"
    "1. Choose a game mode to start playing.\n"
    "2. The goal is to complete a line (horizontally, vertically, or diagonally) with your symbol (X).\n"
    "3. You will play as 'X', and the bot will play as 'O'.\n"
    "4. If you lose, you can play again by clicking 'Play again'."
)

instructions_label = Label(
    options_frame, 
    text=instructions_text, 
    font="Courier 12", 
    justify=LEFT, 
    bg="green",  # Green background to match game mode label
    fg="white"  # White text for contrast
)
instructions_label.place(x=30, y=100, width=540, height=250)  # Adjusted placement and size

# Instructions Frame Widgets
back_to_home_options_button = Button(options_frame, text="Home", font="Courier", command=lambda: raise_frame(home_frame))
back_to_home_options_button.place(x=250, y=20, width=100, height=50)

# Start the game with the home frame
raise_frame(home_frame)
root.mainloop()