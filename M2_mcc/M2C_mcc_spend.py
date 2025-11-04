# ===========================================================================
# M2C - TOP 50 MERCHANT CATEGORIES (MCC) BY TOTAL SPEND
# ===========================================================================
"""
## M2C: Top 50 Merchant Categories by Total Spend
"""

top_mcc_by_spend = combined_df.groupby('mcc_code').agg({
    'amount': ['sum', 'count', 'mean'],
    'primary_account_num': 'nunique',
    'merchant_name': 'nunique'
}).round(2)

top_mcc_by_spend.columns = ['total_amount', 'transaction_count', 'avg_transaction', 'unique_accounts', 'num_merchants']
top_mcc_by_spend = top_mcc_by_spend.sort_values('total_amount', ascending=False).head(50)

# Format for display
display_df = top_mcc_by_spend.reset_index()
display_df = display_df.rename(columns={
    'mcc_code': 'MCC Code',
    'total_amount': 'Total Spend',
    'unique_accounts': 'Unique Accounts',
    'transaction_count': 'Transactions',
    'num_merchants': 'Merchants',
    'avg_transaction': 'Avg Transaction'
})

# Format columns
display_df['Total Spend'] = display_df['Total Spend'].apply(lambda x: f"${x:,.0f}")
display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")

print("\n" + "="*110)
print(" " * 35 + "TOP 50 MERCHANT CATEGORIES BY TOTAL SPEND")
print("="*110)

display(display_df)

# Summary stats
total_spend = top_mcc_by_spend['total_amount'].sum()
total_transactions = top_mcc_by_spend['transaction_count'].sum()
total_accounts = top_mcc_by_spend['unique_accounts'].sum()

summary = pd.DataFrame({
    'Metric': [
        'Total Spend (Top 50)', 
        'Total Transactions (Top 50)', 
        'Total Unique Accounts (Top 50)'
    ],
    'Value': [
        f"${total_spend:,.0f}",
        f"{total_transactions:,.0f}", 
        f"{total_accounts:,.0f}"
    ]
})

print("\n")
display(summary)
print("="*110)
