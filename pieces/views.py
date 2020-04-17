from django.shortcuts import render
from pieces.board import Board

def show_board(request):
    board = Board()

    print_board = [
        board.get_tiles_row(row=0),
        board.get_tiles_row(row=1),
        board.get_tiles_row(row=2),
        board.get_tiles_row(row=3),
        board.get_tiles_row(row=4),
    ]

    context = {
        'board': print_board,
    }

    return render(request, 'index.html', context=context)