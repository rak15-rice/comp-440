gene = int # 1 | 2 | 3 | 4
sequence = list[gene]

def score(rounds: int, c1: int, c2: int) -> tuple[int, int]:
    """
    Calculate the score for a battle between two genes.
    
    Args:
        rounds: Number of rounds the battle took (up to 500)
        c1: Number of mites of gene 1 remaining
        c2: Number of mites of gene 2 remaining
    
    Returns:
        A tuple (score1, score2) representing the scores for gene 1 and gene 2
    """
    # Gene 1 destroys gene 2 (c2 == 0)
    if c2 == 0:
        if rounds < 100:
            return (20, 0)
        elif rounds < 200:
            return (19, 1)
        elif rounds < 300:
            return (18, 2)
        else:  # rounds <= 500
            return (17, 3)
    
    # Gene 2 destroys gene 1 (c1 == 0)
    if c1 == 0:
        if rounds < 100:
            return (0, 20)
        elif rounds < 200:
            return (1, 19)
        elif rounds < 300:
            return (2, 18)
        else:  # rounds <= 500
            return (3, 17)
    
    # Battle went to 500 rounds - check ratios
    if rounds == 500:
        # Avoid division by zero
        if c1 == 0 or c2 == 0:
            # This shouldn't happen if we already checked above, but handle it
            if c1 == 0:
                return (0, 20)
            else:
                return (20, 0)
        
        ratio = c1 / c2
        
        # Gene 1 outnumbers gene 2 by at least 10:1
        if ratio >= 10.0:
            return (13, 7)
        
        # Gene 1 outnumbers gene 2 by between 3:1 and 10:1
        if ratio >= 3.0:
            return (12, 8)
        
        # Gene 1 outnumbers gene 2 by between 1.5:1 and 3:1
        if ratio >= 1.5:
            return (11, 9)
        
        # Check if gene 2 outnumbers gene 1
        inv_ratio = c2 / c1
        
        # Gene 2 outnumbers gene 1 by at least 10:1
        if inv_ratio >= 10.0:
            return (7, 13)
        
        # Gene 2 outnumbers gene 1 by between 3:1 and 10:1
        if inv_ratio >= 3.0:
            return (8, 12)
        
        # Gene 2 outnumbers gene 1 by between 1.5:1 and 3:1
        if inv_ratio >= 1.5:
            return (9, 11)
        
        # Neither outnumbers the other by more than 1.5:1
        return (10, 10)
    
    # Battle ended before 500 rounds but both species survived
    # This is an edge case - return a tie score
    return (10, 10)



def seq_to_str(sequence: list[gene]) -> str:
    return "".join(map(str, sequence))

def str_to_seq(string: str) -> list[gene]:
    return list(map(int, list(string)))

def strs_to_seqs(population: list[str]) -> list[list[int]]:
    return list(map(str_to_seq, population))

def seqs_to_strs(population: list[list[int]]) -> list[str]:
    return list(map(seq_to_str, population))

def gene_diff(seq1: list[int], seq2: list[int]) -> int:
    """Returns the count of differing positions."""
    return sum(a != b for a, b in zip(seq1, seq2))


import random

GENE_LEN = 50
ALLELES = (0, 1, 2, 3)

def alternating_gene(a: int, b: int, n: int = GENE_LEN) -> list[int]:
    return [a if i % 2 == 0 else b for i in range(n)]

def repeating_block_gene(block: list[int], n: int = GENE_LEN) -> list[int]:
    out = []
    while len(out) < n:
        out.extend(block)
    return out[:n]

def unique_genes(population: list[list[int]]) -> list[list[int]]:
    seen = set()
    result = []
    for gene in population:
        s = seq_to_str(gene)
        if s not in seen:
            seen.add(s)
            result.append(gene.copy())
    return result

def build_seed_opponent_pool(extra_genes: list[list[int]] | None = None) -> list[list[int]]:
    pool = [
        [0] * GENE_LEN,
        [1] * GENE_LEN,
        [2] * GENE_LEN,
        [3] * GENE_LEN,
        alternating_gene(0, 1),
        alternating_gene(1, 2),
        alternating_gene(2, 3),
        alternating_gene(0, 3),
        repeating_block_gene([0, 1, 2, 3]),
        repeating_block_gene([3, 2, 1, 0]),
        repeating_block_gene([0, 0, 1, 1]),
        repeating_block_gene([3, 3, 2, 2]),
        repeating_block_gene([0, 0, 0, 1, 1, 1]),
        repeating_block_gene([3, 3, 3, 2, 2, 2]),
    ]

    if extra_genes is not None:
        pool.extend([g.copy() for g in extra_genes])

    return unique_genes(pool)

def sample_opponents(
    archive: list[list[int]],
    population: list[list[int]],
    archive_k: int,
    population_k: int,
) -> list[list[int]]:
    chosen = []

    if archive:
        chosen.extend(random.sample(archive, min(archive_k, len(archive))))

    if population:
        chosen.extend(random.sample(population, min(population_k, len(population))))

    return unique_genes(chosen)

def update_pool(
    pool: list[list[int]],
    new_genes: list[list[int]],
    max_archive_size: int = 200,
) -> list[list[int]]:
    merged = unique_genes(pool + [g.copy() for g in new_genes])
    if len(merged) <= max_archive_size:
        return merged

    fixed = []
    others = []
    fixed_strings = {
        "0" * GENE_LEN,
        "1" * GENE_LEN,
        "2" * GENE_LEN,
        "3" * GENE_LEN,
    }

    for gene in merged:
        if seq_to_str(gene) in fixed_strings:
            fixed.append(gene)
        else:
            others.append(gene)

    random.shuffle(others)
    kept = fixed + others[:max_archive_size - len(fixed)]
    return unique_genes(kept)
