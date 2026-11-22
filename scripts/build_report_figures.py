"""Build readable README figures from the actual benchmark and saved results."""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/nab'
OUT = ROOT / 'reports/figures'
OUT.mkdir(parents=True, exist_ok=True)
sns.set_theme(style='whitegrid')
labels = json.loads((RAW/'anomaly_windows.json').read_text())
fig, axes = plt.subplots(2, 1, figsize=(11, 6.5))
for ax, series, title in zip(axes,
        ['cpu_utilization_asg_misconfiguration', 'ec2_cpu_utilization_5f5533'],
        ['Auto Scaling Group CPU history', 'CPU 5f5533 changes its operating level']):
    data = pd.read_csv(RAW/f'{series}.csv', parse_dates=['timestamp'])
    ax.plot(data.timestamp, data.value, color='#254e70', linewidth=.6)
    key = next(k for k in labels if k.endswith('/'+series+'.csv'))
    for start, end in labels[key]:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), color='#e4bd69', alpha=.35)
    ax.set(title=title, xlabel='Date in 2014', ylabel='CPU utilization (%)')
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
fig.suptitle('Historical measurements and shaded NAB annotation windows', fontsize=13)
fig.tight_layout()
fig.savefig(OUT/'telemetry_examples.png', dpi=180, bbox_inches='tight')
plt.close(fig)

data = pd.read_csv(ROOT/'data/processed/day5/model_comparison.csv').set_index('model').loc[['Static IF','Adaptive IF']]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, metric, title in zip(axes, ['TP','FP'], ['Correctly flagged observations','False-positive observations']):
    bars = ax.bar(['Static','Periodically retrained'], data[metric], color=['#254e70','#b47724'])
    ax.bar_label(bars, padding=3)
    ax.set(title=title, ylabel='Observation count', ylim=(0,185))
fig.suptitle('Retraining adds four correct flags and 161 false positives', fontsize=13)
fig.tight_layout()
fig.savefig(OUT/'retraining_tradeoff.png', dpi=180, bbox_inches='tight')
plt.close(fig)
print('Created two README figures from local data and verified results.')
