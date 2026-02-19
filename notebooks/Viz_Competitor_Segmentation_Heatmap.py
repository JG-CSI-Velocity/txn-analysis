# ===========================================================================
# VISUALIZATION: COMPETITOR SEGMENTATION HEATMAP
# ===========================================================================
"""
## Competitor Analysis - Segmentation Heatmap (Top 20)
"""

import matplotlib.pyplot as plt
import numpy as np

# Aggregate segmentation percentages
heatmap_data = []

for competitor, comparison in competitor_spend_analysis.items():
    segment_counts = comparison['Segment'].value_counts()
    total = len(comparison)
    
    heatmap_data.append({
        'competitor': competitor,
        'total_accounts': total,
        'heavy_pct': segment_counts.get('Competitor-Heavy', 0) / total * 100,
        'balanced_pct': segment_counts.get('Balanced', 0) / total * 100,
        'cu_focused_pct': segment_counts.get('CU-Focused', 0) / total * 100
    })

heatmap_df = pd.DataFrame(heatmap_data)
heatmap_df = heatmap_df.sort_values('total_accounts', ascending=False).head(20)

# Prepare data for heatmap
competitors = heatmap_df['competitor'].values
data_matrix = heatmap_df[['heavy_pct', 'balanced_pct', 'cu_focused_pct']].values

# Create heatmap
fig, ax = plt.subplots(figsize=(10, 12))

im = ax.imshow(data_matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=100)

# Set ticks
ax.set_xticks(np.arange(3))
ax.set_yticks(np.arange(len(competitors)))
ax.set_xticklabels(['Competitor-Heavy', 'Balanced', 'CU-Focused'])
ax.set_yticklabels(competitors)

# Rotate the tick labels for better readability
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add text annotations
for i in range(len(competitors)):
    for j in range(3):
        text = ax.text(j, i, f'{data_matrix[i, j]:.0f}%',
                      ha="center", va="center", color="black", fontweight='bold', fontsize=9)

# Add colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Percentage of Accounts', rotation=-90, va="bottom", fontsize=10)

# Title
ax.set_title('Competitor Account Segmentation Heatmap - Top 20 by Total Accounts', 
             fontsize=13, fontweight='bold', pad=20)

# Add account counts on the right
for i, (idx, row) in enumerate(heatmap_df.iterrows()):
    ax.text(3.3, i, f"n={int(row['total_accounts']):,}", 
            va='center', fontsize=8, style='italic')

plt.tight_layout()
plt.show()

print("\n🔥 Red = High Risk (Competitor-Heavy accounts)")
print("🟡 Yellow = Medium Risk (Balanced accounts)")
print("🟢 Green = Low Risk (CU-Focused accounts)")
