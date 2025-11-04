"""
COMPETITOR SPEND ANALYSIS - Additional Cells
=============================================
Analyzes whether competitor accounts have other spending activity
"""

# ===========================================================================
# CELL 9: TOTAL SPEND vs COMPETITOR SPEND ANALYSIS
# ===========================================================================
"""
## Competitor Analysis - Total Spend vs Competitor Spend
"""

competitor_spend_analysis = {}

for competitor, competitor_trans in all_competitor_data.items():
    print(f"\n{'='*100}")
    print(f"SPEND ANALYSIS: {competitor}")
    print(f"{'='*100}\n")
    
    # Get list of accounts with competitor transactions
    competitor_accounts = competitor_trans['primary_account_num'].unique()
    
    # Get ALL transactions for these accounts
    all_spend_for_accounts = combined_df[
        combined_df['primary_account_num'].isin(competitor_accounts)
    ].copy()
    
    # Calculate total spend by account
    total_spend_summary = all_spend_for_accounts.groupby('primary_account_num').agg({
        'amount': ['sum', 'count'],
        'transaction_date': ['min', 'max']
    }).round(2)
    
    total_spend_summary.columns = ['total_spend', 'total_transactions', 'first_date', 'last_date']
    
    # Get competitor spend by account (from our earlier analysis)
    account_summary = all_account_summaries[competitor]
    
    # Merge to compare
    comparison = pd.DataFrame({
        'Total_Spend': total_spend_summary['total_spend'],
        'Total_Transactions': total_spend_summary['total_transactions'],
        'Competitor_Spend': account_summary['Total Amount'],
        'Competitor_Transactions': account_summary['Transaction Count']
    })
    
    # Calculate other (non-competitor) spend
    comparison['Other_Spend'] = comparison['Total_Spend'] - comparison['Competitor_Spend']
    comparison['Other_Transactions'] = comparison['Total_Transactions'] - comparison['Competitor_Transactions']
    
    # Calculate percentages
    comparison['Competitor_Pct'] = (comparison['Competitor_Spend'] / comparison['Total_Spend'] * 100).round(1)
    comparison['Other_Pct'] = (comparison['Other_Spend'] / comparison['Total_Spend'] * 100).round(1)
    
    # Sort by total spend
    comparison = comparison.sort_values('Total_Spend', ascending=False)
    
    # Create segments
    comparison['Segment'] = 'Mixed'
    comparison.loc[comparison['Competitor_Pct'] >= 80, 'Segment'] = 'Competitor-Heavy (80%+)'
    comparison.loc[comparison['Competitor_Pct'] < 20, 'Segment'] = 'Minimal Competitor (<20%)'
    comparison.loc[(comparison['Competitor_Pct'] >= 20) & (comparison['Competitor_Pct'] < 80), 'Segment'] = 'Mixed (20-80%)'
    
    # Display top 25
    display_comparison = comparison.head(25).copy()
    display_comparison['Total_Spend'] = display_comparison['Total_Spend'].apply(lambda x: f"${x:,.2f}")
    display_comparison['Competitor_Spend'] = display_comparison['Competitor_Spend'].apply(lambda x: f"${x:,.2f}")
    display_comparison['Other_Spend'] = display_comparison['Other_Spend'].apply(lambda x: f"${x:,.2f}")
    display_comparison['Competitor_Pct'] = display_comparison['Competitor_Pct'].apply(lambda x: f"{x:.1f}%")
    display_comparison['Other_Pct'] = display_comparison['Other_Pct'].apply(lambda x: f"{x:.1f}%")
    
    print("Top 25 Accounts - Total vs Competitor Spend:")
    display(display_comparison[['Total_Spend', 'Total_Transactions', 'Competitor_Spend', 
                                'Competitor_Transactions', 'Other_Spend', 'Other_Transactions', 
                                'Competitor_Pct', 'Segment']])
    
    # Segment summary
    segment_summary = comparison.groupby('Segment').agg({
        'Total_Spend': ['count', 'sum', 'mean'],
        'Competitor_Spend': ['sum', 'mean'],
        'Other_Spend': ['sum', 'mean']
    }).round(2)
    
    segment_summary.columns = ['Account_Count', 'Total_Spend_Sum', 'Total_Spend_Avg',
                               'Competitor_Spend_Sum', 'Competitor_Spend_Avg',
                               'Other_Spend_Sum', 'Other_Spend_Avg']
    
    segment_summary = segment_summary.reset_index()
    
    # Format for display
    display_segments = segment_summary.copy()
    for col in ['Total_Spend_Sum', 'Total_Spend_Avg', 'Competitor_Spend_Sum', 
                'Competitor_Spend_Avg', 'Other_Spend_Sum', 'Other_Spend_Avg']:
        display_segments[col] = display_segments[col].apply(lambda x: f"${x:,.2f}")
    
    print(f"\nSegment Summary:")
    display(display_segments)
    
    # Key insights
    competitor_heavy = len(comparison[comparison['Competitor_Pct'] >= 80])
    minimal_competitor = len(comparison[comparison['Competitor_Pct'] < 20])
    total_accounts = len(comparison)
    
    insights = pd.DataFrame({
        'Insight': [
            'Total Accounts Analyzed',
            'Competitor-Heavy (80%+ at competitor)',
            'Minimal Competitor (<20% at competitor)',
            'Mixed Spending (20-80%)',
            '',
            'AT RISK: High competitor spend',
            'OPPORTUNITY: Low competitor spend'
        ],
        'Value': [
            f"{total_accounts:,}",
            f"{competitor_heavy:,} ({competitor_heavy/total_accounts*100:.1f}%)",
            f"{minimal_competitor:,} ({minimal_competitor/total_accounts*100:.1f}%)",
            f"{len(comparison[(comparison['Competitor_Pct'] >= 20) & (comparison['Competitor_Pct'] < 80)]):,}",
            '',
            f"{competitor_heavy:,} accounts to retain",
            f"{minimal_competitor:,} accounts to grow"
        ]
    })
    
    print(f"\nKey Insights:")
    display(insights)
    
    # Store for export and visualization
    competitor_spend_analysis[competitor] = comparison


