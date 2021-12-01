import sys

def sum_of_window_elements(data, starting_point, window_size):
    result = 0
    for i in range(window_size):
        result += data[starting_point + i]
    return result

def windows_descending(file_path, window_size):
    with open(file_path, 'r') as day_1_input:
        depth_data = [int(single_input.rstrip()) for single_input in day_1_input.readlines()]

    times_depth_higher = 0

    for i in range(len(depth_data) - window_size):
        times_depth_higher += int(
            sum_of_window_elements(depth_data, i, window_size) < \
            sum_of_window_elements(depth_data, i + 1, window_size))
    
    return times_depth_higher

if __name__ == '__main__':
    print(windows_descending(sys.argv[1], int(sys.argv[2])))