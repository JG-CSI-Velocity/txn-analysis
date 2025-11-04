# M5E-4: BUSINESS SPEND INCREASES VISUALIZATION
print("\n" + "="*120)
print("💰 BUSINESS SPEND INCREASES - VISUALIZATION")
print("="*120)

import matplotlib.pyplot as plt

# Rebuild movers_df with spend data
sorted_months = sorted(business_df['year_month'].unique())
monthly_movers = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    
    prev_data = business_df[business_df['year_month'] == prev_month]
    prev_rankings = prev_data.groupby('merchant_consolidated').agg({
        'amount': 'sum'
    })
    prev_rankings.columns = ['prev_spend']
    prev_rankings = prev_rankings.sort_values('prev_spend', ascending=False)
    prev_rankings['rank'] = range(1, len(prev_rankings) + 1)
    
    curr_data = business_df[business_df['year_month'] == curr_month]
    curr_rankings = curr_data.groupby('merchant_consolidated').agg({
        'amount': 'sum'
    })
    curr_rankings.columns = ['curr_spend']
    curr_rankings = curr_rankings.sort_values('curr_spend', ascending=False)
    curr_rankings['rank'] = range(1, len(curr_rankings) + 1)
    
    common = set(prev_rankings.index) & set(curr_rankings.index)
    
    for merchant in common:
        prev_rank = prev_rankings.loc[merchant, 'rank']
        curr_rank = curr_rankings.loc[merchant, 'rank']
        prev_spend = prev_rankings.loc[merchant, 'prev_spend']
        curr_spend = curr_rankings.loc[merchant, 'curr_spend']
        spend_change = curr_spend - prev_spend
        
        if prev_rank <= 100 or curr_rank <= 100:
            monthly_movers.append({
                'merchant': merchant,
                'spend_change': spend_change
            })

movers_df = pd.DataFrame(monthly_movers)
top_spend = movers_df.nlargest(50, 'spend_change')

fig, ax = plt.subplots(figsize=(12, 10))
plot_data = top_spend.sort_values('spend_change', ascending=True)
merchants = plot_data['merchant'].str[:35]
spend_changes = plot_data['spend_change']

bars = ax.barh(range(len(merchants)), spend_changes, color='#8e44ad', alpha=0.8, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(merchants)))
ax.set_yticklabels([f"#{i+1} {m}" for i, m in enumerate(merchants)], fontsize=8)
ax.set_xlabel('Spend Increase ($)', fontsize=11, fontweight='bold')
ax.set_title('Business Accounts - Top 50 Spend Increases', fontsize=13, fontweight='bold', pad=15)

for i, (bar, val) in enumerate(zip(bars, spend_changes)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' ${val:,.0f}', va='center', fontsize=7, fontweight='bold')

ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
print("="*120)
