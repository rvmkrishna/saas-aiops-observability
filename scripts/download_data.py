
from pathlib import Path
from urllib.request import urlretrieve
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "raw" / "nab"
DEST.mkdir(parents=True, exist_ok=True)

BASE = "https://raw.githubusercontent.com/numenta/NAB/master"

SOURCES = {
    "ec2_cpu_utilization_5f5533.csv":
        "realAWSCloudwatch",
    "ec2_cpu_utilization_24ae8d.csv":
        "realAWSCloudwatch",
    "ec2_cpu_utilization_53ea38.csv":
        "realAWSCloudwatch",
    "ec2_request_latency_system_failure.csv":
        "realKnownCause",
    "cpu_utilization_asg_misconfiguration.csv":
        "realKnownCause",
    "ec2_cpu_utilization_825cc2.csv":
        "realAWSCloudwatch",
    "ec2_network_in_257a54.csv":
        "realAWSCloudwatch",
    "elb_request_count_8c0756.csv":
        "realAWSCloudwatch",
}

labels_file = DEST / "anomaly_windows.json"

if not labels_file.exists():
    urlretrieve(
        BASE + "/labels/combined_windows.json",
        labels_file
    )

with open(labels_file, encoding="utf-8") as f:
    labels = json.load(f)

for filename, folder in SOURCES.items():
    source = f"{folder}/{filename}"
    target = DEST / filename

    if not target.exists():
        url = f"{BASE}/data/{source}"
        print("Downloading:", source)
        urlretrieve(url, target)

    df = pd.read_csv(target)

    assert {"timestamp", "value"}.issubset(df.columns)
    assert source in labels
    assert len(df) > 0

    print("PASS:", filename, "rows:", len(df))

# Maintain original Day 1 filename compatibility
original = DEST / "ec2_cpu_utilization_5f5533.csv"
legacy = DEST / "cpu.csv"

if not legacy.exists():
    import shutil
    shutil.copyfile(original, legacy)

print("\nDATASET DOWNLOAD AND VALIDATION COMPLETE")
