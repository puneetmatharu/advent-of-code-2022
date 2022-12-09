import numpy as np
from pathlib import Path


EXAMPLE_DATA_PT1_PATH = Path.cwd().parent / "data" / "example_pt1.dat"
EXAMPLE_DATA_PT2_PATH = Path.cwd().parent / "data" / "example_pt2.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def simulate(n_knot: int, moves: list[tuple[str, int]]) -> int:
    direction_vector_map = {"L": [-1, 0], "R": [1, 0], "U": [0, 1], "D": [0, -1]}
    tail_history = {(0, 0)}
    n_knot = n_knot
    knots = [np.array([0, 0], dtype=int) for _ in range(n_knot)]
    for (direction, amount) in moves:
        for _ in range(amount):
            knots[0] += direction_vector_map[direction]
            for i in range(1, n_knot):
                disp = knots[i - 1] - knots[i]
                if np.max(np.abs(knots[i - 1] - knots[i])) > 1:
                    knots[i] += np.sign(disp) * np.ceil(np.abs(disp) / 2).astype(int)
            tail_history |= {tuple(knots[-1].tolist())}
    return len(tail_history)


def solve_pt1(moves: list[tuple[str, int]]) -> int:
    return simulate(n_knot=2, moves=moves)


def solve_pt2(moves: list[tuple[str, int]]) -> int:
    return simulate(n_knot=10, moves=moves)


def load(fpath: str) -> str:
    with open(fpath, "r") as f:
        moves = [line.split(" ") for line in f.read().split("\n")]
    moves = [(direction, int(amount)) for (direction, amount) in moves]
    return moves


def main() -> int:
    example_data1 = load(EXAMPLE_DATA_PT1_PATH)
    example_data2 = load(EXAMPLE_DATA_PT2_PATH)
    test_data = load(TEST_DATA_PATH)

    example_solution1 = 13
    example_solution2 = 36
    test_solution1 = 6175
    test_solution2 = 2578

    example_answer1 = solve_pt1(example_data1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(test_data)
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(example_data2)
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(test_data)
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
