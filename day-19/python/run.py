import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"


class Type(str, Enum):
    Ore = "ore",
    Clay = "clay",
    Obsidian = "obsidian",
    Geode = "geode",


class Blueprint:
    def __init__(self, i: int, ore: int, clay: int, obsidian: tuple[int, int], geode: tuple[int, int]):
        self.i = i
        self.prices = {
            "ore": {"ore": ore},
            "clay": {"ore": clay},
            "obsidian": {"ore": obsidian[0], "clay": obsidian[1]},
            "geode": {"ore": geode[0], "obsidian": geode[1]},
        }

    def __str__(self) -> str:
        return f"i: {self.i}, prices: {self.prices}"


def simulate_blueprint(
    bp: Blueprint,
    robots: dict = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
    collected_ore: dict = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0},
    time_limit: int = 24,
) -> int:
    def have_enough_money(cost: dict, available_ore: dict):
        for (ore_type, num) in cost.items():
            if available_ore[ore_type] < num:
                return False
        return True

    mins = 0
    while mins < time_limit:
        print(f"\n== Minute {mins + 1} ==")
        new_robots = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        for rt in ("geode", "obsidian", "clay", "ore"):
            if have_enough_money(bp.prices[rt], collected_ore):
                robots_if_bought = robots.copy()
                robots_if_not_bought = robots.copy()

                geodes_if_bought = simulate_blueprint(bp, robots, collected_ore, time_limit - mins)

                new_robots[rt] += 1
                print(f"Spend {bp.prices[rt]} to build a {rt}-collecting robot.")
                for (ore_type, num) in bp.prices[rt].items():
                    collected_ore[ore_type] -= num
        for (rt, n) in robots.items():
            collected_ore[rt] += n
            if n > 0:
                print(
                    f"{n} {rt}-collecting robot collects {n} {rt}; you now have {collected_ore[rt]} {rt}.")
        for (rt, num) in new_robots.items():
            if num > 0:
                robots[rt] += num
                print(f"The new {rt}-collecting robot is ready; you now have {robots[rt]} of them.")
        mins += 1
    return collected_ore["geode"]


def solve_pt1(blueprints: list[Blueprint]) -> int:
    best_bp = 0
    max_geodes = 0
    for bp in blueprints:
        collected_geodes = simulate_blueprint(bp)
        if collected_geodes > max_geodes:
            best_bp = bp.i
            max_geodes = collected_geodes
    return best_bp * max_geodes


def solve_pt2(text: str) -> int:
    return None


def load(fpath: str) -> str:
    text = None
    with open(fpath, "r") as f:
        text = f.read()
    pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    matches = [map(int, m) for m in re.findall(pattern, text)]
    blueprints = [Blueprint(i, o1, c1, (ob1, ob2), (g1, g2))
                  for (i, o1, c1, ob1, ob2, g1, g2) in matches]
    [print(bp) for bp in blueprints]
    return blueprints


def main() -> int:
    data1 = load(EXAMPLE_DATA_PATH)
    data2 = load(TEST_DATA_PATH)

    example_solution1 = 12
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
