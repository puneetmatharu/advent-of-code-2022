import re
import numpy as np
from enum import IntEnum
from pathlib import Path
from typing import Union


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"

# Bit of a cheat but I'm too lazy to set up the face connectivity automatically :)

EXAMPLE_CONNECTIVITY = {
    1: {'L': (3, "R"), 'R': (6, "R"), 'U': (2, "R"), 'D': (4, 'U')},
    2: {'L': (1, "R"), 'R': (3, 'L'), 'U': (6, "D"), 'D': (5, "D")},
    3: {'L': (2, 'R'), 'R': (4, 'L'), 'U': (1, "L"), 'D': (5, "L")},
    4: {'L': (3, 'R'), 'R': (6, "U"), 'U': (1, 'D'), 'D': (5, 'U')},
    5: {'L': (3, "D"), 'R': (6, 'L'), 'U': (4, 'D'), 'D': (2, "D")},
    6: {'L': (5, 'R'), 'R': (1, "R"), 'U': (4, "R"), 'D': (2, "U")},
}

TEST_CONNECTIVITY = {
    1: {'L': (4, "L"), 'R': (2, 'L'), 'U': (6, "L"), 'D': (3, 'U')},
    2: {'L': (1, 'R'), 'R': (5, "R"), 'U': (6, "D"), 'D': (3, "R")},
    3: {'L': (4, "U"), 'R': (2, "D"), 'U': (1, 'D'), 'D': (5, 'U')},
    4: {'L': (1, "L"), 'R': (5, 'L'), 'U': (3, "L"), 'D': (6, 'U')},
    5: {'L': (4, 'R'), 'R': (2, "R"), 'U': (3, 'D'), 'D': (6, "R")},
    6: {'L': (1, "L"), 'R': (5, "D"), 'U': (4, 'D'), 'D': (2, "U")},
}


DirectionVectors = {
    "R": np.array([0, 1]),
    "D": np.array([1, 0]),
    "L": np.array([0, -1]),
    "U": np.array([-1, 0]),
}


class Tile(IntEnum):
    OpenTile = 0
    SolidWall = 1
    OutOfBounds = 2


class Board:
    def turn_left(self) -> None:
        self.direction = {"R": "U", "U": "L", "L": "D", "D": "R"}[self.direction]

    def turn_right(self) -> None:
        self.direction = {"R": "D", "D": "L", "L": "U", "U": "R"}[self.direction]

    def get_password(self) -> int:
        ((i, j), dv) = (self.get_global_pos(), {"R": 0, "D": 1, "L": 2, "U": 3}[self.direction])
        return (1000 * (1 + i)) + (4 * (1 + j)) + dv

    def get_global_pos(self) -> Union[tuple[int, int], np.ndarray]:
        raise NotImplementedError("Boop.")


class FlatBoard(Board):
    def __init__(self, board: list[list[str]]) -> None:
        self.parse_board(board)
        self.start = np.array([0, int(np.argwhere(self.board[0] == Tile.OpenTile)[0])])
        self.pos = np.copy(self.start)
        self.direction = "R"

    def parse_board(self, board: list[list[str]]) -> str:
        tile_map = {".": Tile.OpenTile, "#": Tile.SolidWall, " ": Tile.OutOfBounds}
        data = [[x for x in map(lambda c: tile_map[c], line)] for line in board]
        self.board = np.array(data)

    def get_global_pos(self) -> Union[tuple[int, int], np.ndarray]:
        return self.pos

    def is_off_map(self, pos: tuple[int, int]) -> bool:
        if not ((0 <= pos[0] < self.board.shape[0]) and (0 <= pos[1] < self.board.shape[1])):
            return True
        if self.board[pos[0], pos[1]] == Tile.OutOfBounds:
            return True
        return False

    def move_forward(self, n_space: int) -> None:
        for _ in range(n_space):
            next_pos = self.pos + DirectionVectors[self.direction]
            if self.is_off_map(next_pos):
                if self.direction in ("L", "R"):
                    row = self.board[self.pos[0]]
                    ind = -1 if (self.direction == "L") else 0
                    next_pos[1] = int(np.argwhere(row != Tile.OutOfBounds)[ind])
                elif self.direction in ("U", "D"):
                    col = self.board[:, self.pos[1]]
                    ind = -1 if (self.direction == "U") else 0
                    next_pos[0] = int(np.argwhere(col != Tile.OutOfBounds)[ind])
            if self.board[next_pos[0], next_pos[1]] == Tile.SolidWall:
                return
            self.pos = next_pos


