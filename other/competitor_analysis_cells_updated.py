"""
COMPETITOR ANALYSIS - JUPYTER NOTEBOOK CELLS
=============================================
Add these cells to your existing Transaction_Analysis.ipynb notebook.
They use the data you've already loaded (combined_df).
"""

# ===========================================================================
# CELL 1: CONFIGURATION
# ===========================================================================
"""
## Competitor Analysis - Configuration
"""

# Define competitors to analyze (UPDATE THIS FOR EACH CLIENT)
COMPETITOR_MERCHANTS = [
    'CAPE COD FIVE LOAN PAYMT',
    # Add more competitors as needed:
    # 'ANOTHER_COMPETITOR_NAME',
]

print("✓ Configuration set")
print(f"Analyzing {len(COMPETITOR_MERCHANTS)} competitor(s)")


# ===========================================================================
# CELL 2: FIND COMPETITOR TRANSACTIONS
# ===========================================================================
"""
## Competitor Analysis - Find Transactions
"""

all_competitor_data = {}
summary_data = []

for competitor in COMPETITOR_MERCHANTS:
    # Find all transactions matching this competitor
    competitor_mask = combined_df['merchant_name'].str.contains(
        competitor, 
        case=False, 
        na=False
    )
    
    competitor_trans = combined_df[competitor_mask].copy()
    
    if len(competitor_trans) == 0:
        print(f"⚠ No transactions found for: {competitor}")
        continue
    
    # Merchant variations table
    merchant_variations = competitor_trans.groupby('merchant_name').size().reset_index()
    merchant_variations.columns = ['Merchant Name', 'Transaction Count']
    merchant_variations = merchant_variations.sort_values('Transaction Count', ascending=False)
    
    print(f"\n{'='*100}")
    print(f"Competitor: {competitor}")
    print(f"{'='*100}\n")
    print(f"Merchant Name Variations ({len(merchant_variations)} found):")
    display(merchant_variations)
    
    # Summary statistics table
    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Transactions',
            'Unique Accounts',
            'Total Amount',
            'Average Transaction',
            'Median Transaction',
            'Min Transaction',
            'Max Transaction',
            'Date Range'
        ],
        'Value': [
            f"{len(competitor_trans):,}",
            f"{competitor_trans['primary_account_num'].nunique():,}",
            f"${competitor_trans['amount'].sum():,.2f}",
            f"${competitor_trans['amount'].mean():,.2f}",
            f"${competitor_trans['amount'].median():,.2f}",
            f"${competitor_trans['amount'].min():,.2f}",
            f"${competitor_trans['amount'].max():,.2f}",
            f"{competitor_trans['transaction_date'].min().strftime('%Y-%m-%d')} to {competitor_trans['transaction_date'].max().strftime('%Y-%m-%d')}" if 'transaction_date' in competitor_trans.columns else 'N/A'
        ]
    })
    
    print(f"\nOverall Statistics:")
    display(summary_stats)
    
    # Store for next cell
    all_competitor_data[competitor] = competitor_trans


# ===========================================================================
# CELL 3: ACCOUNT-LEVEL SUMMARY
# ===========================================================================
"""
## Competitor Analysis - Account Level Detail
"""

all_account_summaries = {}

