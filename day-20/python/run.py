import numpy as np
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def mix(lst: list[int], num_times: int = 1) -> None:
    def calculate_new_index(x: int, old_pos: int, num_entry: int) -> int:
        new_pos = old_pos + x
        if x > 0:
            return new_pos % (num_entry - 1)
        new_pos = new_pos % (num_entry - 1)
        if new_pos == 0:
            new_pos += (num_entry - 1)
        return new_pos

    num_entry = len(lst)
    data = np.stack([lst, list(range(len(lst)))], axis=0)
    for _ in range(num_times):
        for i in range(num_entry):
            (x, old_pos) = list(data[:, i])
            if x == 0:
                continue
            new_pos = calculate_new_index(x, old_pos, num_entry)
            assert 0 <= new_pos < num_entry
            if new_pos > old_pos:
                data[1, (old_pos < data[1]) & (data[1] <= new_pos)] -= 1
                data[1, i] = new_pos
            else:
                data[1, (new_pos <= data[1]) & (data[1] < old_pos)] += 1
                data[1, i] = new_pos

    (values, positions) = data.tolist()
    new_list = [x for (_, x) in sorted(zip(positions, values))]
    return new_list


def solve_pt1(data: list[int]) -> int:
    mixed_data = mix(data)
    i_zero = mixed_data.index(0)
    mixed_sum = 0
    for i in (1000, 2000, 3000):
        mixed_sum += mixed_data[(i_zero + i) % len(mixed_data)]
    return mixed_sum


def solve_pt2(data: list[int]) -> int:
    decryption_key = 811589153
    decrypted_data = [v * decryption_key for v in data]
    mixed_data = mix(decrypted_data, num_times=10)
    i_zero = mixed_data.index(0)
    mixed_sum = 0
    for i in (1000, 2000, 3000):
        mixed_sum += mixed_data[(i_zero + i) % len(mixed_data)]
    return mixed_sum


def load(fpath: str) -> list[int]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    data = list(map(int, text))
    return data


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 3
    example_solution2 = 1623178306
    test_solution1 = 11123
    test_solution2 = 4248669215955

    example_answer1 = solve_pt1(data1.copy())
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(data2.copy())
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(data1.copy())
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(data2.copy())
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
