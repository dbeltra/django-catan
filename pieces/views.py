from django.shortcuts import render
from pieces.board import Board

def show_board(request):
    board = Board()

    print_board = [
        {
            'number':'-1',
            'tiles': board.get_tiles_row(row=-1)
        },{
            'number':'0',
            'tiles': board.get_tiles_row(row=0)
        },{
            'number':'1',
            'tiles': board.get_tiles_row(row=1)
        },{
            'number':'2',
            'tiles': board.get_tiles_row(row=2)
        },{
            'number':'3',
            'tiles': board.get_tiles_row(row=3)
        },{
            'number':'4',
            'tiles': board.get_tiles_row(row=4)
        },{
            'number':'5',
            'tiles': board.get_tiles_row(row=5)
        },
    ]

    context = {
        'board': print_board,
    }

    return render(request, 'index.html', context=context)