"""Exhaustively count functions for n <= 6. This is a finite check, not a proof.

Run from any directory with Python 3.9+. No dependencies, network, or model calls.
The enumeration was not supplied to the solver agents.
"""
from itertools import product
import json


def cyclic_vertices(function):
    vertices = set()
    for start in range(len(function)):
        orbit = []
        positions = {}
        current = start
        while current not in positions:
            positions[current] = len(orbit)
            orbit.append(current)
            current = function[current]
        vertices.update(orbit[positions[current]:])
    return vertices


def counts():
    rows = []
    for n in range(1, 7):
        favorable = sum(len(cyclic_vertices(f)) == 1 for f in product(range(n), repeat=n))
        assert favorable == n ** (n - 1)
        rows.append({"n": n, "all_functions": n ** n,
                     "one_cyclic_vertex": favorable, "expected": n ** (n - 1)})
    return rows


if __name__ == "__main__":
    print(json.dumps(counts(), indent=2))
