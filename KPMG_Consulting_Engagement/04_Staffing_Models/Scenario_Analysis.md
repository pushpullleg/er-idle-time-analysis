# Staffing & Scheduling Analysis
## Scenario Modeling for Throughput Improvement

---

## Current Staffing Reality (Q1 2025 Data)

### Baseline Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| **Avg Doctors On Duty** | 3.2 per shift | Min: 1, Max: 5 |
| **Avg Nurses On Duty** | 8.0 per shift | Min: 3, Max: 11 |
| **Doctor Utilization Rate** | ~50% | (Target: 75–80%) |
| **Patients/Doctor/Hour** | 1.8 | (Bottleneck constraint) |
| **Current Throughput** | 6.9 patients/hour | 3.2 doctors × 1.8 patients/doctor/hr |
| **Avg Doctor Cycle Time** | 107.3 min | Registration → Exit (per patient) |

### Why Utilization is Only 50%?
- **2,179 idle-doctor events** (14.5% of visits): Doctors available but patients not assigned
- **Root cause:** Manual assignment → Information gap → Coordination delays
- **Not a staffing problem:** Adding doctors won't help if assignment process is broken

---

## Scenario Analysis: Process vs. Staffing Levers

### Scenario 1: Do Nothing (Baseline)

| Metric | Value |
|--------|-------|
| Doctors on duty | 3.2 avg |
| Doctor utilization | 50% |
| Throughput | 6.9 patients/hour |
| Annual visits | 61,000 |
| Revenue @ $800/visit | $48.8M |
| Investment | $0 |
| **Net annual benefit** | **$0** |

---

### Scenario 2: Process Fixes Only (Queue Board + Auto-Dispatch + NP Fast-Track)
#### *No additional staffing*

**Assumptions:**
- Queue board + auto-dispatch eliminates 2–3 min coordination delays per patient
- Parallel processing during wait reduces doctor cycle from 107.3 → 85 min
- NP fast-track handles 20% of low-acuity patients (40–50 min LOS vs. 107 min)

**Model:**
```
Current patient mix (simple calculation):
├─ 80% complex cases (needs MD): 1.8 patients/hr × 3.2 docs × 0.80 = ~4.6 patients/hr
└─ 20% simple cases (can use NP): 1.8 patients/hr × 3.2 docs × 0.20 = ~1.15 patients/hr

Future (with process fixes):
├─ 80% complex: Cycle 107.3 → 85 min
  → 3.2 docs × 1.8 patients/doc/hr × (107.3/85) = 3.2 × 2.28 = 7.3 patients/hr
├─ 20% simple + NP fast-track:
  → NP cycles faster: 40–50 min vs. 85 min MD time
  → 1 NP equivalently handles 2 patients × MD rate = ~1.8 patients/hr
└─ Total: 7.3 + 1.8 = 9.1 patients/hr

Staffing: Same 3.2 MDs + 1 NP (~$150K/year)
```

**Results:**

| Metric | Current | Future | Change |
|--------|---------|--------|--------|
| **Doctors (MD) on duty** | 3.2 | 3.2 | No change |
| **NPs** | 0 | 1.0 | +1 FTE |
| **Doctor utilization** | 50% | 75% | +25 pts |
| **Throughput (patients/hr)** | 6.9 | 9.1 | **+2.2 (+32%)** |
| **Annual visits** | 61,000 | 79,900 | **+18,900** |
| **Annual revenue @ $800/visit** | $48.8M | $63.9M | **+$15.1M** |
| **Investment (yr 1)** | – | $690K consulting + $150K NP salary = $840K | |
| **Payback period** | – | 0.8 months (21 days) | **Immediate ROI** |
| **Net annual benefit** | – | **$14.26M** | **ROI: 1,600%** |

---

### Scenario 3: Moderate Staffing Increase (Add 1 MD + 1 NP)

**Assumptions:**
- Same process improvements as Scenario 2
- Add 1 additional MD to baseline
- Add 1 NP for fast-track

**Model:**
```
Total MD capacity: 4.2 (from 3.2) + 1 NP
└─ 80% complex: 4.2 × 2.28 = 9.6 patients/hr
└─ 20% simple + NP: 1.8 patients/hr
└─ Total: 11.4 patients/hr
```

