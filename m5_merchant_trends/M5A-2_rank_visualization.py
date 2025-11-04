# M5A-2: MONTHLY RANK TRACKING - VISUALIZATION
print("\n" + "="*120)
print("📈 RANK MOVEMENT VISUALIZATION")
print("="*120)

# Create line chart showing rank changes for top 50 merchants
import matplotlib.pyplot as plt

# Get sorted months (should already exist from M5A-1)
sorted_months = sorted(combined_df['year_month'].unique())

# Rebuild rank_df for visualization (in case cells run separately)
monthly_rankings = {}
for month in sorted_months:
    month_data = combined_df[combined_df['year_month'] == month]
    rankings = month_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    for rank, merchant in enumerate(rankings.index, 1):
        if merchant not in monthly_rankings:
            monthly_rankings[merchant] = {}
        monthly_rankings[merchant][month] = rank

# Get top 50 merchants
top_merchants = set()
for month in sorted_months:
    month_data = combined_df[combined_df['year_month'] == month]
    top_50 = month_data.groupby('merchant_consolidated')['amount'].sum().nlargest(50)
    top_merchants.update(top_50.index)

rank_matrix = []
for merchant in top_merchants:
    row = {'merchant': merchant}
    for month in sorted_months:
        row[month] = monthly_rankings.get(merchant, {}).get(month, None)
    rank_matrix.append(row)

rank_df = pd.DataFrame(rank_matrix)
rank_df['avg_rank'] = rank_df[sorted_months].mean(axis=1, skipna=True)
rank_df = rank_df.sort_values('avg_rank').head(50)

# Create visualization
fig, ax = plt.subplots(figsize=(16, 12))

# Use a larger color palette
colors = plt.cm.tab20(range(20))
colors2 = plt.cm.tab20b(range(20))
colors3 = plt.cm.tab20c(range(10))
all_colors = list(colors) + list(colors2) + list(colors3)

for idx, (_, row) in enumerate(rank_df.iterrows()):
    merchant = row['merchant']
    ranks = [row[month] for month in sorted_months]
    
    # Convert None to NaN for plotting
    ranks = [r if r is not None else float('nan') for r in ranks]
    
    # Plot line - thinner lines for 50 merchants
    ax.plot(range(len(sorted_months)), ranks, 
            marker='o', linewidth=1.5, markersize=4,
            label=merchant[:30], color=all_colors[idx % len(all_colors)], alpha=0.7)

# Invert y-axis (rank 1 at top)
ax.invert_yaxis()
ax.set_ylabel('Rank Position', fontsize=12, fontweight='bold')
ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_title('Top 50 Merchants - Rank Movement Over Time', fontsize=14, fontweight='bold', pad=20)

# Set x-axis
ax.set_xticks(range(len(sorted_months)))
ax.set_xticklabels([str(m) for m in sorted_months], rotation=45, ha='right')

# Set y-axis to show ranks 1-50
ax.set_ylim(50, 1)
ax.set_yticks(range(1, 51, 5))

# Grid
ax.grid(True, alpha=0.3, linestyle='--')

# Legend - split into 2 columns for better readability
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=7, ncol=2)

plt.tight_layout()
plt.show()

print("\n💡 CHART INSIGHTS:")
print("-"*120)
print(f"   • All 50 top merchants displayed with rank trajectories")
print(f"   • Lower position on chart = higher rank (#1 at top)")
print(f"   • Gaps in lines indicate merchant dropped below #50 that month")
print(f"   • Multiple colors distinguish individual merchant paths")
print("="*120)
