import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

with open("data/metadata_analysis.json", "r") as f:
    data = json.load(f)

regex_fields = {
    "filing_date", "filing_year", "closing_year",
    "settlement_judgment_date", "summary_published_date",
    "last_checked_date", "order_start_year", "order_end_year"
}

def get_method(field, stats):
    pct = stats["coverage_pct"]
    unique = stats["unique_value_count"]
    is_list = stats["is_list_field"]

    if pct < 10:
        return "skip"
    elif field in regex_fields:
        return "regex"
    elif unique <= 20 and not is_list:
        return "classifier"
    elif is_list and unique <= 50:
        return "multi"
    else:
        return "llm"

colors = {
    "skip":       "#888780",
    "regex":      "#1D9E75",
    "classifier": "#378ADD",
    "multi":      "#EF9F27",
    "llm":        "#FF2E2E"
}

labels = {
    "skip":       "Skip / low priority  (<10% coverage)",
    "regex":      "Regex",
    "classifier": "Classifier head",
    "multi":      "Multi-label classifier",
    "llm":        "LLM extractor"
}

fig, ax = plt.subplots(figsize=(12, 7))

for field, stats in data.items():
    method = get_method(field, stats)
    x = stats["coverage_pct"]
    y = np.log10(stats["unique_value_count"] + 1)
    ax.scatter(x, y, color=colors[method], s=80, alpha=0.85, edgecolors="white", linewidths=0.5)

# Y-axis: convert log ticks back to readable numbers
ytick_vals = [1, 10, 100, 1000, 10000]
ax.set_yticks([np.log10(v + 1) for v in ytick_vals])
ax.set_yticklabels([str(v) for v in ytick_vals])

ax.set_xlabel("Coverage (%)", fontsize=13)
ax.set_ylabel("Unique values (log scale)", fontsize=13)
ax.set_title("Metadata fields by coverage and cardinality", fontsize=15, fontweight="medium")
ax.set_xlim(-2, 107)

# Legend
patches = [mpatches.Patch(color=colors[m], label=labels[m]) for m in colors]
ax.legend(handles=patches, fontsize=10, loc="upper left", framealpha=0.9)

plt.tight_layout()
plt.savefig("metadata_scatter.png", dpi=150)
print("Saved to metadata_scatter.png")
plt.show()