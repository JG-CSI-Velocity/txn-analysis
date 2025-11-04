# M5 SECTION SUMMARY - MONTH-OVER-MONTH ANALYSIS
# Complete overview of all M5 components

"""
================================================================================
M5: MONTH-OVER-MONTH MERCHANT ANALYSIS (SPLIT ANALYSIS & VISUALIZATION CELLS)
================================================================================

This section provides comprehensive month-over-month tracking and analysis of
merchant performance, spending patterns, and lifecycle behaviors.

COMPONENTS (17 CELLS TOTAL):
-----------------------------

M5A: MONTHLY RANK TRACKING - TOP 50 MERCHANTS
   • M5A-1: Analysis - Rank matrix table showing top 50 merchants across all months
   • M5A-2: Visualization - Line chart with 50 merchant trajectories
   Files: M5A_monthly_rank_tracking.py, M5A-2_rank_visualization.py

M5B: GROWTH LEADERS & DECLINERS
   • M5B-1: Analysis - Top 50 growth leaders and top 50 decliners tables
   • M5B-2: Visualization - Growth leaders horizontal bar chart (top 50)
   • M5B-3: Visualization - Decliners horizontal bar chart (top 50)
   Files: M5B-1_growth_analysis.py, M5B-2_growth_leaders_viz.py, M5B-3_decliners_viz.py

M5C: SPENDING CONSISTENCY ANALYSIS
   • M5C-1: Analysis - Top 50 consistent and top 50 volatile merchants tables
   • M5C-2: Visualization - Consistent merchants chart (lowest CV%)
   • M5C-3: Visualization - Volatile merchants chart (highest CV%)
   Files: M5C-1_consistency_analysis.py, M5C-2_consistent_viz.py, M5C-3_volatile_viz.py

M5D: NEW VS DECLINING MERCHANTS
   • M5D-1: Analysis - Monthly cohort table + top 5 new merchants from recent 3 months
   • M5D-2: Visualization - Dual chart (merchant flow + new merchant spending)
   Files: M5D-1_cohort_analysis.py, M5D-2_cohort_viz.py

M5E: BUSINESS ACCOUNT - MONTH-OVER-MONTH
   • M5E-1: Analysis - Top 50 climbers, fallers, and spend increases tables
   • M5E-2: Visualization - Business rank climbers chart (purple)
   • M5E-3: Visualization - Business rank fallers chart (purple)
   Files: M5E-1_business_analysis.py, M5E-2_business_climbers_viz.py, M5E-3_business_fallers_viz.py

M5F: PERSONAL ACCOUNT - MONTH-OVER-MONTH
   • M5F-1: Analysis - Top 50 climbers, fallers, and spend increases tables
   • M5F-2: Visualization - Personal rank climbers chart (teal)
   • M5F-3: Visualization - Personal rank fallers chart (red)
   Files: M5F-1_personal_analysis.py, M5F-2_personal_climbers_viz.py, M5F-3_personal_fallers_viz.py

================================================================================
KEY DATAFRAMES USED:
================================================================================

1. combined_df  - All transactions (M5A, M5B, M5C, M5D)
2. business_df  - Business accounts only (M5E)
3. personal_df  - Personal accounts only (M5F)

All use merchant_consolidated column for consistency

================================================================================
CELL STRUCTURE:
================================================================================

✓ ANALYSIS CELLS: Tables, statistics, summary metrics
✓ VISUALIZATION CELLS: Charts only (can be run separately)
✓ Each viz cell rebuilds necessary data (can run independently)
✓ All cells numbered sequentially within each component

================================================================================
ANALYSIS TECHNIQUES:
================================================================================

✓ Rank Tracking: Month-over-month position changes for top merchants
✓ Growth Analysis: Absolute and percentage spending changes
✓ Consistency Metrics: Coefficient of Variation (CV = StdDev/Mean × 100)
✓ Cohort Analysis: New vs returning vs lost merchant tracking
✓ Lifecycle Tracking: First appearance, activity duration, spending patterns

================================================================================
VISUALIZATION STANDARDS:
================================================================================

✓ All tables: display(df.style.hide(axis='index')) - no index column
✓ Currency: $X,XXX.XX format
✓ Percentages: X.X% format
✓ Rank indicators: ↑↓ arrows with numeric changes
✓ Charts: Inverted ranking (#1 at top), rank labels on left
✓ Color coding: Blue (overall), Purple (business), Teal/Red (personal)
✓ Summary statistics at end of each analysis cell
✓ Charts sized appropriately: (12,10) or (14,10) or (16,12)
✓ Top 50 shown in all tables and visualizations

================================================================================
BUSINESS INSIGHTS PROVIDED:
================================================================================

1. Which merchants are consistently top performers? (M5A)
2. Which merchants have the most dramatic spending changes? (M5B)
3. Which merchants have predictable vs volatile spending? (M5C)
4. How many new merchants appear each month? (M5D)
5. What percentage of spend comes from new merchants? (M5D)
6. Which business merchants are growing/declining fastest? (M5E)
7. Which personal merchants show the most volatility? (M5F)

================================================================================
USAGE INSTRUCTIONS:
================================================================================

Run cells in order within each component:
1. M5A-1 (analysis) → M5A-2 (visualization)
2. M5B-1 (analysis) → M5B-2 (viz) → M5B-3 (viz)
3. M5C-1 (analysis) → M5C-2 (viz) → M5C-3 (viz)
4. M5D-1 (analysis) → M5D-2 (visualization)
5. M5E-1 (analysis) → M5E-2 (viz) → M5E-3 (viz)
6. M5F-1 (analysis) → M5F-2 (viz) → M5F-3 (viz)

Each viz cell can also run independently (rebuilds necessary data)

================================================================================
FILE COUNT: 17 CELLS
================================================================================

M5A: 2 cells (1 analysis + 1 viz)
M5B: 3 cells (1 analysis + 2 viz)
M5C: 3 cells (1 analysis + 2 viz)
M5D: 2 cells (1 analysis + 1 viz)
M5E: 3 cells (1 analysis + 2 viz)
M5F: 3 cells (1 analysis + 2 viz)

================================================================================
NEXT STEPS:
================================================================================

After M5, consider:
• M6: Time-based patterns (weekday/weekend, hourly, seasonal)
• M7: Geographic analysis (if location data available)
• M8: Account behavior patterns
• M9: Anomaly detection

================================================================================
"""

print(__doc__)
