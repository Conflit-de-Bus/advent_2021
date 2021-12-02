import sys

def import_file_as_list(file_path):
    with open(file_path, 'r') as file:
        result = [line for line in file.readlines()]
    return result

class Submarine:

    def __init__(self, starting_position=(0,0), with_aim=False):
        self.x_position = starting_position[0]
        self.y_position = starting_position[1]
        self.aim = 0
        self.with_aim = with_aim

    def get_position(self):
        return (self.x_position, self.y_position)

    def go_up(self, movement):
        self.y_position -= movement * (int(not self.with_aim))
        self.aim -= movement

    def go_down(self, movement):
        self.y_position += movement * (int(not self.with_aim))
        self.aim += movement

    def go_forward(self, movement):
        self.x_position += movement
        self.y_position += movement * self.aim * int(self.with_aim)

    def move(self, movement_type, movement_amount):
        movement_functions = {
            "up": self.go_up,
            "down": self.go_down,
            "forward": self.go_forward
        }
        if movement_type in movement_functions:
            movement_functions[movement_type](movement_amount)

if __name__ == '__main__':
    movements_list = import_file_as_list(sys.argv[1])
    with_aim = len(sys.argv)  >= 3 and sys.argv[2].lower() == 'true'

    sub = Submarine(with_aim=with_aim)
    
    for movement in movements_list:
        sub.move(movement.rstrip().split(" ")[0], int(movement.rstrip().split(" ")[1]))
    
    print(f"position is {sub.get_position()}")
    print(f"result is {sub.x_position * sub.y_position}")
