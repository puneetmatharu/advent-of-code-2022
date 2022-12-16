import re
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


Point = tuple[int, int]


class BoundingBox:
    def __init__(self, x_bl: Point, x_tr: Point):
        self.x_bl = x_bl
        self.x_tr = x_tr

    def contains(self, x: Point) -> bool:
        return (self.x_bl[0] <= x[0] <= self.x_tr[0]) and (self.x_bl[1] <= x[1] <= self.x_tr[1])


class SensorBeaconPair:
    def __init__(self, sensor: Point, beacon: Point):
        self.sensor = sensor
        self.beacon = beacon
        self.beacon_dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

    def __iter__(self) -> tuple[Point, Point]:
        return iter((self.sensor, self.beacon))

    @staticmethod
    def l1_dist(x1: Point, x2: Point) -> int:
        return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])

    def covered(self, y: int) -> set[Point]:
        if abs(y - self.sensor[1]) > self.beacon_dist:
            return set()
        d = self.beacon_dist - self.l1_dist(self.sensor, (self.sensor[0], y))
        return set(range(self.sensor[0] - d, self.sensor[0] + d + 1))

    def covers(self, x: Point) -> bool:
        return self.l1_dist(self.sensor, x) <= self.beacon_dist

    def gen_boundary(self) -> list[Point]:
        d = self.beacon_dist + 1
        pts = [
            (self.sensor[0] - d, self.sensor[1]),
            (self.sensor[0] + d, self.sensor[1]),
            (self.sensor[0], self.sensor[1] - d),
            (self.sensor[0], self.sensor[1] + d),
        ]
        for x in range(1, d):
            y = d - x
            pts += [
                (self.sensor[0] - x, self.sensor[1] - y),
                (self.sensor[0] + x, self.sensor[1] - y),
                (self.sensor[0] - x, self.sensor[1] + y),
                (self.sensor[0] + x, self.sensor[1] + y),
            ]
        return pts


def solve_pt1(pairs: list[SensorBeaconPair], y: int) -> int:
    covered = set.union(*[p.covered(y=y) for p in pairs])
    covered -= set([x_pt for pair in pairs for (x_pt, y_pt) in pair if y_pt == y])
    return len(covered)


def solve_pt2(pairs: list[SensorBeaconPair]) -> int:
    def calculate_tuning_signal(x: Point):
        return (4_000_000 * x[0]) + x[1]

    (x_p, y_p) = ([p.sensor[0] for p in pairs], [p.sensor[1] for p in pairs])
    (x_bl, x_tr) = (min(x_p), min(y_p)), (max(x_p), max(y_p))
    bbox = BoundingBox(x_bl, x_tr)
    for (i, p) in enumerate(pairs):
        for pt in p.gen_boundary():
            if not bbox.contains(pt):
                continue
            for (j, p_other) in enumerate(pairs):
                if i == j:
                    continue
                if p_other.covers(pt):
                    break
            else:
                return calculate_tuning_signal(pt)


def load(fpath: str) -> list[SensorBeaconPair]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    data = [[list(map(int, p)) for p in re.findall(r"x=(-?\d+), y=(-?\d+)", line)] for line in text]
    data = [SensorBeaconPair(tuple(s), tuple(b)) for (s, b) in data]
    return data


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 26
    example_solution2 = 56_000_011
    test_solution1 = 4_883_971
    test_solution2 = 12_691_026_767_556  # (x, y) = (3172756, 2767556)

    example_answer1 = solve_pt1(data1, y=10)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2, y=2_000_000)
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
