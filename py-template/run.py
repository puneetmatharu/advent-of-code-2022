from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd() / "example.dat"
TEST_DATA_PATH = Path.cwd() / "test.dat"


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
    enable_example_part2 = True
    enable_test_part1 = True
    enable_test_part2 = True
        
    data1 = load(EXAMPLE_DATA_PATH)
    if enable_test_part1 or enable_test_part2:
        data2 = load(TEST_DATA_PATH)
    
    example_answer1 = None
    example_answer2 = None
    
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
