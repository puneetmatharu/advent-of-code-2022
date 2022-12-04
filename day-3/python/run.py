from pathlib import Path
from typing import List, Tuple


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def char_to_ind(c: str) -> int:
    return ord(c) - (38 if c.isupper() else 96)


def solve_pt1(data: List[Tuple[str]]) -> int:
    data = [(s[:len(s)//2], s[len(s)//2:]) for s in data]
    wrongly_packed = [set(comp1) & set(comp2) for (comp1, comp2) in data]
    priority_sum = sum([char_to_ind(next(iter(c))) for c in wrongly_packed])
    return priority_sum


def solve_pt2(data: List[Tuple[str]]) -> int:
    assert len(data) % 3 == 0
    groups = [data[3*i:3*i+3] for i in range(len(data) // 3)]
    badges = [set(a) & set(b) & set(c) for (a, b, c) in groups]
    priority_sum = sum([char_to_ind(next(iter(badge))) for badge in badges])
    return priority_sum


def load(fpath: str) -> List[Tuple[str]]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    return text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_answer1 = 157
    example_answer2 = 70

    answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {answer1}")
    assert answer1 == example_answer1
    print(f"[TEST] Answer to Part 1: {solve_pt1(data2)}")

    answer2 = solve_pt2(data1)
    print(f"[EXAMPLE] Answer to Part 2: {answer2}")
    assert answer2 == example_answer2
    print(f"[TEST] Answer to Part 2: {solve_pt2(data2)}")


if __name__ == "__main__":
    main()
