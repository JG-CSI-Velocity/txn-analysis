# ===========================================================================
# VISUALIZATION: COMPETITOR SEGMENTATION SUMMARY
# ===========================================================================
"""
## Competitor Analysis - Segmentation Overview (All Competitors)
"""

import matplotlib.pyplot as plt
import pandas as pd

# Aggregate segmentation data across all competitors
segment_summary = []

for competitor, comparison in competitor_spend_analysis.items():
    segment_counts = comparison['Segment'].value_counts()
    total = len(comparison)
    
    segment_summary.append({
        'competitor': competitor,
        'total_accounts': total,
        'competitor_heavy': segment_counts.get('Competitor-Heavy', 0),
        'balanced': segment_counts.get('Balanced', 0),
        'cu_focused': segment_counts.get('CU-Focused', 0)
    })

summary_df = pd.DataFrame(segment_summary)

# Calculate percentages
summary_df['heavy_pct'] = (summary_df['competitor_heavy'] / summary_df['total_accounts'] * 100)
summary_df['balanced_pct'] = (summary_df['balanced'] / summary_df['total_accounts'] * 100)
summary_df['cu_focused_pct'] = (summary_df['cu_focused'] / summary_df['total_accounts'] * 100)

# Sort by total accounts (show biggest threats first)
summary_df = summary_df.sort_values('total_accounts', ascending=False).head(15)

# Create stacked bar chart
fig, ax = plt.subplots(figsize=(14, 10))

y_pos = range(len(summary_df))
competitors = summary_df['competitor'].values

# Create stacked bars
p1 = ax.barh(y_pos, summary_df['heavy_pct'], 
             color='#FF6B6B', label='Competitor-Heavy', height=0.7)
p2 = ax.barh(y_pos, summary_df['balanced_pct'], 
             left=summary_df['heavy_pct'],
             color='#FFA500', label='Balanced', height=0.7)
p3 = ax.barh(y_pos, summary_df['cu_focused_pct'], 
             left=summary_df['heavy_pct'] + summary_df['balanced_pct'],
             color='#4ECDC4', label='CU-Focused', height=0.7)

# Customize
ax.set_yticks(y_pos)
ax.set_yticklabels(competitors)
ax.set_xlabel('Percentage of Accounts (%)', fontsize=12, fontweight='bold')
ax.set_title('Competitor Account Segmentation - Top 15 by Total Accounts', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim(0, 100)

# Add grid
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add account counts as text on the right
for i, (idx, row) in enumerate(summary_df.iterrows()):
    ax.text(102, i, f"{int(row['total_accounts']):,}", 
            va='center', fontsize=9, fontweight='bold')

# Add column header for account counts
ax.text(102, len(summary_df), 'Accounts', 
        va='center', fontsize=9, fontweight='bold', style='italic')

plt.tight_layout()
plt.show()

print("\n📊 Segmentation Summary:")
print("="*80)
print(f"Total Competitors Analyzed: {len(competitor_spend_analysis)}")
print(f"Showing Top 15 by Account Count")
print("\nSegment Definitions:")
print("  🔴 Competitor-Heavy: >50% of spend goes to competitor")
print("  🟠 Balanced: 25-50% of spend goes to competitor")
print("  🔵 CU-Focused: <25% of spend goes to competitor")
print("="*80)
