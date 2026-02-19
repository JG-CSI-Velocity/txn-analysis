# 09_competition_merged.py
# M6A: COMPETITOR CONFIGURATION & DETECTION (MERGED)
# Client: 1776 - CoastHills Credit Union (California)
# Market: Santa Barbara, San Luis Obispo, Ventura counties
# ===========================================================================
#
# MATCHING STRATEGY (three-tier, ordered by confidence):
#   1. exact:       merchant name matches exactly (short/ambiguous terms)
#   2. starts_with: merchant name begins with pattern (primary method)
#   3. contains:    pattern appears anywhere in name (use sparingly)
#
# Base nationals/digital/wallets/BNPL are universal.
# Regionals and credit unions are CoastHills-specific (Central Coast CA).
# ===========================================================================

import pandas as pd

# ===========================================================================
# COMPETITOR CONFIGURATION
# ===========================================================================

COMPETITOR_MERCHANTS = {

    # =======================================================================
    # BIG NATIONALS -- Major banks with CA branch presence
    # =======================================================================
    'big_nationals': {
        'starts_with': [
            # Bank of America (major CA presence)
            'BANK OF AMERICA', 'BANKOFAMERICA', 'B OF A', 'BOA ',
            'BK OF AMERICA', 'BK OF AMER',

            # Wells Fargo (major CA presence)
            'WELLS FARGO', 'WELLS FARGO BANK', 'WF BANK', 'WF HOME',
            'WELLSFARGO',

            # JPMorgan Chase (major CA presence)
            'CHASE BANK', 'CHASE BK', 'CHASE CREDIT', 'CHASE CARD',
            'CHASE HOME', 'CHASE AUTO', 'CHASE MTG',
            'JPMORGAN', 'JPMORGAN CHASE', 'JP MORGAN',

            # Citibank
            'CITIBANK', 'CITI BANK', 'CITI CARD', 'CITICORP',
            'CITI MORTGAGE', 'CITIMORTGAGE',

            # US Bank
            'US BANK', 'U.S. BANK', 'US BK', 'USB ',

            # Capital One (banking arm)
            'CAPITAL ONE BK', 'CAPITAL ONE BANK', 'CAPITAL ONE 360',
            'CAP ONE BANK', 'CAPITALONE BK', 'CAPITAL ONE',

            # PNC Bank
            'PNC BANK', 'PNC BK',
        ],
        'exact': [
            'CHASE', 'BOA', 'CITI',
        ],
    },

    # =======================================================================
    # REGIONALS -- Central Coast CA community/savings banks
    # =======================================================================
    'regionals': {
        'starts_with': [
            # Mechanics Bank (Central Coast presence)
            'MECHANICS BANK', 'MECHANICS BK',

            # Pacific Premier Bank (CA regional)
            'PACIFIC PREMIER', 'PACIFIC PREMIER BANK', 'PACIFIC PREMIER BK',

            # Columbia Bank (CA regional)
            'COLUMBIA BANK', 'COLUMBIA BK', 'COLUMBIA BANKING',

            # American Riviera Bank (Santa Barbara local)
            'AMERICAN RIVIERA', 'AMERICAN RIVIERA BANK', 'AMERICAN RIVIERA BK',

            # Community Bank of Santa Maria (local)
            'COMMUNITY BANK OF SANTA', 'COMMUNITY BANK SANTA MARIA',
            'COMMUNITY BK SANTA MARIA',

            # Bank of the Sierra (CA regional)
            'BANK OF THE SIERRA', 'BK OF THE SIERRA', 'SIERRA BANK',

            # West Coast Community Bank (local)
            'WEST COAST COMMUNITY', 'WEST COAST COMMUNITY BANK',
            'WEST COAST COMMUNITY BK',
        ],
        'exact': [
            'MECHANICS BANK',
        ],
    },

    # =======================================================================
    # CREDIT UNIONS -- Local/regional CUs competing in CoastHills's market
    # =======================================================================
    'credit_unions': {
        'starts_with': [
            # SESLOC CU (San Luis Obispo -- direct competitor)
            'SESLOC CREDIT UNION', 'SESLOC CU', 'SESLOC FEDERAL',
            'SESLOC FCU', 'SESLOC',

            # SLO Credit Union (San Luis Obispo -- direct competitor)
            'SLO CREDIT UNION', 'SLO CU', 'SLO FEDERAL', 'SLO FCU',
            'SAN LUIS OBISPO CU', 'SAN LUIS OBISPO CREDIT',

            # National CUs with CA presence
            'NAVY FEDERAL', 'NAVY FED', 'NFCU',
            'GOLDEN 1 CREDIT', 'GOLDEN 1 CU',
            'PENTAGON FEDERAL', 'PENTAGON FCU', 'PENFED',
            'STATE EMPLOYEES CU', 'SECU ',
            'USAA',
            'ALLIANT CREDIT',
            'DIGITAL FCU',
        ],
        'exact': [
            'SESLOC',
        ],
    },

    # =======================================================================
    # DIGITAL BANKS -- Online-only banks (universal, no location customization)
    # =======================================================================
    'digital_banks': {
        'starts_with': [
            # Pure digital banks
            'ALLY BANK', 'ALLY BK', 'ALLY FINANCIAL',
            'DISCOVER BANK', 'DISCOVER BK', 'DISCOVER SAVINGS',
            'SOFI BANK', 'SOFI MONEY', 'SOFI LENDING', 'SOFI CREDIT',
            'SOFI',
            'CHIME BANK', 'CHIME FINANCIAL',
            'VARO BANK', 'VARO MONEY',
            'GO2BANK',
            'GREEN DOT BANK', 'GREEN DOT BK', 'GREENDOT',

            # Neobank / BaaS infrastructure banks
            'THE BANCORP', 'BANCORP BANK',
            'STRIDE BANK',
            'COASTAL COMMUNITY BK',

            # Big tech / investment bank offerings
            'MARCUS BY GS', 'MARCUS BY GOLDMAN', 'MARCUS GOLDMAN',
            'GOLDMAN SACHS BANK',
            'SCHWAB BANK', 'CHARLES SCHWAB BK', 'SCHWAB BK',
            'FIDELITY CASH', 'FIDELITY BROKERAGE',

            # Investment/robo platforms with banking
            'ROBINHOOD CASH', 'ROBINHOOD MONEY',
            'BETTERMENT',
            'WEALTHFRONT',

            # International digital banks
            'REVOLUT',
            'N26 BANK', 'N26',
            'MONZO',

            # Fintech lending
            'DAVE INC', 'DAVE APP',
            'EARNIN',
            'BRIGIT',
            'POSSIBLE FINANCE',
            'CURRENT CARD',
        ],
        'contains': [
            'CHIME',
            'VARO',
            'GREEN DOT',
            'SYNCHRONY',
        ],
        'exact': [
            'CHIME', 'REVOLUT', 'BETTERMENT', 'WEALTHFRONT',
            'SOFI', 'ROBINHOOD', 'MARCUS',
        ],
    },

    # =======================================================================
    # WALLETS & P2P -- Payment platforms (universal)
    # =======================================================================
    'wallets_p2p': {
        'starts_with': [
            'PAYPAL',
            'VENMO',
            'CASH APP', 'CASHAPP',
            'APPLE CASH', 'APPLE CARD', 'APPLE PAY CASH',
            'GOOGLE PAY', 'GOOGLEPAY',
            'ZELLE',
            'SQ *',
        ],
        'contains': [
            'PAYPAL',
            'VENMO',
            'CASH APP', 'CASHAPP',
            'APPLE CASH',
            'GOOGLE PAY',
            'ZELLE',
        ],
        'exact': [
            'PAYPAL', 'VENMO',
        ],
    },

    # =======================================================================
    # BNPL -- Buy Now Pay Later (universal)
    # =======================================================================
    'bnpl': {
        'starts_with': [
            'KLARNA',
            'AFTERPAY',
            'AFFIRM', 'AFFIRM INC',
            'SEZZLE',
            'QUADPAY',
            'ZIP PAY', 'ZIPPAY',
        ],
        'contains': [
            'AFTERPAY',
            'KLARNA',
            'AFFIRM',
            'SEZZLE',
            'ZIP PAY',
            'QUADPAY',
        ],
        'exact': [
            'KLARNA', 'AFTERPAY', 'SEZZLE',
        ],
    },

    # =======================================================================
    # ALT FINANCE -- Alternative financial services
    # =======================================================================
    'alt_finance': {
        'starts_with': [
            'FLEX FINANCE', 'FLEXFINANCE',
            'MONEYLION',
            'ALBERT SAVINGS',
            'EMPOWER FINANCE',
        ],
    },
}

