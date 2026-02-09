def shoot(board: list[list[int | str]], x: int, y: int):
    if board[x][y] in ["*", "x"]:
        raise Exception("Вы уже делали ход по этой клетке!")
    elif board[x][y] in [1, 2, 3, 4]:
        board[x][y] = "x"
        return board
    
    board[x][y] = "*" # Промах
    return board