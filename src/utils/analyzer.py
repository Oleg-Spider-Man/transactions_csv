from typing import Dict


def format_results_for_bot(results: Dict[str, float]) -> str:
    lines = []
    for category, amount in results.items():
        lines.append(f"{category}: {amount:.2f}")
    return "\n".join(lines)
