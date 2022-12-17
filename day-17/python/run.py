from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


Chamber = np.ndarray
Rock = np.ndarray


ROCKS = (
    np.array([[1, 1, 1, 1]], dtype=bool),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
    np.array([[1], [1], [1], [1]], dtype=bool),
    np.array([[1, 1], [1, 1]], dtype=bool),
)


class Jet:
    LEFT = -1
    RIGHT = 1


@dataclass
class JetPattern:
    jets: list[Jet]
    _i: int = 0

    def next(self) -> Jet:
        old_i = self._i
        self._i = (self._i + 1) % len(self.jets)
        return self.jets[old_i]


def print_chamber(c: Chamber) -> None:
    # return
    def to_str(x): return "#" if x else "."
    s = "\n".join(["".join(list(map(to_str, row))) for row in c[::-1]])
    print(s, "\n")


def highest_rock(chamber: Chamber):
    rocks = np.argwhere(np.logical_or.reduce(chamber, 1) == True)
    if len(rocks) > 0:
        return int(rocks[-1]) + 1
    return 0


def simulate_rock(chamber: Chamber, rock: Rock, jp: JetPattern) -> Chamber:
    def does_overlap(chamber, rock, i_bl, j_bl) -> bool:
        return np.any(rock & chamber[i_bl:i_bl + rock.shape[0], j_bl:j_bl + rock.shape[1]])

    # Pad chamber
    (ch, rh, hr) = (chamber.shape[0], rock.shape[0], highest_rock(chamber))
    if ch < (hr + 3 + rh):
        num_rows_to_add = (hr + 3 + rh) - ch
        chamber = np.pad(chamber, pad_width=((0, num_rows_to_add), (0, 0)))

    # Simulate
    hr = highest_rock(chamber)
    (rh, rw) = rock.shape
    (i_rock, j_rock) = (hr + 3, 2)
    able_to_fall = True
    while able_to_fall:
        # Simulate jet
        (i_new, j_new) = (i_rock, j_rock + jp.next())
        if (j_new >= 0) and ((j_new + rw - 1) < chamber.shape[1]):
            if not does_overlap(chamber, rock, i_new, j_new):
                (i_rock, j_rock) = (i_new, j_new)

        # Try to fall
        (i_new, j_new) = (i_rock - 1, j_rock)
        if (i_rock == 0) or does_overlap(chamber, rock, i_new, j_new):
            break
        (i_rock, j_rock) = (i_new, j_new)
    chamber[i_rock:i_rock + rh, j_rock:j_rock + rw] |= rock
    return chamber


def solve_pt1(jp: JetPattern) -> int:
    chamber = np.ndarray((3, 7), dtype=bool)
    for i in range(2022):
        chamber = simulate_rock(chamber, ROCKS[i % len(ROCKS)], jp)
    hr = highest_rock(chamber)
    return hr


def solve_pt2(jp: JetPattern) -> int:
    chamber = np.ndarray((3, 7), dtype=bool)
    for i in range(1_000_000):
        chamber = simulate_rock(chamber, ROCKS[i % len(ROCKS)], jp)
    hr = highest_rock(chamber)
    return None


def load(fpath: str) -> JetPattern:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    jets = [(Jet.LEFT if (c == "<") else Jet.RIGHT) for c in list(text)]
    return JetPattern(jets)


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 3068
    # example_solution2 = 0
    test_solution1 = 3166
    # test_solution2 = 0

    example_answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2)
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    # example_answer2 = solve_pt2(data1)
    # print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    # assert example_answer2 == example_solution2
    # test_answer2 = solve_pt2(data2)
    # print(f"[TEST] Answer to Part 2: {test_answer2}")
    # assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
