import statistics
from pathlib import Path

import _PyPacwar
import helpers
import gene_bank


VALIDATION_PATH = Path("validation_pool.txt")
OUTPUT_PATH = Path("gene_bank_vs_validation_rankings.txt")


def battle_points(me, opp):
    rounds, c_me, c_opp = _PyPacwar.battle(me, opp)
    return helpers.score(rounds, c_me, c_opp)[0]


def read_gene_file(path):
    genes = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            genes.append(helpers.str_to_seq(line.split()[0]))
    return helpers.unique_genes(genes)


def evaluate_gene(gene, validation_genes):
    gene_string = helpers.seq_to_str(gene)
    scores = []
    skipped_self = 0

    for opponent in validation_genes:
        if gene_string == helpers.seq_to_str(opponent):
            skipped_self += 1
        else:
            scores.append(battle_points(gene, opponent))

    return {
        "gene": gene_string,
        "matches_used": len(scores),
        "skipped_self": skipped_self,
        "avg_score": float(statistics.fmean(scores)),
        "median_score": float(statistics.median(scores)),
        "min_score": min(scores),
        "max_score": max(scores),
        "wins": sum(score >= 11 for score in scores),
        "ties": sum(score == 10 for score in scores),
        "losses": sum(score <= 9 for score in scores),
        "validation_member": skipped_self > 0,
    }


def rank_genes(genes, validation_genes):
    results = [evaluate_gene(gene, validation_genes) for gene in helpers.unique_genes(genes)]
    results.sort(
        key=lambda result: (
            result["avg_score"],
            result["min_score"],
            result["wins"],
            result["median_score"],
            result["max_score"],
            result["gene"],
        ),
        reverse=True,
    )
    return results


def format_results(results):
    lines = ["Ranked by avg_score, then min_score, then wins, then median_score, then max_score.", ""]
    for i, result in enumerate(results, start=1):
        lines.append(
            f"{i:03d} gene={result['gene']} "
            f"avg={result['avg_score']:.2f} median={result['median_score']:.2f} "
            f"min={result['min_score']} max={result['max_score']} "
            f"wins={result['wins']} ties={result['ties']} losses={result['losses']} "
            f"matches_used={result['matches_used']} skipped_self={result['skipped_self']} "
            f"validation_member={result['validation_member']}"
        )
    return lines


def main():
    validation_genes = read_gene_file(VALIDATION_PATH)
    genes = gene_bank.get_gene_bank()
    ranked = rank_genes(genes, validation_genes)

    print(f"validation_path={VALIDATION_PATH}")
    print(f"validation_size={len(validation_genes)}")
    print(f"unique_gene_bank={len(helpers.unique_genes(genes))}")
    print("top_genes:")
    for line in format_results(ranked[:20]):
        print(line)

    OUTPUT_PATH.write_text("\n".join(format_results(ranked)) + "\n")
    print(f"wrote_ranking={OUTPUT_PATH}")


if __name__ == "__main__":
    main()

