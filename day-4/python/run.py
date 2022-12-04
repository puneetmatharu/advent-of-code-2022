from pathlib import Path
from typing import List, Tuple


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def solve_pt1(data: List[str]) -> int:
    n_fully_contained = 0
    for line in data:
        (elf1, elf2) = [list(map(int, rng.split("-"))) for rng in line.split(",")]
        (elf1, elf2) = (set(range(elf1[0], elf1[1] + 1)), set(range(elf2[0], elf2[1] + 1)))
        if len(elf1 | elf2) == max(len(elf1), len(elf2)):
            n_fully_contained += 1
    return n_fully_contained


def solve_pt2(data: List[str]) -> int:
    n_overlap = 0
    for line in data:
        (elf1, elf2) = [list(map(int, rng.split("-"))) for rng in line.split(",")]
        overlap = set(range(elf1[0], elf1[1] + 1)) & set(range(elf2[0], elf2[1] + 1))
        if len(overlap) > 0:
            n_overlap += 1
    return n_overlap


def load(fpath: str) -> List[str]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    return text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_answer1 = 2
    example_answer2 = 4

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
