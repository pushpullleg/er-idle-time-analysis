# KPMG Consulting Engagement Index
## Quick Reference Guide to All Deliverables

**Hospital:** Meridian City ER  
**Challenge:** Improve ED efficiency: from 6.9 to 9+ patients/hour (+32% throughput)  
**Investment:** $840K | **Payback:** <3 weeks | **5-Yr NPV:** ~$65M  
**Timeline:** 12 weeks to pilot completion + 8 weeks full rollout  

---

## 🎯 The Opportunity (1-Minute Summary)

- **Problem:** 38.6-min post-triage wait queue (22% of total LOS)
- **Root Cause:** Doctor stage is bottleneck (107.3 min = 62% of LOS); not a staffing problem, a process problem
- **Evidence:** 2,179 idle-doctor events (14.5% of visits); 1,387 wasted patient-hours in Q1
- **Solution:** Real-time queue board + auto-dispatch + 1 NP fast-track
- **Result:** Post-triage wait ↓73% (38.6→8 min), throughput ↑32% (6.9→9.1/hr), no new MDs needed

---

## 📚 Engagement Folder Structure

```
KPMG_Consulting_Engagement/
│
├─ README.md                          ← START HERE (this folder overview)
├─ ENGAGEMENT_OVERVIEW.md             ← Engagement structure & success metrics
│
├─ 01_Executive_Deliverables/
│  └─ Executive_Summary.md            ← 10-page board-ready case (ROI, strategy, roadmap)
│
├─ 02_Process_Design/
│  ├─ Future_State_Workflow.md        ← Current vs. future swimlanes; key interventions
│  └─ [Additional: SOP checklists, dispatch rules, etc. TBD]
│
├─ 03_Analytics_Dashboards/
│  ├─ bottleneck_analysis.py          ← Python script to generate KPI dashboards
│  ├─ kpi_summary.txt                 ← Current-state fact sheet
│  ├─ los_distribution.png            ← Chart: LOS by stage (histogram + pie)
│  ├─ hourly_patterns.png             ← Chart: wait times & staffing by hour
│  └─ staffing_scenarios.png          ← Chart: throughput under 4 scenarios
│
├─ 04_Staffing_Models/
│  └─ Scenario_Analysis.md            ← 4 staffing scenarios (Scenario 2 = recommended)
│
├─ 05_Pilot_Implementation/
│  ├─ Pilot_Charter.md                ← 80-day pilot execution plan (timeline, KPIs, gates)
│  └─ [Additional: KPI dashboard template, issue tracker, etc. TBD]
│
├─ 06_Change_Management/
│  ├─ Change_Communications_Plan.md   ← 16-week phased comms (staff engagement, training)
│  └─ [Additional: Training slides, laminated cards, FAQ, etc. TBD]
│
└─ 07_Presentations/
   ├─ [C_Suite_Presentation.pptx - TBD]          ← 15-slide exec summary (30 min)
   ├─ [Operations_Workshop.pptx - TBD]           ← 20-slide process deep-dive (90 min)
   ├─ [Floor_Level_Briefing.pptx - TBD]          ← 10-slide staff overview (20 min)
   └─ [Steering_Committee_Update.pptx - TBD]     ← 8-slide weekly update (15 min)
```

---

## 📖 Document Guide: What to Read & When

### By Role

**Hospital CFO / Finance:**
1. **Executive_Summary.md** – Financial opportunity & ROI
2. **Scenario_Analysis.md** – Staffing costs & payback period
3. **Charts** – Scenario comparison (staffing_scenarios.png)
4. **Time:** 30 min

**ER Medical Director / Chief Nursing Officer:**
1. **Future_State_Workflow.md** – Process improvements (dispatch rules, NP model)
2. **Pilot_Charter.md** – Clinical governance & safety protocols
3. **Change_Communications_Plan.md** – Staff training approach
4. **Time:** 45 min

**Operations / ER Manager:**
1. **Future_State_Workflow.md** – Day-to-day workflow changes
2. **Pilot_Charter.md** – KPI tracking, daily standups, issue escalation
3. **Change_Communications_Plan.md** – Staff engagement & feedback loops
4. **Time:** 45 min

**Project Manager / Consultant:**
1. **README.md** (main folder) – Full engagement roadmap
2. **All documents** (complete deep-dive)
3. **Charts** – For dashboards & reporting
4. **Time:** 4–6 hours

**Clinical Staff (Doctors, Nurses, Registration):**
1. **Change_Communications_Plan.md** (staff sections only)
2. **Laminated quick-ref cards** (queue board how-to, dispatch rules)
3. **Training slides** (TBD – from Change Communications Plan template)
4. **Time:** 45 min training

**IT / Systems:**
1. **Future_State_Workflow.md** – Queue board & dispatch system requirements
2. **Pilot_Charter.md** – Tech rollout timeline, system issues escalation
3. **Time:** 30 min

