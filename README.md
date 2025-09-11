# A Comparative Evaluation of Embedding Models for Semantic Activity Label Matching in Business Processes

As modern embedding models continue to evolve and increasingly capture the semantic context of data and text with greater precision, new opportunities for their application are emerging.
A particularly relevant use case in the context of process modeling and process mining is the mapping of natural language queries (NLQs) to elements of process models (e.g., activities) without requiring prior knowledge of their technical labels. This makes access significantly easier, especially for people without in-depth domain expertise.
Although numerous modern embedding models exist today, many of which are specifically designed for semantic text search and are freely available as open-source models on platforms such as Hugging Face, there are still no significant evaluations of these modern models within the mentioned application context. 
<br>Therefore, this bachelor thesis investigates which embedding models achieve the best results in various tests and evaluations when mapping NLQs to the correct activities of Process models. Particular attention is given to the robustness of the models in handling erroneous or incomplete NLQs and to their accuracy in searching for activities.
<br>The results of this work can, on the one hand, contribute to optimizing semantic search in process data-driven applications, and on the other hand, provide general recommendations on which embedding model is most suitable under specific assumptions in the fields of process modeling and process mining.
---

## Setup and Requirements

The project uses a Python-based setup and requires several dependencies. It's recommended to use a virtual environment to manage these dependencies.

### Project Requirements
- **Python Version**: 3.11.11  

- **Dependencies**: Install all required packages using:  

```bash
pip install -r requirements.txt
```

> Run this command after activating your virtual environment.

### Project Setup
#### Qdrant Database Setup (Docker)
The project uses Qdrant as a vector database. You can run it locally using Docker:
```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

#### Ollama 
The project uses Ollama, a tool for running large language models locally, to paraphrase the activities for evaluation.
- Install: [Ollama.com](https://ollama.com/) or via Homebrew (macOS):

```bash
brew install ollama
```

- Run Ollama daemon:

```bash
ollama run
```

- Install models (examples: `gemma3:12b`, `mistral-small3.2`, `cogito:14b`):

```bash
ollama pull <model_name>
```


---

## Evaluation and Testing

The evaluation process involves several steps to prepare the data, generate ground truth paraphrases, and simulate noisy inputs.

### Testing an Embedding Model

1. **Database Setup**  
   Run `database/setup.py`.  
   - Set the path to your SAP data CSV file in the `path_to_sap_data` variable.  
   - Choose the embedding model you want to test by setting the `model_name` variable.  

2. **Generate Paraphrases**  
   Navigate to the `utils` folder and run the paraphrase generator script.  
   - Creates a noise-free ground truth.  
   - Run this separately for each LLM you want to generate paraphrases for.  

3. **Simulate Noise**  
   In the `utils` folder, run the noise generator script.  
   - Simulates spelling mistakes.  
   - Control the noise level with the `ERROR_RATE` variable.  
   - Run separately for each LLM you are testing.  
   - **Note:** The `ERROR_RATE` parameter controls how much random noise is added to a string. Each character has a probability equal to `error_rate` of being changed, deleted, or having a random character inserted. A higher `error_rate` produces more “noisy” text, while a lower rate keeps the text closer to the original. For example, with `error_rate = 0.2`, roughly 1 in 5 characters will be altered randomly.

4. **Merge Paraphrases**  
   Use the paraphrase merger script in the `utils` folder.  
   - Combines noise-free and noisy ground truths into a single dataset.  
   - Consolidates all generated paraphrases from your LLMs.  

5. **Run Tests**  
   Execute the Jupyter notebook.  
   - Set the noise error rate in the `noise_error_rate` variable to match your generated data.  
   - Specify the embedding model you want to test in the `embedding_model_used` variable.

---

## Results and Resources

- Personal evaluation results presented in my thesis are located in the **`test` directory**.  
- For a broader comparison of embedding models, see the [**Massive Text Embedding Benchmark (MTEB) leaderboard**](https://huggingface.co/spaces/mteb/leaderboard)

---

This work aims to provide actionable insights for improving semantic search in process-data applications and to offer general recommendations for selecting suitable embedding models in the context of process modeling and process mining.
