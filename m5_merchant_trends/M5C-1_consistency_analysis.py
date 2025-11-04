# M5C-1: SPENDING CONSISTENCY ANALYSIS
# Identifies merchants with stable vs volatile spending patterns
print("\n" + "="*120)
print(" " * 40 + "M5C-1: SPENDING CONSISTENCY ANALYSIS")
print("="*120)

# Calculate monthly spending for each merchant
sorted_months = sorted(combined_df['year_month'].unique())

merchant_monthly = combined_df.groupby(['merchant_consolidated', 'year_month'])['amount'].sum().reset_index()

# Pivot to get monthly spending pattern
spending_pivot = merchant_monthly.pivot(index='merchant_consolidated', columns='year_month', values='amount').fillna(0)

# Calculate consistency metrics
consistency_data = []

for merchant in spending_pivot.index:
    monthly_values = spending_pivot.loc[merchant].values
    
    # Filter out zero months
    non_zero_values = monthly_values[monthly_values > 0]
    
    # Only analyze merchants with at least 3 months of activity
    if len(non_zero_values) >= 3:
        total_spend = non_zero_values.sum()
        mean_spend = non_zero_values.mean()
        std_spend = non_zero_values.std()
        cv = (std_spend / mean_spend * 100) if mean_spend > 0 else 0  # Coefficient of variation
        months_active = len(non_zero_values)
        
        consistency_data.append({
            'merchant': merchant,
            'total_spend': total_spend,
            'mean_monthly': mean_spend,
            'std_dev': std_spend,
            'coefficient_variation': cv,
            'months_active': months_active,
            'consistency_score': 100 - min(cv, 100)  # Inverse of CV (higher = more consistent)
        })

consistency_df = pd.DataFrame(consistency_data)

# Filter for significant merchants (at least $10,000 total spend)
consistency_df = consistency_df[consistency_df['total_spend'] >= 10000].copy()

print("\n📊 TOP 50 MOST CONSISTENT MERCHANTS (Low Variation)")
print("="*120)
print("Lower Coefficient of Variation = More Predictable Spending Pattern")
print("-"*120)

most_consistent = consistency_df.nlargest(50, 'consistency_score').copy()
most_consistent['merchant'] = most_consistent['merchant'].str[:40]

consistent_display = most_consistent[[
    'merchant', 'total_spend', 'mean_monthly', 'std_dev', 'coefficient_variation', 'months_active'
]].copy()

consistent_display.columns = ['Merchant', 'Total Spend', 'Avg Monthly', 'Std Dev', 'CV (%)', 'Months Active']

# Format numbers
consistent_display['Total Spend'] = consistent_display['Total Spend'].apply(lambda x: f"${x:,.0f}")
consistent_display['Avg Monthly'] = consistent_display['Avg Monthly'].apply(lambda x: f"${x:,.0f}")
consistent_display['Std Dev'] = consistent_display['Std Dev'].apply(lambda x: f"${x:,.0f}")
consistent_display['CV (%)'] = consistent_display['CV (%)'].apply(lambda x: f"{x:.1f}%")

display(consistent_display.style.hide(axis='index'))

print("\n" + "="*120)

print("\n📊 TOP 50 MOST VOLATILE MERCHANTS (High Variation)")
print("="*120)
print("Higher Coefficient of Variation = More Unpredictable Spending Pattern")
print("-"*120)

most_volatile = consistency_df.nsmallest(50, 'consistency_score').copy()
most_volatile['merchant'] = most_volatile['merchant'].str[:40]

volatile_display = most_volatile[[
    'merchant', 'total_spend', 'mean_monthly', 'std_dev', 'coefficient_variation', 'months_active'
]].copy()

volatile_display.columns = ['Merchant', 'Total Spend', 'Avg Monthly', 'Std Dev', 'CV (%)', 'Months Active']

# Format numbers
volatile_display['Total Spend'] = volatile_display['Total Spend'].apply(lambda x: f"${x:,.0f}")
volatile_display['Avg Monthly'] = volatile_display['Avg Monthly'].apply(lambda x: f"${x:,.0f}")
volatile_display['Std Dev'] = volatile_display['Std Dev'].apply(lambda x: f"${x:,.0f}")
volatile_display['CV (%)'] = volatile_display['CV (%)'].apply(lambda x: f"{x:.1f}%")

display(volatile_display.style.hide(axis='index'))

print("\n💡 CONSISTENCY METRICS EXPLAINED:")
print("-"*120)
print("   • Coefficient of Variation (CV) = Standard Deviation / Mean × 100")
print("   • CV < 50%: Consistent spending pattern")
print("   • CV 50-100%: Moderate variation")
print("   • CV > 100%: High volatility (spiky spending)")
print("\n📈 SUMMARY STATISTICS:")
print("-"*120)
print(f"   • Total merchants analyzed: {len(consistency_df):,}")
print(f"   • Average CV: {consistency_df['coefficient_variation'].mean():.1f}%")
print(f"   • Median CV: {consistency_df['coefficient_variation'].median():.1f}%")
print(f"   • Consistent merchants (CV < 50%): {(consistency_df['coefficient_variation'] < 50).sum():,} ({(consistency_df['coefficient_variation'] < 50).sum() / len(consistency_df) * 100:.1f}%)")
print(f"   • Volatile merchants (CV > 100%): {(consistency_df['coefficient_variation'] > 100).sum():,} ({(consistency_df['coefficient_variation'] > 100).sum() / len(consistency_df) * 100:.1f}%)")
print("="*120)
