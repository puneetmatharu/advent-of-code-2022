import functools
from pathlib import Path
from typing import Union


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def is_valid_packet(x: Union[int, list], y: Union[int, list]) -> bool:
    def is_int(x) -> bool: return isinstance(x, int)
    def is_list(x) -> bool: return isinstance(x, list)

    if is_int(x) and is_int(y):
        if x < y:
            return True
        elif x > y:
            return False
    elif is_list(x) and is_list(y):
        for (a, b) in zip(x, y):
            check = is_valid_packet(a, b)
            if check is not None:
                return check
        else:
            if len(x) < len(y):
                return True
            elif len(x) > len(y):
                return False
    elif is_list(x) and is_int(y):
        check = is_valid_packet(x, [y])
        if check is not None:
            return check
    elif is_int(x) and is_list(y):
        check = is_valid_packet([x], y)
        if check is not None:
            return check
    return None


def compare(x: Union[int, list], y: Union[int, list]):
    in_correct_order = is_valid_packet(x, y)
    if in_correct_order == True:
        return -1
    elif in_correct_order == False:
        return 1
    return 0


def solve_pt1(data: list[tuple]) -> int:
    results = [i + 1 for (i, (a, b)) in enumerate(data) if is_valid_packet(a, b)]
    return sum(results)


def solve_pt2(data: list[tuple]) -> int:
    packets = [x for pair in data for x in pair]
    packets += [[[2]], [[6]]]
    packets = sorted(packets, key=functools.cmp_to_key(compare))
    i_divider_packet1 = packets.index([[2]]) + 1
    i_divider_packet2 = packets.index([[6]]) + 1
    return i_divider_packet1 * i_divider_packet2


def load(fpath: str) -> str:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    pairs = [(eval(text[3*i]), eval(text[3*i+1])) for i in range((len(text) + 1)//3)]
    return pairs


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 13
    example_solution2 = 140
    test_solution1 = 5_013
    test_solution2 = 25_038

    example_answer1 = solve_pt1(data1)
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2)
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
