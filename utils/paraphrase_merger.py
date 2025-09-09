import json
from collections import defaultdict
from typing import List, Dict


def merge_paraphrases(files: List[str], output_file: str) -> None:
    """
    Merge multiple JSON paraphrase files into a single list grouped by original activity.

    Args:
        files: List of JSON file paths to merge.
        output_file: Path to save the merged result.
    """
    all_entries: List[Dict] = []

    # Load all files
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            all_entries.extend(json.load(f))

    # Dictionary to collect paraphrases per original activity
    merged = defaultdict(lambda: {
        "original_activity": "",
        "cleaned_activity": "",
        "paraphrases": []
    })

    for entry in all_entries:
        orig = entry["original_activity"]
        cleaned = entry["cleared_activity"]
        paraphrase = entry["paraphrase"]

        merged[orig]["original_activity"] = orig
        merged[orig]["cleaned_activity"] = cleaned
        merged[orig]["paraphrases"].append(paraphrase)

    # Remove duplicates while preserving order
    for value in merged.values():
        value["paraphrases"] = list(dict.fromkeys(value["paraphrases"]))

    # Convert to list and save
    merged_list = list(merged.values())
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=2)

    print(f"Merged paraphrases saved to '{output_file}'")


if __name__ == "__main__":
    INPUT_FILES = [
        "activities_paraphrased_1_temp_0_cogito:14b.json",
        "activities_paraphrased_1_temp_0_gemma3:12b.json",
        "activities_paraphrased_1_temp_0_mistral-small3.2:24b.json"
    ]
    OUTPUT_FILE = "activities_with_synonyms_merged_noise_0.0.json"

    merge_paraphrases(INPUT_FILES, OUTPUT_FILE)
