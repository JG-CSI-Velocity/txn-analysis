# M5D-1: NEW VS DECLINING MERCHANTS - ANALYSIS
# Tracks merchant lifecycle - new entrants, established, and declining merchants
print("\n" + "="*120)
print(" " * 40 + "M5D-1: NEW VS DECLINING MERCHANTS - ANALYSIS")
print("="*120)

sorted_months = sorted(combined_df['year_month'].unique())

# Track merchant activity by month
merchant_activity = {}

for month in sorted_months:
    month_data = combined_df[combined_df['year_month'] == month]
    active_merchants = set(month_data['merchant_consolidated'].unique())
    
    for merchant in active_merchants:
        if merchant not in merchant_activity:
            merchant_activity[merchant] = {
                'first_month': month,
                'last_month': month,
                'months_active': []
            }
        merchant_activity[merchant]['last_month'] = month
        merchant_activity[merchant]['months_active'].append(month)

# Analyze each month's cohorts
cohort_analysis = []

for i, month in enumerate(sorted_months):
    month_data = combined_df[combined_df['year_month'] == month]
    current_merchants = set(month_data['merchant_consolidated'].unique())
    
    # New merchants (first appearance this month)
    new_merchants = {m for m in current_merchants if merchant_activity[m]['first_month'] == month}
    
    # Returning merchants (active before, not in previous month, but back now)
    if i > 0:
        prev_month = sorted_months[i-1]
        prev_data = combined_df[combined_df['year_month'] == prev_month]
        prev_merchants = set(prev_data['merchant_consolidated'].unique())
        
        returning = {m for m in current_merchants 
                    if m not in prev_merchants and merchant_activity[m]['first_month'] != month}
        
        # Lost merchants (in previous month, not in current)
        lost = prev_merchants - current_merchants
    else:
        returning = set()
        lost = set()
    
    # Calculate spending
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

print("\n📊 MONTHLY COHORT ANALYSIS")
print("="*120)

display_cohort = cohort_df.copy()
display_cohort['month'] = display_cohort['month'].astype(str)
display_cohort['new_pct'] = (display_cohort['new_merchants'] / display_cohort['total_merchants'] * 100)
display_cohort['returning_pct'] = (display_cohort['returning_merchants'] / display_cohort['total_merchants'] * 100)
display_cohort['new_spend_pct'] = (display_cohort['new_spend'] / display_cohort['total_spend'] * 100)

display_cols = display_cohort[[
    'month', 'total_merchants', 'new_merchants', 'new_pct', 
    'returning_merchants', 'returning_pct', 'lost_merchants',
    'new_spend', 'new_spend_pct'
]].copy()

display_cols.columns = [
    'Month', 'Total Merchants', 'New', 'New %', 
    'Returning', 'Return %', 'Lost',
    'New Merchant $', 'New $ %'
]

# Format
display_cols['New %'] = display_cols['New %'].apply(lambda x: f"{x:.1f}%")
display_cols['Return %'] = display_cols['Return %'].apply(lambda x: f"{x:.1f}%")
display_cols['New Merchant $'] = display_cols['New Merchant $'].apply(lambda x: f"${x:,.0f}")
display_cols['New $ %'] = display_cols['New $ %'].apply(lambda x: f"{x:.1f}%")

display(display_cols.style.hide(axis='index'))

print("\n" + "="*120)

# Top New Merchants by First Month
print("\n🆕 TOP NEW MERCHANTS BY COHORT (First Appearance)")
print("="*120)

new_merchant_data = []

for merchant, data in merchant_activity.items():
    first_month = data['first_month']
    
    # Get total spend for this merchant
    merchant_df = combined_df[combined_df['merchant_consolidated'] == merchant]
    total_spend = merchant_df['amount'].sum()
    months_active = len(data['months_active'])
    
    new_merchant_data.append({
        'merchant': merchant,
        'first_month': first_month,
        'total_spend': total_spend,
        'months_active': months_active,
        'avg_monthly': total_spend / months_active
    })

new_merchant_df = pd.DataFrame(new_merchant_data)

# Show top 5 new merchants from each of the last 3 months
recent_months = sorted_months[-3:]

for month in recent_months:
    month_new = new_merchant_df[new_merchant_df['first_month'] == month].nlargest(5, 'total_spend')
    
    if len(month_new) > 0:
        print(f"\n{str(month)} Cohort - Top 5 New Merchants:")
        print("-"*120)
        
        display_new = month_new[['merchant', 'total_spend', 'months_active', 'avg_monthly']].copy()
        display_new['merchant'] = display_new['merchant'].str[:45]
        display_new.columns = ['Merchant', 'Total Spend', 'Months Active', 'Avg Monthly']
        
        display_new['Total Spend'] = display_new['Total Spend'].apply(lambda x: f"${x:,.0f}")
        display_new['Avg Monthly'] = display_new['Avg Monthly'].apply(lambda x: f"${x:,.0f}")
        
        display(display_new.style.hide(axis='index'))

print("\n💡 SUMMARY STATISTICS:")
print("-"*120)
print(f"   • Total unique merchants across all months: {len(merchant_activity):,}")
print(f"   • Average new merchants per month: {cohort_df['new_merchants'].mean():.0f}")
print(f"   • Average returning merchants per month: {cohort_df['returning_merchants'].mean():.0f}")
print(f"   • Average lost merchants per month: {cohort_df['lost_merchants'].mean():.0f}")
print(f"   • Average new merchant contribution: {(cohort_df['new_spend'] / cohort_df['total_spend'] * 100).mean():.1f}% of monthly spend")
print("="*120)
