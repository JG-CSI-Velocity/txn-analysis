# ===========================================================================
# M6B-6: COMPETITIVE THREAT ASSESSMENT (IMPROVED)
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6B-6: COMPETITIVE THREAT ASSESSMENT")
print("="*120)

if len(all_competitor_data) > 0:
    threat_data = []
    
    # Get total accounts for penetration calculation
    total_accounts = combined_df['primary_account_num'].nunique()
    
    for competitor, competitor_trans in all_competitor_data.items():
        category = competitor_trans['competitor_category'].iloc[0]
        total_spend = competitor_trans['amount'].sum()
        unique_accounts = competitor_trans['primary_account_num'].nunique()
        
        # Account penetration (% of total accounts using this competitor)
        penetration_pct = (unique_accounts / total_accounts) * 100
        
        # Calculate recent growth (last 3 months vs previous 3 months)
        sorted_months = sorted(competitor_trans['year_month'].unique())
        if len(sorted_months) >= 6:
            recent_3 = sorted_months[-3:]
            previous_3 = sorted_months[-6:-3]
            
            recent_spend = competitor_trans[competitor_trans['year_month'].isin(recent_3)]['amount'].sum()
            previous_spend = competitor_trans[competitor_trans['year_month'].isin(previous_3)]['amount'].sum()
            
            growth_rate = ((recent_spend - previous_spend) / previous_spend * 100) if previous_spend > 0 else 0
        else:
            growth_rate = 0
        
        # Threat Score = Weighted combination
        # 40% = Account penetration (how many accounts they've captured)
        # 30% = Total spend (how much money is at risk)
        # 30% = Growth rate (are they gaining momentum?)
        
        threat_score = (
            (penetration_pct * 4) +  # Weight: 40% (multiply by 4 to normalize)
            (total_spend / 100000) * 3 +  # Weight: 30% (normalize to reasonable scale)
            (max(growth_rate, 0) / 10) * 3  # Weight: 30% (only positive growth matters)
        )
        
        threat_data.append({
            'competitor': competitor,
            'category': category,
            'total_spend': total_spend,
            'unique_accounts': unique_accounts,
            'penetration_pct': penetration_pct,
            'growth_rate': growth_rate,
            'threat_score': threat_score
        })
    
    threat_df = pd.DataFrame(threat_data).sort_values('threat_score', ascending=False).head(10)
    
    # Format for display
    display_df = threat_df.copy()
    display_df['category'] = display_df['category'].str.replace('_', ' ').str.title()
    display_df['total_spend'] = display_df['total_spend'].apply(lambda x: f"${x:,.0f}")
    display_df['unique_accounts'] = display_df['unique_accounts'].apply(lambda x: f"{x:,}")
    display_df['penetration_pct'] = display_df['penetration_pct'].apply(lambda x: f"{x:.2f}%")
    display_df['growth_rate'] = display_df['growth_rate'].apply(lambda x: f"{x:+.1f}%")
    display_df['threat_score'] = display_df['threat_score'].apply(lambda x: f"{x:.1f}")
    
    display_df.columns = [
        'Competitor', 'Category', 'Total Spend', 'Accounts', 
        'Penetration', 'Growth (6mo)', 'Threat Score'
    ]
    
    print("\nTop 10 Competitive Threats:")
    print("Threat Score = 40% Penetration + 30% Total Spend + 30% Growth Rate\n")
    display(display_df.style.hide(axis='index'))
    
    print("\n💡 Highest threat = High account penetration + Large spend + Growing momentum")

print("="*120)
