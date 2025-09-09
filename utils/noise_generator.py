import json
import random
import string

def add_noise(text: str, error_rate: float) -> str:
    """
    Introduce random character-level noise into a string.
    """
    chars = list(text)
    i = 0
    while i < len(chars):
        if random.random() < error_rate:
            operation = random.choice(["replace", "delete", "insert"])

            if operation == "replace":
                chars[i] = random.choice(string.ascii_letters)

            elif operation == "delete" and len(chars) > 1:
                chars.pop(i)
                continue  # don't increment i since char is removed

            elif operation == "insert":
                chars.insert(i, random.choice(string.ascii_letters))
                i += 1  # skip newly inserted char
        i += 1

    return "".join(chars)


def add_noise_to_paraphrases(input_file: str, output_file: str, error_rate: float):
    """
    Load a JSON file of activities with paraphrases, add noise, and save the result.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        activities = json.load(f)

    for activity in activities:
        activity["paraphrases"] = [
            add_noise(p, error_rate) for p in activity.get("paraphrases", [])
        ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(activities, f, ensure_ascii=False, indent=2)

    print(f"Noisy paraphrases saved to {output_file}")


if __name__ == "__main__":
    # Default parameters
    INPUT_FILE = "activities_with_synonyms_merged_noise_0.0.json"
    ERROR_RATE = 0.2
    OUTPUT_FILE = f"activities_with_synonyms_merged_noise_{ERROR_RATE}.json"

    add_noise_to_paraphrases(INPUT_FILE, OUTPUT_FILE, ERROR_RATE)
