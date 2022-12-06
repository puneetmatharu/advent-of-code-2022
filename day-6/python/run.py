from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def find_unique_substring_marker(s: str, size: int) -> int:
    return size + [i for i in range(len(s) - size + 1) if len(set(s[i:i + size])) == size][0]


def solve_pt1(line: str) -> int:
    return find_unique_substring_marker(line, size=4)


def solve_pt2(line: str) -> int:
    return find_unique_substring_marker(line, size=14)


def load(fpath: str) -> str:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    return text


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_answer1 = [7, 5, 6, 10, 11]
    example_answer2 = [19, 23, 23, 29, 26]

    answer1 = [solve_pt1(line) for line in data1.split("\n")]
    print(f"[EXAMPLE] Answer to Part 1: {answer1}")
    assert answer1 == example_answer1
    print(f"[TEST] Answer to Part 1: {solve_pt1(data2)}")

    answer2 = [solve_pt2(line) for line in data1.split("\n")]
    print(f"[EXAMPLE] Answer to Part 2: {answer2}")
    assert answer2 == example_answer2
    print(f"[TEST] Answer to Part 2: {solve_pt2(data2)}")


if __name__ == "__main__":
    main()
