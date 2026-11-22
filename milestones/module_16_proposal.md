# Module 16 Formal problem proposal

## Project
SaaS anomaly detection with machine learning

This proposal documents the project scope for Assignment 16.1. It was assembled from the completed project for milestone submission; it is not a claim of an earlier submission or an unobserved forecast. Expected outcomes below are research expectations, not measured results. Actual findings are documented in the Module 20 notebook and final README.

## Research question
Can a machine-learning anomaly detector identify unusual cloud-service measurements more effectively than a simple statistical rule, while keeping false alarms manageable when normal workloads change?

Operations teams face a trade-off: missed anomalies can delay investigation, while repeated false alarms waste attention. The proposed solution produces a normal or potentially anomalous decision for each measurement to support human investigation. It does not predict an outage in advance, confirm root causes or automatically remediate incidents.

## Expected data sources and structure
Use public data from the Numenta Anomaly Benchmark (NAB), specifically realAWSCloudwatch and realKnownCause. These are multiple series within one benchmark, not independent providers.

| Data group | Series | Purpose |
|---|---|---|
| Initial CPU measurements | EC2 CPU 5f5533, 24ae8d, 53ea38 | Compare normal variation, annotated unusual periods and workload changes |
| Known-cause examples | EC2 request latency system failure; Auto Scaling Group CPU misconfiguration | Evaluate selected failure-related scenarios |
| Additional evaluation series | EC2 CPU 825cc2, network-in 257a54, ELB request-count 8c0756 | Examine static versus periodically updated detectors |

Each CSV contains timestamp and value columns. A separate JSON file maps series identifiers to start/end annotation windows. The signals have different units and cover different periods; the initial models should treat each series separately rather than join unrelated timestamps as if they describe one service. Window membership supplies evaluation labels, not confirmed incident duration or root cause.

Source: https://github.com/numenta/NAB
Acquisition: scripts/download_data.py in this repository. The current data inventory is reported in the analysis, rather than treated as information known before acquisition. No customer or proprietary telemetry is required.

## Expected techniques
1. Inspect column types, time coverage, cadence, missing entries, duplicate timestamps and distributions. Visualize measurements with annotation windows.
2. Sort chronologically, remove unusable and duplicate observations, and construct current-value, recent-average, variability, change and lag features. Historical reference features must exclude future values.
3. Separate training, validation and test periods chronologically. Fit transformations only on training/reference data; do not randomly shuffle time points.
4. Compare an explainable statistical Z-score rule with unsupervised Isolation Forest. The latter learns unusual combinations of features without incident labels.
5. Examine changing distributions and compare a static detector with periodic retraining on additional series.
6. Report precision, recall, F1, false-positive counts and rates; inspect both per-series results and aggregate counts. Event-window detection is supplemental and requires adequate event samples.

A supervised comparison is a later extension, documented separately in Notebook 06. It should not be represented as part of the original unsupervised design or as evidence that reliable production incident labels exist.

## Expected results and success criteria
The hypothesis is that Isolation Forest may detect more labeled unusual observations than a single statistical threshold because it considers several features. Improvement is not guaranteed: it may create additional false alarms, miss unfamiliar patterns or confuse a new normal workload with an incident. Periodic retraining may help with change, but may also learn anomalous behavior or increase noise.

Success means producing a reproducible comparison that identifies where each method helps or fails, rather than promising a minimum score. F1 balances precision and recall; recall and false-positive counts must also be considered because a high average score does not define an acceptable alerting workload. When no positive labels occur, recall is undefined. When a model makes no positive predictions, precision is undefined.

No expected business savings, recovery-time reduction or production accuracy is asserted. Operational thresholds should be agreed with practitioners before a future pilot. The analysis can recommend a candidate for further testing, not establish production readiness.

## Risks and boundaries
Historical benchmark data may not represent modern SaaS workloads. Annotation windows are an imperfect proxy for incidents; adjacent readings are correlated. Few events and retrospective inspection limit generalization. Unseen workloads and incident-reviewed labels are needed before deployment. OpenTelemetry ingestion, logs/traces, incident correlation and automated remediation are proposed future work and were not deployed.

## Deliverables and progression
- Module 11: a concise prospectus defining the question, data needs and candidate techniques.
- Module 16: this formal proposal with expected data, methods and outcomes.
- Module 20: an executable initial-report notebook with the problem, EDA, methods and actual initial results.
- Module 24: the final nontechnical README and technical analyses, including later experiments and limitations.

Program-leader review sessions are course milestones. No meeting, feedback or approval is claimed here without a record.

[Module 20 initial report](../notebooks/20_initial_report_and_eda.ipynb) · [Final report](../README.md)
