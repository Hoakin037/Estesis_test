from random import choice, randint

def can_place(board: list[list[int | str]], row: int, col: int, size: int, direction: str):
    for i in range(size):
        r,c = row, col
        if direction == "H" : c += i # Горизонтально
        else: r += i # Вертикально

        # Проверка границ поля
        if not (0 <= r < 10 and 0 <= c < 10):
            return False
        
        # Проверка кораблей рядом
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = r + dr, c + dc
                if 0 <= nr < 10 and 0 <= nc < 10:
                    if board[nr][nc] != 0:
                        return False
    return True

def place_ship(board: list[list[int | str]], size: int):
    placed = False

    while not placed:
        direction = choice("H", "V")
        row = randint(0, 9)
        col = randint(0, 9)

        if can_place(board, row, col, size, direction):
            for i in range(size):
                if direction == "H" : board[row][col + i] = size
                else: board[row + i][col] = size
            placed = True

def generate_full_board():
    board = [[0 for _ in range(10)] for _ in range(10)]

    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for ship_size in ships:
        place_ship(board, ship_size)
    return board
