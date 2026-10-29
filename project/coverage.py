"""Weighted maximum coverage with a fixed number of service locations."""
import itertools
import numpy as np


def make_case(size, replicate):
    m, d, k = {'Small': (12, 30, 3), 'Medium': (24, 70, 5), 'Large': (36, 110, 7)}[size]
    seed = 4000 + m * 10 + replicate
    rng = np.random.default_rng(seed)
    facilities = rng.uniform(0, 100, (m, 2))
    demand = rng.uniform(0, 100, (d, 2))
    weights = rng.integers(1, 11, d)
    radius = 22
    matrix = np.linalg.norm(facilities[:, None] - demand[None, :], axis=2) <= radius
    return {'id': f'{size}_{replicate}', 'size': size, 'seed': seed, 'k': k, 'radius': radius,
            'facilities': facilities.tolist(), 'demand': demand.tolist(),
            'weights': weights.tolist(), 'matrix': matrix.astype(int).tolist()}


def arrays(case):
    return np.asarray(case['matrix'], dtype=bool), np.asarray(case['weights'], dtype=int)


def value(selected, matrix, weights):
    return int(weights[np.any(matrix[list(selected)], axis=0)].sum()) if len(selected) else 0


def greedy(case):
    matrix, weights = arrays(case)
    selected = []
    for _ in range(case['k']):
        # Smallest index breaks equal marginal gains.
        j = max((j for j in range(len(matrix)) if j not in selected),
                key=lambda j: (value(selected + [j], matrix, weights), -j))
        selected.append(j)
    return sorted(selected)


def reference(case):
    matrix, weights = arrays(case)
    upper = min(int(weights[np.any(matrix, axis=0)].sum()),
                int(np.sort(matrix @ weights)[-case['k']:].sum()))
    if len(matrix) <= 12:
        best = max(itertools.combinations(range(len(matrix)), case['k']),
                   key=lambda s: value(s, matrix, weights))
        return {'kind': 'exact', 'value': value(best, matrix, weights), 'selection': list(best)}
    return {'kind': 'upper_bound', 'value': upper, 'selection': None}