**Results:**

| Metric | Current | Scenario 3 | Change |
|--------|---------|-----------|--------|
| **Doctors (MD)** | 3.2 | 4.2 | +1.0 |
| **NPs** | 0 | 1.0 | +1.0 |
| **Throughput (patients/hr)** | 6.9 | 11.4 | **+4.5 (+65%)** |
| **Annual visits** | 61,000 | 99,800 | **+38,800** |
| **Revenue** | $48.8M | $79.8M | **+$31M** |
| **Additional cost (salaries)** | – | $350K MD + $150K NP = $500K | |
| **Total investment** | – | $690K consulting + $500K salaries = $1.19M | |
| **Net annual benefit** | – | **$29.81M** | **ROI: 2,500%** |

---

### Scenario 4: Aggressive Staffing (Add 2 MDs + 2 NPs + Extra Nurses)

**Assumptions:**
- Process improvements + significant staffing boost
- Better handles surge hours
- Enables 24/7 NP coverage

**Model:**
```
Total MD capacity: 5.2 + 2 NPs
└─ 80% complex: 5.2 × 2.28 = 11.9 patients/hr
└─ 20% simple + 2 NPs: 3.6 patients/hr
└─ Total: 15.5 patients/hr

Realistic ceiling (space/room constraints): 12.5 patients/hr
```

**Results:**

| Metric | Current | Scenario 4 | Change |
|--------|---------|-----------|--------|
| **Doctors (MD)** | 3.2 | 5.2 | +2.0 |
| **NPs** | 0 | 2.0 | +2.0 |
| **Nurses** | 8.0 | 10.5 | +2.5 |
| **Throughput (patients/hr)** | 6.9 | 12.5 | **+5.6 (+81%)** |
| **Annual visits** | 61,000 | 109,500 | **+48,500** |
| **Revenue** | $48.8M | $87.6M | **+$38.8M** |
| **Additional cost (salaries)** | – | $700K (MDs) + $300K (NPs) + $250K (nurses) = $1.25M | |
| **Total investment** | – | $690K consulting + $1.25M salaries = $1.94M | |
| **Net annual benefit** | – | **$36.86M** | **ROI: 1,900%** |

---

## Comparison: Which Scenario to Choose?

| Aspect | Scenario 2 | Scenario 3 | Scenario 4 |
|--------|-----------|-----------|-----------|
| **Staffing changes** | +1 NP | +1 MD, +1 NP | +2 MD, +2 NP, +2.5 nurses |
| **Throughput gain** | +32% | +65% | +81% |
| **Investment** | $0.84M | $1.19M | $1.94M |
| **Annual benefit** | $14.26M | $29.81M | $36.86M |
| **ROI** | 1,600% | 2,500% | 1,900% |
| **Risk level** | Low (process only) | Medium (1 new hire) | High (6+ new roles, space constraints) |
| **Time to value** | 4–6 weeks | 8–12 weeks | 16–20 weeks |
| **Implementation effort** | Moderate | Medium | High |

---

## Recommended Path: Scenario 2 → Scenario 3 (Phased)

### Phase 1 (Weeks 1–12): Process Optimization (Scenario 2)
- Install queue board + auto-dispatch
- Implement structured shift handoffs
- Launch NP fast-track with 1 FTE
- **Expected outcome:** 32% throughput gain, $14M annual benefit, rapid ROI

### Phase 2 (Months 4–6): Monitor & Decide
- Run KPIs for 8 weeks post-Phase 1 launch
- Assess space/room constraints
- If throughput plateaus OR demand exceeds capacity → proceed to Phase 3

### Phase 3 (Months 7–12): Staffing Augmentation (Scenario 3)
- Hire 1 additional MD (if case volume warrants)
- Expand NP coverage to 2 FTEs
- **Expected outcome:** Additional 33% gain, cumulative 65% improvement

### Why Phased?
1. **Validates process first** – Many hospitals discover process fixes eliminate need for staff increases
2. **Reduces hiring risk** – Avoid over-staffing if demand doesn't support it
3. **Tests NP model** – 1 FTE fast-track NP is a low-risk pilot for expanded roles
4. **Manages change** – Staff digest process changes before adding new people
5. **Better ROI validation** – Separate "process benefit" from "staffing benefit" for board reporting

