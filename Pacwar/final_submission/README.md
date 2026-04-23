# PacWar Final Submission

This folder contains the code and data used for my final PacWar submission.

# Files

- `geneticEvolution.py`: core genetic algorithm used to generate candidate genes
- `helpers.py`: helper functions, including battle scoring and gene utilities
- `gene_bank.py`: gene bank of candidate genes
- `training_pool_v1.txt`: training pool used during generation
- `validation_pool.txt`: evaluation pool used to rank genes
- `rank_gene_bank_vs_validation.py`: ranks the genes in `gene_bank.py` against the evaluation pool
- `gene_bank_vs_validation_rankings.txt`: saved ranking output
- `score.py`: round-robin scoring helper


# Environment Assumption 
- `_PyPacwar` executable located within this directory


# Final Generation Run

The final submitted gene was generated with these settings:

- Population size: `400`
- Generations per run: `30`
- Restarts: `60`
- Seeds: `1` through `60`
- Mutation rate: `0.01`
- Survival rate: `0.05`
- selection_k = 15`
- pool_k = 6
- population_k = 10



# How to Run

Run commands from inside this folder.

Generate genes:

python geneticEvolution.py


Rank the gene bank against the evaluation pool:

python rank_gene_bank_vs_validation.py

  The results of the rankings are written to:
  gene_bank_vs_validation_rankings.txt