for competitor, competitor_trans in all_competitor_data.items():
    print(f"\n{'='*100}")
    print(f"ACCOUNT ANALYSIS: {competitor}")
    print(f"{'='*100}\n")
    
    # Create account-level summary
    account_summary = competitor_trans.groupby('primary_account_num').agg({
        'amount': ['sum', 'count', 'mean', 'min', 'max'],
        'transaction_date': ['min', 'max']
    }).round(2)
    
    account_summary.columns = [
        'Total Amount', 
        'Transaction Count', 
        'Avg Amount', 
        'Min Amount', 
        'Max Amount',
        'First Transaction',
        'Last Transaction'
    ]
    
    account_summary = account_summary.sort_values('Total Amount', ascending=False)
    
    # Add frequency metrics
    account_summary['Days Active'] = (
        account_summary['Last Transaction'] - account_summary['First Transaction']
    ).dt.days
    
    account_summary['Recency (Days)'] = (
        pd.Timestamp.now() - account_summary['Last Transaction']
    ).dt.days
    
    # Format for display
    display_summary = account_summary.head(25).copy()
    display_summary['Total Amount'] = display_summary['Total Amount'].apply(lambda x: f"${x:,.2f}")
    display_summary['Avg Amount'] = display_summary['Avg Amount'].apply(lambda x: f"${x:,.2f}")
    display_summary['Min Amount'] = display_summary['Min Amount'].apply(lambda x: f"${x:,.2f}")
    display_summary['Max Amount'] = display_summary['Max Amount'].apply(lambda x: f"${x:,.2f}")
    display_summary['First Transaction'] = display_summary['First Transaction'].dt.strftime('%Y-%m-%d')
    display_summary['Last Transaction'] = display_summary['Last Transaction'].dt.strftime('%Y-%m-%d')
    
    print(f"Top 25 Accounts by Total Spend:")
    display(display_summary)
    
    # Store for export (keep numeric for export)
    all_account_summaries[competitor] = account_summary
    
    # Segmentation table
    segmentation = pd.DataFrame({
        'Segment': [
            'High Value (>$1,000)',
            'Medium Value ($500-$1,000)',
            'Lower Value (<$500)',
            '',
            'Frequent Users (5+ transactions)',
            'Recent Activity (last 30 days)',
            'Recent Activity (last 90 days)'
        ],
        'Account Count': [
            len(account_summary[account_summary['Total Amount'] > 1000]),
            len(account_summary[(account_summary['Total Amount'] >= 500) & (account_summary['Total Amount'] <= 1000)]),
            len(account_summary[account_summary['Total Amount'] < 500]),
            '',
            len(account_summary[account_summary['Transaction Count'] >= 5]),
            len(account_summary[account_summary['Recency (Days)'] <= 30]),
            len(account_summary[account_summary['Recency (Days)'] <= 90])
        ]
    })
    
    print(f"\nAccount Segmentation:")
    display(segmentation)


# ===========================================================================
# CELL 4: EXPORT RESULTS
# ===========================================================================
"""
## Competitor Analysis - Export to CSV
"""

# Create output directory if needed
output_dir = BASE_PATH / "Analysis Outputs" / f"{CLIENT_ID} - {CLIENT_NAME}" / "Competitor Analysis"
output_dir.mkdir(parents=True, exist_ok=True)

export_summary = []

for competitor in all_account_summaries.keys():
    competitor_clean = competitor.replace(' ', '_').replace('/', '_')
    
    # Export 1: Account Summary
    account_summary = all_account_summaries[competitor]
    output_file_summary = output_dir / f"Competitor_{competitor_clean}_Account_Summary.csv"
    account_summary.to_csv(output_file_summary)
    export_summary.append(['Account Summary', output_file_summary.name, len(account_summary)])
    
    # Export 2: Transaction Detail
    competitor_trans = all_competitor_data[competitor]
    competitor_trans_export = competitor_trans[[
        'primary_account_num',
        'transaction_date',
        'merchant_name',
        'amount',
        'source_file'
    ]].sort_values(['primary_account_num', 'transaction_date'])
    
    output_file_detail = output_dir / f"Competitor_{competitor_clean}_Transaction_Detail.csv"
    competitor_trans_export.to_csv(output_file_detail, index=False)
    export_summary.append(['Transaction Detail', output_file_detail.name, len(competitor_trans_export)])
    
    # Export 3: Marketing List (Priority Accounts)
    marketing_list = pd.DataFrame({
        'Account_Number': account_summary.index,
        'Transaction_Count': account_summary['Transaction Count'].astype(int),
        'Total_Spend': account_summary['Total Amount'].round(2),
        'Avg_Transaction': account_summary['Avg Amount'].round(2),
        'Last_Transaction_Date': account_summary['Last Transaction'].dt.strftime('%Y-%m-%d'),
        'Recency_Days': account_summary['Recency (Days)'].astype(int),
        'First_Transaction_Date': account_summary['First Transaction'].dt.strftime('%Y-%m-%d'),
        'Days_Active': account_summary['Days Active'].astype(int)
    })
    
    output_file_list = output_dir / f"Competitor_{competitor_clean}_Marketing_List.csv"
    marketing_list.to_csv(output_file_list, index=False)
    export_summary.append(['Marketing List', output_file_list.name, len(marketing_list)])

# Display export summary
export_df = pd.DataFrame(export_summary, columns=['File Type', 'Filename', 'Row Count'])
print(f"\n✓ All exports complete!")
print(f"Files saved to: {output_dir}\n")
display(export_df)


