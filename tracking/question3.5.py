import random

Q = [
    [0.463, 0.093, 0.446, 0],
    [0.408, 0.593, 0, 0],
    [0.055, 0, 0.946, 0],
    [0, 0.5, 0.5, 0],
]

def estimate_probability(iters: int):
    state = 0 # random.randint(0, 3)
    counts = { i: 0 for i in range(4)}
    
    for i in range(iters):
        rand = random.random()
        cum_prob = 0
        
        for cand_state, prob in enumerate(Q[state]):
            cum_prob += prob
            if rand <= cum_prob:
                state = cand_state
                break
        
        # Ignore some initial samples to account for burn in.
        if i > 100:
            counts[state] += 1
    
    return (counts[0] + counts[1]) / sum(counts.values())

if __name__ == "__main__":
    for iters in (1_000, 5_000, 10_000):
        print(f"{estimate_probability(iters):.3f}")
