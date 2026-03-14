# export_artifacts.py
import json
from pathlib import Path
from datetime import datetime

# Example results from your evaluation pipeline
results = [
    {
        "question": "How to check for the forced submission students by event?",
        "answer": "Please navigate to the SAT & PSAT student submission report and filter force submission and event name accordingly.",
        "ground_truth": "Please navigate to the SAT & PSAT student submission report and filter force submission and event name accordingly source(SAT & PSAT Student Submission report.pdf)",
        "contexts": ["Please refer to the SAT & PSAT Student Submission report for details on forced submissions by event."]
    },
    {
        "question": "show student with confidence index as HIGH for the event psat 8/9 fall 2024 primary?",
        "answer": "Please navigate to the SAT & PSAT student submission Report and select confidence index as 'HIGH' and event name as PSAT 8/9 fall 2024 primary filter.",
        "ground_truth": "Please navigate to the SAT & PSAT student submission Report and select confidence index as 'HIGH' and event name as PSAT 8/9 fall 2024 primary filter.",
        "contexts": ["Please refer to the SAT & PSAT Student Submission report for filtering students by confidence index and event."]
    }
]


def export_results(results, folder="artifacts"):
    """
    Export evaluation results to a JSONL file in the specified folder.
    The filename includes a timestamp to avoid overwriting previous runs.
    """
    artifact_dir = Path(folder)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_file = artifact_dir / f"run_{timestamp}.jsonl"

    with artifact_file.open("w", encoding="utf-8") as f:
        for record in results:
            f.write(json.dumps(record) + "\n")

    print(f"Artifacts exported to {artifact_file}")

# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    export_results(results)
