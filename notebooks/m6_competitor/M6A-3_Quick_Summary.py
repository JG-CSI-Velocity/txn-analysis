# ===========================================================================
# M6A-3: QUICK SUMMARY
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6A-3: COMPETITOR DETECTION SUMMARY")
print("="*120)

if len(all_competitor_data) == 0:
    print("\n⚠ No competitor transactions found")
else:
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('total_amount', ascending=False)
    
    total_competitor_trans = summary_df['total_transactions'].sum()
    total_competitor_spend = summary_df['total_amount'].sum()
    total_competitor_accounts = summary_df['unique_accounts'].sum()
    
    print(f"\n✓ Found {len(all_competitor_data)} competitors with activity")
    print(f"  • Total Transactions: {total_competitor_trans:,}")
    print(f"  • Total Spend: ${total_competitor_spend:,.2f}")
    print(f"  • Unique Accounts: {total_competitor_accounts:,}")
    
    # Quick category breakdown
    print("\n📊 By Category:")
    category_summary = summary_df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
    for cat, amount in category_summary.items():
        print(f"  • {cat.replace('_', ' ').title()}: ${amount:,.0f}")

print("\n" + "="*120)
print("✓ Detection complete - data in 'all_competitor_data' and 'summary_data'")
print("="*120)
