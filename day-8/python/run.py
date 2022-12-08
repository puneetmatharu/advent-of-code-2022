import numpy as np
from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def solve_pt1(x: np.ndarray) -> int:
    (m, n) = x.shape
    outer_trees = 2 * (m + n) - 4  # outer edges
    visible_tree_coords = []
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            if x[i, j] > np.max(x[i, :j]):  # trees to the left
                visible_tree_coords.append((i, j))
            if x[i, j] == 9:  # nothing can be taller
                break
        for j in reversed(range(1, n - 1)):
            if x[i, j] > np.max(x[i, j+1:]):  # trees to the right
                visible_tree_coords.append((i, j))
            if x[i, j] == 9:  # nothing can be taller
                break
    for j in range(1, n - 1):
        for i in range(1, m - 1):
            if x[i, j] > np.max(x[:i, j]):  # trees above
                visible_tree_coords.append((i, j))
            if x[i, j] == 9:  # nothing can be taller
                break
    for j in range(1, n - 1):
        for i in reversed(range(1, m - 1)):
            if x[i, j] > np.max(x[i+1:, j]):  # trees below
                visible_tree_coords.append((i, j))
            if x[i, j] == 9:  # nothing can be taller
                break
    unique_visible_tree_coords = list(set(visible_tree_coords))
    return outer_trees + len(unique_visible_tree_coords)


def solve_pt2(x: np.ndarray) -> int:
    (m, n) = x.shape
    scenic_scores = []
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            tree = x[i, j]
            trees_left = 0
            trees_right = 0
            trees_up = 0
            trees_down = 0
            for t in x[:i, j]:
                trees_left += 1
                if t >= tree:
                    break
            for t in x[i+1:, j]:
                trees_right += 1
                if t >= tree:
                    break
            for t in x[i, :j]:
                trees_up += 1
                if t >= tree:
                    break
            for t in x[i, j+1:]:
                trees_down += 1
                if t >= tree:
                    break
            print(f"({i}, {j}, {tree}) = [{trees_left}, {trees_right}, {trees_up}, {trees_down}]")
            scenic_scores += [trees_left * trees_right * trees_up * trees_down]
    return max(scenic_scores)


def load(fpath: str) -> np.ndarray:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    data = np.array([[int(c) for c in line] for line in text])
    return data


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_answer1 = 21
    example_answer2 = 8

    answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {answer1}")
    assert answer1 == example_answer1
    print(f"[TEST] Answer to Part 1: {solve_pt1(data2)}")

    answer2 = solve_pt2(data1)
    print(f"[EXAMPLE] Answer to Part 2: {answer2}")
    assert answer2 == example_answer2
    # print(f"[TEST] Answer to Part 2: {solve_pt2(data2)}")


if __name__ == "__main__":
    main()
