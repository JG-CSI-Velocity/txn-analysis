# ===========================================================================
# M6A-1: COMPETITOR CONFIGURATION
# ===========================================================================

print("\n" + "="*120)
print(" " * 40 + "M6A: COMPETITOR CONFIGURATION")
print("="*120)

COMPETITOR_MERCHANTS = {
    'big_nationals': [
        'JPMORGAN', 'CHASE', 'BANK OF AMERICA', 'WELLS FARGO', 'U.S. BANK',
        'US BANK', 'PNC BANK', 'PNC', 'CITIBANK', 'CITI CARD', 'CAPITAL ONE',
    ],
    
    'regionals': [
        'BMO', 'BMO HARRIS', 'FIFTH THIRD', '5/3 BANK', 'HUNTINGTON',
        'OLD NATIONAL', 'FIRST MIDWEST', 'WINTRUST', 'TOWN BANK',
        'NORTH SHORE BANK', 'LAKE FOREST BANK', 'BYLINE BANK',
        'FIRST AMERICAN BANK', 'ASSOCIATED BANK', 'CIBC BANK',
        'MARQUETTE BANK', 'REPUBLIC BANK', 'FIRST MERCHANTS',
        'PEOPLES BANK', 'PROVIDENCE BANK',
    ],
    
    'credit_unions': [
        'ALLIANT CREDIT UNION', 'ALLIANT CU', 'CONSUMERS CREDIT UNION',
        'BAXTER CREDIT UNION', 'BCU', 'CREDIT UNION 1', 'CU1',
        'CORPORATE AMERICA FAMILY', 'CAFCU', 'FIRST NORTHERN CREDIT UNION',
        'ABRI CREDIT UNION', 'NUMARK CREDIT UNION', 'EARTHMOVER CREDIT UNION',
        'CHICAGO PATROLMEN', 'NORTHSTAR CREDIT UNION', 'UNITED CREDIT UNION',
        'SELFRELIANCE', 'CHICAGO MUNICIPAL EMPLOYEES',
    ],
    
    'digital_banks': [
        'ALLY BANK', 'DISCOVER BANK', 'CAPITAL ONE 360', 'SOFI BANK', 'SOFI',
        'CHIME', 'THE BANCORP', 'STRIDE BANK', 'VARO BANK', 'VARO', 'CURRENT',
        'GO2BANK', 'GREEN DOT', 'REVOLUT', 'MARCUS', 'GOLDMAN SACHS',
        'SCHWAB BANK', 'CHARLES SCHWAB', 'FIDELITY CASH', 'ROBINHOOD',
        'BETTERMENT', 'WEALTHFRONT',
    ],
    
    'wallets_p2p': [
        'PAYPAL', 'VENMO', 'CASH APP', 'SQ*', 'SUTTON', 'LINCOLN SAVINGS',
        'APPLE CASH', 'APPLE CARD', 'GOOGLE PAY',
    ],
    
    'bnpl': [
        'KLARNA', 'AFTERPAY', 'AFFIRM', 'ZIP', 'QUADPAY', 'SEZZLE',
    ]
}

total_competitors = sum(len(v) for v in COMPETITOR_MERCHANTS.values())
print(f"\n✓ Configured {len(COMPETITOR_MERCHANTS)} categories with {total_competitors} total competitors")
print("="*120)
