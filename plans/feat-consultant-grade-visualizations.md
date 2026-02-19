# Consultant-Grade Visualization Overhaul

## Enhancement Summary

**Deepened on:** 2026-02-07
**Sections enhanced:** 6 phases + design philosophy + registry + acceptance criteria
**Review agents used:** architecture-strategist, performance-oracle, code-simplicity-reviewer, pattern-recognition-specialist, kieran-python-reviewer, web research (3 queries)

### Key Improvements from Deepening
1. **Cut 3 chart types** (radar, waffle, sankey) -- saves ~230 LOC, no data supports them
2. **Fixed dual-key registry bug** -- Python dict cannot have duplicate keys; use composite keys
3. **Fixed lollipop trace explosion** -- original design creates 50 traces per chart; use 2-trace approach
4. **Eliminated annotations.py** -- inline 2 helper functions into theme.py instead of a separate module
5. **Added lazy theme registration** -- avoids import side-effect hazard
6. **Split PNG scale** -- scale=1 for Excel-embedded (fast), scale=3 for standalone (crisp)
7. **Added `outputs.chart_images` toggle** -- separate from `outputs.excel` for user control
8. **Fixed `._append()` deprecation** -- trends.py uses deprecated pandas method

### Charts Cut (with reasoning)
| Chart | Reason |
|-------|--------|
| Radar (5C) | Misleading for 4-axis data; area distortion makes comparison unreliable. Threat scatter already covers this. |
| Waffle (5E) | Overkill for 4 segments. A simple table with percentage bars is clearer. |
| Sankey (5F) | M7 financial_services_detection doesn't output account_type->category->merchant flows. Would require restructuring the analysis. |

---

## Overview

Replace the current basic Plotly horizontal bars with a modern, boutique-consultant visual system. Every chart should look like it came from a McKinsey or BCG deliverable -- muted palettes, insight-driven titles, annotation-heavy storytelling, minimal gridlines, and strategic use of color (gray base + 1-2 accents).

**Current state**: 16 charts (9 identical horizontal bars + 7 specialized), Tableau-10 default colors, `plotly_white` theme, no annotations, generic label-style titles, charts built in memory but never exported to PNG or embedded in Excel.

**Target state**: 19 charts across 31 analyses, custom consultant theme, lollipop charts replacing bars, 3 new chart types (treemap, bump, bullet), insight titles, direct labeling, source footers, PNG export wired and embedded in Excel.

---

## Design Philosophy

### The Three Rules

1. **Gray + One Accent**: All data is `#C4C4C4`. The 1-3 items that matter get `#005EB8` (navy blue accent). This makes the insight pop without the reader having to decode a rainbow.

2. **Title = Insight**: "Top 5 merchants capture 62% of total spend" not "Top Merchants by Spend." The chart title is a complete sentence stating the finding.

3. **Less is More**: No gridlines (or barely visible ones). No chart borders. No legend boxes. No bold axis labels. Direct-label lines instead of using a legend. Every pixel earns its place.

### Color Palette

```
Navy (titles, emphasis)     #051C2C
Blue Primary (accent)       #005EB8
Blue Secondary              #0090D4
Teal                        #4ABFBF
Coral (negative/alert)      #E4573D
Gold (highlight)            #F3C13A
Warm Gray (context data)    #A2AAAD
Light Gray (gridlines)      #E8E8E8
Near Black (body text)      #222222
Gray Base (non-accent bars) #C4C4C4
```

### Research Insights: Color Management

**Problem discovered**: The codebase currently has 4 competing color authorities:
1. `settings.py` `BRAND_COLORS` dict
2. `settings.py` `ChartConfig.colors` field
3. Per-chart hardcoded hex strings (e.g., `"#1f77b4"` in overall.py)
4. The proposed `theme.py` constants

**Resolution**: Single source of truth in `theme.py`. All color constants defined there, imported everywhere else. `ChartConfig.colors` becomes a passthrough that defaults to theme colors but can be overridden via YAML.

```python
# theme.py -- THE color authority
ACCENT = "#005EB8"
ACCENT_SECONDARY = "#0090D4"
GRAY_BASE = "#C4C4C4"
CORAL = "#E4573D"
TEAL = "#4ABFBF"
NAVY = "#051C2C"
# ... etc

# settings.py -- delegates to theme
from txn_analysis.charts.theme import ACCENT, GRAY_BASE  # etc
BRAND_COLORS = {"primary": ACCENT, "secondary": GRAY_BASE, ...}
```