# ===========================================================================
# CELL 10: VISUALIZATION - Competitor vs Other Spend
# ===========================================================================
"""
## Competitor Analysis - Spend Comparison Chart
"""

for competitor, comparison in competitor_spend_analysis.items():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get top 20 by total spend
    top_20 = comparison.head(20).sort_values('Total_Spend')
    
    # Create stacked bar chart
    bars1 = ax.barh(range(len(top_20)), top_20['Other_Spend'], 
                    label='Other Spend', color='#4ECDC4')
    bars2 = ax.barh(range(len(top_20)), top_20['Competitor_Spend'], 
                    left=top_20['Other_Spend'], label='Competitor Spend', color='#FF6B6B')
    
    ax.set_yticks(range(len(top_20)))
    ax.set_yticklabels([f"Account {i+1}" for i in range(len(top_20))])
    ax.set_xlabel('Total Spend ($)', fontsize=12)
    ax.set_title(f'Top 20 Accounts: Competitor vs Other Spend - {competitor}', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='lower right')
    ax.grid(axis='x', alpha=0.3)
    
    # Add total value labels
    for i, (idx, row) in enumerate(top_20.iterrows()):
        total = row['Total_Spend']
        comp_pct = row['Competitor_Pct']
        ax.text(total, i, f' ${total:,.0f} ({comp_pct:.0f}%)', 
                va='center', fontsize=9)
    
    plt.tight_layout()
    plt.show()


# ===========================================================================
# CELL 11: VISUALIZATION - Segment Distribution
# ===========================================================================
"""
## Competitor Analysis - Account Segment Pie Chart
"""

