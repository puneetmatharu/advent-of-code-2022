from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def get_message(crates: list[list[str]]) -> None:
    return "".join([stack[-1] for stack in crates if len(stack) > 0])


def solve_pt1(crates: list[list[str]], moves: list[tuple[int, int, int]]) -> int:
    for (n, start, end) in moves:
        crates[end] = crates[end] + crates[start][-n:][::-1]
        crates[start] = crates[start][:-n]
    return get_message(crates)


def solve_pt2(crates: list[list[str]], moves: list[tuple[int, int, int]]) -> int:
    for (n, start, end) in moves:
        crates[end] = crates[end] + crates[start][-n:]
        crates[start] = crates[start][:-n]
    return get_message(crates)


def load(fpath: str) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    lines = None
    with open(fpath, "r") as f:
        lines = f.read().split("\n")

    stack_height = next(i for (i, l) in enumerate(lines) if l.startswith(" 1"))
    crates_info = lines[:stack_height]

    n_column = int(lines[stack_height].strip().split(" ")[-1])
    crates = [[] for _ in range(n_column)]
    for line in crates_info[::-1]:
        crate_labels = [line[4 * i + 1] for i in range(n_column)]
        for (i, letter) in enumerate(crate_labels):
            if letter != " ":
                crates[i] += letter

    moves_info = lines[stack_height + 2:]
    moves = [None] * len(moves_info)
    for (i, line) in enumerate(moves_info):
        (num_crate, start, end) = list(map(int, line.split(" ")[1::2]))
        moves[i] = (num_crate, start - 1, end - 1)
    return (crates, moves)


def main() -> int:
    (crates_example, moves_example) = load(EXAMPLE_DATA_PATH)
    (crates_test, moves_test) = load(TEST_DATA_PATH)

    example_answer1 = "CMZ"
    example_answer2 = "MCD"
    test_answer1 = "SBPQRSCDF"
    test_answer2 = "RGLVRCQSB"

    answer11 = solve_pt1(deepcopy(crates_example), deepcopy(moves_example))
    answer12 = solve_pt1(deepcopy(crates_test), deepcopy(moves_test))
    print(f"[EXAMPLE] Answer to Part 1: {answer11}")
    print(f"[TEST] Answer to Part 1: {answer12}")
    assert answer11 == example_answer1
    assert answer12 == test_answer1

    answer21 = solve_pt2(deepcopy(crates_example), deepcopy(moves_example))
    answer22 = solve_pt2(deepcopy(crates_test), deepcopy(moves_test))
    print(f"[EXAMPLE] Answer to Part 2: {answer21}")
    print(f"[TEST] Answer to Part 2: {answer22}")
    assert answer21 == example_answer2
    assert answer22 == test_answer2


if __name__ == "__main__":
    main()