### Typography

| Role | Font | Size | Color |
|------|------|------|-------|
| Chart title (insight) | Georgia, serif | 18px bold | `#051C2C` |
| Subtitle (context) | Arial, sans-serif | 12px | `#888888` |
| Axis labels | Arial | 11px | `#555555` |
| Data labels | Arial | 10px | `#333333` |
| Source footer | Arial | 9px | `#AAAAAA` |

### Research Insights: Typography

**Font fallback**: Georgia is not available on all systems (notably Linux CI servers). The Plotly template should specify `"Georgia, 'Times New Roman', serif"` as the font family so rendering doesn't fall back to the Plotly default sans-serif.

---

## Proposed Solution

### Phase 1: Theme Foundation

Create `charts/theme.py` -- a custom Plotly template that becomes the default for all charts.

**What it does**:
- Registers a `"consultant"` template via `plotly.io.templates`
- Sets palette, fonts, margins, grid behavior, hover style as defaults
- Defines ALL color constants as module-level variables (single source of truth)
- Provides `ensure_theme()` function for lazy registration

**Files**:
- `txn_analysis/charts/theme.py` (NEW) -- template + color constants + `insight_title()` + `add_source_footer()` helpers
- `txn_analysis/settings.py` (MODIFY) -- change `ChartConfig.theme` default from `"plotly_white"` to `"consultant"`, point `BRAND_COLORS` at theme imports
- `txn_analysis/charts/__init__.py` (MODIFY) -- call `ensure_theme()` in `create_charts()`, not at import time

**Key decisions**:
- Theme fully replaces `plotly_white` (not layered)
- `config.colors` in YAML still works as override but defaults to consultant palette
- Per-chart hardcoded colors replaced with theme constant imports

### Research Insights: Phase 1

