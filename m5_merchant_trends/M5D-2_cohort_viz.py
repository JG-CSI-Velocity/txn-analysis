# M5D-2: COHORT VISUALIZATION
print("\n" + "="*120)
print("📊 MERCHANT FLOW VISUALIZATION")
print("="*120)

# Rebuild cohort_df (in case cells run separately)
sorted_months = sorted(combined_df['year_month'].unique())

merchant_activity = {}
for month in sorted_months:
    month_data = combined_df[combined_df['year_month'] == month]
    active_merchants = set(month_data['merchant_consolidated'].unique())
    
    for merchant in active_merchants:
        if merchant not in merchant_activity:
            merchant_activity[merchant] = {'first_month': month, 'last_month': month, 'months_active': []}
        merchant_activity[merchant]['last_month'] = month
        merchant_activity[merchant]['months_active'].append(month)

cohort_analysis = []
for i, month in enumerate(sorted_months):
    month_data = combined_df[combined_df['year_month'] == month]
    current_merchants = set(month_data['merchant_consolidated'].unique())
    
    new_merchants = {m for m in current_merchants if merchant_activity[m]['first_month'] == month}
    
    if i > 0:
        prev_month = sorted_months[i-1]
        prev_data = combined_df[combined_df['year_month'] == prev_month]
        prev_merchants = set(prev_data['merchant_consolidated'].unique())
        returning = {m for m in current_merchants if m not in prev_merchants and merchant_activity[m]['first_month'] != month}
        lost = prev_merchants - current_merchants
    else:
        returning = set()
        lost = set()
    
    new_spend = month_data[month_data['merchant_consolidated'].isin(new_merchants)]['amount'].sum()
    returning_spend = month_data[month_data['merchant_consolidated'].isin(returning)]['amount'].sum()
    
    cohort_analysis.append({
        'month': month,
        'total_merchants': len(current_merchants),
        'new_merchants': len(new_merchants),
        'returning_merchants': len(returning),
        'lost_merchants': len(lost),
        'new_spend': new_spend,
        'returning_spend': returning_spend,
        'total_spend': month_data['amount'].sum()
    })

cohort_df = pd.DataFrame(cohort_analysis)

# Visualization
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

months_str = [str(m) for m in cohort_df['month']]
x_pos = range(len(months_str))

# Chart 1: Merchant Flow
ax1.bar(x_pos, cohort_df['new_merchants'], label='New Merchants', color='#2ecc71', alpha=0.8)
ax1.bar(x_pos, cohort_df['returning_merchants'], bottom=cohort_df['new_merchants'], 
        label='Returning Merchants', color='#3498db', alpha=0.8)
ax1.plot(x_pos, cohort_df['lost_merchants'], label='Lost Merchants', 
         color='#e74c3c', linewidth=3, marker='o', markersize=8)

ax1.set_ylabel('Number of Merchants', fontsize=11, fontweight='bold')
ax1.set_title('Merchant Flow Analysis - New, Returning, and Lost', fontsize=13, fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(months_str, rotation=45, ha='right')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Chart 2: Spending from New Merchants
ax2.bar(x_pos, cohort_df['new_spend'], label='New Merchant Spend', color='#9b59b6', alpha=0.8)
ax2_pct = ax2.twinx()
ax2_pct.plot(x_pos, cohort_df['new_spend'] / cohort_df['total_spend'] * 100, 
             color='#e74c3c', linewidth=3, marker='s', markersize=8, label='% of Total Spend')

ax2.set_ylabel('New Merchant Spend ($)', fontsize=11, fontweight='bold')
ax2_pct.set_ylabel('% of Total Spend', fontsize=11, fontweight='bold', color='#e74c3c')
ax2.set_title('New Merchant Spending Contribution', fontsize=13, fontweight='bold', pad=15)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(months_str, rotation=45, ha='right')
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Combine legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_pct.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()

print("="*120)
