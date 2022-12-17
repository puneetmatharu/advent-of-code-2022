from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def solve_pt1(text: str) -> int:
    return None


def solve_pt2(text: str) -> int:
    return None


def load(fpath: str) -> str:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    return text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 0
    # example_solution2 = 0
    # test_solution1 = 0
    # test_solution2 = 0

    example_answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    # test_answer1 = solve_pt1(data2)
    # print(f"[TEST] Answer to Part 1: {test_answer1}")
    # assert test_answer1 == test_solution1

    # example_answer2 = solve_pt2(data1)
    # print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    # assert example_answer2 == example_solution2
    # test_answer2 = solve_pt2(data2)
    # print(f"[TEST] Answer to Part 2: {test_answer2}")
    # assert test_answer2 == test_solution2

if __name__ == "__main__":
    main()
