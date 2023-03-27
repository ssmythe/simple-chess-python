#!/usr/bin/env python

import chess
import chess.engine
import random

def evaluate_position(board):
    # Space: number of possible moves
    legal_moves = list(board.legal_moves)
    space = len(legal_moves)

    # Time: number of moves played
    time = board.fullmove_number

    # Force: material balance
    force = sum([piece_value(board.piece_at(square)) for square in chess.SQUARES])

    return space - time + force

def piece_value(piece):
    if piece is None:
        return 0

    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    value = piece_values[piece.piece_type]

    # Negate the value if the piece belongs to the black player
    if piece.color == chess.BLACK:
        value = -value

    return value

def simple_engine(board):
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)

    best_move = None
    best_eval = float('-inf')

    for move in legal_moves:
        board.push(move)
        eval = evaluate_position(board)
        board.pop()

        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move

def main():
    board = chess.Board()
    last_move_san = None
    last_move_uci = None

    while not board.is_game_over():
        if last_move_san and last_move_uci:
            print(f"\n\nLast move: {last_move_san} ({last_move_uci})")

        print(f"\nMove number: {board.fullmove_number}")
        legal_moves_formatted = [f"{board.san(move)} ({move.uci()})" for move in board.legal_moves]
        print("Legal moves: ", ', '.join(legal_moves_formatted))
        print(board)
        if board.turn == chess.WHITE:
            move = chess.Move.from_uci(input("Enter your move: "))
        else:
            move = simple_engine(board)

        last_move_san = board.san(move)
        last_move_uci = move.uci()
        board.push(move)

    print(board)
    print("Game over. Result: ", board.result())

if __name__ == "__main__":
    main()
