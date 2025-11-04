# ===========================================================================
# M2D VISUALIZATION - Top 20 MCC Categories Comparison
# ===========================================================================
"""
## M2D: MCC Category Comparison - Top 20 by Spend
"""

fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# Get top 20 by spend
top_20_mcc = top_mcc_by_spend.head(20).iloc[::-1]

mcc_codes = [str(code) for code in top_20_mcc.index]

# Chart 1: Total Spend
ax1 = axes[0]
values1 = top_20_mcc['total_amount'].values
colors1 = plt.cm.Blues(np.linspace(0.5, 0.9, 20))

bars1 = ax1.barh(range(20), values1, color=colors1, edgecolor='black', linewidth=0.5)
ax1.set_yticks(range(20))
ax1.set_yticklabels(mcc_codes, fontsize=9)
ax1.set_xlabel('Total Spend ($)', fontsize=10, fontweight='bold')
ax1.set_title('By Total Spend', fontsize=11, fontweight='bold')
ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
ax1.grid(axis='x', linestyle='--', alpha=0.3)
ax1.set_axisbelow(True)

# Chart 2: Transaction Count
ax2 = axes[1]
values2 = top_20_mcc['transaction_count'].values
colors2 = plt.cm.Greens(np.linspace(0.5, 0.9, 20))

bars2 = ax2.barh(range(20), values2, color=colors2, edgecolor='black', linewidth=0.5)
ax2.set_yticks(range(20))
ax2.set_yticklabels([''] * 20)  # Hide y-labels for middle chart
ax2.set_xlabel('Transactions', fontsize=10, fontweight='bold')
ax2.set_title('By Transaction Count', fontsize=11, fontweight='bold')
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
ax2.grid(axis='x', linestyle='--', alpha=0.3)
ax2.set_axisbelow(True)

# Chart 3: Unique Accounts
ax3 = axes[2]
values3 = top_20_mcc['unique_accounts'].values
colors3 = plt.cm.Oranges(np.linspace(0.5, 0.9, 20))

bars3 = ax3.barh(range(20), values3, color=colors3, edgecolor='black', linewidth=0.5)
ax3.set_yticks(range(20))
ax3.set_yticklabels([''] * 20)  # Hide y-labels for right chart
ax3.set_xlabel('Unique Accounts', fontsize=10, fontweight='bold')
ax3.set_title('By Account Count', fontsize=11, fontweight='bold')
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.1f}K' if x >= 1000 else f'{x:.0f}'))
ax3.grid(axis='x', linestyle='--', alpha=0.3)
ax3.set_axisbelow(True)

# Overall title
fig.suptitle('Top 20 MCC Categories - Three Perspectives', fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout()
plt.show()
