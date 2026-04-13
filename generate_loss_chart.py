import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/training_data.csv")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["Step"], df["Training Loss"], color="#3B6D11", linewidth=2)
ax.fill_between(df["Step"], df["Training Loss"], alpha=0.1, color="#3B6D11")

epoch_boundaries = [1667, 3334]
for boundary in epoch_boundaries:
    ax.axvline(x=boundary, color="#888780", linestyle="--", linewidth=1)

ax.text(833,  1.62, "Epoch 1", ha="center", fontsize=10, color="#888780")
ax.text(2500, 1.62, "Epoch 2", ha="center", fontsize=10, color="#888780")
ax.text(4167, 1.62, "Epoch 3", ha="center", fontsize=10, color="#888780")

ax.set_xlabel("Training step", fontsize=12)
ax.set_ylabel("Training loss", fontsize=12)
ax.set_title("BERT fine-tuning — training loss over 5,000 steps", fontsize=14)
ax.set_xlim(100, 5000)
ax.set_ylim(0.8, 1.7)
ax.grid(axis="y", color="gray", alpha=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("training_loss.png", dpi=150)
print("Saved to training_loss.png")
plt.show()