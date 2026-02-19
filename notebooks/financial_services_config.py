# ===========================================================================
# M7 CELL 1: CONFIGURATION - Financial Services Patterns
# ===========================================================================
"""
## Financial Services Opportunity - Configuration
"""

# Define financial services categories and merchant patterns
FINANCIAL_SERVICES_PATTERNS = {
    'Auto Loans': [
        'TOYOTA MOTOR CREDIT',
        'TOYOTA FINANCIAL',
        'VW CREDIT',
        'VOLKSWAGEN CREDIT',
        'FORD MOTOR CREDIT',
        'FORD CREDIT',
        'GM FINANCIAL',
        'HONDA FINANCE',
        'HONDA FINANCIAL',
        'NISSAN MOTOR ACCEPTANCE',
        'NISSAN FINANCIAL',
        'ALLY AUTO',
        'CAPITAL ONE AUTO',
        'CHASE AUTO FINANCE',
        'SANTANDER CONSUMER',
        'HYUNDAI MOTOR FINANCE',
        'KIA MOTORS FINANCE',
        'SUBARU MOTOR FINANCE',
        'MAZDA FINANCIAL',
        'BMW FINANCIAL',
        'MERCEDES-BENZ FINANCIAL',
        'TESLA FINANCE'
    ],
    
    'Investment/Brokerage': [
        'MORGAN STANLEY CLIENT',
        'MORGAN STANLEY BROKERAGE',
        'RAYMOND JAMES ASSOC',
        'RAYMOND JAMES & ASSOC',
        'CHARLES SCHWAB',
        'SCHWAB BROKERAGE',
        'FIDELITY INVESTMENTS',
        'FIDELITY BROKERAGE',
        'VANGUARD BROKERAGE',
        'VANGUARD GROUP',
        'E\*TRADE',
        'ETRADE',
        'TD AMERITRADE',
        'MERRILL LYNCH',
        'MERRILL EDGE',
        'RBC CAPITAL MARKETS',
        'LPL FINANCIAL',
        'BETTERMENT LLC',
        'WEALTHFRONT BROKERAGE',
        'ROBINHOOD SECURITIES',
        'WEBULL CORPORATION',
        'INTERACTIVE BROKERS',
        'TASTYTRADE'
    ],
    
    'Treasury/Bonds': [
        'TREASURY DIRECT',
        'TREASURYDIRECT',
        'US TREASURY'
    ],
    
    'Mortgage/HELOC': [
        'ROCKET MORTGAGE',
        'QUICKEN LOANS',
        'PENNYMAC LOAN',
        'PENNYMAC CORP',
        'FREEDOM MORTGAGE',
        'MR COOPER MORTGAGE',
        'CALIBER HOME LOANS',
        'OCWEN LOAN',
        'NEWREZ LLC',
        'FLAGSTAR BANK MORTGAGE',
        'LAKEVIEW LOAN',
        'CARRINGTON MORTGAGE',
        'GUILD MORTGAGE',
        'UNITED WHOLESALE MORTGAGE'
    ],
    
    'Personal Loans': [
        'SOFI LENDING',
        'SOFI LOAN',
        'LENDING CLUB CORP',
        'PROSPER FUNDING',
        'UPSTART NETWORK',
        'MARCUS BY GOLDMAN',
        'MARCUS PERSONAL',
        'DISCOVER PERSONAL LOANS',
        'LIGHTSTREAM',
        'PAYOFF INC',
        'BEST EGG'
    ],
    
    'Credit Cards': [
        'AMEX EPAYMENT',
        'AMERICAN EXPRESS PAYMENT',
        'AMERICAN EXPRESS AUTOPAY',
        'DISCOVER CARD PAYMENT',
        'DISCOVER E-PAYMENT',
        'CAPITAL ONE CREDIT CARD',
        'CAPITAL ONE CC PAYMENT',
        'CITI CARD PAYMENT',
        'CITICARDS PAYMENT',
        'BARCLAYS CREDIT CARD',
        'BARCLAYCARD PAYMENT',
        'SYNCHRONY BANK PAYMENT',
        'SYNCHRONY CREDIT',
        'CHASE CARD SERVICES',
        'CHASE CREDIT CARD PAYMENT'
    ],
    
    'Student Loans': [
        'DEPT OF EDUCATION',
        'DEPARTMENT OF EDUCATION',
        'ED FINANCIAL SERVICES',
        'NAVIENT CORPORATION',
        'NAVIENT PAYMENT',
        'NELNET PAYMENT',
        'NELNET LOAN',
        'GREAT LAKES BORROWER',
        'GREAT LAKES HIGHER ED',
        'MOHELA LOAN',
        'AIDVANTAGE',
        'EARNEST OPERATIONS',
        'COMMONBOND LENDING'
    ],
    
    'Business Loans': [
        'SBA LOAN PAYMENT',
        'SMALL BUSINESS ADMIN',
        'KABBAGE INC',
        'BLUEVINE CAPITAL',
        'FUNDBOX INC',
        'LENDIO FUNDING',
        'AMERICAN EXPRESS BUSINESS LOAN',
        'AMEX BUSINESS FINANCING',
        'PAYPAL WORKING CAPITAL',
        'SQUARE CAPITAL',
        'ONDECK CAPITAL'
    ],
    
    # Updated for Great Lakes CU area (IL/WI/Northwest Indiana)
    'Other Banks': [
        # National Banks
        'BANK OF AMERICA PAYMENT',
        'BANK OF AMERICA TRANSFER',
        'CHASE BANK PAYMENT',
        'CHASE TRANSFER',
        'WELLS FARGO PAYMENT',
        'WELLS FARGO TRANSFER',
        'US BANK PAYMENT',
        'PNC BANK PAYMENT',
        'CITIBANK PAYMENT',
        
        # Regional Banks (IL/WI/IN)
        'BMO HARRIS PAYMENT',
        'BMO HARRIS TRANSFER',
        'FIFTH THIRD PAYMENT',
        '5/3 BANK PAYMENT',
        'HUNTINGTON BANK PAYMENT',
        'OLD NATIONAL BANK PAYMENT',
        'FIRST MIDWEST PAYMENT',
        'WINTRUST PAYMENT',
        
        # Other Credit Unions (Potential competitors)
        'ALLIANT CREDIT UNION PAYMENT',
        'BAXTER CREDIT UNION PAYMENT',
        'CONSUMERS CREDIT UNION PAYMENT',
        'CREDIT UNION 1 PAYMENT',
        
        # Digital Banks
        'ALLY BANK PAYMENT',
        'DISCOVER BANK PAYMENT',
        'CAPITAL ONE 360 PAYMENT',
        'MARCUS BY GOLDMAN PAYMENT',
        'CHIME TRANSFER'
    ]
}

print("="*100)
print(" " * 30 + "M7: FINANCIAL SERVICES OPPORTUNITY ANALYSIS")
print("="*100)
print("\n✓ Financial services patterns configured")
print(f"\nTracking {len(FINANCIAL_SERVICES_PATTERNS)} categories:")
for category, patterns in FINANCIAL_SERVICES_PATTERNS.items():
    print(f"  • {category}: {len(patterns)} patterns")

print("\n💡 Note: Patterns are specific to avoid false matches")
print("   (e.g., 'TRADER JOE' won't match investment patterns)")
print("="*100)
