import argparse, json, os
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--world-dir", required=True, help="Path to run (e.g., runs/<world_id>)")
    args = p.parse_args()

    lineage_path = os.path.join(args.world_dir, "lineage.json")
    if not os.path.exists(lineage_path):
        print(f"No lineage.json found in {args.world_dir}")
        return

    with open(lineage_path, "r") as f:
        data = json.load(f)

    epochs, scores = [], []
    for ep in data.get("epochs", []):
        epochs.append(ep["epoch"])
        scores.append(ep["best_score"])

    plt.figure(figsize=(10, 5))
    plt.plot(epochs, scores, marker='o', linestyle='-', color='b')
    plt.axhline(y=0.85, color='r', linestyle='--', label='Curriculum Threshold')
    plt.title(f"Evolution Curve: {data['world_id'][:8]}")
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.ylim(0, 1.1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    out_file = os.path.join(args.world_dir, "evolution_curve.png")
    plt.savefig(out_file)
    print(f"Plot saved to {out_file}")

if __name__ == "__main__":
    main()