class CubeBoard(Board):
    class Face:
        def __init__(self, face_id: int, data: np.ndarray, coords: np.ndarray) -> None:
            self.face_id = face_id
            self.data = data
            self.coords = coords
            self.neighbours: dict = {"L": None, "R": None, "U": None, "D": None}

    def __init__(
        self,
        board: list[list[str]],
        connectivity: dict,
        side_length: int,
    ) -> None:
        self.parse_board(board, side_length)
        self.start = np.array([0, int(np.argwhere(self.get_face(1).data[0] == Tile.OpenTile)[0])])
        self.local_pos = np.copy(self.start)
        self.connectivity = connectivity
        self.face = 1
        self.direction = "R"
        self.side_length = side_length

    def parse_board(self, board: list[list[str]], side_length: int) -> None:
        tile_map = {".": Tile.OpenTile, "#": Tile.SolidWall, " ": Tile.OutOfBounds}
        data = np.array([[x for x in map(lambda c: tile_map[c], line)] for line in board])
        on_board_mask = (data == Tile.OpenTile) | (data == Tile.SolidWall)
        counter = 1
        faces = []
        (n_row, n_col) = data.shape
        board_coords = np.stack(np.meshgrid(range(n_row), range(n_col), indexing="ij"), axis=-1)
        (n_region_row, n_region_col) = (data.shape[0] // side_length, data.shape[1] // side_length)
        for i in range(n_region_row):
            for j in range(n_region_col):
                i_slice = slice(i * side_length, (i + 1) * side_length)
                j_slice = slice(j * side_length, (j + 1) * side_length)
                if np.all(on_board_mask[i_slice, j_slice]):
                    faces += [
                        self.Face(counter, data[i_slice, j_slice], board_coords[i_slice, j_slice])
                    ]
                    counter += 1
        self.faces = faces
        self.board = data

    def get_global_pos(self):
        return self.get_face(self.face).coords[self.local_pos[0], self.local_pos[1]]

    def get_face(self, i: int) -> Face:
        return self.faces[i - 1]

    def is_off_face(self, local_pos: tuple[int, int]) -> bool:
        if (0 <= local_pos[0] < self.side_length) and (0 <= local_pos[1] < self.side_length):
            return False
        return True

    def local_coords_along_edge(self, edge: str) -> None:
        # Local coords ordered by a clockwise traversal around the face edge
        if edge == "L":
            return np.array([[i, 0] for i in reversed(range(self.side_length))])
        elif edge == "U":
            return np.array([[0, i] for i in range(self.side_length)])
        elif edge == "R":
            return np.array([[i, self.side_length - 1] for i in range(self.side_length)])
        elif edge == "D":
            return np.array([[self.side_length - 1, i] for i in reversed(range(self.side_length))])

    def index_along_edge(self) -> None:
        assert any([self.local_pos[0] in (0, self.side_length - 1),
                   self.local_pos[1] in (0, self.side_length - 1)])
        if self.direction == "L":
            return (self.side_length - 1) - self.local_pos[0]
        elif self.direction == "U":
            return self.local_pos[1]
        elif self.direction == "R":
            return self.local_pos[0]
        elif self.direction == "D":
            return (self.side_length - 1) - self.local_pos[1]

    def is_blocked(self, face: int, pos: Union[list, np.ndarray]) -> bool:
        if self.get_face(face).data[pos[0], pos[1]] == Tile.SolidWall:
            return True
        return False

    def move_forward(self, n_space: int) -> None:
        for _ in range(n_space):
            next_pos = self.local_pos + DirectionVectors[self.direction]
            if self.is_off_face(next_pos):
                (new_face, next_edge) = self.connectivity[self.face][self.direction]
                new_direction = {"L": "R", "R": "L", "U": "D", "D": "U"}[next_edge]  # reflect
                current_index = self.index_along_edge()
                next_edge_local_coords = self.local_coords_along_edge(next_edge)
                next_pos = next_edge_local_coords[(self.side_length - 1) - current_index]
                if self.is_blocked(new_face, next_pos):
                    return
                (self.face, self.local_pos, self.direction) = (new_face, next_pos, new_direction)
            if self.is_blocked(self.face, next_pos):
                return
            self.local_pos = next_pos


def solve_pt1(board: list[list[str]], moves: list[Union[int, str]]) -> int:
    board = FlatBoard(board)
    for (i, m) in enumerate(moves):  # moves = (number, letter, number, ...)
        if i % 2 == 0:
            board.move_forward(m)
        elif m == "L":
            board.turn_left()
        elif m == "R":
            board.turn_right()
    return board.get_password()


def solve_pt2(board: list[list[str]], moves: list[Union[int, str]], connectivity: dict, side_length: int) -> int:
    board = CubeBoard(board, connectivity, side_length)
    for (i, m) in enumerate(moves):  # moves = (number, letter, number, ...)
        if i % 2 == 0:
            board.move_forward(m)
        elif m == "L":
            board.turn_left()
        elif m == "R":
            board.turn_right()
    return board.get_password()


def load(fpath: str) -> tuple[list[list[str]], list[Union[int, str]]]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    longest_line = max([len(line) for line in text[:-2]])
    board = [list(line.ljust(longest_line)) for line in text[:-2]]
    moves = re.findall(r"([LR]|\d+)", text[-1])
    moves[::2] = list(map(int, moves[::2]))
    return (board, moves)


def main() -> int:
    (board1, moves1) = load(EXAMPLE_DATA_PATH)
    (board2, moves2) = load(TEST_DATA_PATH)

    example_solution1 = 6032
    example_solution2 = 5031
    test_solution1 = 164014
    test_solution2 = 47525

    example_answer1 = solve_pt1(board1, moves1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(board2, moves2)
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(board1, moves1, EXAMPLE_CONNECTIVITY, 4)
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(board2, moves2, TEST_CONNECTIVITY, 50)
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
