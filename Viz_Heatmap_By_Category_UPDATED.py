# ===========================================================================
# VISUALIZATION: COMPETITOR SEGMENTATION HEATMAP BY CATEGORY
# ===========================================================================
"""
## Competitor Analysis - Segmentation Heatmap (By Category)
"""

import matplotlib.pyplot as plt
import numpy as np

# Group competitors by category
category_groups = {}

for competitor, comparison in competitor_spend_analysis.items():
    # Get category from the competitor data
    category = all_competitor_data[competitor]['competitor_category'].iloc[0]
    
    if category not in category_groups:
        category_groups[category] = []
    
    segment_counts = comparison['Segment'].value_counts()
    total = len(comparison)
    
    category_groups[category].append({
        'competitor': competitor,
        'total_accounts': total,
        'heavy_pct': segment_counts.get('Competitor-Heavy', 0) / total * 100,
        'balanced_pct': segment_counts.get('Balanced', 0) / total * 100,
        'cu_focused_pct': segment_counts.get('CU-Focused', 0) / total * 100
    })

# Create one heatmap per category (only if >5 competitors)
for category, competitors in category_groups.items():
    cat_df = pd.DataFrame(competitors)
    cat_df = cat_df.sort_values('total_accounts', ascending=False)
    
    # Skip small categories
    if len(cat_df) < 3:
        continue
    
    # Take top 20 if more than 20
    if len(cat_df) > 20:
        cat_df = cat_df.head(20)
    
    # Prepare data for heatmap
    competitor_names = cat_df['competitor'].values
    data_matrix = cat_df[['heavy_pct', 'balanced_pct', 'cu_focused_pct']].values
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, max(8, len(cat_df) * 0.4)))
    
    # Create heatmap - Use RdYlGn (not reversed) so:
    # Red = High % (bad when in Competitor-Heavy column)
    # Green = High % (good when in CU-Focused column)
    im = ax.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
    
    # Set ticks
    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(len(competitor_names)))
    ax.set_xticklabels(['Competitor-Heavy\n(>50%)', 'Balanced\n(25-50%)', 'CU-Focused\n(<25%)'], fontsize=10)
    ax.set_yticklabels(competitor_names, fontsize=9)
    
    # Rotate the tick labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    
    # Add text annotations
    for i in range(len(competitor_names)):
        for j in range(3):
            # Choose text color based on background
            text_color = "white" if data_matrix[i, j] < 30 or data_matrix[i, j] > 70 else "black"
            text = ax.text(j, i, f'{data_matrix[i, j]:.0f}%',
                          ha="center", va="center", color=text_color, fontweight='bold', fontsize=13)
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('% of Accounts', rotation=-90, va="bottom", fontsize=10)
    
    # Format category name for title
    category_title = category.replace('_', ' ').title()
    ax.set_title(f'{category_title} - Segmentation Heatmap (Top {len(cat_df)} by Accounts)', 
                 fontsize=13, fontweight='bold', pad=20)
    
    # Add account counts on the right
    for i, (idx, row) in enumerate(cat_df.iterrows()):
        ax.text(3.3, i, f"n={int(row['total_accounts']):,}", 
                va='center', fontsize=8, style='italic')
    
    plt.tight_layout()
    plt.show()
    
    # Print category summary
    print(f"\n{category_title}:")
    print(f"  🔥 Red = High Risk (>50% spend to competitor)")
    print(f"  🟡 Yellow = Medium Risk (25-50% spend to competitor)")
    print(f"  🟢 Green = Low Risk (<25% spend to competitor)")
    print("-"*80)

print("\n✓ Category-specific heatmaps complete")
