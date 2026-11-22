# Module 11 Project prospectus

## Question and operational motivation
Can machine learning identify unusual SaaS-related cloud measurements more effectively than a statistical rule without overwhelming operations teams with false alarms?

The project studies the balance between missed anomalies and alert noise. Its output is a candidate anomaly for human investigation, not a verified incident or an advance outage forecast.

## Data needs
Public NAB time series for CPU utilization, request latency, network traffic and request counts, with timestamps, numeric values and separate annotation windows. Multiple series come from one benchmark. Logs, traces, customer impact and deployment records are outside the available data.

## Proposed approach
Explore data quality and distributions, create features from current and earlier measurements, split by time, and compare a Z-score baseline with Isolation Forest. Assess precision, recall, F1 and false positives; investigate changing workloads and periodic retraining.

## Intended contribution and limits
Provide reproducible evidence about which approaches warrant further testing. Do not assume machine learning or retraining will outperform the baseline. Production integration through OpenTelemetry is future work, not an implemented capability.

This prospectus is assembled from the completed project to document the milestone; it does not claim a historical submission or program-leader approval.

[Formal Module 16 proposal](module_16_proposal.md) · [Project repository](../README.md)
