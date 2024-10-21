from radon import cc_visit

from asunder.metrics.base_metric import Metric


class CycleComplexityMetric(Metric):
    name: str = "complexity"

    def compute(self, source_code: str) -> float:
        try:
            blocks = cc_visit(source_code)
            total_complexity = sum(block.complexity for block in blocks)
            return total_complexity
        except Exception as e:
            print(f"Error computing complexity: {e}")
            return 0.0

    def description(self) -> str:
        return "Complexity: Uses cyclomatic complexity to determine the branching and decision points"
