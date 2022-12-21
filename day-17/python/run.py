import numpy as np
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


Rock = np.ndarray


ROCKS: tuple[Rock] = (
    np.array([[1, 1, 1, 1]], dtype=bool),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
    np.array([[1], [1], [1], [1]], dtype=bool),
    np.array([[1, 1], [1, 1]], dtype=bool),
)


class JetPattern:
    def __init__(self, pattern: str) -> None:
        self.jets = [(-1 if (c == "<") else 1) for c in list(pattern)]
        self._i = 0

    @property
    def index(self) -> int:
        return self._i

    def next(self) -> int:
        old_i = self._i
        self._i = (self._i + 1) % len(self.jets)
        return self.jets[old_i]


class Chamber:
    def __init__(self, data: np.ndarray) -> None:
        self.data = data

    def expand_height(self, n_row: int) -> int:
        self.data = np.pad(self.data, pad_width=((0, n_row), (0, 0)))

    def height(self) -> int:
        return self.data.shape[0]

    def width(self) -> int:
        return self.data.shape[1]

    def does_overlap(self, rock: Rock, i_bl: int, j_bl: int) -> bool:
        return np.any(rock & self.data[i_bl:i_bl + rock.shape[0], j_bl:j_bl + rock.shape[1]])

    def set_rock(self, rock: Rock, i: int, j: int) -> None:
        self.data[i:i + rock.shape[0], j:j + rock.shape[1]] |= rock

    def highest_rock(self):
        rocks = np.argwhere(np.logical_or.reduce(self.data, 1) == True)
        if len(rocks) > 0:
            return int(rocks[-1]) + 1
        return 0


def simulate_rock_fall(chamber: Chamber, rock: Rock, jp: JetPattern) -> Chamber:
    # Pad chamber
    (ch, rh, hr) = (chamber.height(), rock.shape[0], chamber.highest_rock())
    if ch < (hr + 3 + rh):
        num_rows_to_add = (hr + 3 + rh) - ch
        chamber.expand_height(num_rows_to_add)

    # Simulate
    hr = chamber.highest_rock()
    (rh, rw) = rock.shape
    (i_rock, j_rock) = (hr + 3, 2)
    able_to_fall = True
    while able_to_fall:
        # Simulate jet
        (i_new, j_new) = (i_rock, j_rock + jp.next())
        if (j_new >= 0) and ((j_new + rw - 1) < chamber.width()):
            if not chamber.does_overlap(rock, i_new, j_new):
                (i_rock, j_rock) = (i_new, j_new)

        # Try to fall
        (i_new, j_new) = (i_rock - 1, j_rock)
        if (i_rock == 0) or chamber.does_overlap(rock, i_new, j_new):
            break
        (i_rock, j_rock) = (i_new, j_new)
    chamber.set_rock(rock, i_rock, j_rock)
    return chamber


def solve_pt1(jp: JetPattern) -> int:
    chamber = Chamber(data=np.ndarray((3, 7), dtype=bool))
    for i in range(2022):
        chamber = simulate_rock_fall(chamber, ROCKS[i % len(ROCKS)], jp)
    hr = chamber.highest_rock()
    return hr


def solve_pt2(jp: JetPattern) -> int:
    chamber = Chamber(data=np.ndarray((3, 7), dtype=bool))
    num_rock = len(ROCKS)
    history = np.array([0])  # rock

    (start, end) = (None, None)
    (uids, uids_as_list) = (set(), [None])
    for i in range(10_000):
        rock_type = i % num_rock
        if i >= 1:
            dh = history[i] - history[i - 1]
            uid = (dh, rock_type, jp.index)
            if uid in uids:
                (start, end) = (uids_as_list.index(uid), i)
                period = end - start
                break
            uids |= {uid}
            uids_as_list += [uid]
        chamber = simulate_rock_fall(chamber, ROCKS[rock_type], jp)
        history = np.append(history, [chamber.highest_rock()])
    else:
        raise ValueError("Unable to find period!")

    moves_start = start
    moves_left = 1_000_000_000_000 - moves_start
    num_period = moves_left // period
    remaining_moves = moves_left % period

    height_at_cycle_start = history[start]
    height_gain_per_cycle = (history[end] - history[start])
    height_gain_over_n_cycles = num_period * height_gain_per_cycle
    remaining_height = (history[start + remaining_moves] - history[start])
    total_height = height_at_cycle_start + height_gain_over_n_cycles + remaining_height
    return total_height


def load(fpath: str) -> JetPattern:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    return JetPattern(text)


def main() -> int:
    example_solution1 = 3068
    example_solution2 = 1514285714288
    test_solution1 = 3166
    test_solution2 = 1577207977186

    example_answer1 = solve_pt1(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(load(TEST_DATA_PATH))
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(load(TEST_DATA_PATH))
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
