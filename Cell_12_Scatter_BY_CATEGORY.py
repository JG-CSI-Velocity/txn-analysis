# ===========================================================================
# CELL 12: VISUALIZATION - Spend Distribution by Category (Aggregated)
# ===========================================================================
"""
## Competitor Analysis - Category-Level Spend Distribution
Shows one scatter plot per competitor category (not per competitor)
"""

import matplotlib.pyplot as plt
import numpy as np

# Group all competitor data by category
category_spend_data = {}

for competitor, comparison in competitor_spend_analysis.items():
    # Get category
    category = all_competitor_data[competitor]['competitor_category'].iloc[0]
    
    if category not in category_spend_data:
        category_spend_data[category] = []
    
    # Add each account's data with category tag
    for idx, row in comparison.iterrows():
        category_spend_data[category].append({
            'account': row['account'],
            'competitor_spend': row['competitor_spend'],
            'total_spend': row['total_spend'],
            'competitor_pct': row['competitor_pct'],
            'competitor_name': competitor
        })

# Create one scatter plot per category
for category, accounts in category_spend_data.items():
    cat_df = pd.DataFrame(accounts)
    
    # Skip small categories
    if len(cat_df) < 10:
        continue
    
    # Calculate your CU spend
    cat_df['your_cu_spend'] = cat_df['total_spend'] - cat_df['competitor_spend']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Create scatter plot
    scatter = ax.scatter(cat_df['your_cu_spend'], 
                        cat_df['competitor_spend'],
                        s=80,
                        alpha=0.6,
                        c=cat_df['competitor_pct'],
                        cmap='RdYlGn_r',
                        edgecolors='black',
                        linewidth=0.5,
                        vmin=0,
                        vmax=100)
    
    # Format category name
    category_title = category.replace('_', ' ').title()
    
    ax.set_xlabel('Your CU Spend ($)', fontsize=15, fontweight='bold')
    ax.set_ylabel(f'{category_title} Spend ($)', fontsize=15, fontweight='bold')
    ax.set_title(f'Spend Distribution - {category_title} Category', 
                 fontsize=18, fontweight='bold', pad=25)
    ax.grid(alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('% of Spend at Competitor', rotation=270, labelpad=30, fontsize=13, fontweight='bold')
    cbar.ax.tick_params(labelsize=11)
    
    # Add diagonal line (50/50 split)
    max_val = max(cat_df['your_cu_spend'].max(), cat_df['competitor_spend'].max())
    if max_val > 0:
        ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.6, linewidth=3, label='50/50 Split Line')
    
    # Add reference lines (medians)
    median_cu = cat_df['your_cu_spend'].median()
    median_comp = cat_df['competitor_spend'].median()
    ax.axvline(median_cu, color='blue', linestyle=':', alpha=0.4, linewidth=2.5)
    ax.axhline(median_comp, color='red', linestyle=':', alpha=0.4, linewidth=2.5)
    
    # Add quadrant labels
    ax.text(0.97, 0.97, '🚨 HIGH RISK\n\nHigh Competitor\nLow Your CU', 
            transform=ax.transAxes, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='#FF6B6B', alpha=0.9, edgecolor='darkred', linewidth=2),
            fontweight='bold', fontsize=12)
    
    ax.text(0.03, 0.03, '📉 LOW VALUE\n\nLow Both', 
            transform=ax.transAxes, ha='left', va='bottom',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8, edgecolor='gray', linewidth=2),
            fontsize=11)
    
    ax.text(0.97, 0.03, '💰 HIGH VALUE\n\nHigh Both', 
            transform=ax.transAxes, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, edgecolor='blue', linewidth=2),
            fontsize=11)
    
    ax.text(0.03, 0.97, '✅ WINNING\n\nLow Competitor\nHigh Your CU', 
            transform=ax.transAxes, ha='left', va='top',
            bbox=dict(boxstyle='round', facecolor='#4ECDC4', alpha=0.9, edgecolor='darkgreen', linewidth=2),
            fontweight='bold', fontsize=12)
    
    # Calculate statistics
    total_accounts = len(cat_df)
    unique_competitors = cat_df['competitor_name'].nunique()
    avg_cu_spend = cat_df['your_cu_spend'].mean()
    avg_comp_spend = cat_df['competitor_spend'].mean()
    avg_comp_pct = cat_df['competitor_pct'].mean()
    total_category_spend = cat_df['competitor_spend'].sum()
    
    # Stats box
    stats_text = f'📊 {category_title.upper()} SUMMARY\n'
    stats_text += f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
    stats_text += f'Total Accounts: {total_accounts:,}\n'
    stats_text += f'Competitors in Category: {unique_competitors}\n'
    stats_text += f'Avg CU Spend: ${avg_cu_spend:,.0f}\n'
    stats_text += f'Avg Competitor: ${avg_comp_spend:,.0f}\n'
    stats_text += f'Avg % at Competitor: {avg_comp_pct:.1f}%\n'
    stats_text += f'Total Category Spend: ${total_category_spend:,.0f}'
    
    ax.text(0.50, 0.97, stats_text, transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.95, edgecolor='black', linewidth=2.5),
            fontsize=11, fontweight='bold', family='monospace')
    
    plt.tight_layout()
    plt.show()
    
    # Print detailed quadrant analysis
    print(f"\n📊 {category_title} - Quadrant Analysis:")
    print("="*100)
    
    # Count accounts in each quadrant
    high_risk = len(cat_df[(cat_df['competitor_spend'] > median_comp) & 
                            (cat_df['your_cu_spend'] < median_cu)])
    winning = len(cat_df[(cat_df['competitor_spend'] < median_comp) & 
                          (cat_df['your_cu_spend'] > median_cu)])
    high_value = len(cat_df[(cat_df['competitor_spend'] > median_comp) & 
                             (cat_df['your_cu_spend'] > median_cu)])
    low_value = len(cat_df[(cat_df['competitor_spend'] < median_comp) & 
                            (cat_df['your_cu_spend'] < median_cu)])
    
    print(f"  🚨 High Risk (top-right):    {high_risk:,} accounts ({high_risk/total_accounts*100:.1f}%) - Using competitor MORE")
    print(f"  ✅ Winning (top-left):       {winning:,} accounts ({winning/total_accounts*100:.1f}%) - Loyal to your CU")
    print(f"  💰 High Value (bottom-right): {high_value:,} accounts ({high_value/total_accounts*100:.1f}%) - Big spenders everywhere")
    print(f"  📉 Low Value (bottom-left):   {low_value:,} accounts ({low_value/total_accounts*100:.1f}%) - Small/inactive accounts")
    
    print(f"\n  Top 5 Competitors in {category_title}:")
    top_5_in_category = cat_df.groupby('competitor_name')['competitor_spend'].sum().sort_values(ascending=False).head(5)
    for i, (comp, spend) in enumerate(top_5_in_category.items(), 1):
        print(f"    {i}. {comp}: ${spend:,.0f}")
    
    print("="*100)

print("\n✓ Category-level scatter plot analysis complete")
print("\n💡 Shows aggregated spend patterns across entire competitor categories")
print("   Much cleaner than 47 individual scatter plots!")
