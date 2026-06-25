import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#f5f5f7'
plt.rcParams['axes.labelcolor'] = '#6e7d95'
plt.rcParams['xtick.color'] = '#6e7d95'
plt.rcParams['ytick.color'] = '#6e7d95'

print("[PhishNet Visualizer] Generating Figure 4.1: Dataset Class Distribution...")

categories = ['Legitimate (Class 0)', 'Phishing (Class 1)']
counts = [380869, 427173]
percentages = [47.15, 52.85]

fig1, ax1 = plt.subplots(figsize=(7, 5), facecolor='#090e1a')
ax1.set_facecolor('#12192c')

bars1 = ax1.bar(
    categories,
    counts,
    color=['#30d158', '#ff453a'],
    edgecolor='#1d2942',
    width=0.5
)

ax1.set_title(
    'PHISHNET INGESTION PIPELINE: DATASET CLASS DISTRIBUTION',
    fontsize=11,
    fontweight='bold',
    pad=15
)

ax1.set_ylabel('Total URL Records', fontsize=10)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#1d2942')
ax1.spines['bottom'].set_color('#1d2942')
ax1.yaxis.grid(True, linestyle='--', alpha=0.1, color='#f5f5f7')

for bar, pct in zip(bars1, percentages):
    height = bar.get_height()
    ax1.annotate(
        f'{height:,}\n({pct:.2f}%)',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 5),
        textcoords="offset points",
        ha='center',
        va='bottom',
        fontsize=9,
        fontweight='bold'
    )

plt.tight_layout()
plt.savefig('dataset_distribution.png', dpi=300, facecolor=fig1.get_facecolor())
plt.close()

print("[PhishNet Visualizer] Generating Figure 4.2: Model Performance Metrics Comparison...")

models = [
    'Logistic Regression',
    'Linear SVM',
    'Gradient Boosting',
    'Random Forest'
]

accuracy = [0.8354, 0.8339, 0.9030, 0.9441]
precision = [0.8399, 0.8357, 0.8928, 0.9402]
recall = [0.8507, 0.8534, 0.9280, 0.9549]
f1_score = [0.8453, 0.8445, 0.9100, 0.9475]

x = np.arange(len(models))
width = 0.2

fig2, ax2 = plt.subplots(figsize=(11, 6), facecolor='#090e1a')
ax2.set_facecolor('#12192c')

rects1 = ax2.bar(
    x - 1.5 * width,
    accuracy,
    width,
    label='Accuracy',
    color='#0a84ff',
    edgecolor='#1d2942'
)

rects2 = ax2.bar(
    x - 0.5 * width,
    precision,
    width,
    label='Precision',
    color='#30d158',
    edgecolor='#1d2942'
)

rects3 = ax2.bar(
    x + 0.5 * width,
    recall,
    width,
    label='Recall',
    color='#ffd60a',
    edgecolor='#1d2942'
)

rects4 = ax2.bar(
    x + 1.5 * width,
    f1_score,
    width,
    label='F1-Score',
    color='#bf5af2',
    edgecolor='#1d2942'
)

ax2.set_title(
    'SUPERVISED ALGORITHMIC PERFORMANCE COMPARISON MATRIX',
    fontsize=11,
    fontweight='bold',
    pad=20
)

ax2.set_xticks(x)
ax2.set_xticklabels(models, fontsize=9, fontweight='bold')
ax2.set_ylabel('Performance Metric Score', fontsize=10)
ax2.set_ylim(0.0, 1.1)

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#1d2942')
ax2.spines['bottom'].set_color('#1d2942')

ax2.yaxis.grid(True, linestyle='--', alpha=0.1, color='#f5f5f7')

def label_bars(rects):
    for rect in rects:
        height = rect.get_height()
        ax2.annotate(
            f'{height:.2%}',
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=8,
            fontweight='bold'
        )

label_bars(rects1)
label_bars(rects2)
label_bars(rects3)
label_bars(rects4)

ax2.legend(
    loc='lower right',
    facecolor='#0d1322',
    edgecolor='#1d2942',
    labelcolor='#f5f5f7'
)

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, facecolor=fig2.get_facecolor())
plt.close()

print("[PhishNet Visualizer] SUCCESS: 'dataset_distribution.png' and 'model_comparison.png' exported cleanly.")