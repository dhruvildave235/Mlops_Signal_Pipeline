# 🚀 MLOps Batch Processing Pipeline (Technical Assessment)

## 📌 Overview

This project implements a **minimal MLOps-style batch job** designed to demonstrate:

* ✅ **Reproducibility** (deterministic results using config + seed)
* ✅ **Observability** (structured logging + machine-readable metrics)
* ✅ **Deployment Readiness** (Dockerized, one-command execution)

The pipeline simulates a **trading-signal generation system**, similar to real-world production pipelines.

---

## ⚙️ Features

* YAML-based configuration
* Robust input validation (config + dataset)
* Rolling mean computation on financial OHLCV data
* Binary signal generation
* Structured JSON metrics output
* Detailed logging for observability
* Fully Dockerized execution
* No hardcoded paths (CLI-driven)

---

## 📂 Project Structure

```
.
├── run.py              # Main pipeline script
├── config.yaml         # Configuration file
├── data.csv            # Input dataset (OHLCV)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container setup
├── README.md           # Project documentation
├── metrics.json        # Sample output (success)
├── run.log             # Sample log file
```

---

## ▶️ How to Run (Local)

```bash
pip install -r requirements.txt

python run.py \
  --input data.csv \
  --config config.yaml \
  --output metrics.json \
  --log-file run.log
```

---

## 🐳 Run with Docker

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

✔ Produces:

* `metrics.json`
* `run.log`
* Prints metrics to stdout

---

## 📊 Output Format

### ✅ Success Output

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```

### ❌ Error Output

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}
```

---

## 🧠 Processing Logic

1. Load and validate configuration (YAML)
2. Set deterministic seed (`numpy.random.seed`)
3. Load and validate dataset
4. Compute rolling mean on `close` column
5. Generate signal:

   ```
   signal = 1 if close > rolling_mean else 0
   ```
6. Exclude initial NaN rows (due to rolling window)
7. Compute metrics:

   * rows_processed
   * signal_rate
   * latency_ms
8. Save metrics + logs

---

## 🛡️ Error Handling

The pipeline gracefully handles:

* Missing input files
* Invalid CSV format
* Empty dataset
* Missing required column (`close`)
* Invalid configuration structure

⚠️ Metrics JSON is always generated (even on failure)

---

## 🔍 Observability

Logging includes:

* Job start & end timestamps
* Config validation details
* Dataset loading stats
* Processing steps
* Metrics summary
* Error traces (if any)

---

## 🔁 Reproducibility

* Controlled via:

  ```yaml
  seed: 42
  ```
* Ensures deterministic outputs across runs

---

## 📦 Dependencies

* pandas
* numpy
* pyyaml

---

## 👨‍💻 Author

**Dhruvil Dave**
Aspiring Software Developer | AI/ML Enthusiast

---

## 🚀 Notes

* Designed for simplicity, clarity, and production-readiness
* Easily extendable for real-world ML pipelines
* Follows best practices for MLOps batch processing

---
