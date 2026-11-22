"""Independently recalculate saved metrics and check their annotation labels."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'data/raw/nab'
labels = json.loads((RAW/'anomaly_windows.json').read_text())

def metrics(y, prediction):
    tp = int(((y == 1) & (prediction == 1)).sum())
    fp = int(((y == 0) & (prediction == 1)).sum())
    fn = int(((y == 1) & (prediction == 0)).sum())
    tn = int(((y == 0) & (prediction == 0)).sum())
    return dict(TP=tp, FP=fp, FN=fn, TN=tn,
                precision=tp/(tp+fp) if tp+fp else np.nan,
                recall=tp/(tp+fn) if tp+fn else np.nan,
                f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else np.nan,
                false_positive_rate=fp/(fp+tn) if fp+tn else np.nan)

def check_source(series, group, label_column):
    filename = series if series.endswith('.csv') else series+'.csv'
    key = next(k for k in labels if k.endswith('/'+filename))
    expected = np.zeros(len(group), dtype=int)
    for start, end in labels[key]:
        expected[group.timestamp.between(pd.Timestamp(start), pd.Timestamp(end)).to_numpy()] = 1
    assert np.array_equal(expected, group[label_column].to_numpy())
    raw = pd.read_csv(RAW/filename, parse_dates=['timestamp']).drop_duplicates('timestamp').set_index('timestamp')
    assert np.allclose(group.value.to_numpy(), raw.loc[group.timestamp,'value'].to_numpy())
    assert group.timestamp.is_unique and group.timestamp.is_monotonic_increasing
    return expected

def compare(calculated, saved):
    for key, value in calculated.items():
        # Original per-series convention leaves F1 undefined if no positive labels exist.
        if key == 'f1' and calculated['TP']+calculated['FN'] == 0 and pd.isna(saved[key]):
            continue
        assert np.isclose(value, saved[key], equal_nan=True), (key, value, saved[key])

messages = []
for day, label_column, columns in [
    ('day3', 'anomaly_label', {'Statistical Z-score':'stat_prediction', 'Isolation Forest':'if_prediction'}),
    ('day5', 'label', {'Static IF':'static_pred', 'Adaptive IF':'adaptive_pred'}),
]:
    folder = ROOT/'data/processed'/day
    predictions = pd.read_csv(folder/'test_predictions.csv', parse_dates=['timestamp'])
    saved = pd.read_csv(folder/'per_series_comparison.csv')
    for series, group in predictions.groupby('series'):
        y = check_source(series, group, label_column)
        filename = series if series.endswith('.csv') else series+'.csv'
        raw = pd.read_csv(RAW/filename, parse_dates=['timestamp']).dropna().drop_duplicates('timestamp').sort_values('timestamp').iloc[12:]
        expected_times = raw.iloc[int(len(raw)*.8):].timestamp.to_numpy()
        assert np.array_equal(group.timestamp.to_numpy(), expected_times)
        for model, column in columns.items():
            compare(metrics(y, group[column].to_numpy()), saved[(saved.series == series)&(saved.model == model)].iloc[0])
    aggregate = pd.read_csv(folder/'model_comparison.csv').set_index('model')
    for model, column in columns.items():
        compare(metrics(predictions[label_column].to_numpy(), predictions[column].to_numpy()), aggregate.loc[model])
    messages.append(f'PASS {day}: annotations, source values, splits, per-series and aggregate metrics')

folder = ROOT/'data/processed/validation'
predictions = pd.read_csv(folder/'test_predictions.csv', parse_dates=['timestamp'])
saved = pd.read_csv(folder/'test_metrics.csv').set_index('model')
for model, group in predictions.groupby('model'):
    for series, part in group.groupby('series'):
        check_source(series, part, 'label')
    compare(metrics(group.label.to_numpy(), group.prediction.to_numpy()), saved.loc[model])
selection = pd.read_csv(folder/'model_selection.csv')
assert np.allclose(selection.mean_cv_f1, (selection.fold_1_f1+selection.fold_2_f1)/2)
winner = selection.sort_values(['mean_cv_f1','model'], ascending=[False,True]).iloc[0]['model']
assert list(saved.index[saved.selected_by_cv]) == [winner]
grid = pd.read_csv(folder/'grid_search_results.csv')
assert len(grid) == 10 and int(selection.configurations.sum())*2 == 20
for model, group in grid.groupby('model'):
    assert np.isclose(group.mean_test_f1.max(), selection.set_index('model').loc[model,'mean_cv_f1'])
folds = pd.read_csv(folder/'folds.csv')
assert (pd.to_datetime(folds.train_end) < pd.to_datetime(folds.validation_start)-pd.Timedelta(hours=1)).all()
messages.append('PASS supervised extension: labels, raw values, confusion counts, metrics, CV winner and grid size')
for path in (ROOT/'notebooks').glob('*.ipynb'):
    notebook = json.loads(path.read_text(encoding='utf-8'))
    assert any(c['cell_type']=='markdown' for c in notebook['cells'])
    for cell in notebook['cells']:
        if cell['cell_type']=='code':
            assert cell['execution_count'] is not None, path.name
            assert all(o.get('output_type')!='error' for o in cell.get('outputs',[])), path.name
messages.append('PASS four notebooks contain explanatory text and executed code with no saved errors')
report = ROOT/'reports/verification.txt'
report.parent.mkdir(exist_ok=True)
report.write_text('\n'.join(messages)+'\n', encoding='utf-8')
print('\n'.join(messages))
