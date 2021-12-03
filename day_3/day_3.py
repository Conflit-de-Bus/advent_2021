import sys

def import_file_as_list(file_path):
    with open(file_path, 'r') as file:
        result = [line for line in file.readlines()]
    return result

def sum_of_position_in_words(data_list_list, position):
    """Consider the data (list of lists) as a table
    Make the sum of the nth column of that table
    """
    result = 0
    for word in data_list_list:
        result += word[position]
    return result

def sum_of_colums(data_list_list):
    """Consider the data (list of lists) as a table
    Return a list containing the sum of all its columns
    """
    result = []
    word_length = len(data_list_list[0])
    for i in range(word_length):
        result.append(sum_of_position_in_words(data_list_list, i))
    return result
    

def result_word_to_gamma_and_epsilon(result_word, data_length):
    """From the list of the sum of a all bits, determine the
    gamma and epsilon.
    Compare each sum with half the length of the list
    Return the two results as decimal
    """
    gamma_b_str, epsilon_b_str = "", ""
    for bit_sum in result_word:
        gamma_b_str += str(int(bit_sum >= (data_length / 2)))
        epsilon_b_str += str(int(bit_sum <= (data_length / 2)))
    return (int(gamma_b_str, 2), int(epsilon_b_str, 2))

def prepare_data(file_path):
    """Take all the lines from the input file and turn it
    into a list of lists. This can be considered as a table, with
    each row being a line of the table, and each column representing
    the nth char
    """
    data = [line.rstrip() for line in import_file_as_list(file_path)]
    result = []
    for line in data:
        result.append([int(char) for char in line])
    return result

def filter_lines_with_probable_nth(data, position, most_probable=True):
    """Recursive
    Take a list of lists and filter it colums by column
    Use the most or least probable value to filter columns
    Pass the filtered list.
    Stop conditions: if there is a single line left, or if we
    are at the end of the lines. In this last case, take the first
    result.
    """
    if position == len(data[0]) or len(data) == 1:
        result = ""
        for digit in data[0]:
            result += str(digit)
        return int(result, 2)
    if most_probable:
        probable_nth = int(sum_of_position_in_words(data, position) >= \
            (len(data) / 2))
    else:
        probable_nth = int(sum_of_position_in_words(data, position) < \
            (len(data) / 2))
    new_data = [word for word in data if word[position] == probable_nth]
    return filter_lines_with_probable_nth(
        new_data,
        position + 1,
        most_probable
    )


if __name__ == '__main__':
    data_as_lists = prepare_data(sys.argv[1])
    result_word = sum_of_colums(data_as_lists)
    gamma, epsilon = result_word_to_gamma_and_epsilon(
        result_word,
        len(data_as_lists)
    )
    print(f"gamma = {gamma}, epsilon = {epsilon}")
    print(f"first result = {gamma * epsilon }")
    oxygen = filter_lines_with_probable_nth(data_as_lists, 0, True)
    co2 =  filter_lines_with_probable_nth(data_as_lists, 0, False)
    print(f"oxygen = {oxygen}, co2 = {co2}")
    print(f"second result = {oxygen * co2}")
