# ===========================================================================
# M3A - TOP 50 BUSINESS MERCHANTS BY TOTAL SPEND
# ===========================================================================
"""
## M3A: Top 50 Business Merchants by Total Spend (Consolidated)
Analysis of merchants used by business accounts only
"""

# Use consolidated merchant names for business data
top_business_spend = business_df.groupby('merchant_consolidated').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique'
}).round(2)

top_business_spend.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts']
top_business_spend = top_business_spend.sort_values('total_amount', ascending=False).head(50)

# Format for display
display_df = top_business_spend.reset_index()
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
print(" " * 30 + "TOP 50 BUSINESS MERCHANTS BY TOTAL SPEND")
print("="*100)

display(display_df)

# Summary stats
total_spend = top_business_spend['total_amount'].sum()
total_transactions = top_business_spend['transaction_count'].sum()
total_accounts = top_business_spend['unique_accounts'].sum()

# Calculate % of total business spend
business_total = business_df['amount'].sum()
top_50_pct = (total_spend / business_total) * 100

summary = pd.DataFrame({
    'Metric': [
        'Total Spend (Top 50)',
        '% of Total Business Spend',
        'Total Transactions (Top 50)',
        'Total Business Accounts (Top 50)',
        'Total Business Spend (All)',
        'Total Business Accounts (All)'
    ],
    'Value': [
        f"${total_spend:,.0f}",
        f"{top_50_pct:.1f}%",
        f"{total_transactions:,.0f}",
        f"{total_accounts:,.0f}",
        f"${business_total:,.0f}",
        f"{business_df['primary_account_num'].nunique():,}"
    ]
})

print("\n")
display(summary)
print("="*100)
