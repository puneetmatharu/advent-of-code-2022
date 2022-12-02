from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def solve_pt1(text: str) -> int:
    return None


def solve_pt2(text: str) -> int:
    return None


def load(fpath: str) -> List[str]:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    return text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_answer1 = 24000
    example_answer2 = 45000

    answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {answer1}")
    assert answer1 == example_answer1

    answer2 = solve_pt2(data1)
    print(f"[EXAMPLE] Answer to Part 2: {answer2}")
    assert answer2 == example_answer2

    print(f"[TEST] Answer to Part 1: {solve_pt1(data2)}")
    print(f"[TEST] Answer to Part 2: {solve_pt2(data2)}")


if __name__ == "__main__":
    main()
