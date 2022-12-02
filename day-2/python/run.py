from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
from enum import IntEnum


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


class Outcome(IntEnum):
    Lose = 0
    Draw = 3
    Win = 6


class Move(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


def to_beat(move: Move) -> Move:
    return CYCLE[(CYCLE.index(move) - 1) % 3]


def to_lose(move: Move) -> Move:
    return CYCLE[(CYCLE.index(move) + 1) % 3]


# Cyclic array; A beats B, B beats C, C beats A
CYCLE = [Move.Rock, Move.Scissors, Move.Paper]


# Cyclic array; A beats B, B beats C, C beats A
WIN_CYCLE = [Move.Rock, Move.Scissors, Move.Paper]


def does_beat(your_move: Move, their_move: Move) -> bool:
    return True if their_move == to_lose(your_move) else False


def get_outcome(their_move: Move, your_move: Move) -> int:
    if your_move == their_move:
        return Outcome.Draw
    elif does_beat(your_move, their_move):
        return Outcome.Win
    return Outcome.Lose


def get_desired_move(their_move: Move, your_outcome: Outcome) -> Move:
    if your_outcome == Outcome.Draw:
        return their_move
    if your_outcome == Outcome.Lose:
        return to_lose(their_move)
    return to_beat(their_move)


def solve_pt1(move_pairs: List[Tuple[str, str]]) -> int:
    letter_to_their_move = dict(A=Move.Rock, B=Move.Paper, C=Move.Scissors)
    letter_to_your_move = dict(X=Move.Rock, Y=Move.Paper, Z=Move.Scissors)
    total_score = 0
    for (them, you) in move_pairs:
        their_move = letter_to_their_move[them]
        your_move = letter_to_your_move[you]
        your_outcome = get_outcome(their_move, your_move)
        total_score += (your_outcome + your_move)
    return total_score


def solve_pt2(move_pairs: List[Tuple[str, str]]) -> int:
    letter_to_their_move = dict(A=Move.Rock, B=Move.Paper, C=Move.Scissors)
    letter_to_your_outcome = dict(X=Outcome.Lose, Y=Outcome.Draw, Z=Outcome.Win)
    total_score = 0
    for (them, you) in move_pairs:
        their_move = letter_to_their_move[them]
        your_outcome = letter_to_your_outcome[you]
        your_move = get_desired_move(their_move, your_outcome)
        total_score += (your_outcome + your_move)
    return total_score


def load(fpath: str) -> List[Tuple[str, str]]:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    parsed_text = [x.split(" ") for x in text.split("\n")]
    return parsed_text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_answer1 = 15
    example_answer2 = 12

    answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {answer1}")
    assert answer1 == example_answer1
    print(f"[TEST] Answer to Part 1: {solve_pt1(data2)}")

    answer2 = solve_pt2(data1)
    print(f"[EXAMPLE] Answer to Part 2: {answer2}")
    assert answer2 == example_answer2
    print(f"[TEST] Answer to Part 2: {solve_pt2(data2)}")


if __name__ == "__main__":
    main()
