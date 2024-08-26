from django.shortcuts import render, redirect
import random

# Global Variables
player_symbol = 'X'
bot_symbol = 'O'
game_buttons = []
grid_size = 3
game_over = False

def initialize_game():
    global game_buttons, game_over
    game_buttons = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    game_over = False

def check_win():
    for row in range(grid_size):
        if all(cell == player_symbol for cell in game_buttons[row]):
            return player_symbol
        if all(cell == bot_symbol for cell in game_buttons[row]):
            return bot_symbol
    for col in range(grid_size):
        if all(game_buttons[row][col] == player_symbol for row in range(grid_size)):
            return player_symbol
        if all(game_buttons[row][col] == bot_symbol for row in range(grid_size)):
            return bot_symbol
    if all(game_buttons[i][i] == player_symbol for i in range(grid_size)) or \
       all(game_buttons[i][grid_size-i-1] == player_symbol for i in range(grid_size)):
        return player_symbol
    if all(game_buttons[i][i] == bot_symbol for i in range(grid_size)) or \
       all(game_buttons[i][grid_size-i-1] == bot_symbol for i in range(grid_size)):
        return bot_symbol
    if all(game_buttons[row][col] != '' for row in range(grid_size) for col in range(grid_size)):
        return 'Tie'
    return None

def bot_move():
    empty_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) if game_buttons[i][j] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        game_buttons[row][col] = bot_symbol
        return row, col
    return None, None

def index(request):
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        col = int(request.POST.get('col'))
        if game_buttons[row][col] == '' and not game_over:
            game_buttons[row][col] = player_symbol
            winner = check_win()
            if winner:
                return render(request, 'game/index.html', {'game_buttons': game_buttons, 'winner': winner})
            bot_r, bot_c = bot_move()
            winner = check_win()
            if winner:
                return render(request, 'game/index.html', {'game_buttons': game_buttons, 'winner': winner})
    return render(request, 'game/index.html', {'game_buttons': game_buttons})
