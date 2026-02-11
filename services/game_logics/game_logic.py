from fastapi import WebSocket


async def shoot(board: list[list[int | str]], websocket: WebSocket, x: int, y: int, current_turn: int):
    cell = board[x][y]

    if cell in ["*", "x"]:
        await websocket.send_json({
            "type": "error",
            "message": "Вы уже делали ход по этой клетке!"
        })
        return board, current_turn

    if cell in [1, 2, 3, 4]:
        board[x][y] = "x"
        await websocket.send_json({
            "type": "hit",
            "message": f"Попадание по клетке ({x},{y})!"
        })
        return board, current_turn

    # Промах
    board[x][y] = "*"
    await websocket.send_json({
        "type": "miss",
        "message": f"Промах по клетке ({x},{y})!"
    })
    new_turn = 2 if current_turn == 1 else 1
    return board, new_turn


def check_ships(board: list) -> bool:
    target = {1, 2, 3, 4}
    found = False
    for row in board:
        for x in row:
            if x in target:
                found = True
                return found
                break
        if found:
            break

    return found
