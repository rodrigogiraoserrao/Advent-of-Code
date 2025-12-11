from functools import cache


def parse_input(filepath):
    connections = {}
    with open(filepath, "r") as f:
        for line in f:
            source, _, targets = line.partition(": ")
            connections[source] = set(targets.split())

    return connections


def part1(connections):

    def count_paths(from_, to_):
        if from_ == to_:
            return 1

        return sum(
            count_paths(neighbour, to_)
            for neighbour in connections[from_]
        )

    return count_paths("you", "out")


def part2(connections):

    @cache
    def count_paths(from_, to_, visited_dac, visited_fft):
        if from_ == to_:
            return visited_dac and visited_fft

        return sum(
            count_paths(
                neighbour,
                to_,
                visited_dac or neighbour == "dac",
                visited_fft or neighbour == "fft",
            )
            for neighbour in connections[from_]
        )

    return count_paths("svr", "out", False, False)


if __name__ == "__main__":
    connections = parse_input("input.txt")
    print(part1(connections))
    print(part2(connections))