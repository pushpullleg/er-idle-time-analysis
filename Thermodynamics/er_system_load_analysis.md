# ⚙️ Hourly ER System Load Simulation and Insight Analysis  
**Dataset:** Meridian Hospital Emergency Department (ER)

---

## 🧠 Context

We’re modeling **Meridian City Hospital’s Emergency Department** as a single dynamic system that evolves *hour by hour*.  
The goal is to understand how workload pressure builds and dissipates based on **arrivals**, **exits**, and **backlog**.

### System Dynamics Formula
```python
System_Load[t] = Arrivals[t] - Exits[t] + Backlog[t-1]
Backlog[t] = max(0, System_Load[t])
```

This represents how each hour’s arrivals and discharges affect the accumulated queue (backlog), which reflects the *operational load* on the system.

---

## 🎯 Objective

Simulate, analyze, and visualize **hourly load patterns over the last 90 days**, revealing:
- Load peaks and troughs  
- System recovery times  
- Lag correlations between arrivals and exits  
- Throughput efficiency

---

## 🧩 Tasks

### 1. Data Preparation
- Convert timestamps to hourly bins (`2025-01-01 00:00`, `2025-01-01 01:00`, etc.)  
- Aggregate counts for **Arrivals** and **Exits** per hour  
- Fill missing hours with zeros (continuous time series)  
- Initialize `Backlog[0] = 0` or from the first known backlog value  

---

### 2. Simulation Logic
For each hour `t`:
```python
Backlog[t] = max(0, Backlog[t-1] + Arrivals[t] - Exits[t])
System_Load[t] = Backlog[t]
```

Run this sequentially for **90 days** (≈ 2,160 hours).

---

### 3. Metrics and Analysis
- **Descriptive stats:** min, max, mean, median, std. dev of `System_Load`
- **Temporal:** timestamps of max/min load
- **Percentiles:** 75th, 90th, and 95th percentile load levels
- **Peak Duration:** continuous hours above threshold
- **Lag Correlation:** arrivals vs exits (1–6 hour lags)
- **Volatility Index:** rolling std. dev (24-hour window)
- **Throughput Ratio:** average `Exits / Arrivals` by day or week

---

### 4. Visualization Goals
- **Line Chart:** `System_Load` over time (smooth curve)
- **Overlay Plot:** Arrivals and Exits to visualize balance
- **Heatmap:** Hour of Day × Day of Week showing average load
- **Highlights:** Annotate peaks and recovery periods

---

### 5. Output Files
| File Name | Description |
|------------|-------------|
| `er_hourly_load_simulation.csv` | Clean dataset with all computed fields |
| `er_hourly_load_trend.png` | Time-series visualization of hourly load |
| `er_heatmap.png` | Hourly/day pattern visualization |
| `er_load_insights.txt` | Text summary with analysis & interpretations |

---

## 🧮 Recommended Tools
- **Python:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy.stats`
- **Optional:** `plotly` (interactive charts), `statsmodels` or `prophet` (forecasting)

---

## 📖 Interpretation Guide (for the Agent’s Report)

After running analysis, the agent should **summarize insights like a data scientist:**

### 1. Load Behavior
- Identify when the ER operates under heavy pressure (e.g., late evenings, weekends).  
- Describe whether load is stable, cyclical, or trending upward.

### 2. Peaks and Recovery
- Quantify **duration of overload** (continuous high-load hours).  
- Measure **average recovery time** — hours required to return to baseline.

### 3. Response Dynamics
- Interpret **lag correlation** between arrivals and exits.  
  Example: exits lag arrivals by 2 hours → slower throughput.  
- Suggest operational meaning: shift overlaps, triage delays, bed turnover issues.

### 4. System Efficiency
- Discuss **throughput ratio** trends (`Exits / Arrivals`).  
- Identify systematic under- or over-capacity periods.

### 5. Strategic Insights
- Recommend potential optimizations:  
  - Adjust staffing schedules  
  - Improve discharge flow  
  - Balance shift coverage  
  - Streamline triage timing  

---

## ✅ Goal

Produce a **90-day, hour-by-hour simulation** of ER load evolution that quantifies system stress, identifies inefficiencies, and uncovers actionable operational patterns.

---

**End of File**
