# ===========================================================================
# BRIDGE: Build all_competitor_data from tagged DataFrame
# ===========================================================================
# Run this cell AFTER:
#   %run 09_competition_merged.py
#   combined_df = tag_competitors(combined_df, merchant_col='merchant_consolidated')
#
# This reconstructs the all_competitor_data dict that every downstream
# cell (M6A-3 through M6B) expects.
# ===========================================================================

competitor_txns = combined_df[combined_df['competitor_category'].notna()].copy()

merch_col = 'merchant_consolidated'

# Build the dict every downstream cell expects
all_competitor_data = {}
for merchant, group in competitor_txns.groupby(merch_col):
    all_competitor_data[merchant] = group

# Also build summary_data (used by M6A-3 and overall summary cells)
summary_data = (
    competitor_txns.groupby(['competitor_category', 'competitor_match'])
    .agg(
        total_transactions=('amount', 'count'),
        unique_accounts=('primary_account_num', 'nunique'),
        total_amount=('amount', 'sum'),
    )
    .reset_index()
    .rename(columns={
        'competitor_category': 'category',
        'competitor_match': 'competitor',
    })
    .sort_values('total_amount', ascending=False)
)

# Build all_competitors (flat dict for audit function)
all_competitors = {}
for cat, rules in COMPETITOR_MERCHANTS.items():
    patterns = []
    patterns.extend(rules.get('exact', []))
    patterns.extend(rules.get('starts_with', []))
    patterns.extend(rules.get('contains', []))
    all_competitors[cat] = patterns

# Also tag business/personal if they exist
if 'business_df' in dir() and len(business_df) > 0:
    business_df = tag_competitors(business_df, merchant_col='merchant_consolidated')
if 'personal_df' in dir() and len(personal_df) > 0:
    personal_df = tag_competitors(personal_df, merchant_col='merchant_consolidated')

print(f"Competitor transactions: {len(competitor_txns):,}")
print(f"Unique competitors:     {len(all_competitor_data)}")
print(f"Categories with hits:   {competitor_txns['competitor_category'].nunique()}")
