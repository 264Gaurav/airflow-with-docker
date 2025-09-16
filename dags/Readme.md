# End-to-End MLOps/LLMOps Project Setup

This README describes **what to track with each tool** (Git, DVC, LangSmith, MLflow, Airflow, RAGAS) and **how they work together** to manage and track an end-to-end ML/AI or RAG (Retrieval Augmented Generation) pipeline.

---

## 📦 Responsibility Matrix

| **Tool / Platform** | **What to Track / Handle**                                                                                                                                                                                                                                                                                                                           | **Why / Use Case**                                                                                                               |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Git**             | - Source code (pipelines, DAGs, preprocessing, training, eval, RAG logic)<br>- `.dvc` metadata files (not raw data)<br>- Configs (YAML/JSON)<br>- Environment files (`requirements.txt`, `conda.yaml`)<br>- CI/CD workflows                                                                                                                          | Version control for **code & configuration**. Ensures reproducibility and collaborative development.                             |
| **DVC**             | - Large datasets (corpus, embeddings, fine-tuning data)<br>- Model weights/checkpoints (optional if not stored in MLflow)<br>- Feature stores or indexes (e.g., FAISS, vector DB dumps)<br>- Preprocessed data versions<br>- DVC hashes as pointers in Git                                                                                           | Data & model versioning with **storage abstraction** (S3, GCS, Azure). Guarantees reproducibility by linking exact dataset used. |
| **LangSmith**       | - Prompt templates & chains<br>- Traces of LLM calls (inputs/outputs)<br>- Latency & token usage<br>- Error logs (timeouts, hallucinations)<br>- User feedback & ratings<br>- Prompt experiments A/B testing                                                                                                                                         | Debugging & monitoring of **LLM calls**. Understand behavior, costs, and performance of prompts/models.                          |
| **MLflow**          | - Experiment parameters (hyperparameters, configs, retrieval strategy)<br>- Metrics (accuracy, recall\@k, BLEU, RAGAS scores)<br>- Model artifacts (saved models, tokenizers, indexes)<br>- Links/tags (Git commit, DVC hash, Airflow run IDs)<br>- Environment snapshot (conda/requirements, Docker tag)<br>- Model registry (staging → production) | Central **experiment & model tracking** system. Provides lineage, promotion, and long-term reproducibility.                      |
| **Airflow**         | - Pipeline DAGs (ETL, training, eval, deploy)<br>- Scheduling (cron / event-driven)<br>- Orchestration of tasks across tools (DVC → train → eval → register)<br>- Logs of task execution, retries, alerts<br>- Dependencies & SLAs                                                                                                                   | **Orchestrator** for workflows. Ensures tasks run in order, on schedule, with retries & monitoring.                              |
| **RAGAS**           | - Evaluation metrics for RAG pipelines:<br> • Faithfulness<br> • Answer Relevance<br> • Context Recall<br> • Context Precision<br>- Evaluation reports (JSON/CSV)<br>- Benchmarks for deployment readiness                                                                                                                                           | Provides **objective evaluation** of retrieval-augmented generation pipelines. Helps decide whether to promote a model.          |

---

## 🔄 How They Work Together in a Project

Below is the flow of how these tools integrate for an **end-to-end ML or RAG pipeline**:

1. **Code & Config (Git)**

   - Developers write pipeline code (preprocessing, training, evaluation, deployment).
   - DAGs and configs are stored in Git.
   - `.dvc` files are versioned alongside code.

2. **Data & Artifacts (DVC)**

   - Datasets, preprocessed features, embeddings, and indexes are stored in remote storage (S3, GCS, etc.).
   - DVC tracks these versions and connects them with Git commits.

3. **Orchestration (Airflow)**

   - Airflow DAG schedules and runs pipeline tasks: `extract → preprocess → train → evaluate → register`.
   - Each task may call DVC to pull data, run training, or save outputs.
   - Airflow handles retries, dependencies, and operational logging.

4. **Experiment Tracking (MLflow)**

   - Training tasks start an MLflow run and log:

     - Params (e.g., embedding model name, retriever config).
     - Metrics (accuracy, recall\@k, latency).
     - Artifacts (trained models, indexes).
     - Tags (Git commit SHA, DVC data hash, Airflow run IDs).

   - MLflow Model Registry manages model lifecycle (staging → production).

5. **LLM Observability (LangSmith)**

   - During evaluation and testing, all prompt executions are traced in LangSmith.
   - Provides latency, token usage, error rates, and qualitative debugging of outputs.

6. **Evaluation (RAGAS)**

   - Automated evaluation of generated responses with metrics like faithfulness and context recall.
   - Results are logged back to MLflow as artifacts.
   - If thresholds are passed → Airflow task promotes the model in MLflow Registry.

7. **Deployment & Monitoring**

   - Deployed model versions are pulled from MLflow Registry.
   - Continuous monitoring can re-trigger evaluation DAGs on new data.

---

## ✅ Best Practices

- **Git + DVC** → ensure code/data lineage and reproducibility.
- **Airflow** → schedule, orchestrate, and log operational pipeline runs.
- **MLflow** → log experiments, metrics, and register models for lifecycle management.
- **LangSmith** → trace and debug LLM executions for quality & cost.
- **RAGAS** → evaluate RAG pipeline quality automatically before deployment.
- **Link IDs** → Always connect runs with metadata:

  - MLflow tags: `airflow.dag_id`, `airflow.dag_run_id`, `git.commit`, `dvc.hash`.
  - Airflow XComs to pass `mlflow_run_id` between tasks.

---

## 📂 Example Project Structure

```
project-root/
│── dags/
│   ├── etl_pipeline.py          # Airflow DAGs
│   ├── train_pipeline.py
│── data/
│   ├── raw/                     # Raw data (DVC tracked)
│   ├── processed/                # Processed features (DVC tracked)
│── models/                      # MLflow logged models
│── configs/
│   ├── train_config.yaml
│── notebooks/
│── requirements.txt
│── dvc.yaml                      # DVC pipeline definitions
│── README.md                     # Project documentation
```

---

By combining **Git, DVC, Airflow, MLflow, LangSmith, and RAGAS**, you get a **complete MLOps/LLMOps stack**:

- Versioned code + data → reproducibility.
- Orchestrated pipelines → automation.
- Experiment & model registry → reproducible experiments + lifecycle.
- Observability (LangSmith) + Evaluation (RAGAS) → quality control before deployment.

---