**Lazy registration instead of import side-effect**:
The original plan called for `import txn_analysis.charts.theme` at module top-level to auto-register. This is fragile -- import order matters, and it runs Plotly initialization at import time (slow for tests, breaks if Plotly isn't installed).

Instead, use a lazy pattern:

```python
# theme.py
_REGISTERED = False

def ensure_theme() -> None:
    global _REGISTERED
    if _REGISTERED:
        return
    import plotly.io as pio
    pio.templates["consultant"] = _build_template()
    pio.templates.default = "consultant"
    _REGISTERED = True

def _build_template() -> dict:
    return go.layout.Template(
        layout=go.Layout(
            font=dict(family="Arial, Helvetica, sans-serif", size=11, color="#555555"),
            title=dict(
                font=dict(family="Georgia, 'Times New Roman', serif", size=18, color="#051C2C"),
                x=0.02, xanchor="left",
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(gridcolor="#E8E8E8", gridwidth=0.5, zeroline=False),
            margin=dict(l=200, r=40, t=80, b=60),
            hoverlabel=dict(bgcolor="white", bordercolor="#C4C4C4"),
        )
    )
```

**Annotation helpers live in theme.py** (not a separate annotations.py):
- `insight_title(main, subtitle="")` -- returns Plotly title dict
- `add_source_footer(fig, client_name, date_range)` -- adds annotation at bottom-left

These are 5-10 lines each. A separate module is unnecessary overhead.

**Source footer signature**: The original plan had `add_source_footer(fig, settings)` which requires importing Settings into the chart layer (circular dependency risk). Instead, pass `client_name: str` and `date_range: str` explicitly. The caller (`create_charts()`) extracts these from Settings.

### Phase 2: ~~Annotation Helpers + Source Footers~~ (MERGED INTO PHASE 1)

**CUT**: `annotations.py` as a separate file. The two useful functions (`insight_title`, `add_source_footer`) are small enough to live in `theme.py`. The `add_callout()` function can be added later only if a chart actually needs it (YAGNI).

**Source footer application**: Applied as post-processing in `create_charts()`, not inside individual chart functions. This keeps chart functions pure (they return a Figure, they don't need Settings context).

```python
# charts/__init__.py
def create_charts(results, config, client_name="", date_range=""):
    ensure_theme()
    charts = {}
    for result in results:
        if result.name in CHART_REGISTRY:
            fig = CHART_REGISTRY[result.name](result, config)
            add_source_footer(fig, client_name, date_range)
            charts[result.name] = fig
    return charts
```

### Phase 3: Lollipop Migration (9 charts)

Replace `horizontal_bar()` in `charts/bar_charts.py` with `lollipop_chart()`.

**Visual spec**:
- Thin horizontal stems from 0 to value (1.5px, gray `#C4C4C4`)
- Circle marker at the end (10px diameter)
- Top 3 items: accent blue `#005EB8` stems + dots
- Items 4+: gray `#C4C4C4` stems + dots
- Value labels right of each dot (`$1,234,567`)
- Insight title computed dynamically: "Top 5 capture X% of total spend"
- No x-axis (values are directly labeled)
- Left margin 200px for merchant names

**Charts affected** (all via the shared builder):
| Module | Chart | Current Color | New |
|--------|-------|---------------|-----|
| M1 overall.py | top_by_spend | `#1f77b4` | Gray+accent lollipop |
| M1 overall.py | top_by_transactions | `#2ca02c` | Gray+accent lollipop |
| M1 overall.py | top_by_accounts | `#ff7f0e` | Gray+accent lollipop |
| M3 business.py | business_top_spend | `#9467bd` | Gray+accent lollipop |
| M3 business.py | business_top_txn | `#2ca02c` | Gray+accent lollipop |
| M3 business.py | business_top_acct | `#ff7f0e` | Gray+accent lollipop |
| M4 personal.py | personal_top_spend | `#17becf` | Gray+accent lollipop |
| M4 personal.py | personal_top_txn | `#bcbd22` | Gray+accent lollipop |
| M4 personal.py | personal_top_acct | `#e377c2` | Gray+accent lollipop |

### Research Insights: Lollipop Trace Performance

**Critical bug in naive approach**: Creating one `go.Scatter` trace per item (stem + dot) for a top-25 chart produces **50 traces** vs. the current **1 trace** from `go.Bar`. This bloats the Plotly JSON, slows rendering, and makes kaleido PNG export ~3x slower.

**2-trace approach** (recommended):

```python
def lollipop_chart(result: AnalysisResult, config: ChartConfig) -> go.Figure:
    df = result.df.head(config.top_n or 25)
    n = len(df)
    accent_n = min(3, n)

    # Build stem segments with None separators
    xs, ys = [], []
    for _, row in df.iterrows():
        xs.extend([0, row[value_col], None])
        ys.extend([row[label_col]] * 2 + [None])

    # Accent color array: first accent_n items blue, rest gray
    colors = [ACCENT] * accent_n + [GRAY_BASE] * (n - accent_n)

    fig = go.Figure()
    # Trace 1: all stems (single trace with None breaks)
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines",
        line=dict(color=GRAY_BASE, width=1.5),
        showlegend=False, hoverinfo="skip",
    ))
    # Trace 2: all dots (single trace with color array)
    fig.add_trace(go.Scatter(
        x=df[value_col], y=df[label_col], mode="markers+text",
        marker=dict(size=10, color=colors),
        text=df[value_col].apply(format_value),
        textposition="middle right",
        showlegend=False,
    ))
    return fig
```

This keeps it at exactly **2 traces** regardless of how many items are displayed.

**Boilerplate deduplication**: The 3 chart modules (overall.py, business.py, personal.py) currently have ~183 lines of near-identical code. The lollipop builder should be the single shared function in `bar_charts.py`, and the per-module chart functions should be thin wrappers (~5 lines each).

### Phase 4: Restyle Existing Specialized Charts (7 charts)

Apply the consultant theme to the non-bar charts without changing their type.

| Chart | File | Changes |
|-------|------|---------|
| MCC comparison (triple subplot) | `charts/mcc.py` | Convert subplots to lollipops, use sequential navy colorscale |
| Rank trajectory | `charts/trends.py` | Top 3 lines colored, rest gray; direct labels at endpoints; hide legend |
| Growth leaders | `charts/trends.py` | Keep diverging bar; use `#005EB8` (positive) + `#E4573D` (negative) |
| Cohort summary | `charts/trends.py` | Use consultant palette; add insight title |
| Threat scatter | `charts/competitor.py` | Add quadrant annotations ("High Threat", "Monitor"); navy sequential scale |
| Segmentation bar | `charts/competitor.py` | Use consultant palette for segments |
| Competitor heatmap | `charts/competitor.py` | Navy sequential colorscale; remove `RdYlGn_r` |

### Research Insights: Phase 4

**Fix deprecated pandas method**: `charts/trends.py` uses `df._append()` which is deprecated since pandas 2.0 and will be removed. Replace with `pd.concat([df, new_row])`.

**MCC special case**: `chart_mcc_comparison()` has a non-standard signature `(result1, result2, result3, config)` instead of `(result, config)`. This already has special handling in `create_charts()`. Leave this as-is but document it clearly. Do NOT try to unify the signature -- it would require restructuring the MCC analysis to emit a single combined result, which is out of scope.

**Rank trajectory -> bump chart**: The bump chart (Phase 5B) replaces the current rank trajectory. Phase 4 should NOT restyle the rank trajectory since it will be replaced. Mark it as skip.

### Phase 5: New Chart Types (3 new charts)

#### 5A: Treemap -- Merchant Spend Hierarchy
- **Analysis**: `top_merchants_by_spend` (M1)
- **Hierarchy**: MCC Category > Merchant (using `mcc_code` group as parent, `merchant_consolidated` as child)
- **File**: `charts/overall.py` (add `chart_merchant_treemap()`)
- **Fallback**: If MCC data unavailable, skip treemap (graceful degradation)

**Research Insights**:
- Use `go.Treemap` with `branchvalues="total"` so parent sizes equal sum of children
- Color by parent category using consultant palette (sequential navy scale)
- Show values as hover text, not permanent labels (too many small segments)
- Limit to top 10 MCC categories to avoid unreadable micro-tiles

#### 5B: Bump Chart -- Rank Trajectory Upgrade
- **Analysis**: `monthly_rank_tracking` (M5A)
- **Replaces**: Current `chart_rank_trajectory()` multi-line spaghetti
- **Design**: Smooth spline curves, top 3 colored + labeled, rest gray at 50% opacity, Y-axis inverted (rank 1 at top), direct endpoint labels, no legend
- **File**: `charts/trends.py` (replace `chart_rank_trajectory()`)

**Research Insights**:
- Plotly `go.Scatter` with `line_shape="spline"` and `line_smoothing=1.3`
- Use `go.Scatter` with `mode="lines+markers"` for top 3, `mode="lines"` only for the rest
- Add text annotations at the last data point for the top 3 merchants
- Keep it to top 10 merchants max to avoid spaghetti. If more are needed, use a dropdown filter.

#### ~~5C: Radar Chart~~ (CUT)
**Reason**: Radar charts are misleading for 4-axis data. The enclosed area is a meaningless visual artifact that distorts comparison. The existing threat scatter plot already shows the same data more honestly.

#### 5D: Bullet Charts -- KPI Scorecard
- **Analysis**: `portfolio_scorecard` (M9)
- **Scope**: Only 3 KPIs with PULSE benchmarks (Avg Spend/Account/Month, Avg Txn/Account/Month, Average Ticket)
- **Design**: Horizontal bullet with qualitative bands at 70%/85%/100%/115% of benchmark, thick bar for actual value, thin line for benchmark target
- **File**: `charts/scorecard.py` (NEW)

**Research Insights**:
- Build with layered `go.Bar` traces (background bands) + thin `go.Scatter` line (target) + thick `go.Bar` (actual)
- Use 3 gray shades for qualitative bands: `#F0F0F0` (poor), `#D9D9D9` (acceptable), `#C0C0C0` (good)
- Actual bar uses `ACCENT` blue when at/above benchmark, `CORAL` when below
- Stack 3 KPIs vertically using `make_subplots(rows=3, cols=1, shared_xaxes=False)`

#### ~~5E: Waffle Chart~~ (CUT)
**Reason**: Member segments analysis produces only 4 rows (High Value, Active, Low Activity, Dormant). A 100-square waffle chart is visual overkill for 4 data points. The data table with colored percentage bars in Excel is clearer and more informative.

#### ~~5F: Sankey~~ (CUT)
**Reason**: `financial_services_detection` (M7) doesn't output the account_type -> category -> merchant flow structure needed for a Sankey. It outputs a flat table of merchants matched to financial service categories. Building the Sankey would require restructuring the M7 analysis to aggregate flows, which is out of scope for a visualization-only overhaul.

### Phase 6: Wire PNG Export + Excel Embedding

**PNG export**:
- Call `render_chart_png()` during `export_outputs()` for every chart in `result.charts`
- Save to `{output_dir}/charts/{analysis_name}.png`
- Gate behind new `outputs.chart_images: bool` toggle (separate from `outputs.excel`)

**Excel embedding**:
- Wire the existing `chart_png: bytes | None` parameter in `_write_analysis_sheet()`
- Use `openpyxl.drawing.image.Image` to embed below data table
- Position: row after last data row + 2 blank rows, column A
- Scale image to fit within 900px width in Excel

**Files**:
- `txn_analysis/pipeline.py` (MODIFY) -- add PNG rendering loop in `export_outputs()`
- `txn_analysis/exports/excel_report.py` (MODIFY) -- implement `chart_png` embedding
- `txn_analysis/charts/__init__.py` (MODIFY) -- update `CHART_REGISTRY` with new charts
- `txn_analysis/settings.py` (MODIFY) -- add `chart_images: bool = True` to `OutputConfig`

### Research Insights: Phase 6

**Dual scale strategy**:
- `scale=1` (72 DPI) for Excel-embedded PNGs -- fast to render, small file size, looks fine at Excel's zoom level
- `scale=3` (216 DPI) for standalone PNGs saved to disk -- crisp for presentations and reports
- Both use `width=900, height=500` base dimensions

**kaleido performance** (kaleido==0.2.1):
- Single-process, sequential rendering. Each PNG takes ~1.5s.
- 19 charts at scale=1: ~28s. At scale=3: ~40s. Both well under the 60s target.
- v1.0+ has a known 50x regression -- keep the pin at 0.2.1.
- kaleido reuses the Chromium process across calls, so batch rendering is efficient. No need for multiprocessing.

**openpyxl image embedding**:
```python
from openpyxl.drawing.image import Image as XlImage
from io import BytesIO

def _embed_chart(ws, png_bytes: bytes, start_row: int):
    img = XlImage(BytesIO(png_bytes))
    img.width = 900   # pixels
    img.height = 500
    ws.add_image(img, f"A{start_row}")
```

**Pillow dependency**: `openpyxl.drawing.image.Image` requires Pillow at runtime. Pillow is already an indirect dependency via kaleido, but add `Pillow>=9.0` to `requirements.txt` explicitly to avoid surprises.

**Error handling**: If kaleido fails for a single chart (e.g., empty figure), log a warning and skip that chart's PNG. Do not abort the entire export.

---

## Chart Registry After Completion

```
CHART_REGISTRY (19 entries, composite keys for multi-chart analyses):

  # M1: Overall (4 charts -- 3 lollipops + 1 treemap)
  "top_merchants_by_spend"              -> chart_top_by_spend (lollipop)
  "top_merchants_by_transactions"       -> chart_top_by_transactions (lollipop)
  "top_merchants_by_accounts"           -> chart_top_by_accounts (lollipop)
  "top_merchants_by_spend:treemap"      -> chart_merchant_treemap (treemap)

  # M2: MCC (1 triple-subplot lollipop -- special handler, not in registry)
  mcc_comparison                        -> chart_mcc_comparison (special handler)

  # M3: Business (3 lollipops)
  "business_top_by_spend"               -> chart_business_top_by_spend
  "business_top_by_transactions"        -> chart_business_top_by_transactions
  "business_top_by_accounts"            -> chart_business_top_by_accounts

  # M4: Personal (3 lollipops)
  "personal_top_by_spend"               -> chart_personal_top_by_spend
  "personal_top_by_transactions"        -> chart_personal_top_by_transactions
  "personal_top_by_accounts"            -> chart_personal_top_by_accounts

  # M5: Trends (3 charts -- bump replaces rank trajectory)
  "monthly_rank_tracking"               -> chart_bump_rank (bump chart)
  "growth_leaders_decliners"            -> chart_growth_leaders (diverging bar)
  "new_vs_declining_merchants"          -> chart_cohort_summary (grouped bar)

  # M6: Competitor (3 charts)
  "competitor_threat_assessment"         -> chart_threat_scatter (scatter + quadrants)
  "competitor_segmentation"              -> chart_segmentation_bar (stacked bar)
  "competitor_categories"                -> chart_competitor_heatmap

  # M9: Scorecard (1 new)
  "portfolio_scorecard"                  -> chart_scorecard_bullets (bullet row)
```

### Research Insights: Registry Design

**Composite key pattern** for analyses that need 2+ charts:
```python
CHART_REGISTRY: dict[str, ChartFunc] = {
    "top_merchants_by_spend": chart_top_by_spend,
    "top_merchants_by_spend:treemap": chart_merchant_treemap,
    # ...
}
```

The `create_charts()` loop matches on prefix:
```python
for result in results:
    for key, func in CHART_REGISTRY.items():
        if key == result.name or key.startswith(f"{result.name}:"):
            fig = func(result, config)
            charts[key] = fig
```

This avoids the duplicate-key bug in the original plan (Python dicts silently drop duplicate keys).

---

## Acceptance Criteria

### Functional
- [x] ~~Custom `"consultant"` Plotly template registered and used by all charts~~ (via lazy `ensure_theme()`)
- [ ] Custom `"consultant"` Plotly template lazily registered via `ensure_theme()` and used by all charts
- [ ] All 9 horizontal bar charts replaced with lollipop charts (2-trace approach)
- [ ] Gray + accent color pattern on all lollipop charts (top 3 accent, rest gray)
- [ ] Insight-driven titles on every chart (computed dynamically from data)
- [ ] Source footer applied as post-processing in `create_charts()`, not in individual chart functions
- [ ] Direct labeling replaces legends on line charts (bump)
- [ ] 3 new chart types created: treemap, bump, bullet
- [ ] `render_chart_png()` called during export; PNGs saved to `{output_dir}/charts/`
- [ ] Chart PNGs embedded in Excel sheets below data tables
- [ ] All existing 263 tests still pass
- [ ] New tests for each chart function (non-empty fig for valid data, empty fig for empty data)

### Non-Functional
- [ ] No new pip dependencies except explicit `Pillow>=9.0` (already indirect via kaleido)
- [ ] PNG export of 19 charts completes in < 60 seconds (expect ~28s at scale=1)
- [ ] Georgia font fallback to Times New Roman if unavailable
- [ ] Charts degrade gracefully for empty/sparse data (e.g., 1 merchant, 1 month)
- [ ] Single color authority in `theme.py` -- no more 4 competing sources
- [ ] All chart functions return `go.Figure` with typed signatures
- [ ] Zero uses of deprecated `._append()` method

---

## Implementation Phases

| Phase | Scope | Files Changed | Est. New Tests |
|-------|-------|--------------|----------------|
| 1 | Theme foundation + helpers | 3 (theme.py new, settings.py, charts/__init__.py) | 7 |
| ~~2~~ | ~~Annotation helpers~~ | ~~MERGED INTO PHASE 1~~ | -- |
| 3 | Lollipop migration | 4 (bar_charts.py, overall.py, business.py, personal.py) | 10 |
| 4 | Restyle specialized charts | 2 (trends.py, competitor.py) | 7 |
| 5 | New chart types (treemap, bump, bullet) | 3 (scorecard.py new, overall.py, trends.py) | 8 |
| 6 | PNG export + Excel embed | 4 (pipeline.py, excel_report.py, charts/__init__.py, settings.py) | 6 |
| **Total** | | **10 files** (was 13) | **~38 tests** |

### Bug Fixes to Include
- [ ] Replace `._append()` with `pd.concat()` in `charts/trends.py`
- [ ] Remove hardcoded colors from `charts/overall.py`, `business.py`, `personal.py`
- [ ] Remove unused `BRAND_COLORS` entries from `settings.py`

---

## References

### Internal
- Current chart system: `txn_analysis/charts/` (8 files, 16 chart functions)
- Chart config: `txn_analysis/settings.py:28-35` (ChartConfig model)
- Unused PNG export: `txn_analysis/charts/__init__.py:108-122` (render_chart_png)
- Excel embedding stub: `txn_analysis/exports/excel_report.py:137` (chart_png param)
- Analysis registry: `txn_analysis/analyses/__init__.py:67-109` (31 analyses)

### External Design References
- [McKinsey Chart Principles](https://umbrex.com/resources/the-busy-consultants-guide-to-quantitative-charts/design-principles-for-mckinsey-quantitative-charts/)
- [Storytelling with Data -- Cole Nussbaumer Knaflic](https://www.storytellingwithdata.com/books)
- [Plotly Custom Templates](https://plotly.com/python/templates/)
- [Datawrapper -- Fonts for Data Visualization](https://www.datawrapper.de/blog/fonts-for-data-visualization)
- [McKinsey -- Year in Charts](https://www.mckinsey.com/featured-insights/year-in-review/year-in-charts)

### From Deepening Research
- kaleido 0.2.1 reuses Chromium subprocess for sequential chart rendering (~1.5s/chart)
- Plotly template registration: use `pio.templates["name"] = Template(...)` then `pio.templates.default = "name"`
- openpyxl `Image(BytesIO(png_bytes))` requires Pillow; set `.width` and `.height` before `ws.add_image()`
- Plotly `go.Scatter` with None breaks in x/y arrays creates disconnected line segments (efficient for lollipop stems)
