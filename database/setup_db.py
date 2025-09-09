import json
import re
import pandas as pd
from typing import List
from database import vector_db

# Regex pattern for removing ID's from the SAP dataset
ACTIVITY_CLEANING_PATTERN = re.compile(
    r"""^(
        \d\s[A-Z]{2}\s-\s[A-Z]{2}\s-\s\d{2}\s-\s+  |  # 6 SZ - XX - 01 -
        [A-Z]+\s-\s+                                |  # EWM -
        \(\d+\s+[A-Z]+\d*\)\s*                      |  # (2 F2)
        \d\s+[A-Z]\d:\s*                            |  # 2 T3:, 1 G5:
        \(?\d+\s?[A-Z]+\)?\s*[-–—]+\s*              |  # (2 F2), 1 G0 –
        \d\s+[A-Z]\d\s*[-–—]+\s*                    |  # 1 J2 –, 3 M3 –
        \d\s+[A-Z]{2,}\s*[-–—]*\s*                  |  # 5 XU, 2 VM –
        [A-Z]+\d+\s*[-–—]+\s+                       |  # J11 –, BD9 –
        [A-Z]+\d+\s*                                |  # J11 alone
        \d+\s*[A-Z]+\s*[-–—]+\s+                    |  # 22 T –, 2 V8 –
        [A-Z]{2,}\s*[-–—]+\s+                       |  # BDN –
        [A-Z]+\s*-\s*[A-Z]{2}\s*-\s+                |  # BJK - XX -
        \d{1,2}\s*[-–—]+\s+                         |  # 2 –, 04 –
        \d+(?:\.\d+)+\s+                            |  # 8.5.1.3
        [A-Z]+-\d+(?:-\d+)+(?:\s+|(?=[A-Z]))        |  # MFS-50-10-30
        [A-Z]{2}\s*[-–—]\s*\d{2}\s*[-–—]\s+         # XX – 01 –
    )""",
    re.VERBOSE | re.MULTILINE,
)

def extract_and_process_activities(df: pd.DataFrame) -> List[str]:
    """
    Extract activities from SAP data, clean them, save to JSON, and return originals.

    Args:
        df: SAP export DataFrame with columns containing model_id and atom JSON.

    Returns:
        List of original activity texts (to be embedded in vector DB).
    """
    activities_raw: List[str] = []
    activities_clean: List[str] = []
    mapping: dict[str, str] = {}

    for _, row in df.iterrows():
        model_id = row[0]
        atoms_raw = row[2]

        try:
            atoms = json.loads(atoms_raw)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON in model {model_id}")
            continue

        for atom in atoms:
            operands = atom.get("operands", [])
            if not operands:
                print(f"Skipping atom without operands: {atom}")
                continue

            for operand in operands:
                cleaned = ACTIVITY_CLEANING_PATTERN.sub("", operand).strip()
                activities_raw.append(operand)
                activities_clean.append(cleaned)
                mapping[operand] = cleaned

    # Save activities to JSON
    with open("../activities_original.json", "w", encoding="utf-8") as f:
        json.dump(activities_raw, f, ensure_ascii=False, indent=2)

    with open("../activities_clean.json", "w", encoding="utf-8") as f:
        json.dump(activities_clean, f, ensure_ascii=False, indent=2)

    with open("../activities_mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    return activities_raw

if __name__ == "__main__":
    model_name = "all-MiniLM-L6-v2"
    path_to_sap_data = "/Users/dennis/Documents/BP/sap_models_atoms_logs.csv"
    sap_df = pd.read_csv(path_to_sap_data)

    activities = extract_and_process_activities(sap_df)

    collection = model_name.replace("/", "-")
    vector_db.import_activities(
        activities=activities,
        model_name=model_name,
        collection=collection,
    )