---

## 🎯 Quick Navigation

### "I want to understand the business case"
→ **Executive_Summary.md** (10 min read)  
→ **Scenario_Analysis.md** (15 min read)  
→ **staffing_scenarios.png** (2 min visual)  

### "I want to understand the workflow changes"
→ **Future_State_Workflow.md** (20 min read + diagram review)  

### "I want to run the pilot"
→ **Pilot_Charter.md** (30 min read + checklist)  
→ **bottleneck_analysis.py** (run for dashboards)  

### "I want to drive staff adoption"
→ **Change_Communications_Plan.md** (30 min read)  
→ Print laminated quick-ref cards (from document template)  

### "I want the KPI data"
→ **kpi_summary.txt** (2 min read)  
→ **los_distribution.png**, **hourly_patterns.png**, **staffing_scenarios.png** (3 min visual review)  

---

## 📋 Key Documents at a Glance

| Document | Key Insights | Best For | Time |
|----------|--------------|----------|------|
| **Executive_Summary.md** | $5–6M opportunity, process not staffing, 25–35% throughput gain | Board, CEO, CFO | 10 min |
| **Future_State_Workflow.md** | Queue board, auto-dispatch, NP fast-track, parallel processing | Clinical, Ops | 20 min |
| **Scenario_Analysis.md** | 4 staffing models; Scenario 2 (process only) recommended | Finance, HR | 20 min |
| **Pilot_Charter.md** | 80-day pilot: timeline, KPIs, gates, governance | Project Lead | 30 min |
| **Change_Communications_Plan.md** | Staff messaging, training, feedback loops, adoption tracking | Change Lead, HR | 30 min |
| **kpi_summary.txt** | Current state metrics (LOS, wait times, throughput, staffing) | Dashboard, Reports | 5 min |
| **Charts (3 PNG files)** | Visual dashboards (LOS, hourly, scenarios) | Presentations, Steering | 5 min |

---

## 🚀 Implementation Roadmap (12 Weeks to Pilot Completion)

```
PHASE 1: DESIGN & PROCUREMENT (Weeks 1–2)
├─ Exec approval & budget allocation
├─ Clinical steering committee convenes
├─ Queue system vendor evaluation & selection
├─ NP job description & recruiting launched
└─ Dispatch rules designed (clinical validation)

PHASE 2: PILOT PREPARATION (Weeks 3–4)
├─ Staff training curriculum finalized
├─ KPI dashboards configured
├─ Shift handoff playbook drafted
└─ Day shift ready for launch

PHASE 3: PILOT EXECUTION (Weeks 5–10 = 6-week run)
├─ Go-live: Day shift only
├─ Daily standups (15 min)
├─ Weekly steering reviews (1 hour)
├─ Real-time KPI tracking
└─ Staff feedback loops active

PHASE 4: GO/NO-GO GATE & ANALYSIS (Weeks 9–10)
├─ Analyze pilot results vs. success thresholds
├─ Stakeholder debrief (what worked, what was hard)
├─ Executive go/no-go decision
└─ Rollout roadmap confirmation

PHASE 5: FULL SCALE-OUT (Weeks 11–20 if go approved)
├─ Evening shift deployment (Weeks 11–14)
├─ Night shift deployment (Weeks 15–17)
├─ All-shift stabilization (Weeks 18–20)
└─ Governance transition to ops (monthly reviews)

PHASE 6: SUSTAIN & OPTIMIZE (Months 6+)
├─ Monthly KPI scorecards
├─ Quarterly staff surveys
├─ Phase 2 decision (staffing augmentation?)
└─ Continuous process refinement
```

---

## ✅ Success Criteria (Pilot Must Meet All)

| Metric | Current | Target | Type |
|--------|---------|--------|------|
| Throughput (patients/hour) | 6.9 | **8.0+** | Primary |
| Post-triage wait (minutes) | 38.6 | **<12** | Primary |
| Doctor utilization (%) | 50% | **70%+** | Primary |
| Staff adoption (1–10) | – | **7+** | Primary |
| Safety incidents | – | **0** | Primary |
| Patient satisfaction (HCAHPS) | Baseline | **+5 pts** | Secondary |
| LWBS rate (%) | – | **<2%** | Secondary |
| Staff engagement survey | – | **+10 pts** | Secondary |

**Decision:** If all primary criteria met → Proceed to full scale-out. Otherwise → Extend pilot or redesign approach.

---

## 💰 Financial Summary

### Investment (Year 1)
| Item | Cost | Notes |
|------|------|-------|
| Queue board system (annual) | $80K | Software + hardware + support |
| EHR integration (one-time) | $120K | Custom dev + testing |
| KPMG consulting (16 weeks) | $400K | Design, pilot, training |
| Training & change mgmt | $60K | Curriculum, facilitation |
| NP salary (1 FTE, prorated) | $75K | Included in Phase 1 staffing |
| Contingency (10%) | $82.5K | – |
| **Total** | **$807.5K** | – |

