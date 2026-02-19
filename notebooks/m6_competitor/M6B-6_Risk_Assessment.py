# ===========================================================================
# M6B-6: COMPETITIVE RISK ASSESSMENT
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6: COMPETITIVE RISK ASSESSMENT")
print("="*120)

if len(all_competitor_data) > 0:
    # Identify high-risk competitors (high spend + growing)
    risk_data = []
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        total_spend = competitor_trans['amount'].sum()
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        
        # Calculate recent activity (last 90 days)
        recent_cutoff = pd.Timestamp.now() - pd.Timedelta(days=90)
        recent_trans = competitor_trans[competitor_trans['transaction_date'] >= recent_cutoff]
        recent_spend = recent_trans['amount'].sum()
        recent_accounts = recent_trans['primary_account_num'].nunique()
        
        # Risk score (higher = more concerning)
        risk_score = (
            (total_spend / 10000) * 0.4 +  # Total spend weight
            (unique_accounts * 10) * 0.3 +  # Account penetration weight
            (recent_spend / 5000) * 0.3     # Recent activity weight
        )
        
        risk_data.append({
            'competitor': competitor,
            'category': category,
            'total_spend': total_spend,
            'unique_accounts': unique_accounts,
            'recent_spend': recent_spend,
            'recent_accounts': recent_accounts,
            'risk_score': risk_score
        })
    
    risk_df = pd.DataFrame(risk_data).sort_values('risk_score', ascending=False).head(10)
    
    risk_display = risk_df.copy()
    risk_display['category'] = risk_display['category'].str.replace('_', ' ').str.title()
    risk_display['total_spend'] = risk_display['total_spend'].apply(lambda x: f"${x:,.0f}")
    risk_display['unique_accounts'] = risk_display['unique_accounts'].apply(lambda x: f"{x:,}")
    risk_display['recent_spend'] = risk_display['recent_spend'].apply(lambda x: f"${x:,.0f}")
    risk_display['recent_accounts'] = risk_display['recent_accounts'].apply(lambda x: f"{x:,}")
    risk_display['risk_score'] = risk_display['risk_score'].apply(lambda x: f"{x:.1f}")
    
    risk_display.columns = [
        'Competitor', 'Category', 'Total Spend', 'Total Accounts', 
        'Recent Spend (90d)', 'Recent Accounts (90d)', 'Risk Score'
    ]
    
    print("\nTop 10 Competitive Threats (by Risk Score):\n")
    display(risk_display.style.hide(axis='index'))

print("="*120)
