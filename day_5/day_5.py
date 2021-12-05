import sys

def import_file_as_list(file_path):
    with open(file_path, 'r') as file:
        result = [line.rstrip() for line in file.readlines()]
    return result

def display_case(case, case_length):
        result = ""
        for i in range(case_length):
            result += " "
        result = f" {str(case)[::-1]}{result}"
        return result[0:case_length+2][::-1]

class VentsMap:

    def __init__(self, vents_list):
        self.vents = []
        self.vent_positions = {}
        self.map_max_x = 0
        self.map_max_y = 0
        for vent_data in vents_list:
            vent_data_split = vent_data.split(" -> ")
            x1 = int(vent_data_split[0].split(",")[0])
            y1 = int(vent_data_split[0].split(",")[1])
            x2 = int(vent_data_split[1].split(",")[0])
            y2 = int(vent_data_split[1].split(",")[1])
            self.add_vent(x1, y1, x2, y2)
            self.determine_vent_points(x1, y1, x2, y2)

    def add_vent(self, x1, y1, x2, y2):
        self.vents.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})

    def determine_vent_points(self, x1, y1, x2, y2):
        self.map_max_x, self.map_max_y = max(self.map_max_x, x1, x2), max(self.map_max_y, y1, y2)
        if x1 == x2:
            for y_position in range(min(y1, y2), max(y1, y2) + 1):
                self._add_vent_position(x1, y_position)
        elif y1 == y2:
            for x_position in range(min(x1, x2), max(x1, x2) + 1):
                self._add_vent_position(x_position, y1)
        elif (y2 - y1) / (x2 - x1) == 1:
            for delta in range(0, max(x1, x2) - min(x1, x2) + 1):
                self._add_vent_position(min(x1, x2) + delta, min(y1, y2) + delta)
        elif (y2 - y1) / (x2 - x1) == -1:
            for delta in range(0, max(x1, x2) - min(x1, x2) + 1):
                self._add_vent_position(min(x1, x2) + delta, max(y1, y2) - delta)

    def get_intersect_count(self):
        intersect_count = 0
        for point in self.vent_positions:
            if self.vent_positions[point] > 1:
                intersect_count += 1
        return intersect_count

    def _add_vent_position(self, x, y):
        if (x, y) not in self.vent_positions:
            self.vent_positions[(x, y)] = 0
        self.vent_positions[(x, y)] += 1

    def draw_map(self, no_vent_char = " "):
        char_length = len(str(max([self.vent_positions[coordinates] for coordinates in self.vent_positions])))
        for y_position in range(self.map_max_y + 1):
            line_to_print = ""
            for x_position in range(self.map_max_x + 1):
                line_to_print = f"{line_to_print}{display_case(self.vent_positions.get((x_position, y_position)) or no_vent_char, char_length)}"
            print(line_to_print)
            

if __name__ == '__main__':
    data = import_file_as_list(sys.argv[1])
    vents_map = VentsMap(data)
    print(f"there are {vents_map.get_intersect_count()} dangerous points")
    # With the size of the map, it is useless to draw it in a terminal.
    # But in a file, with low zoom, it's pretty fun
    vents_map.draw_map()