# Reporting category groupings
TRUE_COMPETITORS = ['big_nationals', 'regionals', 'credit_unions', 'digital_banks']
PAYMENT_ECOSYSTEMS = ['wallets_p2p', 'bnpl']

# Financial MCC codes for unmatched discovery
FINANCIAL_MCC_CODES = [
    6010,  # Financial Institution -- Manual Cash Disbursements
    6011,  # Financial Institution -- Automated Cash Disbursements (ATMs)
    6012,  # Financial Institution -- Merchandise and Services
    6051,  # Non-Financial Institutions -- Foreign Currency, Money Orders
    6211,  # Security Brokers/Dealers
    6300,  # Insurance
]

# False positive exclusions
FALSE_POSITIVES = [
    'TOWING', 'TOW SERVICE', 'BODY SHOP',
    'AUTO REPAIR', 'AUTO PARTS', 'AUTOZONE', 'AUTO TRADER',
    'TRADER JOE',
    'CHASE OUTDOORS',
    'CURRENT ELECTRIC',
    'COASTHILLS MARKETPLACE',
]


# ===========================================================================
# MATCHING FUNCTIONS
# ===========================================================================

def classify_competitor(merchant_name, config=COMPETITOR_MERCHANTS):
    """
    Classify a merchant as a competitor using three-tier matching.

    Priority: exact -> starts_with -> contains
    Returns: (category, matched_pattern) or (None, None)
    """
    if not merchant_name or not isinstance(merchant_name, str):
        return None, None

    name = merchant_name.upper().strip()

    # Check false positives first
    for fp in FALSE_POSITIVES:
        if fp in name:
            return None, None

    # Pass 1: Exact matches (highest confidence)
    for category, rules in config.items():
        for pattern in rules.get('exact', []):
            if name == pattern:
                return category, pattern

    # Pass 2: Starts-with matches (high confidence)
    for category, rules in config.items():
        for pattern in rules.get('starts_with', []):
            if name.startswith(pattern):
                return category, pattern

    # Pass 3: Contains matches (use sparingly -- higher false positive risk)
    for category, rules in config.items():
        for pattern in rules.get('contains', []):
            if pattern in name:
                return category, pattern

    return None, None


