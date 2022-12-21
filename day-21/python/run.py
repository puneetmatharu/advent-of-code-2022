import re
from operator import add, eq, mul, sub, truediv
from pathlib import Path
from sympy import solve, sympify, Symbol
from typing import Union


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


def flatten_eqn(monkeys: dict, name: str) -> list[Union[int, str]]:
    if name == "humn":
        return ["humn"]
    if isinstance(monkeys[name], int):
        return [monkeys[name]]
    (m1, op, m2) = monkeys[name]
    (eqn1, eqn2) = (flatten_eqn(monkeys, m1), flatten_eqn(monkeys, m2))
    if "humn" not in eqn1 + eqn2:
        return [int(op(*eqn1, *eqn2))]
    return ["(", *eqn1, op, *eqn2, ")"]


def solve_pt1(monkeys: dict, name: str = "root") -> int:
    if isinstance(monkeys[name], int):
        return monkeys[name]
    (m1, op, m2) = monkeys[name]
    value = op(solve_pt1(monkeys, m1), solve_pt1(monkeys, m2))
    monkeys[name] = value
    return int(value)


def solve_pt2(monkeys: dict) -> int:
    def op_to_str(op):
        op_map = {add: "+", sub: "-", mul: "*", truediv: "/"}
        return op_map[op] if op in op_map else op
    (m1, _, m2) = monkeys["root"]
    monkeys["root"] = (m1, eq, m2)
    eqn = [*flatten_eqn(monkeys, m1), "=", *flatten_eqn(monkeys, m2)]
    eqn = "".join(map(str, map(op_to_str, eqn)))
    sympy_eq = sympify("Eq(" + eqn.replace("=", ",") + ")")
    humn = solve(sympy_eq, Symbol("humn"))[0]
    return humn


def load(fpath: str) -> str:
    def is_number(s: str) -> bool:
        return True if (re.search(r"^\d+$", s) is not None) else False
    text = None
    with open(fpath, "r") as f:
        text = f.read().split("\n")
    monkeys = {}
    for line in text:
        (name, job) = line.split(": ")
        if is_number(job):
            monkeys[name] = int(job)
        else:
            (m1, op_str, m2) = job.split(" ")
            op = {"+": add, "-": sub, "*": mul, "/": truediv}[op_str]
            monkeys[name] = [m1, op, m2]
    return monkeys


def main() -> int:
    example_solution1 = 152
    example_solution2 = 301
    test_solution1 = 364367103397416
    test_solution2 = 3782852515583

    example_answer1 = solve_pt1(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 1: {example_answer1}")
    assert example_answer1 == example_solution1
    test_answer1 = solve_pt1(load(TEST_DATA_PATH))
    print(f"[TEST] Answer to Part 1: {test_answer1}")
    assert test_answer1 == test_solution1

    example_answer2 = solve_pt2(load(EXAMPLE_DATA_PATH))
    print(f"[EXAMPLE] Answer to Part 2: {example_answer2}")
    assert example_answer2 == example_solution2
    test_answer2 = solve_pt2(load(TEST_DATA_PATH))
    print(f"[TEST] Answer to Part 2: {test_answer2}")
    assert test_answer2 == test_solution2


if __name__ == "__main__":
    main()
