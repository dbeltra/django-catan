from enum import Enum
import random

NUM_WOOD = 4
NUM_SHEEP = 4
NUM_WHEAT = 4
NUM_ORE = 3
NUM_BRICK = 3
NUM_DESERT = 1

HARBORS = ['wood', 'brick', 'wheat', 'sheep', 'ore', 'generic', 'generic', 'generic', 'generic']


TILES_NUMBERS = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
TILES_DIRECTION_DISTRIBUTION = ['r','br','bl','l','tl','tr']

class Terrain(Enum):
    wood = 'wood'
    brick = 'brick'
    wheat = 'wheat'
    sheep = 'sheep'
    ore = 'ore'
    desert = 'desert'
    sea = 'sea'

    def __repr__(self):
        return self.value

class Tile(object):
    terrain = None
    number = None
    position = None
    row = None
    col = None
    neighbors = None

    def __init__(self, terrain, number, position):
        self.terrain = terrain
        self.number = number
        self.position = position
        self.row = position[0]
        self.col = position[1]

    def __del__(self):
        print('Tile deleted')

    def __repr__(self):
        return f'{self.terrain} : {self.number} : {self.position}'

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def is_border(self):
        if None in self.neighbors.values():
            return True
        else:
            return False


class Board(object):
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
                tile = Tile(terrain=piece, number=None, position=(row_idx,col_idx))
                self.tiles.append(tile)

        self.init_numbers_official()
        self.init_sea()
        self.init_harbors()

    def __del__(self):
        for tile in self.tiles:
            del tile
        print('board erased')

    @classmethod
    def from_json(cls, data):
        tiles = list(map(Tile.from_json, data["tiles"]))
        return cls(tiles)

    def init_numbers_official(self):
        self.numbers = TILES_NUMBERS.copy()

        next_tile = self.tiles[0]
        direction = 'r'
        while next_tile != None:
            current_tile = next_tile
            self.put_number_in_tile(current_tile)
            next_tile, direction = self.get_next_tile(current_tile, direction)

    def get_next_tile(self, tile, direction):
        neighbors = self.find_tile_neighbors(tile)
        next_tile = neighbors[direction]

        if next_tile is None or next_tile.number is not None:
            current_direction_array_idx = TILES_DIRECTION_DISTRIBUTION.index(direction)

            for number_directions_options in range(1, len(TILES_DIRECTION_DISTRIBUTION)):
                next_direction_array_idx = current_direction_array_idx + number_directions_options
                if next_direction_array_idx >= len(TILES_DIRECTION_DISTRIBUTION):
                    next_direction_array_idx = next_direction_array_idx - len(TILES_DIRECTION_DISTRIBUTION)
                       
                new_direction = TILES_DIRECTION_DISTRIBUTION[next_direction_array_idx]
                next_tile = neighbors[new_direction]

                if next_tile is not None and next_tile.number is  None:
                    return next_tile, new_direction
            return None, None
        else:
            return next_tile, direction
        
    def put_number_in_tile(self,tile):
        if tile.terrain is not Terrain.desert:
            tile.number = self.numbers.pop(0)
        else:
            tile.number = 0

    def get_tile_by_position(self, position):
        matching_tile = None
        for tile in self.tiles:
            if tile.position == position and tile.terrain is not Terrain.sea:
                matching_tile = tile
        return matching_tile

    def find_tile_neighbors(self, tile):
        tile.neighbors = {
            'tl': self.find_tile_neighbor_in_direction(tile,'tl')['tile'],
            'tr': self.find_tile_neighbor_in_direction(tile,'tr')['tile'],
            'r': self.find_tile_neighbor_in_direction(tile,'r')['tile'],
            'br': self.find_tile_neighbor_in_direction(tile,'br')['tile'],
            'bl': self.find_tile_neighbor_in_direction(tile,'bl')['tile'],
            'l': self.find_tile_neighbor_in_direction(tile,'l')['tile'],
        }

        return tile.neighbors

    def find_tile_neighbor_in_direction(self, tile, direction):
        neighbor = {}
        if direction == 'r':
            position = (tile.row, tile.col+1)
        if direction == 'l':
            position = (tile.row, tile.col-1)

        nrows = self.num_rows
        if tile.row < (nrows-1)/2:
            if direction == 'tl':
                position = (tile.row-1, tile.col-1)
            if direction == 'tr':
                position = (tile.row-1, tile.col)
            if direction == 'br':
                position = (tile.row+1, tile.col+1)
            if direction == 'bl':
                position = (tile.row+1, tile.col)

        if tile.row == (nrows-1)/2:
            if direction == 'tl':
                position = (tile.row-1, tile.col-1)
            if direction == 'tr':
                position = (tile.row-1, tile.col)
            if direction == 'br':
                position = (tile.row+1, tile.col)
            if direction == 'bl':
                position = (tile.row+1, tile.col-1)

        if tile.row > (nrows-1)/2:
            if direction == 'tl':
                position = (tile.row-1, tile.col)
            if direction == 'tr':
                position = (tile.row-1, tile.col+1)
            if direction == 'br':
                position = (tile.row+1, tile.col)
            if direction == 'bl':
                position = (tile.row+1, tile.col-1)

        neighbor['position'] = position
        neighbor['tile'] = self.get_tile_by_position(position)

        return neighbor

    def init_sea(self):
        sea_tiles = []
        positions_created = []
        nrows = self.num_rows
        for tile in self.tiles:
            neighbors = self.find_tile_neighbors(tile)
            for n in neighbors:
                if neighbors[n] is None:
                    position = self.find_tile_neighbor_in_direction(tile, n)['position']
                    if position not in positions_created:
                        positions_created.append(position)
                        sea_tile = Tile(terrain=Terrain.sea, number=None, position=position)
                        sea_tiles.append(sea_tile)

        self.tiles += sea_tiles

    def init_harbors(self):
        pass

    def get_tiles_row(self, row):
        match_row = []
        highest_col = -50
        for tile in self.tiles:
            if tile.row == row:
                if tile.col > highest_col:
                    match_row.append(tile)
                    highest_col = tile.col
                else:
                    match_row.insert(0,tile)
        return match_row

    def print_board(self):
       for tile in self.tiles:
           print(tile)

