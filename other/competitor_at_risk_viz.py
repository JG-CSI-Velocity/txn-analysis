# ===========================================================================
# CELL 10A: VISUALIZATION - AT RISK Accounts (Competitor-Heavy)
# ===========================================================================
"""
## Competitor Analysis - AT RISK Accounts (80%+ at Competitor)
"""

for competitor, comparison in competitor_spend_analysis.items():
    # Filter to Competitor-Heavy accounts only (80%+ at competitor)
    at_risk = comparison[comparison['Competitor_Pct'] >= 80].copy()
    
    if len(at_risk) == 0:
        print(f"No AT RISK accounts found for {competitor}")
        continue
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get top 20 AT RISK accounts by total spend
    top_20_risk = at_risk.head(20).sort_values('Total_Spend')
    
    # Create stacked bar chart
    bars1 = ax.barh(range(len(top_20_risk)), top_20_risk['Other_Spend'], 
                    label='Your Bank Spend', color='#4ECDC4')
    bars2 = ax.barh(range(len(top_20_risk)), top_20_risk['Competitor_Spend'], 
                    left=top_20_risk['Other_Spend'], label='Competitor Spend', color='#FF6B6B')
    
    ax.set_yticks(range(len(top_20_risk)))
    ax.set_yticklabels([f"Account {i+1}" for i in range(len(top_20_risk))])
    ax.set_xlabel('Total Spend ($)', fontsize=12)
    ax.set_title(f'Top 20 AT RISK Accounts (80%+ at Competitor) - {competitor}', 
                 fontsize=14, fontweight='bold', color='#FF6B6B')
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(axis='x', alpha=0.3)
    
    # Add total value labels with competitor percentage
    for i, (idx, row) in enumerate(top_20_risk.iterrows()):
        total = row['Total_Spend']
        comp_pct = row['Competitor_Pct']
        ax.text(total, i, f' ${total:,.0f} ({comp_pct:.0f}% competitor)', 
                va='center', fontsize=9, fontweight='bold')
    
    # Add summary box
    total_at_risk = len(at_risk)
    total_at_risk_spend = at_risk['Total_Spend'].sum()
    total_competitor_spend = at_risk['Competitor_Spend'].sum()
    
    summary_text = f'Total AT RISK Accounts: {total_at_risk:,}\n'
    summary_text += f'Total Spend: ${total_at_risk_spend:,.0f}\n'
    summary_text += f'Competitor Spend: ${total_competitor_spend:,.0f}\n'
    summary_text += f'At Risk %: {(total_competitor_spend/total_at_risk_spend*100):.1f}%'
    
    ax.text(0.02, 0.98, summary_text, transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='#FFE5E5', alpha=0.9),
            fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n✓ Showing top 20 of {total_at_risk:,} AT RISK accounts")
