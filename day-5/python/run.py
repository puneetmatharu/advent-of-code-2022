import re
from copy import deepcopy as dc
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


@dataclass
class Move:
    num_crate: int
    start: int
    end: int


@dataclass
class Crates:
    crates: list[list[str]]

    def get_message(self) -> None:
        message = ""
        for stack in self.crates:
            if len(stack) > 0:
                message += stack[-1]
        return message


class CrateMover9000:
    @staticmethod
    def move(crates: Crates, n: int, start: int, end: int) -> None:
        assert len(crates[start]) >= n
        taken = crates[start][-n:]
        crates[start] = crates[start][:-n]
        crates[end] = crates[end] + taken[::-1]
        return crates


class CrateMover9001:
    @staticmethod
    def move(crates: Crates, n: int, start: int, end: int) -> None:
        assert len(crates[start]) >= n
        taken = crates[start][-n:]
        crates[start] = crates[start][:-n]
        crates[end] = crates[end] + taken
        return crates


def solve_pt1(crates: Crates, moves: list[Move]) -> int:
    for move in moves:
        crates.crates = CrateMover9000.move(
            crates.crates, move.num_crate, move.start - 1, move.end - 1)
    return crates.get_message()


def solve_pt2(crates: Crates, moves: list[Move]) -> int:
    for move in moves:
        crates.crates = CrateMover9001.move(
            crates.crates, move.num_crate, move.start - 1, move.end - 1)
    return crates.get_message()


def parse_crate_line(line: str, n_column: int) -> list[Optional[str]]:
    assert (len(line) + 1) == (n_column * 4)
    crates = [line[4*i+1] for i in range(n_column)]
    return crates


def load(fpath: str) -> tuple[Crates, list[Move]]:
    lines = None
    with open(fpath, "r") as f:
        lines = f.read().split("\n")
    height = 0
    for i, line in enumerate(lines):
        if line.startswith(" 1"):
            height = i
    crates_info = lines[:height]

    n_column = int(re.sub(" +", " ", lines[height].strip()).split(" ")[-1])

    crates = [[] for _ in range(n_column)]
    for line in reversed(crates_info):
        for (i, letter) in enumerate(parse_crate_line(line, n_column)):
            if letter != " ":
                crates[i] += letter
    crates = Crates(crates)

    moves_info = lines[height+2:]
    moves = [None] * len(moves_info)
    for i, line in enumerate(moves_info):
        moves[i] = Move(*map(int, line.split(" ")[1:6:2]))
    return (crates, moves)


def main() -> int:
    (crates1, moves1) = load(EXAMPLE_DATA_PATH)
    (crates2, moves2) = load(TEST_DATA_PATH)

    example_answer1 = "CMZ"
    example_answer2 = "MCD"
    test_answer1 = "SBPQRSCDF"
    test_answer2 = "RGLVRCQSB"

    answer11 = solve_pt1(dc(crates1), dc(moves1))
    print(f"[EXAMPLE] Answer to Part 1: {answer11}")
    assert answer11 == example_answer1
    answer12 = solve_pt1(dc(crates2), dc(moves2))
    print(f"[TEST] Answer to Part 1: {answer12}")
    assert answer12 == test_answer1

    answer21 = solve_pt2(dc(crates1), dc(moves1))
    print(f"[EXAMPLE] Answer to Part 2: {answer21}")
    assert answer21 == example_answer2
    answer22 = solve_pt2(dc(crates2), dc(moves2))
    print(f"[TEST] Answer to Part 2: {answer22}")
    assert answer22 == test_answer2


if __name__ == "__main__":
    main()
