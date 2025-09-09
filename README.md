# A Comparative Evaluation of Embedding Models for Semantic Activity Label Matching in Business Processes

Large Language Models (LLMs) are increasingly applied in modern software systems to understand and generate natural language (NL), ensuring that produced texts are both syntactically and semantically coherent. A key role in this context is played by embedding models (EMs), which encode natural language queries (NLQs) into fixed-size multidimensional vectors. These embeddings capture semantic meaning and thus enable efficient processing and analysis of natural language. Foundational techniques such as Word2Vec and BERT provide well established approaches for generating word and text embeddings.
<br>The storage and processing of vector representations necessitate the use of specialized databases, known as VectorDBs. A pertinent example within the domain of process modeling and process mining involves the association of NLQs with process model elements (e.g., activities) without requiring prior familiarity with their domain-specific nomenclature. This is especially significant for users lacking domain expertise.
<br>This bachelor thesis, entitled "A Comparative Evaluation of Embedding Models for Semantic Activity Label Matching in Business Processes", investigates which embedding models yield the most accurate results across various evaluations and tests for mapping NLQs to activity labels. Particular focus is placed on the robustness of embeddings with respect to noisy or syntactically incorrect user inputs, as well as on the accuracy of semantic search in vector databases.

The findings of this work may contribute both to improving semantic search in process-data-driven applications and to deriving general recommendations regarding the most suitable embedding models under specific assumptions in the context of process modeling and process mining.

---

## Setup and Requirements

The project uses a Python-based setup and requires several dependencies. It's recommended to use a virtual environment to manage these dependencies.

### Project Requirements
- **Python Version**: 3.11.11  
- **LLM Host**: To generate paraphrases, you must run **Ollama** locally or on a server.  
  - Install all necessary LLMs and embedding models into Ollama.  

- **Dependencies**: Install all required packages using:  

```bash
pip install -r requirements.txt
```

> Run this command after activating your virtual environment.

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
