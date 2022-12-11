from dataclasses import dataclass
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


@dataclass
class Monkey:
    items: list[int]
    op: str
    if_true: int
    if_false: int
    div: int

    def __len__(self):
        return len(self.items)

    def add(self, new: int):
        return self.items.append(new)

    def take(self):
        return self.items.pop(0)

    def apply(self, old):
        return eval(self.op)

    def next_monkey(self, i: int):
        test = (i % self.div == 0)
        return self.if_true if test else self.if_false


def solve_pt1(monkeys: list[Monkey]) -> int:
    counts = [0] * len(monkeys)
    for _ in range(20):
        for i, m in enumerate(monkeys):
            for _ in range(len(m)):
                new_worry = m.apply(old=m.take()) // 3
                monkeys[m.next_monkey(new_worry)].add(new_worry)
                counts[i] += 1
    (x, y) = sorted(counts)[-2:]
    return x * y


def solve_pt2(monkeys: list[Monkey]) -> int:
    counts: list[int] = [0 for _ in monkeys]
    for r in range(600):
        for i, m in enumerate(monkeys):
            for _ in range(len(m)):
                new_worry = m.apply(old=m.take())
                monkeys[m.next_monkey(new_worry)].add(new_worry)
                counts[i] += 1

        if r % 100 == 0:
            print(f"== After round {r} ==")
            for i in range(len(monkeys)):
                print(f"Monkey {i} inspected items {counts[i]} times.")
    (x, y) = sorted(counts)[-2:]
    return x * y


def load(fpath: str) -> list[Monkey]:
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n\n")
    text = [x.split("\n") for x in text]
    monkeys = []
    for desc in text:
        monkeys += [Monkey(
            items=list(map(int, desc[1].split("items: ")[-1].split(", "))),
            op=desc[2].split(": ")[-1].split("= ")[-1],
            if_true=int(desc[4].split(" ")[-1]),
            if_false=int(desc[5].split(" ")[-1]),
            div=int(desc[3].split(" ")[-1])
        )]
    return monkeys


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 10605
    example_solution2 = 2713310158
    test_solution1 = 110220
    # test_solution2 = 0

    example_answer1 = solve_pt1(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(load(TEST_DATA_PATH))
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    # test_answer2 = solve_pt2(load(TEST_DATA_PATH))
    # print(f"[TEST] Answer to Part 2: {test_answer2}")
    # assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
