"""🎄 Solution for Day 11 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 11.py
"""
from functools import cache

inp = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
inp2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""
part1_asserts = [
    (inp, 5),
]
part2_asserts = [
    (inp2, 2),
]


def parse_input(inp: str):
    devices_graph = {
        device[:-1]: childs
        for line in inp.splitlines()
        for device, *childs in [line.split()]
    }

    return devices_graph


def part1(inp: str) -> str | int | None:
    devices = parse_input(inp)
    visited = set()

    def dfs(start):
        if start == "out":
            return 1

        visited.add(start)
        total = 0

        for device in devices[start]:
            if device not in visited:
                total += dfs(device)

        visited.remove(start)

        return total

    return dfs("you")


def part2(inp: str) -> str | int | None:
    devices = parse_input(inp)
    visited = set()

    def dfs(start):
        if start == "out":
            return {"dac", "fft"} <= visited

        visited.add(start)
        total = 0

        for device in devices[start]:
            if device not in visited:
                total += dfs(device)

        visited.remove(start)

        return total

    return dfs("svr")


def main():
    print(part2(inp2))


if __name__ == "__main__":
    main()
