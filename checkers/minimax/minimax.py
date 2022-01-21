from copy import deepcopy
import pygame
import numpy as np

RED = (255,0,0)
WHITE = (255,255,255)

def minimax(position, depth, maxPlayer, game):
    if depth == 0:
        return position.evaluate(), position
    if position is not None and position.winner() is not None:
        return position.evaluate(), position
    best = None
    if maxPlayer:
        maxn = -np.inf
        moves = getAllMoves(position, WHITE, game)
        if not moves:
            return None, None
        for move in moves:
            fitness = minimax(move, depth-1, False, game)
            if fitness is (None, None): 
                continue
            maxn = max(maxn, fitness[0])
            if maxn == fitness[0]:
                best = move
        return maxn, best
    else:
        minn = np.inf
        moves = getAllMoves(position, RED, game)
        if not moves:
            return None, None
        for move in moves:
            fitness = minimax(move, depth-1, True, game)
            if fitness is (None, None):
                continue
            minn = min(minn, fitness[0])
            if minn == fitness[0]:
                best = move
        return minn, best
    # Your Code Goes Here

def simulateMove(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board
    # Your Code Goes Here

def getAllMoves(board, color, game):
    moves = []
    if not board:
        return None
    pieces = board.getAllPieces(color)
    for piece in pieces:
        piece_moves = board.getValidMoves(piece).items()
        for m, s in piece_moves:
            newboard = deepcopy(board)
            newpiece = newboard.getPiece(piece.row, piece.col)
            moves.append(simulateMove(newpiece, m, newboard, game, s))
    return moves
    # Your Code Goes Here