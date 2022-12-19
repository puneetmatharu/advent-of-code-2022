from __future__ import annotations

import numpy as np
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


Point = list[int, int, int]


class Cube:
    def __init__(self, cube_id: int, x: Point):
        self.cube_id = cube_id
        self.x = np.array(x)
        self.neighbours = []

    def is_neighbour(self, other: Cube) -> bool:
        if np.sum(np.abs(self.x - other.x)) == 1:
            return True
        return False

    def surface_area(self) -> int:
        assert len(self.neighbours) <= 6
        return 6 - len(self.neighbours)


def solve_pt1(cubes: list[Cube]) -> int:
    return sum([c.surface_area() for c in cubes])


def solve_pt2(cubes: list[Cube]) -> int:
    # Create bounding box of water
    all_ijk = np.array([c.x for c in cubes])
    all_ijk -= np.min(all_ijk, axis=0)  # shift to zero in each direction
    all_ijk += 1  # add an offset for indexing
    water_box = np.ones((np.max(all_ijk, axis=0) + 2), dtype=bool)

    # Remove lava cubes
    for (i, j, k) in all_ijk:
        water_box[i, j, k] = False

    # Construct grid of connected cubes from water cube locations
    water_cubes = points_to_connected_cubes(np.argwhere(water_box == True))

    # Find all connected outer water cubes
    outer_water_cubes_ids = [next(c.cube_id for c in water_cubes if np.all(c.x == [0, 0, 0]))]
    searching = True
    while searching:
        found_new_neighbour = False
        for i in range(len(outer_water_cubes_ids)):  # cube
            cube_id = outer_water_cubes_ids[i]
            for n in water_cubes[cube_id].neighbours:
                if n.cube_id not in outer_water_cubes_ids:
                    outer_water_cubes_ids += [n.cube_id]
                    found_new_neighbour = True
        if not found_new_neighbour:
            break

    # Get surface area of enclosing water region
    water_surface_area = sum([water_cubes[c_id].surface_area() for c_id in outer_water_cubes_ids])

    # Remove surface area of outside bounding box (only want the inner surface)
    (h, w, d) = water_box.shape
    bbox_outer_surface_area = 2 * (h * w + w * d + h * d)
    water_surface_area -= bbox_outer_surface_area
    return water_surface_area


def points_to_connected_cubes(points: list[Point]) -> list[Cube]:
    cubes = [Cube(i, point) for (i, point) in enumerate(points)]
    for i in range(len(cubes)):
        for j in range(i + 1, len(cubes)):
            if cubes[i].is_neighbour(cubes[j]):
                cubes[i].neighbours += [cubes[j]]
                cubes[j].neighbours += [cubes[i]]
    return cubes


def load(fpath: str) -> list[Cube]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    points = [list(map(int, line.split(","))) for line in text]
    return points_to_connected_cubes(points)


def main() -> int:
    example_solution1 = 64
    example_solution2 = 58
    test_solution1 = 4512
    test_solution2 = 2554

    example_answer1 = solve_pt1(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(load(TEST_DATA_PATH))
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(load(TEST_DATA_PATH))  # Takes ~2m 40s
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
