from enum import Enum
import random

NUM_WOOD = 4
NUM_SHEEP = 4
NUM_WHEAT = 4
NUM_ORE = 3
NUM_BRICK = 3
NUM_DESERT = 1

TILES_NUMBERS = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
TILES_DIRECTION_DISTRIBUTION = ['r','br','bl','l','tl','tr']


class Board:
    tiles = []
    num_rows = None
    numbers = None

    def __init__(self):
        self.tiles = []
        pieces = (
            [Terrain.desert] * NUM_DESERT +
            [Terrain.brick] * NUM_BRICK +
            [Terrain.ore] * NUM_ORE +
            [Terrain.wood] * NUM_WOOD +
            [Terrain.sheep] * NUM_SHEEP +
            [Terrain.wheat] * NUM_WHEAT
        )
        random.shuffle(pieces)

        board_distribution = [
            pieces[0:3],
            pieces[3:7],
            pieces[7:12],
            pieces[12:16],
            pieces[16:19]
        ]

        self.num_rows = len(board_distribution)
        
        for row_idx, row in enumerate(board_distribution):
            for col_idx, piece in enumerate(row):
                tile = Tile(board=self, terrain=piece, number=None, position=(row_idx,col_idx))
                self.tiles.append(tile)

        self.init_numbers()

    def __del__(self):
        for tile in self.tiles:
            del tile
        print('board erased')

    def init_numbers(self):
        self.numbers = TILES_NUMBERS.copy()

        next_tile = self.tiles[0]
        direction = 'r'
        while next_tile != None:
            current_tile = next_tile
            self.put_number_in_tile(current_tile)
            next_tile, direction = self.get_next_tile(current_tile, direction)



    def get_next_tile(self, tile, direction):
        print('-------------------------')
        print(f'current tile {tile}')
        neighbors = tile.find_neighbors()
        next_tile = neighbors[direction]
        print(f'try next tile {next_tile}, direction followed {direction}')
        print(f'neighbors to the candidate tile are {neighbors}')

        if next_tile is None or next_tile.number is not None:
            print(f'theres no neighbours in the {direction} direction, or they already have a number')  
            
            current_direction_array_idx = TILES_DIRECTION_DISTRIBUTION.index(direction)

            for number_directions_options in range(1, len(TILES_DIRECTION_DISTRIBUTION)):
                next_direction_array_idx = current_direction_array_idx + number_directions_options
                if next_direction_array_idx >= len(TILES_DIRECTION_DISTRIBUTION):
                    next_direction_array_idx = next_direction_array_idx - len(TILES_DIRECTION_DISTRIBUTION)
                       
                new_direction = TILES_DIRECTION_DISTRIBUTION[next_direction_array_idx]
                print(f'next should be {neighbors[new_direction]}, direction followed {new_direction}')
                next_tile = neighbors[new_direction]

                if next_tile is not None and next_tile.number is  None:
                    return next_tile, new_direction
                else:
                    print('but its None or already numbered, lets try another direction')

            print(f'theres no possible neighbours, END')  
            return None, None
        else:
            print(f'next tile found {next_tile}, direction followed {direction}')
            return next_tile, direction
        

    def put_number_in_tile(self,tile):
        if tile.terrain is not Terrain.desert:
            tile.number = self.numbers.pop(0)
        else:
            tile.number = 0

    def get_tile_by_position(self, position):
        matching_tile = None
        for tile in self.tiles:
            if tile.position == position:
                matching_tile = tile
        return matching_tile

    def get_tiles_row(self, row):
        match_row = []
        for tile in self.tiles:
            if tile.row == row:
                match_row.append(tile)
        return match_row

    def print_board(self):
       for tile in self.tiles:
           print(tile)

class Tile:
    board = None
    terrain = None
    number = None
    position = None
    row = None
    col = None
    neighbors = None

    def __init__(self, board, terrain, number, position):
        self.board = board
        self.terrain = terrain
        self.number = number
        self.position = position
        self.row = position[0]
        self.col = position[1]

    def __del__(self):
        print('Tile deleted')

    def find_neighbors(self):
        self.neighbors = {
            'tl': None,
            'tr': None,
            'r': self.board.get_tile_by_position((self.row, self.col+1)),
            'br': None,
            'bl': None,
            'l': self.board.get_tile_by_position((self.row, self.col-1)),
        }

        nrows = self.board.num_rows
        if self.row < (nrows-1)/2:
            print('im in the top')
            self.neighbors['tl'] = self.board.get_tile_by_position((self.row-1, self.col-1))
            self.neighbors['tr'] = self.board.get_tile_by_position((self.row-1, self.col))
            self.neighbors['br'] = self.board.get_tile_by_position((self.row+1, self.col+1))
            self.neighbors['bl'] = self.board.get_tile_by_position((self.row+1, self.col))

        if self.row == (nrows-1)/2:
            print('im in the mid')
            self.neighbors['tl'] = self.board.get_tile_by_position((self.row-1, self.col-1))
            self.neighbors['tr'] = self.board.get_tile_by_position((self.row-1, self.col))
            self.neighbors['br'] = self.board.get_tile_by_position((self.row+1, self.col))
            self.neighbors['bl'] = self.board.get_tile_by_position((self.row+1, self.col-1))

        if self.row > (nrows-1)/2:
            print('im in the bottom')
            self.neighbors['tl'] = self.board.get_tile_by_position((self.row-1, self.col))
            self.neighbors['tr'] = self.board.get_tile_by_position((self.row-1, self.col+1))
            self.neighbors['br'] = self.board.get_tile_by_position((self.row+1, self.col))
            self.neighbors['bl'] = self.board.get_tile_by_position((self.row+1, self.col-1))      

        return self.neighbors

    def is_border(self):
        if None in self.neighbors.values():
            return True
        else:
            return False

    def __repr__(self):
        return f'{self.terrain} : {self.number} : {self.position}'


class Terrain(Enum):
    wood = 'wood'
    brick = 'brick'
    wheat = 'wheat'
    sheep = 'sheep'
    ore = 'ore'
    desert = 'desert'

    def __repr__(self):
        return self.value