def tag_competitors(df, merchant_col='merchant_consolidated'):
    """
    Tag all transactions with competitor category and matched pattern.
    Adds two columns: competitor_category, competitor_match

    Parameters:
        df: DataFrame with merchant names
        merchant_col: column name containing merchant names

    Returns:
        DataFrame with competitor_category and competitor_match columns added
    """
    results = df[merchant_col].apply(
        lambda x: classify_competitor(x) if pd.notna(x) else (None, None)
    )
    df['competitor_category'] = results.apply(lambda x: x[0])
    df['competitor_match'] = results.apply(lambda x: x[1])
    return df


def discover_unmatched_financial(df, merchant_col='merchant_consolidated',
                                 mcc_col='mcc_code'):
    """
    Find merchants with financial MCC codes that weren't matched as competitors.
    These are candidates to ADD to the config.

    Returns a DataFrame of unmatched financial merchants sorted by spend.
    """
    untagged = df[df['competitor_category'].isna()].copy()

    if mcc_col in untagged.columns:
        financial = untagged[untagged[mcc_col].isin(FINANCIAL_MCC_CODES)]
    else:
        financial_keywords = [
            'BANK', ' BK ', 'BK,', 'CREDIT UNION', ' CU ', 'CU,',
            'FEDERAL CU', 'FCU', 'SAVINGS BANK', 'SVG BK',
            'FINANCIAL', 'LENDING', 'MORTGAGE', 'MTG ',
        ]
        mask = untagged[merchant_col].str.upper().apply(
            lambda x: any(kw in f' {x} ' for kw in financial_keywords)
            if pd.notna(x) else False
        )
        financial = untagged[mask]

    if len(financial) == 0:
        print("No unmatched financial merchants found.")
        return pd.DataFrame()

    summary = financial.groupby(merchant_col).agg(
        transaction_count=('amount', 'count'),
        total_spend=('amount', 'sum'),
        unique_accounts=('primary_account_num', 'nunique'),
    ).sort_values('total_spend', ascending=False)

    return summary


def print_config_summary(config=COMPETITOR_MERCHANTS):
    """Print a summary of the competitor configuration."""
    print("=" * 80)
    print(" " * 20 + "COMPETITOR CONFIGURATION SUMMARY")
    print("=" * 80)

    total_patterns = 0
    for category, rules in config.items():
        n_starts = len(rules.get('starts_with', []))
        n_exact = len(rules.get('exact', []))
        n_contains = len(rules.get('contains', []))
        n_total = n_starts + n_exact + n_contains
        total_patterns += n_total

        display_name = category.replace('_', ' ').title()
        print(f"\n  {display_name}:")
        print(f"    starts_with: {n_starts:3d} patterns")
        if n_exact:
            print(f"    exact:       {n_exact:3d} patterns")
        if n_contains:
            print(f"    contains:    {n_contains:3d} patterns")

    print(f"\n{'=' * 80}")
    print(f"  Total categories: {len(config)}")
    print(f"  Total patterns:   {total_patterns}")
    print("=" * 80)


# ===========================================================================
# ITEMS REQUIRING REVIEW
# ===========================================================================
# COASTAL COMMUNITY BK - In digital_banks but could be confused with local bank.
#   Using full "COASTAL COMMUNITY BK" prefix to avoid false matches.
# SIERRA BANK - Could match non-"Bank of the Sierra" entities.
#   Using "BANK OF THE SIERRA" as primary, "SIERRA BANK" as fallback.
# SLO / SESLOC - Short prefixes. Using full names + exact matches.
# CAPITAL ONE - Issue user listed bare "CAPITAL ONE" -- added to starts_with
#   alongside "CAPITAL ONE BANK" variants already in base.
# ===========================================================================
