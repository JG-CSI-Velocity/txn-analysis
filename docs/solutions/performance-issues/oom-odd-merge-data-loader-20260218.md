---
module: v4_data_loader
date: 2026-02-18
problem_type: performance_issue
component: database
symptoms:
  - "numpy._core._exceptions._ArrayMemoryError: Unable to allocate 12.1 GiB for an array with shape (293, 5525537) and data type float64"
  - "Application crash during merge_data() when ODD file has 200+ columns"
  - "Streamlit shows 'Analysis failed' immediately after 'Loading data...'"
root_cause: memory_leak
resolution_type: code_fix
severity: critical
tags: [oom, pandas-merge, odd-file, memory, data-loader, numpy]
---

# Troubleshooting: OOM Crash When Merging ODD File with Transaction Data

## Problem
The V4 pipeline crashes with a 12.1 GiB memory allocation error when `merge_data()` left-joins the full ODD DataFrame (293 columns) onto 5.5M transaction rows, because pandas replicates every ODD column across every matched transaction row.

## Environment
- Module: v4_data_loader.py (`merge_data()` function)
- Python: 3.13
- pandas: latest
- Affected Component: `merge_data()` at line 385
- Date: 2026-02-18
- GitHub Issue: JG-CSI-Velocity/txnv3#1

## Symptoms
- `numpy._core._exceptions._ArrayMemoryError: Unable to allocate 12.1 GiB for an array with shape (293, 5525537) and data type float64`
- Crash occurs inside `txn_df.merge(odd_df, ...)` when ODD has ~293 columns and transactions have ~5.5M rows
- Streamlit app shows "Analysis failed" with full traceback pointing to pandas internals (`_merge_blocks`, `np.vstack`)
- Only happens with real client data (large ODD files with many MmmYY time-series columns)

## What Didn't Work

**Direct solution:** The root cause was identified from the traceback on first analysis -- the array shape `(293, 5525537)` immediately revealed the problem: 293 ODD columns being broadcast across 5.5M rows.

## Solution

Only merge the 9 ODD columns that downstream storylines actually need from `combined_df`. Storylines that need full ODD data (S6 Risk, S7 Campaigns) already read `ctx["odd_df"]` directly.

**Code changes:**

```python
# Before (broken) -- merges ALL 293 ODD columns:
combined_df = txn_df.merge(
    odd_df,
    left_on="primary_account_num",
    right_on="Acct Number",
    how="left",
)

# After (fixed) -- merges only 9 essential columns:
_MERGE_COLS = [
    "Acct Number",
    "generation",
    "balance_tier",
    "tenure_years",
    "Branch",
    "Business?",
    "Debit?",
    "Avg Bal",
    "Account Holder Age",
]

merge_cols = [c for c in _MERGE_COLS if c in odd_df.columns]
odd_slim = odd_df[merge_cols].copy()

combined_df = txn_df.merge(
    odd_slim,
    left_on="primary_account_num",
    right_on="Acct Number",
    how="left",
)
```

**Secondary fix** -- guard missing "Business?" column:

```python
# Before (broken):
business_df = combined_df[combined_df["Business?"] == "Yes"].copy()
personal_df = combined_df[combined_df["Business?"] == "No"].copy()

# After (fixed):
if "Business?" in combined_df.columns:
    business_df = combined_df[combined_df["Business?"] == "Yes"].copy()
    personal_df = combined_df[combined_df["Business?"] == "No"].copy()
else:
    business_df = pd.DataFrame(columns=combined_df.columns)
    personal_df = combined_df.copy()
```

## Why This Works

1. **Root cause**: The ODD file contains ~293 columns because it has monthly time-series data (MmmYY Spend, MmmYY Swipes, MmmYY PIN $, MmmYY Sig $, MmmYY Reg E Code, MmmYY OD Limit, MmmYY Mail, MmmYY Resp, MmmYY Segmentation -- each x 12+ months = 100+ columns just from time series, plus base columns). A left-join replicates every column across every matched row: 293 columns x 5.5M rows x 8 bytes = ~12 GiB.

2. **Why slim merge works**: An audit of all 8 storylines showed that `combined_df` is only used for columns already present in the transaction data plus 9 ODD columns (join key, derived demographics, branch, business flag, balance). Storylines that need the full ODD (S6 balance tiers/Reg E/OD limits, S7 campaigns) access `ctx["odd_df"]` directly and do their own targeted joins.

3. **Memory math**: 9 columns x 5.5M rows x 8 bytes = ~0.4 GiB (a 30x reduction).

## Prevention

- When merging a wide DataFrame (100+ columns) into a long DataFrame (1M+ rows), always select only the columns you need before merging.
- Audit which columns downstream code actually reads from the merged result. Most analyses only need a handful of account-level attributes.
- Keep the "full" wide DataFrame available separately in the context dict (`ctx["odd_df"]`) for storylines that need targeted access to specific columns.
- Add a `_MERGE_COLS` constant so the column list is explicit and easy to extend when new storylines need additional ODD columns.

## Related Issues

No related issues documented yet.
