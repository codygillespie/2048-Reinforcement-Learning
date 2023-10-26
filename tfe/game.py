from dataclasses import dataclass
import random

# TODO: Scoring is broken somewhere (increasing when a move that has no affect occurs). Fix it.

@dataclass
class GameState:
    cells: list[int]
    score: int
    history: list['GameState']
    last_move: int # -1 none, 0 up, 1 down, 2 left, 3 right

    @staticmethod
    def new() -> 'GameState':
        
        i, j = random.randint(0, 15), random.randint(0, 15)
        while i == j: j = random.randint(0, 15)
        
        cells = [0] * 16
        cells[i], cells[j] = 2, 2

        return GameState(cells, 0, [], -1)
    
    def up(self) -> 'GameState':
        rows = self.__get_rows()

        while True:
            initial_rows = rows.copy()
            for i in range(3): rows[i], rows[i+1], self.score = self.__merge(rows[i], rows[i+1])
            if rows == initial_rows: break

        return GameState(self.__add_cell_to_random_empty(self.__rows_to_cells(rows)), self.score, self.history + [self], 0)

    def down(self) -> 'GameState':
        rows = self.__get_rows()

        while True:
            initial_rows = rows.copy()
            for i in range(3, 0, -1): rows[i], rows[i-1], self.score = self.__merge(rows[i], rows[i-1])
            if rows == initial_rows: break

        return GameState(self.__add_cell_to_random_empty(self.__rows_to_cells(rows)), self.score, self.history + [self], 1)
    
    def left(self) -> 'GameState':
        columns = self.__get_columns()

        while True:
            initial_columns = columns.copy()
            for i in range(3): columns[i], columns[i+1], self.score = self.__merge(columns[i], columns[i+1])
            if columns == initial_columns: break

        return GameState(self.__add_cell_to_random_empty(self.__columns_to_cells(columns)), self.score, self.history + [self], 2)

    def right(self) -> 'GameState':
        columns = self.__get_columns()

        while True:
            initial_columns = columns.copy()
            for i in range(3, 0, -1): columns[i], columns[i-1], self.score = self.__merge(columns[i], columns[i-1])
            if columns == initial_columns: break

        return GameState(self.__add_cell_to_random_empty(self.__columns_to_cells(columns)), self.score, self.history + [self], 3)
    
    def is_game_over(self) -> bool: return all([self.up().cells == self.cells, self.down().cells == self.cells, self.left().cells == self.cells, self.right().cells == self.cells])
    
    def pretty_print(self) -> None:
        for i in range(4):
            print(*self.cells[i*4:i*4+4], sep='\t')
        print(f'Score: {self.score}')

    # TODO: test this:
    def to_csv(self, filename: str) -> None:
        with open(filename, 'w') as f:
            lines = []
            for state in self.history:
                lines.append(f'{state.last_move},{state.score},{",".join([str(cell) for cell in state.cells])}')
            f.write('\n'.join(lines))

    @staticmethod
    def from_csv(self, filename: str) -> 'GameState':
        with open(filename, 'r') as f:
            lines = f.readlines()
            history = []
            for line in lines:
                last_move, score, cells = line.split(',')
                history.append(GameState([int(cell) for cell in cells.split(',')], int(score), [], int(last_move)))
            return history[-1]

    def __get_rows(self) -> list[list[int]]: return [self.cells[i:i+4] for i in range(0, 16, 4)]
    def __get_columns(self) -> list[list[int]]: return [self.cells[i::4] for i in range(4)]
    def __rows_to_cells(self, rows: list[list[int]]) -> list[int]: return [cell for row in rows for cell in row]
    def __columns_to_cells(self, columns: list[list[int]]) -> list[int]: return [column[i] for i in range(4) for column in columns]
    def __add_cell_to_random_empty(self, cells: list[int]) -> list[int]:
        empty_cells = [i for i in range(16) if cells[i] == 0]
        if len(empty_cells) == 0: return cells
        cells[random.choice(empty_cells)] = random.choice([2, 4])
        return cells

    def __merge(self, v_1: list[int], v_2: list[int]) -> tuple[list[int], list[int], int]:
        # TODO: this isn't scoring correctly
        v_1, v_2 = v_1.copy(), v_2.copy()
        for i in range(len(v_1)):
            if v_1[i] == v_2[i]:
                self.score += v_1[i]
                v_1[i] *= 2
                v_2[i] = 0
            if v_1[i] == 0 and v_2[i] != 0:
                v_1[i], v_2[i] = v_2[i], 0
        return v_1, v_2, self.score
    
def do_game_loop():
    game = GameState.new()
    game.pretty_print()
    while True:
        move = input('Move: ')
        if move == 'w': game = game.up()
        elif move == 's': game = game.down()
        elif move == 'a': game = game.left()
        elif move == 'd': game = game.right()
        else: break
        game.pretty_print()

        if game.is_game_over():
            print('Game over!')
            break

if __name__ == '__main__':
    do_game_loop()