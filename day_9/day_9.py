import sys
import time
import math

DRAW_DELAY = 0

class Board:
    """Defines the whole terrain, contains all points"""

    def __init__(self, file_path: str):
        with open(file_path, 'r') as file:
            self.numbers = [[int(number) for number in line if number != '\n'] for line in file.readlines()]
        self.low_points = []
        self.risk_level = 0
        self.discovered_points = set()

    def check_below_right(self, x: int, y: int):
        """Check if the point on the right of xy coordinates is higher"""
        return x == len(self.numbers[0]) - 1 or self.numbers[y][x+1] > self.numbers[y][x]

    def check_below_left(self, x: int, y: int):
        """Check if the point on the left of xy coordinates is higher"""
        return x == 0 or self.numbers[y][x-1] > self.numbers[y][x]

    def check_below_down(self, x: int, y: int):
        """Check if the point below xy coordinates is higher"""
        return y == len(self.numbers) - 1 or self.numbers[y+1][x] > self.numbers[y][x]

    def check_below_up(self, x: int, y: int):
        """Check if the point above xy coordinates is higher"""
        return y == 0 or self.numbers[y-1][x] > self.numbers[y][x]

    def check_low_point(self, x: int, y: int):
        """Check if a point at xy coordinates is a low point
        This checks that the 4 points around it are higher, or outside
        """
        if not self.check_below_left(x, y):
            return False
        if not self.check_below_up(x, y):
            return False
        if not self.check_below_right(x, y):
            return False
        if not self.check_below_down(x, y):
            return False
        return True

    def determine_low_points(self):
        """Determine the list of low points in the whole board"""
        for y in range(len(self.numbers)):
            for x in range(len(self.numbers[0])):
                if self.check_low_point(x, y):
                    self.low_points.append((x, y))
                    self.risk_level += (self.numbers[y][x] + 1)

    def draw_map(self):
        """Draw a map in the map file
        Depth is visualized with transparency
        """
        with open('./map', 'w+') as file:
            for y in range(len(self.numbers)):
                current_line = ""
                for x in range(len(self.numbers[0])):
                    if self.numbers[y][x] == 9:
                        current_line += '█'
                    elif (x, y) in self.low_points:
                        current_line += ' '
                    elif (x, y) in self.discovered_points:
                        if self.numbers[y][x] < 3:
                            current_line += '░'
                        elif self.numbers[y][x] < 6:
                            current_line += '▒'
                        else:
                            current_line += '▓'
                    else:
                        current_line += ' '
                file.write(f"{current_line}\n")


class Basin:
    """Represents a basin in the whole board. Contains all its points"""

    def __init__(self, board, low_point):
        self.board = board
        self.low_point = low_point
        self.points = {low_point}
        self.expanded_points = {low_point}
        self.current_expansion = set()

    def right_to_add(self, x: int, y: int):
        """Checks if the point right of xy coordinates is part of the basin
        If the point is already in basin, this does not need to add it so it
        will return False
        """
        return not (x == len(self.board.numbers[0]) - 1 or self.board.numbers[y][x+1] == 9 or (x+1, y) in self.current_expansion or (x+1, y) in self.points)

    def left_to_add(self, x: int, y: int):
        """Checks if the point left of xy coordinates is part of the basin
        If the point is already in basin, this does not need to add it so it
        will return False
        """
        return not (x == 0 or self.board.numbers[y][x-1] == 9 or (x-1, y) in self.current_expansion or (x-1, y) in self.points)

    def down_to_add(self, x: int, y: int):
        """Checks if the point down of xy coordinates is part of the basin
        If the point is already in basin, this does not need to add it so it
        will return False
        """
        return not (y == len(self.board.numbers) - 1 or self.board.numbers[y+1][x] == 9 or (x, y+1) in self.current_expansion or (x, y+1) in self.points)

    def up_to_add(self, x: int, y: int):
        """Checks if the point up of xy coordinates is part of the basin
        If the point is already in basin, this does not need to add it so it
        will return False
        """
        return not (y == 0 or self.board.numbers[y-1][x] == 9 or (x, y-1) in self.current_expansion or (x, y-1) in self.points)

    def expand_points(self, draw_map=False, draw_delay=0):
        """Make one round of point expansion.
        Checks if points adjacent of all points in the last expansion round
        have to be added, and define the new last round accordingly. Add
        points to the list of points of the basin
        """
        if draw_map:
            self.board.draw_map()
            time.sleep(draw_delay)
        for point in self.expanded_points:
            if self.right_to_add(point[0], point[1]):
                self.current_expansion.add((point[0] + 1, point[1]))
            if self.left_to_add(point[0], point[1]):
                self.current_expansion.add((point[0] - 1, point[1]))
            if self.down_to_add(point[0], point[1]):
                self.current_expansion.add((point[0], point[1] + 1))
            if self.up_to_add(point[0], point[1]):
                self.current_expansion.add((point[0], point[1] - 1))
        self.points = set.union(self.points, self.current_expansion)
        self.expanded_points = self.current_expansion
        self.current_expansion = set()
        self.board.discovered_points = set.union(self.board.discovered_points, self.points)

    def determine_points(self, draw_map=False, draw_delay=0):
        """Determine all the points of the basin. Use the expansion method.
        This makes rounds of expansion until there is no more points that need
        to be expanded
        """
        while len(self.expanded_points) > 0:
            self.expand_points(draw_map=draw_map, draw_delay=draw_delay)


def get_result(file_path, part, draw_map, draw_delay):
    board = Board(file_path)
    board.determine_low_points()
    if part == 1:
        return board.risk_level
    three_largest_basins_sizes = [0, 0, 0]
    for low_point in board.low_points:
        current_basin = Basin(board, low_point)
        current_basin.determine_points(draw_map, draw_delay)
        if len(current_basin.points) > min(three_largest_basins_sizes):
            three_largest_basins_sizes.remove(min(three_largest_basins_sizes))
            three_largest_basins_sizes.append(len(current_basin.points))
    return math.prod(three_largest_basins_sizes)


if __name__ == '__main__':
    file_path = sys.argv[1]
    part = int(sys.argv[2])
    try:
        draw_map = bool(sys.argv[3])
        draw_delay = float(sys.argv[4])
    except IndexError:
        draw_map = False
        draw_delay = 0
    print(get_result(file_path=file_path, part=part, draw_map=draw_map, draw_delay=draw_delay))