---

## Schedule Optimization: Shift-Level Staffing

### Current Pattern (Q1 Data)
Most shifts run 3–4 doctors, but utilization is low (50%) due to queue issues.

### Optimized Staffing Schedule (Post-Process Fix)

| Shift | Day | Volume Pattern | MD | NP | Nurses | Rationale |
|-------|-----|---|---|---|---|
| **Night** (11p–7a) | Sun–Thu | Low | 2 | 1 | 5 | Fewer patients; NP handles fast-track |
| **Night** | Fri–Sat | Medium | 3 | 1 | 6 | Weekend increase |
| **Day** (7a–3p) | Sun–Thu | Medium–High | 3 | 1 | 8 | Peak volume period |
| **Day** | Fri–Sat | High | 4 | 1 | 9 | Weekend peak |
| **Evening** (3p–11p) | Sun–Thu | High | 4 | 1 | 8 | Evening rush |
| **Evening** | Fri–Sat | Very High | 5 | 2 | 10 | Weekend peak |

**Benefit:** Staffing matches demand curve; reduces idle time during low-volume periods

---

## Key Assumptions & Sensitivity

### Critical Assumptions
1. **Patient mix doesn't change** – Still 20% low-acuity (NP candidates)
2. **Process improvements deliver as modeled** – Queue board + dispatch reduces delays by 2–3 min/patient
3. **Doctor cycle time improves from 107.3 → 85 min** – Via parallelism + NP taking simple cases
4. **Room constraints don't limit capacity** – Current 20–25 beds sufficient for modeled volumes
5. **NP productivity = 1.2–1.5 MDs in throughput** (due to shorter cases, higher utilization)

### Sensitivity Analysis

**What if process improvements deliver only 20% cycle time reduction (vs. 21%)?**
- Doctor cycle: 107.3 → 93 min (vs. 85 min)
- Throughput: ~8.4 patients/hr (vs. 9.1)
- Still +22% gain; ROI remains strong

**What if room turnover can't be optimized below 7 min (vs. 5 min)?**
- Minimal impact (5–10% overall LOS, primarily back-end logistics)
- Core delay is doctor cycle, not room turnover

**What if you can only hire 1 NP in Scenario 3 (not 1 MD)?**
- Throughput: ~8.8 patients/hr (vs. 11.4)
- Still +28% gain; less ambitious but lower hiring risk

---

## Implementation Milestones

### Month 1: Foundation
- Hire 1 NP (or commit budget)
- Install queue management system
- Design dispatch rules with clinical team
- **Target state:** Ready to pilot by Week 4

### Months 2–3: Pilot & Ramp
- Run on Day shift (highest volume) for 4 weeks
- Monitor: Throughput, wait times, staff adoption
- **Gate:** Achieve 8+ patients/hr, 75%+ doc utilization → Proceed

### Months 4–6: Scale & Optimize
- Roll out to all shifts
- Fine-tune dispatch rules based on pilot learnings
- **Target:** Sustain 9+ patients/hr, achieve $14M annual benefit

### Months 7–12: Phase 2 Evaluation
- Monthly KPI reviews
- Assess space/room constraints
- **Decision point:** Proceed with 1 additional MD + expanded NP coverage?

---

## Business Case Summary

**Scenario 2 (Recommended Start):**
```
Investment: $840K (consulting + 1 NP)
Year 1 Benefit: $14.26M (18,900 additional visits)
Payback: 21 days
5-Year NPV @ 10% discount: ~$65M
```

**Path to Scenario 3:**
```
Incremental Investment: +$350K additional MD salary
Incremental Benefit: +$15.5M annually
Combined 5-Year NPV: ~$130M
```

---

## Next Steps

1. **Approve Scenario 2** as starting point
2. **Recruit/promote 1 NP** (1–2 month hiring cycle)
3. **Procure queue board system** (2–4 week lead time)
4. **Convene clinical steering committee** to design dispatch rules
5. **Schedule pilot kickoff** for Week 5

---

**Prepared by:** KPMG Operations Consulting  
**Date:** November 2025

