import json
from collections import Counter, defaultdict

with open("data/cases.json", "r") as f:
    cases = json.load(f)

total = len(cases)
print(f"Total cases: {total}\n")

# Collect all keys
all_keys = set()
for case in cases:
    all_keys.update(case.keys())

results = {}

for field in sorted(all_keys):
    non_empty_count = 0
    unique_values = set()
    list_lengths = []
    is_list_field = False

    for case in cases:
        val = case.get(field)

        #non-empty
        if val is not None and val != "" and val != [] and val != {}:
            non_empty_count += 1

            #list fields
            if isinstance(val, list):
                is_list_field = True
                list_lengths.append(len(val))
                for item in val:
                    unique_values.add(str(item))
            else:
                unique_values.add(str(val))

    coverage_pct = round((non_empty_count / total) * 100, 2)

    results[field] = {
        "non_empty_count": non_empty_count,
        "coverage_pct": coverage_pct,
        "unique_value_count": len(unique_values),
        "is_list_field": is_list_field,
        "avg_labels_per_sample": (
            round(sum(list_lengths) / len(list_lengths), 2) if list_lengths else None
        ),
        "max_labels_per_sample": max(list_lengths) if list_lengths else None,
        "sample_values": list(unique_values)[:10]  # preview
    }

print(f"{'Field':<35} {'Coverage':>10} {'Unique Vals':>12} {'List?':>6} {'Avg Labels':>11}")
print("-" * 80)
for field, stats in results.items():
    avg = str(stats["avg_labels_per_sample"]) if stats["avg_labels_per_sample"] else "—"
    print(
        f"{field:<35} {str(stats['coverage_pct']) + '%':>10} "
        f"{stats['unique_value_count']:>12} "
        f"{'Yes' if stats['is_list_field'] else 'No':>6} "
        f"{avg:>11}"
    )

with open("data/metadata_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n Results saved to metadata_analysis.json")

print("\n\n--- Recommended Method per Field ---\n")

for field, stats in results.items():
    pct = stats["coverage_pct"]
    unique = stats["unique_value_count"]
    is_list = stats["is_list_field"]

    #hardcoded regex fields
    regex_fields = {
    #90.19% coverage
    "filing_date",     

    #96.49%
    "filing_year",           

    #65.52% 
    "closing_year",         

    #46.47%
    "settlement_judgment_date",  

    #96.07%
    "summary_published_date",   

    #88.84%
    "last_checked_date",        

    #44.09%
    "order_start_year",       

    #34.22%
    "order_end_year",    

    #38.56%
    "terminating_date"  

    #18.46%
    "settlement_judgment_year", 

    #19.2%
    "injunction_duration"
}

    if pct < 10:
        method = "Skip, too sparse for reliable training"
    elif field in regex_fields:
        method = "Regex"
    elif unique <= 20 and not is_list:
        method = "Classifier Head"
    elif is_list and unique <= 50:
        method = "Multi-Label Classifier"
    else:
        #low coverage, verify if worth the LLM cost
        if pct < 30:
            method = "LLM Extractor"
        #high coverage
        else:
            method = "LLM Extractor"

    print(f"  {field:<35} ({pct}% coverage, {unique} unique) → {method}")