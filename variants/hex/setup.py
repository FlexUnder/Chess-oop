from base import WHITE, BLACK
from variants.hex.board import Board
from variants.hex import pieces


def create_board():
    board = Board()
    _setup_white(board)
    _setup_black(board)
    return board


def _setup_white(board):
    W = WHITE
    p = pieces

    board.set_piece(-5,  5, p.Rook(W))
    board.set_piece(-4,  5, p.Knight(W))
    board.set_piece(-3,  5, p.Bishop(W))
    board.set_piece(-2,  5, p.Queen(W))
    board.set_piece(-1,  5, p.King(W))
    board.set_piece( 0,  5, p.Bishop(W))
    board.set_piece( 1,  4, p.Bishop(W))
    board.set_piece( 2,  3, p.Knight(W))
    board.set_piece( 3,  2, p.Rook(W))

    for q, r in [(-4,4),(-3,4),(-2,4),(-1,4),(0,4),(1,3),(2,2),(3,1),(4,0)]:
        board.set_piece(q, r, p.Pawn(W))


def _setup_black(board):
    B = BLACK
    p = pieces

    board.set_piece( 5, -5, p.Rook(B))
    board.set_piece( 4, -5, p.Knight(B))
    board.set_piece( 3, -5, p.Bishop(B))
    board.set_piece( 2, -5, p.Queen(B))
    board.set_piece( 1, -5, p.King(B))
    board.set_piece( 0, -5, p.Bishop(B))
    board.set_piece(-1, -4, p.Bishop(B))
    board.set_piece(-2, -3, p.Knight(B))
    board.set_piece(-3, -2, p.Rook(B))

    for q, r in [(4,-4),(3,-4),(2,-4),(1,-4),(0,-4),(-1,-3),(-2,-2),(-3,-1),(-4,0)]:
        board.set_piece(q, r, p.Pawn(B))
