# 🏦 Credit Union Transaction Analysis Framework

A comprehensive Python-based framework for analyzing credit union debit card transaction data to identify competitive threats, member behavior patterns, and financial services opportunities.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Analysis Modules](#analysis-modules)
- [Key Outputs](#key-outputs)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Best Practices](#best-practices)

---

## 🎯 Overview

This framework provides credit unions with actionable insights from debit card transaction data by:

- **Identifying competitive threats** from banks, fintechs, and alternative financial services
- **Segmenting members** by spend patterns and loyalty
- **Discovering financial services opportunities** through transaction pattern analysis
- **Tracking merchant trends** including new entrants and declining relationships
- **Visualizing member behavior** through comprehensive charts and heatmaps

Built for: **Credit unions, community banks, and regional financial institutions**

---

## ✨ Features

### 🔍 Competitive Intelligence
- Automatic detection of 47+ competitor patterns across 6 categories
- Account segmentation by competitor spend percentage
- Risk assessment and threat scoring
- Business vs. personal account analysis

### 📊 Merchant Analysis
- Universal merchant name consolidation (1M+ → 400K unique merchants)
- Top merchant rankings by spend, accounts, and transactions
- Monthly trend analysis and growth tracking
- New vs. declining merchant identification

### 💰 Financial Services Opportunities
- Auto loan, mortgage, investment, and credit card opportunity detection
- Student loan and business loan analysis
- Cross-sell opportunity identification

### 📈 Visualizations
- Category-specific segmentation heatmaps
- Spend distribution scatter plots
- Monthly trend charts
- Risk assessment dashboards

---

## 📁 Project Structure

```
transaction-analysis/
│
├── data_prep/
│   ├── merchant_consolidation.py      # Universal merchant name standardization
│   ├── odd_import.py                  # Account flag integration
│   └── business_personal_split.py     # Account type segmentation
│
├── modules/
│   ├── m1_general_analysis/           # Monthly summaries and trends
│   ├── m2_mcc_analysis/              # MCC code patterns
│   ├── m3_business_analysis/         # Business account insights
│   ├── m4_personal_analysis/         # Personal account insights
│   ├── m5_merchant_trends/           # Merchant lifecycle tracking
│   ├── m6_competitor_analysis/       # Competitive intelligence
│   └── m7_financial_services/        # Opportunity identification
│
├── visualizations/
│   ├── segmentation_heatmaps.py      # Category-specific heatmaps
│   ├── spend_scatter_plots.py        # Distribution analysis
│   └── trend_charts.py               # Time series visualizations
│
├── config/
│   ├── competitors.py                # Competitor pattern definitions
│   └── financial_services.py        # Financial services patterns
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
# Required Python packages
pandas >= 2.0.0
numpy >= 1.24.0
matplotlib >= 3.7.0
openpyxl >= 3.1.0
```

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/transaction-analysis.git
cd transaction-analysis

# Install requirements
pip install -r requirements.txt
```

### Data Requirements

Your transaction data should include:
- `merchant_name` - Raw merchant name from card processor
- `transaction_date` - Transaction timestamp
- `amount` - Transaction amount
- `primary_account_num` - Account identifier
- `mcc_code` - Merchant Category Code (optional)

---

## 📊 Analysis Modules

### Module 1: General Analysis
**Purpose:** High-level portfolio overview and monthly trends

**Key Outputs:**
- Monthly transaction summaries
- Growth rates (MoM, YoY)
- Account activity metrics
- Spend distribution by amount ranges

**Use Case:** Executive dashboards and board reporting

---

### Module 2: MCC Analysis
**Purpose:** Industry spend pattern analysis

**Key Outputs:**
- Top spending categories
- Industry penetration rates
- Category growth trends

**Use Case:** Understanding member spending behavior by industry

---

### Module 3: Business Analysis
**Purpose:** Business account merchant patterns

**Key Outputs:**
- Top 50 business merchants by spend
- Business-specific trends
- Industry concentration analysis

**Use Case:** Commercial banking strategy and B2B partnerships

---

### Module 4: Personal Analysis
**Purpose:** Personal account merchant patterns

**Key Outputs:**
- Top 50 personal merchants by spend
- Consumer spending trends
- Retail relationship analysis

**Use Case:** Consumer banking strategy and retail partnerships

---

### Module 5: Merchant Trends
**Purpose:** Merchant lifecycle tracking

**Key Outputs:**
- **M5A-C:** Top merchants with rank changes
- **M5D:** New vs. declining merchants
- **M5E:** Business rank climbers

**Key Metrics:**
- New merchant cohorts by month
- Merchant retention rates
- Growth momentum tracking

**Use Case:** Early detection of emerging competitors and declining relationships

---

### Module 6: Competitor Analysis ⭐
**Purpose:** Comprehensive competitive intelligence

#### M6A: Detection & Configuration
- Configures 6 competitor categories
- Searches transaction data for competitor patterns
- Identifies 47+ competitors across categories

#### M6B: Detailed Analysis
**M6B-1:** High-level metrics (penetration, spend, accounts)  
**M6B-2:** Top 20 competitors by spend  
**M6B-3:** Category breakdown  
**M6B-4:** Business vs. personal split  
**M6B-5:** Monthly trend analysis  
**M6B-6:** Bank competitive threats (threat scoring)  
**M6B-7:** Non-bank threats (wallets, BNPL)

#### Account Segmentation
- **Competitor-Heavy:** >50% spend at competitor (🔴 High Risk)
- **Balanced:** 25-50% spend at competitor (🟠 Medium Risk)
- **CU-Focused:** <25% spend at competitor (🟢 Low Risk)

**Competitor Categories:**
1. Big Nationals (Chase, Wells Fargo, BofA, Citi)
2. Regionals (BMO, Fifth Third, Huntington)
3. Credit Unions (Alliant, other local CUs)
4. Digital Banks (Marcus, Chime, Ally, SoFi)
5. Wallets/P2P (Cash App, Venmo, PayPal, Zelle)
6. BNPL (Klarna, Afterpay, Affirm)

**Visualizations:**
- Category-specific segmentation heatmaps
- Spend distribution scatter plots
- Risk assessment dashboards

**Use Case:** Retention strategy, competitive positioning, market share defense

---

### Module 7: Financial Services Opportunities
**Purpose:** Cross-sell opportunity identification

**Categories Tracked:**
- Auto Loans (Toyota, Ford, GM Financial, Ally)
- Investment/Brokerage (Schwab, Fidelity, Robinhood)
- Mortgage/HELOC (Rocket, Quicken, PennyMac)
- Personal Loans (SoFi, LendingClub, Marcus)
- Credit Cards (Amex, Discover, Capital One)
- Student Loans (Dept of Education, Navient, Nelnet)
- Business Loans (SBA, Kabbage, BlueVine)
- Other Banks (competitor transfers)

**Key Outputs:**
- Members with external auto loans
- Investment account holders
- Mortgage payment patterns
- Cross-sell opportunity sizing

**Use Case:** Product development, marketing campaigns, member outreach

---

## 🎨 Key Outputs

### Segmentation Heatmaps
**Purpose:** Visual risk assessment by competitor category

**Color Coding:**
- 🔴 **Competitor-Heavy Column:** Red = High % at risk
- 🟠 **Balanced Column:** Orange = Medium risk
- 🟢 **CU-Focused Column:** Green = High loyalty

**Example Insight:**  
"20% of members using digital banks are Competitor-Heavy (high risk)"

---

### Scatter Plots
**Purpose:** Spend distribution analysis

**Four Quadrants:**
- 🚨 **Top-Right:** High competitor spend, low CU spend (LOSING THEM)
- ✅ **Top-Left:** Low competitor spend, high CU spend (WINNING)
- 💰 **Bottom-Right:** High spend at both (BIG SPENDERS)
- 📉 **Bottom-Left:** Low spend everywhere (SMALL ACCOUNTS)

---

### Risk Assessment
**Purpose:** Prioritize retention efforts

**Threat Score Formula:**
```
Threat Score = (Penetration × 40%) + (Total Spend × 30%) + (Growth Rate × 30%)
```

**Filters:**
- Minimum 100 accounts
- Minimum $50K spend
- Only bank competitors (excludes wallets/BNPL)

---

## 🛠️ Requirements

### System Requirements
- Python 3.8+
- 8GB RAM minimum (16GB recommended for large datasets)
- Jupyter Notebook or JupyterLab

### Python Packages
```
pandas==2.1.0
numpy==1.24.3
matplotlib==3.7.2
openpyxl==3.1.2
```

---

## ⚙️ Configuration

### Competitor Patterns (M6A)
Edit `config/competitors.py` to customize:
```python
COMPETITOR_MERCHANTS = {
    'big_nationals': [
        'CHASE',
        'BANK OF AMERICA',
        # Add your competitors...
    ]
}
```

### Financial Services Patterns (M7)
Edit `config/financial_services.py` to customize:
```python
FINANCIAL_SERVICES_PATTERNS = {
    'Auto Loans': [
        'GM FINANCIAL',
        'TOYOTA FINANCIAL',
        # Add your patterns...
    ]
}
```

### Merchant Consolidation
Edit `data_prep/merchant_consolidation.py` to add:
```python
def standardize_merchant_name(merchant_name):
    merchant_upper = str(merchant_name).upper()
    
    if 'YOUR PATTERN' in merchant_upper:
        return 'STANDARDIZED NAME'
    
    return merchant_name
```

---

## 📝 Best Practices

### Data Preparation
1. ✅ Always run consolidation **before** splitting business/personal
2. ✅ Verify `year_month` column exists before monthly analysis
3. ✅ Check for duplicates in account numbers
4. ✅ Validate date ranges match expected time periods

### Performance Optimization
1. ⚡ Use `merchant_consolidated` for analysis (400K vs 1M merchants)
2. ⚡ Filter by date range before processing if analyzing subsets
3. ⚡ Cache competitor detection results (stored in `all_competitor_data`)
4. ⚡ Use vectorized operations instead of loops

### Analysis Tips
1. 💡 Run M6 **after** consolidation for accurate competitor detection
2. 💡 Focus on "Competitor-Heavy" accounts for retention campaigns
3. 💡 Use M5D to identify emerging competitive threats early
4. 💡 Cross-reference M6 with M7 to find holistic opportunities

### Visualization Guidelines
1. 📊 Use category-specific heatmaps (not individual competitors)
2. 📊 Filter scatter plots to material accounts (>$100 spend)
3. 📊 Color code by risk level for executive presentations
4. 📊 Include account counts on all charts for context

---

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

Built for credit unions to compete effectively in an evolving financial services landscape.

**Key Principles:**
- Member-first data analysis
- Actionable insights over vanity metrics
- Privacy-respecting competitive intelligence
- Open-source community collaboration

---

## 📞 Support

For questions or issues:
- Create a GitHub issue
- Documentation: [Wiki](https://github.com/your-org/transaction-analysis/wiki)

---

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Maintained By:** Me

---

⭐ If this framework helps your credit union, please star the repository!
