# ===========================================================================
# M6A-2: COMPETITOR DETECTION
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6A-2: SEARCHING FOR COMPETITORS")
print("="*120)

all_competitor_data = {}
summary_data = []

# Flatten competitors
all_competitors = []
for category, merchants in COMPETITOR_MERCHANTS.items():
    for merchant in merchants:
        all_competitors.append((merchant, category))

print(f"Searching {len(combined_df):,} transactions for {len(all_competitors)} competitor patterns...")

# Search for each competitor
for competitor, category in all_competitors:
    competitor_mask = combined_df['merchant_name'].str.contains(
        competitor, 
        case=False, 
        na=False,
        regex=False
    )
    
    competitor_trans = combined_df[competitor_mask].copy()
    
    if len(competitor_trans) == 0:
        continue
    
    competitor_trans['competitor_category'] = category
    all_competitor_data[competitor] = competitor_trans
    
    summary_data.append({
        'competitor': competitor,
        'category': category,
        'total_transactions': len(competitor_trans),
        'unique_accounts': competitor_trans['primary_account_num'].nunique(),
        'total_amount': competitor_trans['amount'].sum()
    })

print(f"\n✓ Found {len(all_competitor_data)} competitors with transaction activity")
print("="*120)
