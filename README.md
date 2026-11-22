## Capstone Results

This project evaluates anomaly detection using AWS CloudWatch
time-series data from the Numenta Anomaly Benchmark.

Implemented:
- Statistical Z-score anomaly detection
- Isolation Forest
- Periodic Isolation Forest retraining
- Time-aware feature engineering
- Chronological model evaluation
- Distribution-shift analysis

Key findings:
- Isolation Forest improved detection on selected failure scenarios.
- One CPU series produced a 100% false-positive rate after
  a substantial change in operating conditions.
- Periodic retraining increased false positives from 6 to 167
  on the Day 5 evaluation datasets.

The OpenTelemetry integration is a proposed production
architecture and has not been deployed.

See CAPSTONE_REPORT.md for methodology, experimental
results, limitations, and future work.

## Reproducing the experiments

1. Install dependencies from requirements.txt.
2. Download the documented NAB datasets and annotations.
3. Run the notebooks in order.
4. Review outputs in data/processed/.
The data directories are intentionally excluded from Git.
## Installation and Reproduction

**Requirements:** Python 3.11 or 3.12, Git, and Jupyter Notebook.

Clone the repository:

```bash
git clone https://github.com/rvmkrishna/saas-aiops-observability.git
cd saas-aiops-observability
```

Create a Python virtual environment and install dependencies.

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Download and validate the public NAB datasets:

```powershell
.\.venv\Scripts\python.exe scripts\download_data.py
```

Execute notebooks in this order:

1. `notebooks/01_telemetry_eda.ipynb` — exploratory data analysis and feature engineering.
2. `notebooks/02_anomaly_detection.ipynb` — statistical baseline, Isolation Forest and evaluation.
3. `notebooks/05_drift_aware_detection.ipynb` — static versus adaptive Isolation Forest.

Generated data and model outputs are stored under `data/processed/` and excluded from Git.

**Dataset attribution:** Numenta Anomaly Benchmark (NAB), https://github.com/numenta/NAB.

**Scope:** The evaluated data comes from historical AWS CloudWatch metrics. OpenTelemetry ingestion, log/trace correlation, and production incident handling are proposed extensions, not implemented experimental results.