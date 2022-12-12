from __future__ import annotations

from collections import deque
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


@dataclass
class Node:
    coords: tuple[int, int]
    parent: Node = None

    def __repr__(self):
        return str(self.coords)

    def __eq__(self, other):
        return self.coords == other.coords

    def path_to_root(self):
        if self.parent is None:
            return []
        return self.parent.path_to_root() + [self]


def shortest_path_length(hmap: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    (m, n) = hmap.shape
    q = deque()
    src = Node(start)
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
                next_node = Node((i_next, j_next), parent=current_node)
                if next_node.coords not in visited:
                    q.append(next_node)
                    visited.add(next_node.coords)
    return 99999


@dataclass
class MapData:
    hmap: np.ndarray
    start: tuple[int, int]
    end: tuple[int, int]


def solve_pt1(data: MapData) -> int:
    return shortest_path_length(data.hmap, data.start, data.end)


def solve_pt2(data: MapData) -> int:
    shortest_path = 99999
    for start in [tuple(p) for p in np.argwhere(data.hmap == 0)]:
        shortest_path = min(shortest_path, shortest_path_length(data.hmap, start, data.end))
    return shortest_path


def load(fpath: str) -> MapData:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    start = next(((i, j) for (i, line) in enumerate(text)
                 for (j, c) in enumerate(line) if c == "S"))
    end = next(((i, j) for (i, line) in enumerate(text) for (j, c) in enumerate(line) if c == "E"))
    data = np.array([[ord(c.lower()) - 97 for c in line] for line in text])
    data[start] = 0
    data[end] = 25
    return MapData(data, start, end)


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 31
    example_solution2 = 29
    test_solution1 = 456
    test_solution2 = 454

    example_answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2)
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(data1)
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(data2)
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
