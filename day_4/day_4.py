import sys

class BingoGame:

    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file.readlines()]
        self.sequence = [int(number) for number in lines[0].split(",")]
        self.remaining_boards = {}
        self.complete_boards = {}
        self.winner = None
        self.last_winner = None
        i = 2
        while i < len(lines):
            temp_board = []
            while i < len(lines) and lines[i] != "":
                temp_board.append(lines[i])
                i += 1
            new_board = BingoBoard(temp_board)
            self.remaining_boards[id(new_board)] = new_board
            i += 1

    def play(self):
        self.end = False
        for number in self.sequence:
            boards_complete_this_number = []
            for board_id in self.remaining_boards:
                board = self.remaining_boards[board_id]
                board.draw_number(number)
                if board.row_or_column_complete:
                    self.complete_boards[board_id] = board
                    boards_complete_this_number.append(board_id)
                    self.end = True
            for board_id in boards_complete_this_number:
                del self.remaining_boards[board_id]
            if number == self.sequence[-1] or len(self.remaining_boards) == 0:
                self._select_winner(boards_complete_this_number, True)
            if self.end and self.winner == None:
                self._select_winner(self.complete_boards)

    def _select_winner(self, checked_boards, last_winner=False):
        for board_id in checked_boards:
            board = self.complete_boards[board_id]
            if last_winner:
                if self.last_winner is None or board.score <= self.winner.score:
                    self.last_winner = board
            else:
                if self.winner is None or board.score > self.winner.score:
                    self.winner = board
        return self.winner


class BingoBoard:

    def __init__(self, board_table):
        self.score = 0
        self.board = [[self._make_board_case(int(number)) for number in list(filter(lambda number_str: number_str != "", line.split(" ")))] for line in board_table]
        self.row_or_column_complete = False

    def _make_board_case(self, number):
        self.score += number
        return {"number": number, "drawn": False}

    def draw_number(self, number):
        for row in self.board:
            for case in row:
                if case["number"] == number:
                    self.score -= number
                    case["drawn"] = True
                    if self._check_if_complete():
                        self.score *= number
                    return True

    def _check_if_complete(self):
        for row in self.board:
            if self._check_row_is_complete(row):
                self.row_or_column_complete = True
                return True
        for column in range(len(row)):
            if self._check_column_is_complete(column):
                self.row_or_column_complete = True
                return True
        return False

    def _check_row_is_complete(self, row):
        for case in row:
            if not case["drawn"]:
                return False
        return True

    def _check_column_is_complete(self, column_position):
        for row in self.board:
            if not row[column_position]["drawn"]:
                return False
        return True

    def _display_case(self, number, drawn, number_length):
        result = ""
        for i in range(number_length - 2):
            result += " "
        result = f"  {str(number)[::-1]}{result}"
        if drawn:
            result = f"X{result[1:]}"
        return result[0:number_length][::-1]

    def __str__(self):
        
        result = ""
        for row in self.board:
            row_line = "|"
            for case in row:
                row_line = f"{row_line}{self._display_case(case['number'], case['drawn'], 6)}|"
            result = f"{result}{row_line}" + "\n"
        return result


if __name__ == '__main__':
    game = BingoGame(sys.argv[1])
    game.play()
    print(f"winner is board {id(game.winner)} with {game.winner.score} points:\n{game.winner}")
    print(f"last winner is board {id(game.last_winner)} with {game.last_winner.score} points:\n{game.last_winner}")
    if len(game.remaining_boards) != 0:
        print(f"{len(game.complete_boards)} boards were completed, {len(game.remaining_boards)} were not")