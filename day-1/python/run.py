from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def solve_pt1(text: str) -> int:
    groups = text.split("\n\n")
    cals_per_elf = [sum(map(int, x.split("\n"))) for x in groups]
    max_cals = max(cals_per_elf)
    return max_cals


def solve_pt2(text: str) -> int:
    groups = text.split("\n\n")
    cals_per_elf = [sum(map(int, x.split("\n"))) for x in groups]
    cals_per_elf = sorted(cals_per_elf)
    assert len(cals_per_elf) > 3
    return sum(cals_per_elf[-3:])


def load(fpath: str) -> List[str]:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    return text


def main() -> int:
    enable_example_part2 = True
    enable_test_part1 = True
    enable_test_part2 = True
        
    data1 = load(EXAMPLE_DATA_PATH)
    if enable_test_part1 or enable_test_part2:
        data2 = load(TEST_DATA_PATH)
    
    example_answer1 = 24000
    example_answer2 = 45000
    
    answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {answer1}")
    assert answer1 == example_answer1
    
    if enable_example_part2:
        answer2 = solve_pt2(data1)
        print(f"[EXAMPLE] Answer to Part 2: {answer2}")
        assert answer2 == example_answer2

    if enable_test_part1:
        answer1 = solve_pt1(data2)
        print(f"[TEST] Answer to Part 1: {answer1}")
        
    if enable_test_part2:
        answer2 = solve_pt2(data2)
        print(f"[TEST] Answer to Part 2: {answer2}")


if __name__ == "__main__":
    main()
