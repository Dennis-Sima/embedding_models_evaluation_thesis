import json
from tqdm import tqdm
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


def init_llm(model_name: str, base_url: str, temperature: float = 0.0):
    """
    Initialize LLM chain for paraphrasing with Ollama.
    """
    system_prompt = (
        "You are a paraphrasing assistant. Your only task is to generate a concise English paraphrase of the input text that preserves its meaning. "
        "Do NOT include explanations, definitions, notes, or any extra information. Your output must: "
        "be brief and concise (no more words than the input), contain no newline characters ('\\n') or '\"', punctuation, or formatting, "
        "and only include the paraphrased text—nothing else."
    )

    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url=base_url,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    chain = prompt | llm
    return chain


def generate_paraphrases(
    activities: dict[str, str],
    chain,
    model_name: str,
    temperature: float,
    num_paraphrases: int = 1,
    output_prefix: str = "activities_paraphrased",
):
    """
    Generate paraphrases for a set of activities using the provided LLM chain.
    """
    results = []
    filename = f"{output_prefix}_{num_paraphrases}_temp_{temperature}_{model_name.replace(':', '-')}.json"

    for original, cleaned in tqdm(activities.items(), desc="Generating paraphrases"):
        for _ in range(num_paraphrases):
            response = chain.invoke({"input": cleaned})
            paraphrased = response.content.strip()

            results.append({
                "original_activity": original,
                "cleared_activity": cleaned,
                "paraphrase": paraphrased,
            })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nParaphrased activities saved to {filename}")
    return results


if __name__ == "__main__":
    # Model parameters
    MODEL_NAME = "gemma3:12b"
    BASE_URL = "http://localhost:11434"
    TEMPERATURE = 0.0
    NUM_PARAPHRASES = 1

    # Load activities mapping (original -> cleaned)
    with open("../activities.json", "r", encoding="utf-8") as f:
        activity_map = json.load(f)

    # Initialize model
    chain = init_llm(MODEL_NAME, BASE_URL, TEMPERATURE)

    generate_paraphrases(
        activities=activity_map,
        chain=chain,
        model_name=MODEL_NAME,
        temperature=TEMPERATURE,
        num_paraphrases=NUM_PARAPHRASES,
    )
