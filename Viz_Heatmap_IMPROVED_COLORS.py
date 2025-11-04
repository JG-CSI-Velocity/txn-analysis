# ===========================================================================
# VISUALIZATION: COMPETITOR SEGMENTATION HEATMAP (IMPROVED COLORS)
# ===========================================================================
"""
## Competitor Analysis - Segmentation Heatmap with Column-Specific Colors
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Group competitors by category
category_groups = {}

for competitor, comparison in competitor_spend_analysis.items():
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

# Create improved heatmap per category
for category, competitors in category_groups.items():
    cat_df = pd.DataFrame(competitors)
    cat_df = cat_df.sort_values('total_accounts', ascending=False)
    
    if len(cat_df) < 3:
        continue
    
    if len(cat_df) > 20:
        cat_df = cat_df.head(20)
    
    competitor_names = cat_df['competitor'].values
    data_matrix = cat_df[['heavy_pct', 'balanced_pct', 'cu_focused_pct']].values
    
    # Create figure with custom coloring - WIDER
    fig, ax = plt.subplots(figsize=(16, max(10, len(cat_df) * 0.5)))
    
    # Function to get color based on column and value
    def get_cell_color(col_idx, value):
        """
        Column 0 (Competitor-Heavy): Red scale - High is BAD
        Column 1 (Balanced): Orange scale - Neutral
        Column 2 (CU-Focused): Green scale - High is GOOD
        """
        if col_idx == 0:  # Competitor-Heavy (low is good)
            if value >= 20:
                return '#8B0000'  # Dark red - Very bad
            elif value >= 10:
                return '#CD5C5C'  # Light red - Bad
            elif value >= 5:
                return '#FFB6C1'  # Pink - Slightly bad
            else:
                return '#F0F0F0'  # Light gray - Good
        
        elif col_idx == 1:  # Balanced (neutral)
            if value >= 30:
                return '#FF8C00'  # Dark orange
            elif value >= 20:
                return '#FFA500'  # Orange
            elif value >= 10:
                return '#FFD700'  # Light orange/yellow
            else:
                return '#F0F0F0'  # Light gray
        
        else:  # CU-Focused (high is good)
            if value >= 90:
                return '#006400'  # Dark green - Excellent
            elif value >= 80:
                return '#228B22'  # Green - Very good
            elif value >= 70:
                return '#90EE90'  # Light green - Good
            else:
                return '#F0F0F0'  # Light gray - Not good
    
    # Create colored grid manually - WIDER CELLS
    for i in range(len(competitor_names)):
        for j in range(3):
            color = get_cell_color(j, data_matrix[i, j])
            rect = mpatches.Rectangle((j*2-0.9, i-0.45), 1.8, 0.9, 
                                      facecolor=color, edgecolor='white', linewidth=3)
            ax.add_patch(rect)
            
            # Determine text color for readability
            if color in ['#8B0000', '#006400', '#228B22']:
                text_color = 'white'
            else:
                text_color = 'black'
            
            # Add percentage text - LARGER & BOLDER
            ax.text(j*2, i, f'{data_matrix[i, j]:.0f}%',
                   ha="center", va="center", color=text_color, 
                   fontweight='bold', fontsize=18)
    
    # Set limits and ticks - ADJUSTED FOR WIDER CELLS
    ax.set_xlim(-1, 5)
    ax.set_ylim(-0.5, len(competitor_names)-0.5)
    
    ax.set_xticks([0, 2, 4])
    ax.set_yticks(np.arange(len(competitor_names)))
    ax.set_xticklabels(['🔴 Competitor-Heavy\n(>50%)', 
                        '🟠 Balanced\n(25-50%)', 
                        '🟢 CU-Focused\n(<25%)'], fontsize=14, fontweight='bold')
    ax.set_yticklabels(competitor_names, fontsize=13, fontweight='bold')
    
    # Format category name
    category_title = category.replace('_', ' ').title()
    ax.set_title(f'{category_title} - Account Segmentation (Top {len(cat_df)} by Accounts)', 
                 fontsize=17, fontweight='bold', pad=20)
    
    # Add account counts on the right - MUCH LARGER
    for i, (idx, row) in enumerate(cat_df.iterrows()):
        ax.text(5.5, i, f"n={int(row['total_accounts']):,}", 
                va='center', fontsize=14, fontweight='bold')
    
    ax.invert_yaxis()  # Top to bottom
    
    plt.tight_layout()
    plt.show()
    
    # Print legend
    print(f"\n{category_title} - Color Guide:")
    print("="*80)
    print("🔴 Competitor-Heavy Column (% at high risk):")
    print("   • Dark Red (≥20%) = 🚨 Very Bad - Many accounts at risk")
    print("   • Light Red (10-19%) = ⚠️ Bad - Significant risk")
    print("   • Pink (5-9%) = 🟡 Slight concern")
    print("   • Gray (<5%) = ✅ Good - Few at risk")
    print("\n🟢 CU-Focused Column (% loyal to you):")
    print("   • Dark Green (≥90%) = 🎯 Excellent - Very loyal")
    print("   • Green (80-89%) = ✅ Very Good - Strong loyalty")
    print("   • Light Green (70-79%) = 👍 Good - Decent loyalty")
    print("   • Gray (<70%) = ⚠️ Concerning - Low loyalty")
    print("="*80 + "\n")

print("\n✓ Improved heatmaps complete - Colors now match risk levels!")
