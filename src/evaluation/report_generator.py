"""Report generator assembling full evaluation sessions into structured reports."""

import time
from typing import Any


class ReportGenerator:
    """Compiles prompt, answers, pairwise results, rankings, and metrics into a standardized report."""

    @staticmethod
    def generate_report(
        session_id: str,
        mode: str,
        prompt: str,
        system_prompt: str | None,
        answers: list[dict[str, Any]],
        pairwise_comparisons: list[dict[str, Any]],
        rankings: list[dict[str, Any]],
        metrics: dict[str, Any],
        status: str = "COMPLETED",
    ) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "mode": mode,
            "status": status,
            "timestamp": time.time(),
            "input": {"prompt": prompt, "system_prompt": system_prompt},
            "answers": answers,
            "pairwise_comparisons": pairwise_comparisons,
            "rankings": rankings,
            "metrics": metrics,
        }
