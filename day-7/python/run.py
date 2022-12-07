# -------------------------------------------------------------------------------------------------

from __future__ import annotations

import textwrap
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Union

# -------------------------------------------------------------------------------------------------

EXAMPLE_DATA_PATH = Path.cwd().parent / "data" / "example.dat"
ANSWER_DATA_PATH = Path.cwd().parent / "data" / "answer1.dat"
TEST_DATA_PATH = Path.cwd().parent / "data" / "test.dat"

# -------------------------------------------------------------------------------------------------

@dataclass
class Directory:
    name: str = ""
    parent: Optional[Directory] = None
    children: list[Union[Directory, File]] = field(default_factory=list)

    def has_child_dir(self, name: str) -> bool:
        for child in self.children:
            if is_dir(child) and (child.name == name):
                return True
        return False

    def get_child_dir(self, name: str) -> Optional[Directory]:
        for child in self.children:
            if is_dir(child) and (child.name == name):
                return child
        return None

    def add_file(self, name: str, size: int) -> None:
        self.children += [File(parent=self, name=name, size=size)]

    def add_dir(self, name: str) -> None:
        self.children += [Directory(parent=self, name=name)]
        
    @property
    def root(self) -> None:
        if self.parent is None:
            return self
        return self.parent.root

    @property
    def size(self) -> int:
        return sum([child.size for child in self.children])

    def __str__(self) -> str:
        full_str = f"- {self.name} (dir)"
        if len(self.children) != 0:
            full_str += "\n" + textwrap.indent("\n".join([str(c) for c in self.children]), prefix="  ")
        return full_str

    def __getattr__(self, name: str) -> Optional[Union[Directory, File]]:
        for child in self.children:
            if child.name == name:
                return child
        return None


@dataclass
class File:
    name: str
    size: int
    parent: Optional[Directory] = None

    def __str__(self):
        return f"- {self.name} (file, size={self.size})"


def is_file(x: Union[File, Directory]) -> bool:
    return isinstance(x, File)


def is_dir(x: Union[File, Directory]) -> bool:
    return isinstance(x, Directory)


Root = Directory

# -------------------------------------------------------------------------------------------------

def solve_pt1(root: Root) -> int:
    def _get_matching_dirs(root: Directory) -> list[Directory]:
        matching_dirs = []
        if root.size <= 100_000:
            matching_dirs += [root]
        for child in root.children:
            if is_dir(child):
                matching_dirs += _get_matching_dirs(child)
        return matching_dirs

    dirs = _get_matching_dirs(root)
    total_size = sum([d.size for d in dirs])
    return total_size


def solve_pt2(root: Root) -> int:
    def _flatten_dirs(root: Directory) -> list[Directory]:
        matching_dirs = [root]
        for child in root.children:
            if is_dir(child):
                matching_dirs += _flatten_dirs(child)
        return matching_dirs

    DISK_SPACE_THRESHOLD = 40_000_000
    need_to_free = root.size - DISK_SPACE_THRESHOLD
    all_dirs = _flatten_dirs(root)
    sorted_dirs = sorted(all_dirs, key=lambda d: d.size)
    for d in sorted_dirs:
        if d.size > need_to_free:
            return d.size


def parse(commands: list[str]) -> Root:
    current_node = Root(name="/")
    done = False
    line_num = 0
    while not done:
        if line_num >= len(commands):
            break
        next_line = commands[line_num]
        line_num += 1
        if next_line.startswith("$ cd"):
            cd_dest = next_line.split(" ")[-1]
            if cd_dest == "/":
                current_node = current_node.root
            elif cd_dest == "..":
                current_node = current_node.parent
            else:
                current_node = current_node.get_child_dir(cd_dest)
        elif next_line.startswith("$ ls"):
            while True:
                if line_num == len(commands):  # fully consumed
                    break
                next_line = commands[line_num]
                if next_line.startswith("$"): # finished processing ls output
                    break
                if next_line.startswith("dir"):
                    current_node.add_dir(name=next_line[4:])
                else:
                    (size, name) = next_line.split(" ")
                    current_node.add_file(name=name, size=int(size))
                line_num += 1
    root = current_node.root
    return root


def load(fpath: str) -> list[str]:
    with open(fpath, "r") as f:
        commands = f.read()
    return commands


def main() -> int:
    root1 = parse(load(EXAMPLE_DATA_PATH).split("\n"))
    root2 = parse(load(TEST_DATA_PATH).split("\n"))

    parsed_example = load(ANSWER_DATA_PATH)
    assert str(root1) == parsed_example

    assert root1.size == 48_381_165
    assert root1.a.e.size == 584
    assert root1.a.size == 94_853
    assert root1.d.size == 24_933_642

    example_answer1 = 95_437
    example_answer2 = 24_933_642
    test_answer1 = 1_667_443
    test_answer2 = 8_998_590

    answer11 = solve_pt1(root1)
    answer12 = solve_pt1(root2)
    print(f"[EXAMPLE] Answer to Part 1: {answer11}")
    print(f"[TEST] Answer to Part 1: {answer12}")
    assert answer11 == example_answer1
    assert answer12 == test_answer1

    answer21 = solve_pt2(root1)
    answer22 = solve_pt2(root2)
    print(f"[EXAMPLE] Answer to Part 2: {answer21}")
    print(f"[TEST] Answer to Part 2: {answer22}")
    assert answer21 == example_answer2
    assert answer22 == test_answer2


if __name__ == "__main__":
    main()

# -------------------------------------------------------------------------------------------------