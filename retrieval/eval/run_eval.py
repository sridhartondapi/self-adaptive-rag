# run_eval.py
from pathlib import Path
import json
from datetime import datetime
from datasets import Dataset
from .ragas_eval import run_ragas_eval

# Load exported JSONL from artifacts
# Replace the hardcoded artifact_file line with this:
artifact_dir = Path("artifacts")
artifact_files = sorted(artifact_dir.glob("run_*.jsonl"), reverse=True)

if not artifact_files:
    raise FileNotFoundError("No exported JSONL files found in 'artifacts/'")

artifact_file = artifact_files[0]  # automatically pick the latest file
print(f"Using {artifact_file} for evaluation")


eval_records = []
with artifact_file.open("r", encoding="utf-8") as f:
    for line in f:
        eval_records.append(json.loads(line))

dataset = Dataset.from_list(eval_records)
print(f"Loaded {len(dataset)} records for evaluation")

# Run RAGAS evaluation
scores = run_ragas_eval(dataset)
print("Evaluation completed:")
print(scores)

# Save scores to artifacts
artifact_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
score_file = artifact_dir / f"ragas_scores_{timestamp}.jsonl"

with score_file.open("w", encoding="utf-8") as f:
    for record in scores:
        # Convert any NumPy arrays to lists
        for k, v in record.items():
            if hasattr(v, "tolist"):
                record[k] = v.tolist()
        f.write(json.dumps(record) + "\n")


print(f"RAGAS evaluation scores saved to {score_file}")
