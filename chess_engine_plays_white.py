#!/usr/bin/env python

import chess

def evaluate_position(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0,
    }

    score = 0
    for piece_type in piece_values.keys():
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    return score

def simple_engine(board):
    best_move = None
    best_evaluation = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        evaluation = evaluate_position(board)
        board.pop()

        if evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = move

    return best_move

def evaluate_move(board, move):
    board.push(move)
    score = evaluate_position(board)
    board.pop()
    return score

def main():
    board = chess.Board()
    last_move_san = None
    last_move_uci = None

    while not board.is_game_over():
        if last_move_san and last_move_uci:
            print(f"Last move: {last_move_san} ({last_move_uci})")

        print(f"Move number: {board.fullmove_number}")

        legal_moves_evaluated = [
            (evaluate_move(board, move), board.san(move), move.uci())
            for move in board.legal_moves
        ]
        legal_moves_sorted = sorted(legal_moves_evaluated, key=lambda x: x[0], reverse=True)
        legal_moves_formatted = [f"{eval_score} {san} ({uci})" for eval_score, san, uci in legal_moves_sorted]

        print("Legal moves: ", ', '.join(legal_moves_formatted))

        print(board)
        if board.turn == chess.WHITE:
            move = simple_engine(board)
        else:
            while True:
                try:
                    move_uci = input("Enter your move: ")
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        break
                    else:
                        print("Invalid move. Please try again.")
                except ValueError:
                    print("Invalid input format. Please try again.")

        last_move_san = board.san(move)
        last_move_uci = move.uci()
        board.push(move)

    print(board)
    print("Game over. Result: ", board.result())

if __name__ == "__main__":
    main()
