from dataclasses import dataclass
import random

@dataclass
class GameState:
    cells: list[int]
    score: int = 0

    @staticmethod
    def new() -> 'GameState':
        
        i, j = random.randint(0, 16), random.randint(0, 16)
        while i == j: j = random.randint(0, 16)
        
        cells = [0] * 16
        cells[i], cells[j] = 2, 2

        return GameState(cells)
    
    def up(self) -> 'GameState':
        rows = self.__get_rows()

        while True:
            initial_rows = rows.copy()
            for i in range(3): rows[i], rows[i+1], self.score = self.__merge(rows[i], rows[i+1])
            if rows == initial_rows: break

        return GameState(self.__rows_to_cells(rows), self.score)

    def down(self) -> 'GameState':
        rows = self.__get_rows()

        while True:
            initial_rows = rows.copy()
            for i in range(3, 0, -1): rows[i], rows[i-1], self.score = self.__merge(rows[i], rows[i-1])
            if rows == initial_rows: break

        return GameState(self.__rows_to_cells(rows), self.score)
    
    def left(self) -> 'GameState':
        columns = self.__get_columns()

        while True:
            initial_columns = columns.copy()
            for i in range(3): columns[i], columns[i+1], self.score = self.__merge(columns[i], columns[i+1])
            if columns == initial_columns: break

        return GameState(self.__columns_to_cells(columns), self.score)

    def right(self) -> 'GameState':
        columns = self.__get_columns()

        while True:
            initial_columns = columns.copy()
            for i in range(3, 0, -1): columns[i], columns[i-1], self.score = self.__merge(columns[i], columns[i-1])
            if columns == initial_columns: break

        return GameState(self.__columns_to_cells(columns), self.score)

    def __get_rows(self) -> list[list[int]]: return [self.cells[i:i+4] for i in range(0, 16, 4)]
    def __get_columns(self) -> list[list[int]]: return [self.cells[i::4] for i in range(4)]
    def __rows_to_cells(self, rows: list[list[int]]) -> list[int]: return [cell for row in rows for cell in row]
    def __columns_to_cells(self, columns: list[list[int]]) -> list[int]: return [column[i] for i in range(4) for column in columns]

    def __merge(self, v_1: list[int], v_2: list[int]) -> tuple[list[int], list[int], int]:
        v_1, v_2 = v_1.copy(), v_2.copy()
        for i in range(len(v_1)):
            if v_1[i] == v_2[i]:
                v_1[i] *= 2
                v_2[i] = 0
                self.score += v_1[i]
            if v_1[i] == 0 and v_2[i] != 0:
                v_1[i], v_2[i] = v_2[i], 0
        return v_1, v_2, self.score