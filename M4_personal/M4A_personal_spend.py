# ===========================================================================
# M4A - TOP 50 PERSONAL MERCHANTS BY TOTAL SPEND
# ===========================================================================
"""
## M4A: Top 50 Personal Merchants by Total Spend (Consolidated)
Analysis of merchants used by personal accounts only
"""

# Use consolidated merchant names for personal data
top_personal_spend = personal_df.groupby('merchant_consolidated').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique'
}).round(2)

top_personal_spend.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts']
top_personal_spend = top_personal_spend.sort_values('total_amount', ascending=False).head(50)

# Format for display
display_df = top_personal_spend.reset_index()
display_df = display_df.rename(columns={
    'merchant_consolidated': 'Merchant',
    'total_amount': 'Total Spend',
    'transaction_count': 'Transactions',
    'avg_transaction': 'Avg Transaction',
    'unique_accounts': 'Unique Accounts'
})

# Format columns
display_df['Total Spend'] = display_df['Total Spend'].apply(lambda x: f"${x:,.0f}")
display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")

print("\n" + "="*100)
print(" " * 30 + "TOP 50 PERSONAL MERCHANTS BY TOTAL SPEND")
print("="*100)

display(display_df.style.hide(axis='index'))

# Summary stats
total_spend = top_personal_spend['total_amount'].sum()
total_transactions = top_personal_spend['transaction_count'].sum()
total_accounts = top_personal_spend['unique_accounts'].sum()

# Calculate % of total personal spend
personal_total = personal_df['amount'].sum()
top_50_pct = (total_spend / personal_total) * 100

summary = pd.DataFrame({
    'Metric': [
        'Total Spend (Top 50)',
        '% of Total Personal Spend',
        'Total Transactions (Top 50)',
        'Total Personal Accounts (Top 50)',
        'Total Personal Spend (All)',
        'Total Personal Accounts (All)'
    ],
    'Value': [
        f"${total_spend:,.0f}",
        f"{top_50_pct:.1f}%",
        f"{total_transactions:,.0f}",
        f"{total_accounts:,.0f}",
        f"${personal_total:,.0f}",
        f"{personal_df['primary_account_num'].nunique():,}"
    ]
})

print("\n")
display(summary.style.hide(axis='index'))
print("="*100)
