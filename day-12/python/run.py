from __future__ import annotations

import numpy as np
from collections import deque
from dataclasses import dataclass
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


@dataclass
class Node:
    coords: tuple[int, int]
    parent: Node = None

    def __eq__(self, other: Node):
        return self.coords == other.coords

    def path_to_root(self):
        if self.parent is None:
            return []
        return self.parent.path_to_root() + [self]


def path_length(hmap: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    (m, n) = hmap.shape
    src = Node(start)
    q = deque()
    q.append(src)
    visited = {src.coords}
    while q:
        current_node = q.popleft()
        (i, j) = current_node.coords
        if (i, j) == end:
            return len(current_node.path_to_root())
        for (i_off, j_off) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            (i_next, j_next) = (i + i_off, j + j_off)
            if (0 <= i_next < m) and (0 <= j_next < n) and (hmap[i_next, j_next] <= hmap[i, j] + 1):
                if (i_next, j_next) not in visited:
                    next_node = Node((i_next, j_next), parent=current_node)
                    q.append(next_node)
                    visited |= {(i_next, j_next)}
    return 99999


def solve_pt1(hmap: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    return path_length(hmap, start, end)


def solve_pt2(hmap: np.ndarray, end: tuple[int, int]) -> int:
    shortest_path = 99999
    for start in [tuple(p) for p in np.argwhere(hmap == 0)]:
        shortest_path = min(shortest_path, path_length(hmap, start, end))
    return shortest_path


def load(fpath: str) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    start = next(((i, j) for (i, line) in enumerate(text) for (j, c) in enumerate(line) if c == "S"))
    end = next(((i, j) for (i, line) in enumerate(text) for (j, c) in enumerate(line) if c == "E"))
    data = np.array([[ord(c.lower()) - 97 for c in line] for line in text])
    data[start] = 0
    data[end] = 25
    return (data, start, end)


def main() -> int:
    (data1, start1, end1) = load(EXAMPLE_DATA_PATH)
    (data2, start2, end2) = load(TEST_DATA_PATH)

    example_solution1 = 31
    example_solution2 = 29
    test_solution1 = 456
    test_solution2 = 454

    example_answer1 = solve_pt1(data1, start1, end1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2, start2, end2)
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(data1, end1)
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(data2, end2)
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
