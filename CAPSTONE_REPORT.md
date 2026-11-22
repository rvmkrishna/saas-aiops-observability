# Intelligent Incident Detection for SaaS Platforms: An AIOps Framework Using Machine Learning and OpenTelemetry

## Executive Summary

Modern SaaS platforms depend on reliable operational monitoring to detect service degradation and infrastructure failures. Traditional statistical alerting can generate false alarms or miss abnormal behavior, while machine learning models may become unreliable when operational conditions change.

This project investigates whether machine learning can improve anomaly detection using operational telemetry. It compares statistical Z-score monitoring, Isolation Forest, and periodically retrained Isolation Forest models using datasets from the Numenta Anomaly Benchmark (NAB).

The results demonstrate that no single detection approach consistently performs best. Isolation Forest outperformed statistical thresholding on selected failure scenarios, but experienced a severe false-positive problem following a change in normal CPU behavior. Periodic retraining increased recall slightly on a separate evaluation group but substantially increased false positives.

The project proposes an OpenTelemetry-based architecture for integrating anomaly detection into SaaS observability systems. The implemented experiments use historical AWS CloudWatch metrics rather than live OpenTelemetry telemetry.

## 1. Business Problem

Enterprise SaaS platforms operate distributed applications across infrastructure and service dependencies. Monitoring solutions must identify operational anomalies promptly without overwhelming Site Reliability Engineering (SRE) teams with unnecessary alerts.

The business problem is balancing incident detection effectiveness against alert noise, especially when normal workload patterns evolve.

## 2. Project Objectives

The project evaluates three approaches:

1. Statistical Z-score anomaly detection.
2. Static Isolation Forest anomaly detection.
3. Periodically retrained Isolation Forest anomaly detection.

The primary objectives are to measure detection precision, recall, F1 score, and false-positive rate; investigate model reliability under distribution shift; and propose an OpenTelemetry-compatible operational architecture.

## 3. Data and Methodology

The experiments use publicly available Numenta Anomaly Benchmark (NAB) time-series datasets, including AWS EC2 CPU utilization, request latency, network traffic, load balancer request counts, and infrastructure misconfiguration scenarios.

The available measurements include timestamps, operational metric values, and separately maintained anomaly annotations.

Historical rolling averages, standard deviations, lagged observations, and changes in metric values were used as model features.

Data was divided chronologically into training, validation, and testing periods to preserve temporal order. Model parameters and thresholds were fit using historical data rather than future observations.

The experiments use historical CloudWatch data and do not establish actual incident root causes or production service-level impacts.

## 4. Results: Initial Model Comparison

On the Auto Scaling Group misconfiguration dataset, Isolation Forest achieved:

- Precision: 74.75%.
- Recall: 55.30%.
- F1 score: 63.57%.
- True positives: 829.
- False positives: 280.

The statistical Z-score baseline detected 31 anomalous observations while producing 40 false positives.

On the EC2 request latency failure dataset, Isolation Forest achieved 67.31% precision and 16.59% recall, compared with 33.33% precision and 2.37% recall for Z-score monitoring.

These results demonstrate that a feature-based ML model can detect more labeled anomalous observations in some scenarios, although false alarms and missed detections remain significant.

## 5. Distribution Shift Investigation

One EC2 CPU dataset revealed a major model reliability problem.

Average CPU utilization decreased from approximately 45.17 in training to 38.27 in testing, accompanied by a large reduction in volatility.

The static Isolation Forest model classified all 804 held-out normal-labeled observations as anomalous, yielding a 100% false-positive rate.

Analysis of anomaly-score distributions indicated a substantial shift between training and testing conditions.

This demonstrates how an anomaly detector can mistake a changing normal workload pattern for an incident.

The underlying operational cause of this change was not established by the available data.

## 6. Static Versus Adaptive Isolation Forest

A separate experiment evaluated static and periodically retrained Isolation Forest models on three additional NAB datasets.

The static model achieved:

- Precision: 76.92%.
- Recall: 9.95%.
- F1 score: 0.1762.
- False positives: 6.

The adaptive model achieved:

- Precision: 12.57%.
- Recall: 11.94%.
- F1 score: 0.1224.
- False positives: 167.

The adaptive approach increased recall slightly but generated substantially more false positives.

Both models detected the single annotated anomaly window present in the held-out evaluation periods. This limited event sample does not establish general event-detection reliability.

The experiment demonstrates that periodic retraining without adequate drift controls and model governance is not necessarily beneficial.

## 7. Proposed OpenTelemetry Architecture

A potential production implementation would use OpenTelemetry instrumentation and collectors to gather application and infrastructure telemetry.

The processing architecture would include:

- OpenTelemetry-based metrics, logs, and trace collection.
- Feature extraction and telemetry normalization.
- Statistical and ML anomaly inference.
- Drift monitoring and controlled model recalibration.
- Alert grouping and incident-context enrichment.
- Operator feedback for ongoing model evaluation.

Only the historical metrics-based ML experiments were implemented and evaluated in this capstone. Live OpenTelemetry ingestion and automated incident correlation remain future work.

## 8. Business Implications

The experiments illustrate three key operational considerations.

First, machine learning can improve detection coverage for certain infrastructure anomalies.

Second, model performance can deteriorate when normal workloads change, even without corresponding labeled failures.

Third, naive adaptive retraining can increase alert fatigue rather than reduce it.

For SaaS operators, these findings support the need for model governance, drift detection, careful threshold management, and human oversight.

The project does not claim measured reductions in production incident detection time, incident recovery time, or operational costs.

## 9. Limitations

- The evaluated data consists of historical CloudWatch time series, not live OpenTelemetry signals.
- Several test periods contain no labeled anomalies.
- The adaptive evaluation contains only one annotated anomaly window.
- NAB annotation windows are not equivalent to verified production incident durations.
- Model tuning and experiments were exploratory, and some test results were inspected during development.
- Operational impacts such as MTTD, MTTR, and cost savings were not independently established.
- The system does not currently perform production root-cause analysis or automated remediation.

## 10. Recommendations and Future Work

A production-oriented extension should evaluate:

- Drift detection using recent and historical distributions.
- Controlled, validation-based model recalibration.
- Independent event-level evaluation on additional unseen data.
- OpenTelemetry Collector ingestion and service-level telemetry.
- Correlation between metrics, logs, traces, and deployment events.
- Human-reviewed AI-generated incident explanations.
- Data retention, access control, and governance requirements.

## 11. Conclusion

This capstone demonstrates that anomaly detection for SaaS observability involves more than selecting an ML algorithm.

Feature-based machine learning can improve anomaly detection in some scenarios, but its reliability depends heavily on changing workload distributions and threshold selection.

The findings support a governed AIOps architecture combining statistical monitoring, machine learning, drift-aware model management, and OpenTelemetry-based observability.

## References

- Numenta Anomaly Benchmark: https://github.com/numenta/NAB
- OpenTelemetry Collector Architecture: https://opentelemetry.io/docs/collector/architecture/
- OpenTelemetry Demo: https://opentelemetry.io/docs/demo/
- Scikit-learn Isolation Forest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
