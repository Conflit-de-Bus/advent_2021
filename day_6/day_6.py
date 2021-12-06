import sys

def import_file_as_list(file_path):
    with open(file_path, 'r') as file:
        result = [int(value) for value in file.readlines()[0].rstrip().split(",")]
    return result

class School:

    def __init__(self, fish, frequency, puberty):
        self.ages = {}
        self.frequency = frequency
        self.puberty = puberty
        for i in range(frequency + puberty):
            self.ages[i] = 0
        for single_fish in fish:
            self.ages[single_fish] += 1

    def age_all_fish(self):
        temp_fish = {}
        temp_fish[self.frequency + self.puberty - 1] = self.ages[0]
        for i in range(self.frequency + self.puberty - 1):
            temp_fish[i] = self.ages[i + 1]
        temp_fish[self.frequency - 1] += temp_fish[self.frequency + self.puberty - 1]
        self.ages = temp_fish

    def count_fish(self):
        result = 0
        for age in self.ages:
            result += self.ages[age]
        return result


if __name__ == '__main__':
    fish = import_file_as_list(sys.argv[1])
    school = School(fish, 7, 2)
    for i in range(int(sys.argv[2])):
        school.age_all_fish()
    print(school.count_fish())