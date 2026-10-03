import glob
import json
import os

MODELS_DIR = "results/models"

def list_runs(models_dir=MODELS_DIR):
    runs = []
    for run_dir in sorted(glob.glob(os.path.join(models_dir, "*")), reverse=True):
        if not os.path.isfile(os.path.join(run_dir, "final.zip")):
            continue
        label = os.path.basename(run_dir)
        metadata_path = os.path.join(run_dir, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path) as f:
                metadata = json.load(f)
            label += "  " + metadata["algo"].upper() + "  " + format(metadata["timesteps_trained"], ",") + " timesteps"
        runs.append((label, run_dir))
    return runs

def list_stages(run_dir):
    stages = [("final", os.path.join(run_dir, "final.zip"))]
    checkpoints = glob.glob(os.path.join(run_dir, "checkpoint_*_steps.zip"))
    checkpoints.sort(key=lambda p: int(os.path.basename(p).split("_")[1]))
    for path in checkpoints:
        steps = int(os.path.basename(path).split("_")[1])
        stages.append((format(steps, ",") + " steps", path))
    return stages
