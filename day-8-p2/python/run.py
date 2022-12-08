import numpy as np
from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def solve_pt2(x: np.ndarray) -> int:
    view_dist = lambda tree, others : next((i + 1 for (i, t) in enumerate(others) if t >= tree), len(others))
    (m, n) = x.shape
    max_scenic_score = 0
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            tree = x[i, j]
            (left, right, up, down) = (x[i, :j], x[i, j + 1:], x[:i, j], x[i + 1:, j])
            n_left = view_dist(tree, left[::-1])
            n_right = view_dist(tree, right)
            n_up = view_dist(tree, up[::-1])
            n_down = view_dist(tree, down)
            scenic_score = n_left * n_right * n_up * n_down
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
    return max_scenic_score


def load(fpath: str) -> np.ndarray:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    return np.array([[int(c) for c in line] for line in text])


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution2 = 8
    test_solution2 = 211680

    example_answer2 = solve_pt2(data1)
    test_answer2 = solve_pt2(data2)
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert example_answer2 == example_solution2
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
