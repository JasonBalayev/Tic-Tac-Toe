let playerSymbol = 'X';
let botSymbol = 'O';
let gameOver = false;
let gameBoard = [];
let gridSize = 3;  // Default grid size
let winCondition = 3; // Number of symbols needed to win

// Set the game mode (grid size) and initialize the board
function setGameMode(size) {
    gridSize = size;
    winCondition = 3;  // Win condition remains 3 in a row
    initBoard();
    resetGame();
}

// Initialize the game board with click handlers
function initBoard() {
    gameBoard = Array(gridSize).fill().map(() => Array(gridSize).fill(''));
    $('#board').empty();  // Clear existing board
    for (let i = 0; i < gridSize; i++) {
        let row = $('<div class="row"></div>');
        for (let j = 0; j < gridSize; j++) {
            let cell = $('<div class="cell"></div>').attr('id', `cell-${i}-${j}`);
            cell.click(function() {
                handleCellClick(i, j, $(this));
            });
            row.append(cell);
        }
        $('#board').append(row);
    }
}

function handleCellClick(row, col, cellElement) {
    if (!gameOver && gameBoard[row][col] === '') {
        cellElement.text(playerSymbol);
        gameBoard[row][col] = playerSymbol;
        if (checkWin(playerSymbol)) {
            $('#status').text('Player X wins!');
            gameOver = true;
        } else if (isBoardFull()) {
            $('#status').text('It\'s a tie!');
            gameOver = true;
        } else {
            botMove();
        }
    }
}

function botMove() {
    // Check for any immediate winning move for the bot
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (gameBoard[i][j] === '') {
                gameBoard[i][j] = botSymbol;
                if (checkWin(botSymbol)) {
                    $(`#cell-${i}-${j}`).text(botSymbol);
                    $('#status').text('Player O wins!');
                    gameOver = true;
                    return;
                }
                gameBoard[i][j] = '';  // Undo move
            }
        }
    }

    // Check for any immediate winning move for the player and block it
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (gameBoard[i][j] === '') {
                gameBoard[i][j] = playerSymbol;
                if (checkWin(playerSymbol)) {
                    gameBoard[i][j] = botSymbol;
                    $(`#cell-${i}-${j}`).text(botSymbol);
                    return;
                }
                gameBoard[i][j] = '';  // Undo move
            }
        }
    }

    // If no immediate win or block is possible, use Minimax to choose the best move
    let bestScore = -Infinity;
    let bestMove;
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (gameBoard[i][j] === '') {
                gameBoard[i][j] = botSymbol;
                let score = minimax(gameBoard, 0, false, -Infinity, Infinity);
                gameBoard[i][j] = '';
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = { i, j };
                }
            }
        }
    }
    if (bestMove) {
        gameBoard[bestMove.i][bestMove.j] = botSymbol;
        $(`#cell-${bestMove.i}-${bestMove.j}`).text(botSymbol);
        if (checkWin(botSymbol)) {
            $('#status').text('Player O wins!');
            gameOver = true;
        } else if (isBoardFull()) {
            $('#status').text('It\'s a tie!');
            gameOver = true;
        }
    }
}

function minimax(board, depth, isMaximizing, alpha, beta) {
    if (checkWin(botSymbol)) return 10 - depth;
    if (checkWin(playerSymbol)) return depth - 10;
    if (isBoardFull() || depth > 4) return 0; // Limit depth for larger grids

    if (isMaximizing) {
        let bestScore = -Infinity;
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                if (board[i][j] === '') {
                    board[i][j] = botSymbol;
                    let score = minimax(board, depth + 1, false, alpha, beta);
                    board[i][j] = '';
                    bestScore = Math.max(score, bestScore);
                    alpha = Math.max(alpha, score);
                    if (beta <= alpha) {
                        break; // Alpha-beta pruning
                    }
                }
            }
        }
        return bestScore;
    } else {
        let bestScore = Infinity;
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                if (board[i][j] === '') {
                    board[i][j] = playerSymbol;
                    let score = minimax(board, depth + 1, true, alpha, beta);
                    board[i][j] = '';
                    bestScore = Math.min(score, bestScore);
                    beta = Math.min(beta, score);
                    if (beta <= alpha) {
                        break; // Alpha-beta pruning
                    }
                }
            }
        }
        return bestScore;
    }
}

function checkWin(symbol) {
    // Check all possible lines of three
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            // Check horizontal lines
            if (j + 2 < gridSize && gameBoard[i][j] === symbol && gameBoard[i][j + 1] === symbol && gameBoard[i][j + 2] === symbol) {
                return true;
            }
            // Check vertical lines
            if (i + 2 < gridSize && gameBoard[i][j] === symbol && gameBoard[i + 1][j] === symbol && gameBoard[i + 2][j] === symbol) {
                return true;
            }
            // Check diagonal lines
            if (i + 2 < gridSize && j + 2 < gridSize && gameBoard[i][j] === symbol && gameBoard[i + 1][j + 1] === symbol && gameBoard[i + 2][j + 2] === symbol) {
                return true;
            }
            if (i + 2 < gridSize && j - 2 >= 0 && gameBoard[i][j] === symbol && gameBoard[i + 1][j - 1] === symbol && gameBoard[i + 2][j - 2] === symbol) {
                return true;
            }
        }
    }
    return false;
}

function isBoardFull() {
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (gameBoard[i][j] === '') {
                return false;  // Found an empty cell, so board isn't full
            }
        }
    }
    return true;  // No empty cells found, board is full
}

function resetGame() {
    gameOver = false;
    gameBoard = Array(gridSize).fill().map(() => Array(gridSize).fill(''));
    $('.cell').text('');
    $('#status').text('');
}

// Initialize the game with the default mode (3x3)
$(document).ready(function() {
    setGameMode(gridSize);
});
