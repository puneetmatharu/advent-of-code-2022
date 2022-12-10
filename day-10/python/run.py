import numpy as np
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"
EXAMPLE_SOLUTION_PT2_DATA_PATH = Path.cwd().parent / "data" / "example_solution_pt2.dat"
TEST_SOLUTION_PT2_DATA_PATH = Path.cwd().parent / "data" / "test_solution_pt2.dat"


def parse(instructions: list[str]) -> list[int]:
    history = [1]
    for instr in instructions:
        history += [history[-1]]
        if instr != "noop":
            history += [history[-1] + int(instr.split(" ")[-1])]
    return history


def solve_pt1(instructions: list[str]) -> int:
    history = parse(instructions)
    return sum([i * history[i - 1] for i in range(20, 221, 40)])


def solve_pt2(instructions: list[str]) -> int:
    history = parse(instructions)
    screen = [["." for _ in range(40)] for _ in range(6)]
    for row in range(6):
        for col in range(40):
            spos = history[(40 * row) + col]
            if col in np.clip([spos - 1, spos, spos + 1], 0, 39):
                screen[row][col] = "#"
    screen = "\n".join(["".join(line) for line in screen])
    return screen


def load(fpath: str) -> list[str]:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    return text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH).split("\n")
    data2 = load(TEST_DATA_PATH).split("\n")

    example_solution1 = 13140
    example_solution2 = load(EXAMPLE_SOLUTION_PT2_DATA_PATH)
    test_solution1 = 12460
    test_solution2 = load(TEST_SOLUTION_PT2_DATA_PATH)

    example_answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2)
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(data1)
    print(f"[EXAMPLE] Answer to Part 2:\n{example_answer2}")
    if example_answer2 != example_solution2:
        print(f"Expected:\n{example_solution2}")
    test_answer2 = solve_pt2(data2)
    print(f"[TEST] Answer to Part 2:\n{test_answer2}")
    if test_answer2 != test_solution2:
        print(f"Expected:\n{test_solution2}")


if __name__ == "__main__":
    main()
