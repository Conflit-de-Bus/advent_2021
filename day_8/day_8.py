import sys

def import_file_as_list(file_path):
    with open(file_path, 'r') as file:
        result = [line.rstrip().split(" | ") for line in file.readlines()]
    return result

def line_as_words(line):
    result = []
    for part in line:
        for word in part.split(" "):
            result.append(word)
    return result

def get_one_and_four(line):
    line_all = line_as_words(line)
    line_all = [set(sorted(word)) for word in line_all]
    one, four = None, None
    for word in line_all:
        if len(word) == 2:
            one = word
        elif len(word) == 4:
            four = word
        if one is not None and four is not None:
            return one, four

def word_to_string_value(word, one, four):
    if word == one:
        return "1"
    elif word == four:
        return "4"
    elif len(word) == 3:
        return "7"
    elif len(word) == 7:
        return "8"
    else:
        if len(word) == 5:
            if len(word & one) == 2:
                return "3"
            elif len(word & four) == 2:
                return "2"
            else:
                return "5"
        else:
            if len(word & one) == 1:
                return "6"
            elif len(word & four) == 3:
                return "0"
            else:
                return "9"

def get_result(file_path, part):
    data = import_file_as_list(file_path)
    if part == 1:
        result = 0
        for line in data:
            for value in line[1].split(" "):
                result += int(len(value) in [2, 3, 4, 7])
        return result
    else:
        result = 0
        for line in data:
            one, four = get_one_and_four(line)
            line_result = ""
            line_output = line[1].split(" ")
            line_output = [set(sorted(word)) for word in line_output]
            for word in line_output:
                line_result += word_to_string_value(word, one, four)
            result += int(line_result)
        return result


if __name__ == '__main__':
    file_path = sys.argv[1]
    part = int(sys.argv[2])
    print(get_result(file_path=file_path, part=part))
