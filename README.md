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