# M5A-1: MONTHLY RANK TRACKING - ANALYSIS
# Shows how top merchants move up/down in rankings month-over-month
print("\n" + "="*120)
print(" " * 40 + "M5A-1: MONTHLY RANK TRACKING - TOP MERCHANTS")
print("="*120)

# Get monthly rankings for all merchants
sorted_months = sorted(combined_df['year_month'].unique())
monthly_rankings = {}

for month in sorted_months:
    month_data = combined_df[combined_df['year_month'] == month]
    rankings = month_data.groupby('merchant_consolidated').agg({
        'amount': 'sum'
    }).sort_values('amount', ascending=False)
    
    # Store rank for each merchant
    for rank, merchant in enumerate(rankings.index, 1):
        if merchant not in monthly_rankings:
            monthly_rankings[merchant] = {}
        monthly_rankings[merchant][month] = rank

# Get merchants that appear in top 50 at any point
top_merchants = set()
for month in sorted_months:
    month_data = combined_df[combined_df['year_month'] == month]
    top_50 = month_data.groupby('merchant_consolidated')['amount'].sum().nlargest(50)
    top_merchants.update(top_50.index)

# Create ranking matrix
rank_matrix = []
for merchant in top_merchants:
    row = {'merchant': merchant}
    for month in sorted_months:
        row[month] = monthly_rankings.get(merchant, {}).get(month, None)
    rank_matrix.append(row)

# Convert to DataFrame
rank_df = pd.DataFrame(rank_matrix)

# Calculate average rank and consistency
rank_df['avg_rank'] = rank_df[sorted_months].mean(axis=1, skipna=True)
rank_df['months_in_top_50'] = rank_df[sorted_months].apply(lambda x: (x <= 50).sum(), axis=1)

# Sort by average rank
rank_df = rank_df.sort_values('avg_rank').head(50)

print("\n📊 TOP 50 MERCHANTS BY AVERAGE RANK ACROSS ALL MONTHS")
print("="*120)

# Display table
display_df = rank_df.copy()
display_df['merchant'] = display_df['merchant'].str[:45]

# Format rank columns
for month in sorted_months:
    display_df[month] = display_df[month].apply(lambda x: f"#{int(x)}" if pd.notna(x) and x <= 50 else "-")

display_df['avg_rank'] = display_df['avg_rank'].apply(lambda x: f"#{x:.1f}")
display_df = display_df.rename(columns={
    'merchant': 'Merchant',
    'avg_rank': 'Avg Rank',
    'months_in_top_50': 'Months in Top 50'
})

# Reorder columns
cols = ['Merchant'] + [month for month in sorted_months] + ['Avg Rank', 'Months in Top 50']
display_df = display_df[cols]

display(display_df.style.hide(axis='index'))

print("\n💡 KEY INSIGHTS:")
print("-"*120)
print(f"   • Top 50 merchants tracked across {len(sorted_months)} months")
print(f"   • Table shows rank position for each merchant by month")
print(f"   • '-' indicates merchant ranked below #50 that month")
print(f"   • Avg Rank shows overall performance across all months")
print("="*120)