# ===========================================================================
# CELL 5: VISUALIZATION - Top Accounts
# ===========================================================================
"""
## Competitor Analysis - Top 20 Accounts Chart
"""

for competitor, account_summary in all_account_summaries.items():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    top_20 = account_summary.head(20).sort_values('Total Amount')
    
    bars = ax.barh(range(len(top_20)), top_20['Total Amount'], color='#FF6B6B')
    ax.set_yticks(range(len(top_20)))
    ax.set_yticklabels([f"Account {i+1}" for i in range(len(top_20))])
    ax.set_xlabel('Total Spend ($)', fontsize=12)
    ax.set_title(f'Top 20 Accounts by Spend - {competitor}', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top_20['Total Amount'])):
        ax.text(val, bar.get_y() + bar.get_height()/2, 
                f' ${val:,.0f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.show()


# ===========================================================================
# CELL 6: VISUALIZATION - Transaction Count Distribution
# ===========================================================================
"""
## Competitor Analysis - Transaction Count Distribution
"""

for competitor, account_summary in all_account_summaries.items():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.hist(account_summary['Transaction Count'], bins=30, color='#4ECDC4', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Number of Transactions per Account', fontsize=12)
    ax.set_ylabel('Number of Accounts', fontsize=12)
    ax.set_title(f'Transaction Count Distribution - {competitor}', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add summary stats
    mean_trans = account_summary['Transaction Count'].mean()
    median_trans = account_summary['Transaction Count'].median()
    ax.axvline(mean_trans, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_trans:.1f}')
    ax.axvline(median_trans, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_trans:.1f}')
    ax.legend()
    
    plt.tight_layout()
    plt.show()


# ===========================================================================
# CELL 7: VISUALIZATION - Recency Analysis
# ===========================================================================
"""
## Competitor Analysis - Recency Distribution
"""

for competitor, account_summary in all_account_summaries.items():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.hist(account_summary['Recency (Days)'], bins=30, color='#FFA500', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Days Since Last Transaction', fontsize=12)
    ax.set_ylabel('Number of Accounts', fontsize=12)
    ax.set_title(f'Recency Distribution - {competitor}', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add reference lines
    ax.axvline(30, color='red', linestyle='--', linewidth=2, label='30 days')
    ax.axvline(90, color='darkred', linestyle='--', linewidth=2, label='90 days')
    ax.axvline(180, color='purple', linestyle='--', linewidth=2, label='180 days')
    ax.legend()
    
    # Add stats annotation
    recent_30 = len(account_summary[account_summary['Recency (Days)'] <= 30])
    recent_90 = len(account_summary[account_summary['Recency (Days)'] <= 90])
    total = len(account_summary)
    
    stats_text = f'Last 30 days: {recent_30:,} ({recent_30/total*100:.1f}%)\nLast 90 days: {recent_90:,} ({recent_90/total*100:.1f}%)'
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()


# ===========================================================================
# CELL 8: VISUALIZATION - Spend vs Frequency
# ===========================================================================
"""
## Competitor Analysis - Spend vs Transaction Frequency
"""

for competitor, account_summary in all_account_summaries.items():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    scatter = ax.scatter(account_summary['Transaction Count'], 
                        account_summary['Total Amount'], 
                        alpha=0.6, 
                        c=account_summary['Recency (Days)'],
                        cmap='RdYlGn_r',
                        s=100,
                        edgecolors='black',
                        linewidth=0.5)
    
    ax.set_xlabel('Transaction Count', fontsize=12)
    ax.set_ylabel('Total Spend ($)', fontsize=12)
    ax.set_title(f'Spend vs Transaction Frequency - {competitor}', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Days Since Last Transaction', rotation=270, labelpad=20)
    
    # Identify high-value quadrants
    median_count = account_summary['Transaction Count'].median()
    median_spend = account_summary['Total Amount'].median()
    
    ax.axvline(median_count, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(median_spend, color='gray', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    ax.text(0.75, 0.95, 'High Value\nFrequent', transform=ax.transAxes, 
            ha='center', va='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax.text(0.25, 0.95, 'High Value\nInfrequent', transform=ax.transAxes, 
            ha='center', va='top', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    plt.tight_layout()
    plt.show()
