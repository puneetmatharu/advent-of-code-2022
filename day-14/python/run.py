import numpy as np
from dataclasses import dataclass
from pathlib import Path
from enum import IntEnum


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


@dataclass
class Map:
    data: np.ndarray
    source: tuple[int, int]


class Feature(IntEnum):
    Air = 0
    Source = 1
    Rock = 2
    Sand = 3


def draw(feature_map: np.ndarray):
    def to_str(x: Feature):
        return {
            Feature.Air: ".",
            Feature.Source: "+",
            Feature.Rock: "#",
            Feature.Sand: "o",
        }[x]
    return "\n".join(["".join(list(map(to_str, row))) for row in feature_map])


def solve_pt1(map_data: Map) -> int:
    (m, source) = (np.copy(map_data.data), map_data.source)
    (num_row, num_col) = m.shape
    num_stationary_sand_particles = 0
    able_to_drop_sand = True
    while able_to_drop_sand:
        (i, j) = source
        falling = True
        while falling:
            if i + 1 >= num_row:
                return num_stationary_sand_particles
            elif m[i + 1, j] == Feature.Air:
                (i, j) = (i + 1, j)
            elif j - 1 < 0:
                return num_stationary_sand_particles
            elif m[i + 1, j - 1] == Feature.Air:
                (i, j) = (i + 1, j - 1)
            elif j + 1 >= num_col:
                return num_stationary_sand_particles
            elif m[i + 1, j + 1] == Feature.Air:
                (i, j) = (i + 1, j + 1)
            elif j == 0:
                return num_stationary_sand_particles
            else:
                m[i, j] = Feature.Sand
                num_stationary_sand_particles += 1
                break


def solve_pt2(map_data: Map) -> int:
    (m, source) = (np.copy(map_data.data), list(map_data.source))
    m = np.pad(m, ((0, 2), (0, 0)))
    m[-1, :] = Feature.Rock
    num_col = m.shape[1]
    num_stationary_sand_particles = 0
    able_to_drop_sand = True
    while able_to_drop_sand:
        (i, j) = source
        falling = True
        while falling:
            if m[i + 1, j] == Feature.Air:
                (i, j) = (i + 1, j)
            elif j - 1 < 0:
                m = np.pad(m, ((0, 0), (1, 0)))
                m[-1, 0] = Feature.Rock
                (j, source[1], num_col) = (j + 1, source[1] + 1, num_col + 1)
            elif m[i + 1, j - 1] == Feature.Air:
                (i, j) = (i + 1, j - 1)
            elif j + 1 >= num_col:
                m = np.pad(m, ((0, 0), (0, 1)))
                m[-1, -1] = Feature.Rock
                num_col += 1
            elif m[i + 1, j + 1] == Feature.Air:
                (i, j) = (i + 1, j + 1)
            elif [i, j] == source:
                num_stationary_sand_particles += 1
                return num_stationary_sand_particles
            else:
                m[i, j] = Feature.Sand
                num_stationary_sand_particles += 1
                break


def load(fpath: str) -> Map:
    with open(fpath, "r") as f:
        data = f.read().split("\n")
    data = [[list(map(int, coords.split(",")[::-1])) for coords in line.split(" -> ")] for line in data]
    (i_max, j_min, j_max) = (0, np.Inf, 0)
    for rock_path in data:
        for (i, j) in rock_path:
            (i_max, j_min, j_max) = (max(i, i_max), min(j, j_min), max(j, j_max))
    data = [[(i, j - j_min) for (i, j) in rock_path] for rock_path in data]
    feature_map = np.zeros(shape=(i_max + 1, j_max - j_min + 1), dtype=int)
    for path in data:
        for ((i1, j1), (i2, j2)) in zip(path[:-1], path[1:]):
            ((i_s, i_e), (j_s, j_e)) = (sorted([i1, i2]), sorted([j1, j2]))
            feature_map[i_s:i_e + 1, j_s:j_e + 1] = Feature.Rock
    source = (0, 500 - j_min)
    feature_map[source] = Feature.Source
    return Map(feature_map, source)


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 24
    example_solution2 = 93
    test_solution1 = 838
    test_solution2 = 27539

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
