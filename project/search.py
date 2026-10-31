"""Three local implementations. Each returns the best feasible selection and trace."""
import numpy as np
from coverage import arrays, value, greedy

PARAMS = {'population': 20, 'iterations': 60, 'mutation': .25}


def run(case, algorithm, seed):
    rng = np.random.default_rng(seed)
    matrix, weights = arrays(case)
    m, k = len(matrix), case['k']
    count = PARAMS['population']
    start = greedy(case)
    best, best_value, evaluations, trace = None, -1, 0, []

    def evaluate(s):
        nonlocal best, best_value, evaluations
        evaluations += 1
        v = value(s, matrix, weights)
        if v > best_value:
            best_value, best = v, sorted(map(int, s))
        return v

    if algorithm == 'GA':
        pool = [start] + [sorted(rng.choice(m, k, replace=False).tolist()) for _ in range(count - 1)]
        scores = [evaluate(s) for s in pool]
        trace.append(best_value)
        for _ in range(PARAMS['iterations']):
            children = [best.copy()]
            while len(children) < count:
                parents = []
                for _ in range(2):
                    a, b = rng.integers(count, size=2)
                    parents.append(pool[a if scores[a] >= scores[b] else b])
                union = sorted(set(parents[0]) | set(parents[1]))
                child = rng.choice(union, k, replace=False).tolist()
                if rng.random() < PARAMS['mutation']:
                    outside = [j for j in range(m) if j not in child]
                    if k > 0 and outside:
                        pos = int(rng.integers(k))
                        child[pos] = int(rng.choice(outside))
                children.append(sorted(child))
            pool = children
            scores = [evaluate(s) for s in pool]
            trace.append(best_value)
    else:
        raise ValueError('Unknown algorithm')
    assert evaluations == count * (PARAMS['iterations'] + 1)
    return {'selected': best, 'objective': best_value, 'history': trace, 'evaluations': evaluations}
