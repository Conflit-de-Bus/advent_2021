mkdir day_$1;
mkdir day_$1/inputs;
touch day_$1/inputs/input_test;
touch day_$1/inputs/input;
echo "import day_$1\n\ndef test_result_part_1():\n    assert day_$1.get_result(\"day_$1/inputs/input_test\", 1) == True\n\ndef test_result_part_2():\n    assert day_$1.get_result(\"day_$1/inputs/input_test\", 2) == True" > day_$1/test_day_$1.py;
echo "import sys\n\ndef import_file_as_list(file_path):\n    with open(file_path, 'r') as file:\n        result = []\n    return result\n\ndef get_result(file_path, part):\n    return True\n\n\nif __name__ == '__main__':\n    file_path = sys.argv[1]\n    part = int(sys.argv[2])\n    print(get_result(file_path=file_path, part=part))" > day_$1/day_$1.py;