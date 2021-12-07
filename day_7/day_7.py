import sys

def import_file_as_list(file_path):
    with open(file_path, 'r') as file:
        result = [int(value) for value in file.readlines()[0].rstrip().split(",")]
    return result

def get_result(file_path, part):
    data = import_file_as_list(file_path)
    shortest_distance = int((((max(data) - min(data)) * ((max(data) - min(data)) + 1)) / 2) * len(data))  # populate with maximum possible distance
    for target in range(min(data), max(data) + 1):
        distances_to_target = [abs(target - position) for position in data]
        distance_sum = 0
        for distance in distances_to_target:
            if part == 1:
                distance_sum += distance
            else:
                distance_sum += int((distance * (distance + 1)) / 2)
        shortest_distance = min(shortest_distance, distance_sum)
    return shortest_distance


if __name__ == '__main__':
    file_path = sys.argv[1]
    part = int(sys.argv[2])
    print(get_result(file_path=file_path, part=part))