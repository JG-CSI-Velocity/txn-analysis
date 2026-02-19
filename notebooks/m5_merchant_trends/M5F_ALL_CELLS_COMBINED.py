# M5F: PERSONAL ACCOUNT MONTH-OVER-MONTH ANALYSIS
# All 3 cells combined for reference

"""
This document contains all 3 M5F cells:
- M5F-1: Personal Account Analysis (3 tables)
- M5F-2: Personal Rank Climbers Visualization
- M5F-3: Personal Rank Fallers Visualization
"""

# ============================================================================
# M5F-1: PERSONAL ACCOUNT - MONTH-OVER-MONTH ANALYSIS
# ============================================================================

# M5F-1: PERSONAL ACCOUNT - MONTH-OVER-MONTH ANALYSIS
# Focused analysis on personal merchant changes
print("\n" + "="*120)
print(" " * 35 + "M5F-1: PERSONAL ACCOUNT - MONTH-OVER-MONTH ANALYSIS")
print("="*120)

sorted_months = sorted(personal_df['year_month'].unique())

# Calculate month-over-month changes
monthly_movers = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    
    # Previous and current month rankings
    prev_data = personal_df[personal_df['year_month'] == prev_month]
    prev_rankings = prev_data.groupby('merchant_consolidated').agg({
        'amount': 'sum',
        'primary_account_num': 'nunique',
        'transaction_date': 'count'
    }).sort_values('amount', ascending=False)
    prev_rankings['rank'] = range(1, len(prev_rankings) + 1)
    
    curr_data = personal_df[personal_df['year_month'] == curr_month]
    curr_rankings = curr_data.groupby('merchant_consolidated').agg({
        'amount': 'sum',
        'primary_account_num': 'nunique',
        'transaction_date': 'count'
    }).sort_values('amount', ascending=False)
    curr_rankings['rank'] = range(1, len(curr_rankings) + 1)
    
    # Compare merchants in both months
    common = set(prev_rankings.index) & set(curr_rankings.index)
    
    for merchant in common:
        prev_rank = prev_rankings.loc[merchant, 'rank']
        curr_rank = curr_rankings.loc[merchant, 'rank']
        prev_spend = prev_rankings.loc[merchant, 'amount']
        curr_spend = curr_rankings.loc[merchant, 'amount']
        
        rank_change = prev_rank - curr_rank
        spend_change = curr_spend - prev_spend
        spend_change_pct = (spend_change / prev_spend * 100) if prev_spend > 0 else 0
        
        if prev_rank <= 100 or curr_rank <= 100:
            monthly_movers.append({
                'month_transition': f"{prev_month} → {curr_month}",
                'merchant': merchant,
                'prev_rank': prev_rank,
                'curr_rank': curr_rank,
                'rank_change': rank_change,
                'prev_spend': prev_spend,
                'curr_spend': curr_spend,
                'spend_change': spend_change,
                'spend_change_pct': spend_change_pct
            })

movers_df = pd.DataFrame(monthly_movers)

print("\n📈 TOP 50 PERSONAL RANK CLIMBERS (Biggest Improvements)")
print("="*120)

top_climbers = movers_df[movers_df['rank_change'] > 0].nlargest(50, 'rank_change').copy()
top_climbers['merchant'] = top_climbers['merchant'].str[:40]

climbers_display = top_climbers[[
    'month_transition', 'merchant', 'prev_rank', 'curr_rank', 'rank_change',
    'prev_spend', 'curr_spend', 'spend_change_pct'
]].copy()

climbers_display.columns = [
    'Period', 'Merchant', 'Prev Rank', 'Curr Rank', 'Rank +',
    'Previous $', 'Current $', 'Change %'
]

climbers_display['Previous $'] = climbers_display['Previous $'].apply(lambda x: f"${x:,.0f}")
climbers_display['Current $'] = climbers_display['Current $'].apply(lambda x: f"${x:,.0f}")
climbers_display['Change %'] = climbers_display['Change %'].apply(lambda x: f"{x:+.1f}%")
climbers_display['Rank +'] = climbers_display['Rank +'].apply(lambda x: f"↑{int(x)}")

