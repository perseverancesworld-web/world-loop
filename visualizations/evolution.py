import matplotlib.pyplot as plt
import json
from pathlib import Path

def plot_evolution(lineage_path: str):
    """Simple evolution curve + trait visualization."""
    data = json.loads(open(lineage_path).read())
    epochs = [ep["epoch"] for ep in data.get("epochs", [])]
    scores = [ep["best_score"] for ep in data.get("epochs", [])]

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, scores, marker='o', label="Best Fitness")
    plt.title("World-Loop Evolution")
    plt.xlabel("Epoch")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(True)
    plt.savefig("evolution_plot.png")
    print("Plot saved: evolution_plot.png")