### Return (Annual, Post-Pilot)
| Item | Value | Notes |
|------|-------|-------|
| Additional visits (throughput gain) | +18,900/year | 40–50 patients/day |
| Revenue @ $800/visit | **+$15.1M** | Conservative estimate |
| Net investment cost (amortized) | –$0.8M | Year 1 only |
| **Net annual benefit** | **+$14.3M** | Post-Year 1 recurring |
| Payback period | **<3 weeks** | From start of throughput gain |
| 5-year NPV (10% discount) | **~$65M** | Including staffing scenarios |

---

## 🎁 Ready-to-Use Templates & Tools

### Documents Ready Now
- ✅ Executive Summary
- ✅ Future State Workflow
- ✅ Scenario Analysis
- ✅ Pilot Charter
- ✅ Change Communications Plan
- ✅ KPI Summary (text)
- ✅ Analytics dashboards (3 PNG charts)

### Documents to Create (Next Week)
- ⏳ C-Suite Presentation (15 slides)
- ⏳ Operations Workshop (20 slides)
- ⏳ Floor-Level Briefing (10 slides)
- ⏳ Steering Committee Update (8 slides)
- ⏳ Laminated quick-ref cards (print-ready)
- ⏳ Training curriculum (60–90 min)
- ⏳ KPI dashboard (Excel/Tableau)
- ⏳ Issue tracker (shared Excel)

---

## 📞 How to Get Started

### Week 1 Actions
1. **Download all documents** from this folder
2. **Share Executive_Summary.md** with your executive sponsor
3. **Schedule kickoff meeting** (30 min with exec, clinical, ops leads)
4. **Approve Scenario 2** (process fixes + 1 NP)
5. **Allocate $807.5K budget**

### Week 2 Actions
1. **Convene clinical steering committee** – review workflow changes
2. **Begin queue system vendor evaluation** (procurement team)
3. **Draft NP job description** (HR team)
4. **Confirm pilot start date** (target: Week 5, Nov 24, 2025)

### Week 3–4 Actions
1. **Finalize dispatch rules** (clinical validation)
2. **Order queue system** (2–4 week lead time)
3. **Prepare staff training** (use Change Communications Plan template)
4. **Set up KPI dashboards** (run bottleneck_analysis.py script)

---

## 📊 Where to Find Specific Information

**"What's the post-triage wait time?"**
→ kpi_summary.txt (38.6 min) or los_distribution.png (histogram)

**"How many idle doctor events happened?"**
→ kpi_summary.txt (2,179 events, 14.5% of visits)

**"What's the annual revenue opportunity?"**
→ Executive_Summary.md (+$15.1M annually) or Scenario_Analysis.md (detailed financials)

**"How do I improve patient flow?"**
→ Future_State_Workflow.md (5 interventions: queue board, dispatch, handoff, NP, parallelism)

**"What's the ROI?"**
→ Scenario_Analysis.md (Scenario 2: $14.3M benefit / $0.8M investment = 1,600% ROI)

**"How do I train staff?"**
→ Change_Communications_Plan.md (45-min group training, 10-min 1-on-1 walkthroughs)

**"When do we make the go/no-go decision?"**
→ Pilot_Charter.md (Week 10, based on success criteria)

**"What's the risk?"**
→ Executive_Summary.md → Risk Mitigation section (staff resistance, tech delays, etc.)

---

## 🔄 Document Update Schedule

- **Weekly** (during pilot): Pilot_Charter.md → Weekly KPI scorecard updates
- **Monthly**: Executive_Summary.md → Financial tracking updates
- **Quarterly**: All documents → Business review updates
- **Post-Pilot**: All → Lessons learned, recommendations for Phase 2

---

## 📌 Key Takeaways

1. **The Problem:** Post-triage wait (38.6 min) due to doctor bottleneck (107.3 min cycle), not staffing
2. **The Solution:** Process fixes (queue board, dispatch, NP fast-track) without new MDs
3. **The Impact:** +32% throughput (6.9 → 9.1 patients/hour), +$15M annual revenue, <3 week payback
4. **The Timeline:** 12 weeks to pilot completion, 8 weeks to full scale-out
5. **The Recommendation:** Start with Scenario 2 (process only); add staffing later if demand warrants

---

## 🎯 Next Step

**→ Open [README.md](./README.md) for full engagement overview**  
**→ Open [Executive_Summary.md](./01_Executive_Deliverables/Executive_Summary.md) for board presentation**  
**→ Open [Pilot_Charter.md](./05_Pilot_Implementation/Pilot_Charter.md) to start pilot execution**  

---

**Engagement Status:** ✅ Ready for Stakeholder Review & Approval  
**Prepared by:** KPMG Consulting ER Transformation Practice  
**Date:** November 9, 2025  
**Contact:** [Your Engagement Partner]