display(climbers_display.style.hide(axis='index'))

print("\n" + "="*120)

print("\n📉 TOP 50 PERSONAL RANK FALLERS (Biggest Declines)")
print("="*120)

top_fallers = movers_df[movers_df['rank_change'] < 0].nsmallest(50, 'rank_change').copy()
top_fallers['merchant'] = top_fallers['merchant'].str[:40]

fallers_display = top_fallers[[
    'month_transition', 'merchant', 'prev_rank', 'curr_rank', 'rank_change',
    'prev_spend', 'curr_spend', 'spend_change_pct'
]].copy()

fallers_display.columns = [
    'Period', 'Merchant', 'Prev Rank', 'Curr Rank', 'Rank -',
    'Previous $', 'Current $', 'Change %'
]

fallers_display['Previous $'] = fallers_display['Previous $'].apply(lambda x: f"${x:,.0f}")
fallers_display['Current $'] = fallers_display['Current $'].apply(lambda x: f"${x:,.0f}")
fallers_display['Change %'] = fallers_display['Change %'].apply(lambda x: f"{x:+.1f}%")
fallers_display['Rank -'] = fallers_display['Rank -'].apply(lambda x: f"↓{abs(int(x))}")

display(fallers_display.style.hide(axis='index'))

print("\n💰 TOP 50 PERSONAL SPEND INCREASES")
print("="*120)

top_spend_increase = movers_df.nlargest(50, 'spend_change').copy()
top_spend_increase['merchant'] = top_spend_increase['merchant'].str[:40]

spend_inc_display = top_spend_increase[[
    'month_transition', 'merchant', 'prev_spend', 'curr_spend', 'spend_change', 'spend_change_pct'
]].copy()

spend_inc_display.columns = ['Period', 'Merchant', 'Previous $', 'Current $', 'Change $', 'Change %']

spend_inc_display['Previous $'] = spend_inc_display['Previous $'].apply(lambda x: f"${x:,.0f}")
spend_inc_display['Current $'] = spend_inc_display['Current $'].apply(lambda x: f"${x:,.0f}")
spend_inc_display['Change $'] = spend_inc_display['Change $'].apply(lambda x: f"${x:,.0f}")
spend_inc_display['Change %'] = spend_inc_display['Change %'].apply(lambda x: f"{x:+.1f}%")

display(spend_inc_display.style.hide(axis='index'))

print("\n💡 PERSONAL ACCOUNT SUMMARY:")
print("-"*120)
print(f"   • Total month-over-month comparisons: {len(movers_df):,}")
print(f"   • Merchants with rank improvements: {(movers_df['rank_change'] > 0).sum():,}")
print(f"   • Merchants with rank declines: {(movers_df['rank_change'] < 0).sum():,}")
print(f"   • Average absolute rank change: {movers_df['rank_change'].abs().mean():.1f} positions")
print(f"   • Merchants with spend increases: {(movers_df['spend_change'] > 0).sum():,} ({(movers_df['spend_change'] > 0).sum() / len(movers_df) * 100:.1f}%)")
print("="*120)


# ============================================================================
# M5F-2: PERSONAL RANK CLIMBERS VISUALIZATION
# ============================================================================

# M5F-2: PERSONAL RANK CLIMBERS VISUALIZATION
print("\n" + "="*120)
print("📈 PERSONAL RANK CLIMBERS - VISUALIZATION")
print("="*120)

import matplotlib.pyplot as plt

# Rebuild movers_df
sorted_months = sorted(personal_df['year_month'].unique())
monthly_movers = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    prev_data = personal_df[personal_df['year_month'] == prev_month]
    prev_rankings = prev_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    prev_rankings = prev_rankings.reset_index()
    prev_rankings['rank'] = range(1, len(prev_rankings) + 1)
    prev_rankings = prev_rankings.set_index('merchant_consolidated')
    
    curr_data = personal_df[personal_df['year_month'] == curr_month]
    curr_rankings = curr_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    curr_rankings = curr_rankings.reset_index()
    curr_rankings['rank'] = range(1, len(curr_rankings) + 1)
    curr_rankings = curr_rankings.set_index('merchant_consolidated')
    
    common = set(prev_rankings.index) & set(curr_rankings.index)
    
    for merchant in common:
        prev_rank = prev_rankings.loc[merchant, 'rank']
        curr_rank = curr_rankings.loc[merchant, 'rank']
        rank_change = prev_rank - curr_rank
        
        if prev_rank <= 100 or curr_rank <= 100:
            monthly_movers.append({'merchant': merchant, 'rank_change': rank_change})

