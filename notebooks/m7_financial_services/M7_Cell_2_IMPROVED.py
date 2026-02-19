# ===========================================================================
# CELL 2: IDENTIFY FINANCIAL SERVICES TRANSACTIONS (IMPROVED)
# ===========================================================================
"""
## Financial Services Opportunity - Find Transactions
Uses consolidated merchant names for cleaner results
"""

financial_services_data = {}

print("Scanning for financial services transactions...\n")

for category, patterns in FINANCIAL_SERVICES_PATTERNS.items():
    print(f"{'='*100}")
    print(f"Category: {category}")
    print(f"{'='*100}")
    
    # Create mask for any pattern in this category
    # Use merchant_consolidated if available, otherwise merchant_name
    search_column = 'merchant_consolidated' if 'merchant_consolidated' in combined_df.columns else 'merchant_name'
    
    category_mask = combined_df[search_column].str.contains(
        '|'.join(patterns), 
        case=False, 
        na=False,
        regex=True
    )
    
    category_trans = combined_df[category_mask].copy()
    
    if len(category_trans) == 0:
        print(f"  No transactions found\n")
        continue
    
    # CLEAN UP MERCHANT NAMES (remove payment processor prefixes)
    if search_column in category_trans.columns:
        category_trans[search_column] = category_trans[search_column].str.replace(r'^PNM\*', '', regex=True)
        category_trans[search_column] = category_trans[search_column].str.replace(r'^ACI\*', '', regex=True)
        category_trans[search_column] = category_trans[search_column].str.replace(r'^ACH\*', '', regex=True)
        category_trans[search_column] = category_trans[search_column].str.upper()
        category_trans[search_column] = category_trans[search_column].str.strip()
    
    # FILTER OUT FALSE POSITIVES
    # Remove common false matches
    false_positive_patterns = [
        'TOWING',
        'TOW SERVICE',
        'BODY SHOP',
        'AUTO REPAIR',
        'AUTO PARTS',
        'AUTOZONE',
        'AUTO TRADER',
        'TRADER JOE',
        "TRADER JOE'S"
    ]
    
    for false_pattern in false_positive_patterns:
        false_mask = category_trans[search_column].str.contains(false_pattern, case=False, na=False)
        if false_mask.any():
            removed_count = false_mask.sum()
            category_trans = category_trans[~false_mask]
            print(f"  Filtered out {removed_count} '{false_pattern}' transactions (false positive)")
    
    if len(category_trans) == 0:
        print(f"  No valid transactions after filtering\n")
        continue
    
    # Show merchant variations found (using consolidated names)
    merchant_summary = category_trans.groupby(search_column).agg({
        'amount': ['sum', 'count'],
        'primary_account_num': 'nunique'
    }).round(2)
    
    merchant_summary.columns = ['Total Spend', 'Transactions', 'Unique Accounts']
    merchant_summary = merchant_summary.sort_values('Total Spend', ascending=False)
    
    print(f"\nMerchants Found: {len(merchant_summary)}")
    print(f"Total Transactions: {len(category_trans):,}")
    print(f"Unique Accounts: {category_trans['primary_account_num'].nunique():,}")
    print(f"Total Spend: ${category_trans['amount'].sum():,.2f}\n")
    
    # Display top merchants in this category
    display_merchants = merchant_summary.head(15).reset_index()
    display_merchants.columns = ['Merchant', 'Total Spend', 'Transactions', 'Unique Accounts']
    
    # Format after renaming columns
    display_merchants['Total Spend'] = display_merchants['Total Spend'].apply(lambda x: f"${x:,.2f}")
    display_merchants['Transactions'] = display_merchants['Transactions'].apply(lambda x: f"{int(x):,}")
    display_merchants['Unique Accounts'] = display_merchants['Unique Accounts'].apply(lambda x: f"{int(x):,}")
    
    # Display without hiding index (plain display)
    print(display_merchants.to_string(index=False))
    print()
    
    # Store for analysis
    financial_services_data[category] = {
        'transactions': category_trans,
        'merchant_summary': merchant_summary
    }
    
    print()

print("="*100)
print("✓ Financial services scan complete")
print("="*100)

# Summary across all categories
print("\n📊 SUMMARY ACROSS ALL CATEGORIES:")
print("-"*100)

total_summary = []
for category, data in financial_services_data.items():
    total_summary.append({
        'Category': category,
        'Unique Accounts': data['transactions']['primary_account_num'].nunique(),
        'Total Transactions': len(data['transactions']),
        'Total Spend': data['transactions']['amount'].sum(),
        'Unique Merchants': len(data['merchant_summary'])
    })

if len(total_summary) > 0:
    summary_df = pd.DataFrame(total_summary)
    summary_df = summary_df.sort_values('Total Spend', ascending=False)
    
    display_summary = summary_df.copy()
    display_summary['Unique Accounts'] = display_summary['Unique Accounts'].apply(lambda x: f"{x:,}")
    display_summary['Total Transactions'] = display_summary['Total Transactions'].apply(lambda x: f"{x:,}")
    display_summary['Total Spend'] = display_summary['Total Spend'].apply(lambda x: f"${x:,.0f}")
    display_summary['Unique Merchants'] = display_summary['Unique Merchants'].apply(lambda x: f"{x:,}")
    
    print(display_summary.to_string(index=False))
    print()
    
    print(f"\n💰 Grand Total Spend: ${summary_df['Total Spend'].sum():,.2f}")
    print(f"👥 Total Unique Accounts: {summary_df['Unique Accounts'].sum():,}")
    print(f"📝 Total Transactions: {summary_df['Total Transactions'].sum():,}")