for competitor, comparison in competitor_spend_analysis.items():
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Count by segment
    segment_counts = comparison['Segment'].value_counts()
    
    colors = ['#FF6B6B', '#FFA500', '#4ECDC4']
    explode = (0.1, 0, 0)  # Explode the first slice (Competitor-Heavy)
    
    wedges, texts, autotexts = ax.pie(segment_counts.values, 
                                       labels=segment_counts.index,
                                       autopct='%1.1f%%',
                                       colors=colors,
                                       explode=explode,
                                       startangle=90,
                                       textprops={'fontsize': 12})
    
    # Bold the percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(14)
    
    ax.set_title(f'Account Segmentation by Competitor Spend % - {competitor}', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add legend with counts
    legend_labels = [f"{label}: {count:,} accounts" 
                    for label, count in zip(segment_counts.index, segment_counts.values)]
    ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.tight_layout()
    plt.show()


# ===========================================================================
# CELL 12: VISUALIZATION - Spend Distribution Scatter
# ===========================================================================
"""
## Competitor Analysis - Competitor vs Other Spend Scatter
"""

for competitor, comparison in competitor_spend_analysis.items():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create scatter plot
    scatter = ax.scatter(comparison['Other_Spend'], 
                        comparison['Competitor_Spend'],
                        s=100,
                        alpha=0.6,
                        c=comparison['Competitor_Pct'],
                        cmap='RdYlGn_r',
                        edgecolors='black',
                        linewidth=0.5)
    
    ax.set_xlabel('Other Spend ($)', fontsize=12)
    ax.set_ylabel('Competitor Spend ($)', fontsize=12)
    ax.set_title(f'Competitor vs Other Spend Distribution - {competitor}', 
                 fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Competitor Spend %', rotation=270, labelpad=20)
    
    # Add diagonal line (50/50 split)
    max_val = max(comparison['Other_Spend'].max(), comparison['Competitor_Spend'].max())
    ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, linewidth=2, label='50/50 Split')
    
    # Add reference lines
    median_other = comparison['Other_Spend'].median()
    median_comp = comparison['Competitor_Spend'].median()
    ax.axvline(median_other, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(median_comp, color='gray', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    ax.text(0.95, 0.95, 'High Competitor\nLow Other\n(AT RISK)', 
            transform=ax.transAxes, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='#FF6B6B', alpha=0.7),
            fontweight='bold')
    
    ax.text(0.05, 0.05, 'Low Competitor\nLow Other\n(Low Value)', 
            transform=ax.transAxes, ha='left', va='bottom',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
    
    ax.text(0.95, 0.05, 'High Both\n(High Value)', 
            transform=ax.transAxes, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    ax.text(0.05, 0.95, 'Low Competitor\nHigh Other\n(OPPORTUNITY)', 
            transform=ax.transAxes, ha='left', va='top',
            bbox=dict(boxstyle='round', facecolor='#4ECDC4', alpha=0.7),
            fontweight='bold')
    
    ax.legend()
    plt.tight_layout()
    plt.show()


# ===========================================================================
# CELL 13: EXPORT SPEND ANALYSIS
# ===========================================================================
"""
## Competitor Analysis - Export Spend Comparison
"""

for competitor, comparison in competitor_spend_analysis.items():
    competitor_clean = competitor.replace(' ', '_').replace('/', '_')
    
    # Export full spend comparison
    export_comparison = comparison.copy()
    export_comparison = export_comparison.reset_index()
    export_comparison.columns = ['Account_Number', 'Total_Spend', 'Total_Transactions',
                                 'Competitor_Spend', 'Competitor_Transactions',
                                 'Other_Spend', 'Other_Transactions',
                                 'Competitor_Pct', 'Other_Pct', 'Segment']
    
    output_file = output_dir / f"Competitor_{competitor_clean}_Spend_Comparison.csv"
    export_comparison.to_csv(output_file, index=False)
    
    # Export AT RISK accounts (80%+ competitor)
    at_risk = export_comparison[export_comparison['Competitor_Pct'] >= 80].copy()
    at_risk = at_risk.sort_values('Total_Spend', ascending=False)
    
    output_risk = output_dir / f"Competitor_{competitor_clean}_AT_RISK_Accounts.csv"
    at_risk.to_csv(output_risk, index=False)
    
    # Export OPPORTUNITY accounts (<20% competitor)
    opportunity = export_comparison[export_comparison['Competitor_Pct'] < 20].copy()
    opportunity = opportunity.sort_values('Total_Spend', ascending=False)
    
    output_opp = output_dir / f"Competitor_{competitor_clean}_OPPORTUNITY_Accounts.csv"
    opportunity.to_csv(output_opp, index=False)
    
    print(f"✓ Exported for {competitor}:")
    print(f"  - Full spend comparison: {output_file.name}")
    print(f"  - AT RISK accounts (80%+ competitor): {output_risk.name} ({len(at_risk):,} accounts)")
    print(f"  - OPPORTUNITY accounts (<20% competitor): {output_opp.name} ({len(opportunity):,} accounts)")
    print()

print("\n✓ All spend analysis exports complete!")