movers_df = pd.DataFrame(monthly_movers)
top_climbers = movers_df[movers_df['rank_change'] > 0].nlargest(50, 'rank_change')

fig, ax = plt.subplots(figsize=(12, 10))
plot_data = top_climbers.sort_values('rank_change', ascending=True)
merchants = plot_data['merchant'].str[:35]
rank_changes = plot_data['rank_change']

bars = ax.barh(range(len(merchants)), rank_changes, color='#16a085', alpha=0.8, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(merchants)))
ax.set_yticklabels([f"#{i+1} {m}" for i, m in enumerate(merchants)], fontsize=8)
ax.set_xlabel('Rank Positions Gained', fontsize=11, fontweight='bold')
ax.set_title('Personal Accounts - Top 50 Rank Climbers', fontsize=13, fontweight='bold', pad=15)

for i, (bar, val) in enumerate(zip(bars, rank_changes)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' ↑{int(val)}', va='center', fontsize=8, fontweight='bold')

ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
print("="*120)


# ============================================================================
# M5F-3: PERSONAL RANK FALLERS VISUALIZATION
# ============================================================================

# M5F-3: PERSONAL RANK FALLERS VISUALIZATION
print("\n" + "="*120)
print("📉 PERSONAL RANK FALLERS - VISUALIZATION")
print("="*120)

import matplotlib.pyplot as plt

# Rebuild movers_df
sorted_months = sorted(personal_df['year_month'].unique())
monthly_movers = []

for i in range(1, len(sorted_months)):
    prev_month = sorted_months[i-1]
    curr_month = sorted_months[i]
    prev_data = personal_df[personal_df['year_month'] == prev_month]
    prev_rankings = prev_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    prev_rankings = prev_rankings.reset_index()
    prev_rankings['rank'] = range(1, len(prev_rankings) + 1)
    prev_rankings = prev_rankings.set_index('merchant_consolidated')
    
    curr_data = personal_df[personal_df['year_month'] == curr_month]
    curr_rankings = curr_data.groupby('merchant_consolidated')['amount'].sum().sort_values(ascending=False)
    curr_rankings = curr_rankings.reset_index()
    curr_rankings['rank'] = range(1, len(curr_rankings) + 1)
    curr_rankings = curr_rankings.set_index('merchant_consolidated')
    
    common = set(prev_rankings.index) & set(curr_rankings.index)
    
    for merchant in common:
        prev_rank = prev_rankings.loc[merchant, 'rank']
        curr_rank = curr_rankings.loc[merchant, 'rank']
        rank_change = prev_rank - curr_rank
        
        if prev_rank <= 100 or curr_rank <= 100:
            monthly_movers.append({'merchant': merchant, 'rank_change': rank_change})

movers_df = pd.DataFrame(monthly_movers)
top_fallers = movers_df[movers_df['rank_change'] < 0].nsmallest(50, 'rank_change')

fig, ax = plt.subplots(figsize=(12, 10))
plot_data = top_fallers.sort_values('rank_change', ascending=False)
merchants = plot_data['merchant'].str[:35]
rank_changes = plot_data['rank_change'].abs()

bars = ax.barh(range(len(merchants)), rank_changes, color='#c0392b', alpha=0.8, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(merchants)))
ax.set_yticklabels([f"#{i+1} {m}" for i, m in enumerate(merchants)], fontsize=8)
ax.set_xlabel('Rank Positions Lost', fontsize=11, fontweight='bold')
ax.set_title('Personal Accounts - Top 50 Rank Fallers', fontsize=13, fontweight='bold', pad=15)

for i, (bar, val) in enumerate(zip(bars, rank_changes)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' ↓{int(val)}', va='center', fontsize=8, fontweight='bold')

ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
print("="*120)
