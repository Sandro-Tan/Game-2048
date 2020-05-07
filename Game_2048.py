"""
2048 game
Move and merge squares using arrow keys
Get a 2048-value tile to win

Author: Sandro Tan
Date: Aug 2019
Version: 1.0
"""

import GUI_2048
import random
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # remove all zeros in original line and output into a new list
    newlist = []
    output = []

    for item in line:
        if item != 0:
            newlist.append(item)

    # merge the numbers
    for index in range(len(newlist) - 1):
        if newlist[index] == newlist[index + 1]:
            newlist[index] *= 2
            newlist[index + 1] = 0

    for item in newlist:
        if item != 0:
            output.append(item)

    while len(output) < len(line):
        output.append(0)

    return output


# helper function to return number 2 (90%) or 4 (10%)
def random_number(nums, probs):

    seed = random.random()

    if seed > probs[0]:
        return nums[1]
    else:
        return nums[0]


class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width

        # initial tiles indices
        self.indices_up = [[0, col] for col in range(self.get_grid_width())]
        self.indices_down = [[self.get_grid_height() - 1, col] for col in range(self.get_grid_width())]
        self.indices_left = [[row, 0] for row in range(self.get_grid_height())]
        self.indices_right = [[row, self.get_grid_width() - 1] for row in range(self.get_grid_height())]
        self.indices_dict = {UP: self.indices_up,
                             DOWN: self.indices_down,
                             LEFT: self.indices_left,
                             RIGHT: self.indices_right}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # stores intitial values
        self.cells_value = [[0 for row in range(self.grid_height)] for col in range(self.grid_width)]

        for dummy_idx in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        output = 'Height:' + str(self.get_grid_height())
        output += ' Width:' + str(self.get_grid_width())
        return output

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        '''
        indices dictionary stores the indices of edge cells 
        For example, after pressing up arrow key,
        edge tiles variable will store the indices of the top row
        '''
        edge_tiles = self.indices_dict[direction]

        # Get the lines that hold values
        line = []
        for item in edge_tiles:
            temp = []
            row_index = item[0]
            col_index = item[1]
            temp.append(self.get_tile(row_index, col_index))
            for dummy_idx in range(len(edge_tiles) - 1):
                row_index += OFFSETS[direction][0]
                col_index += OFFSETS[direction][1]
                temp.append(self.get_tile(row_index, col_index))
            line.append(temp)

        # Merge the lines and put them in a new list
        merged = []
        for item in line:
            merged.append(merge(item))

        # Convert row and col in merged list to those in a grid to be painted
        # Still thinking about some way to simplify these codes
        if direction == UP:
            for row in range(len(merged[0])):
                for col in range(len(merged)):
                    self.set_tile(col, row, merged[row][col])

        if direction == DOWN:
            for row in range(len(merged[0])):
                for col in range(len(merged)):
                    self.set_tile(self.get_grid_height() - col - 1, row, merged[row][col])

        if direction == LEFT:
            for row in range(len(merged)):
                for col in range(len(merged[0])):
                    self.set_tile(row, col, merged[row][col])

        if direction == RIGHT:
            for row in range(len(merged)):
                for col in range(len(merged[0])):
                    self.set_tile(row, self.get_grid_width() - col - 1, merged[row][col])

        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        random_row = random.randint(0, self.get_grid_height() - 1)
        random_col = random.randint(0, self.get_grid_width() - 1)
        value = random_number((2, 4), (0.9, 0.1))

        if self.get_tile(random_row, random_col) == 0:
            self.set_tile(random_row, random_col, value)
        # no two tiles at the same location
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.cells_value[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.cells_value[row][col]

    def game_win(self):
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self.get_tile(row, col) == 2048:
                    print("You win!")
        self.reset()


game = TwentyFortyEight(4,4)
GUI_2048.run_gui(game)
