# KPMG Consulting Engagement: Meridian City ER Efficiency
## From Bottleneck to Breakthrough

**Prepared by:** KPMG Consulting ER Transformation Practice  
**Date:** November 2025  
**Status:** Ready for Stakeholder Review & Pilot Launch  

---

## 📊 Engagement Overview

This folder contains a complete consulting engagement package for improving Meridian City ER efficiency. The analysis reveals a **$5–6M annual opportunity** to increase throughput by 25–35% through **process optimization, not staffing increases**.

**Key Finding:** The post-triage wait queue (38.6 min avg) exists because the doctor/treatment stage is the bottleneck (107.3 min cycle time = 62% of total LOS), not because of upstream delays.

---

## 📁 Folder Structure

### 1. **01_Executive_Deliverables/**
**Purpose:** Board-ready communications and fact packs

- **Executive_Summary.md** – 10-page strategic overview with financials, opportunity quantification, and board-level decision framework
  - Current state analysis
  - Root cause diagnosis (Theory of Constraints applied)
  - Financial impact ($5–6M annual upside)
  - Implementation roadmap
  - Success scenarios & KPIs

**Use this for:** Executive steering committee, board presentations, investment approval

---

### 2. **02_Process_Design/**
**Purpose:** Operational redesign blueprints and workflow improvements

- **Future_State_Workflow.md** – Detailed process maps showing current vs. optimized patient flow
  - Current-state swimlanes (pain points identified)
  - Future-state swimlanes (with queue board, auto-dispatch, NP fast-track)
  - Key intervention details:
    - Real-time queue board (central dashboard)
    - Automated dispatch rules (patient → doctor matching)
    - Structured shift handoff playbook (15 min, standardized)
    - Room turnover SOP (5-min max)
    - Fast-track pathway for low-acuity cases (NP model)
    - Parallel processing during patient wait

**Use this for:** Clinical leadership, process improvement team, workflow redesign workshops

---

### 3. **03_Analytics_Dashboards/**
**Purpose:** Data-driven analytics and visualization tools

- **bottleneck_analysis.py** – Python script that analyzes final_data.csv and generates KPI dashboards
  - Real-time KPI summaries
  - Distribution plots (LOS, wait times, cycles)
  - Hourly pattern analysis
  - Staffing scenario comparisons
  
**Generated outputs:**
- `kpi_summary.txt` – Executive KPI fact sheet (text format)
- `los_distribution.png` – Histogram of LOS by stage
- `hourly_patterns.png` – Wait times & staffing by hour of day
- `staffing_scenarios.png` – Throughput comparison (4 staffing models)

**Use this for:** Dashboards, monitoring, steering committee reviews

---

### 4. **04_Staffing_Models/**
**Purpose:** Staffing scenarios and financial modeling

- **Scenario_Analysis.md** – Comprehensive staffing & scheduling analysis
  - **Scenario 1: Do Nothing** – Baseline (no improvement)
  - **Scenario 2: Process Fixes Only** (RECOMMENDED START) – +1 NP, +32% throughput, $14.26M annual benefit, ROI 1,600%
  - **Scenario 3: Moderate Augmentation** – +1 MD + 1 NP, +65% throughput, $29.81M annual benefit
  - **Scenario 4: Aggressive Expansion** – +2 MD + 2 NP, +81% throughput
  
- **Recommended phased approach:**
  - Phase 1 (Weeks 1–12): Process optimization only (Scenario 2)
  - Phase 2 (Months 4–6): Monitor demand, then decide on staffing augmentation (Scenario 3)
  - Rationale: Validate process benefits first, avoid over-hiring, test NP model risk-free

**Use this for:** Finance review, staffing planning, board financials

---

### 5. **05_Pilot_Implementation/**
**Purpose:** Pilot charter, KPI framework, and execution plan

- **Pilot_Charter.md** – Complete 80-day pilot specification (6-week execution + 2-week analysis)
  - Pilot objectives & success criteria
  - Timeline (Weeks 1–10)
  - Governance structure & decision cadence
  - KPI tracking (real-time dashboards + weekly scorecards)
  - Issue escalation matrix (Red/Orange/Yellow/Green)
  - Go/No-Go decision framework
  - Rollout plan (conditional on pilot success)
  - Sustainability & handoff to operations

- **KPI Tracking Framework:**
  - Primary: Throughput, LOS, Post-triage wait, Doctor utilization
  - Secondary: Patient satisfaction, LWBS rate, Safety incidents
  - Business metrics: Revenue impact, staff engagement
  - Weekly report card template

**Use this for:** Pilot execution, daily standups, steering reviews, leadership accountability

---

### 6. **06_Change_Management/**
**Purpose:** Communications, training, and stakeholder engagement

- **Change_Communications_Plan.md** – 16-week phased communications strategy
  - Stakeholder segmentation (executives, clinicians, frontline staff, support functions)
  - Role-specific messaging (addressing unique concerns)
  - Communication timeline (pre-pilot, pilot, post-pilot)
  - All-hands announcements (sample scripts)
  - Weekly newsletters (template)
  - FAQ sheet (30+ Q&As by audience)
  - Laminated quick-reference cards for every workstation
  - Training curriculum outline
  - Feedback loops (surveys, huddles, forums)
  - Success metrics for adoption

**Use this for:** Communications team, training lead, staff engagement

---

### 7. **07_Presentations/**
**Purpose:** Slide decks and presentation materials for various audiences

*To be created based on deliverables above. Templates:*
- C-Suite Presentation (15 slides, 30 min) – Executive brief, ROI, decision gate
- Operations Workshop (20 slides, 90 min) – Process deep-dive, dispatch rules, staffing
- Floor-Level Briefing (10 slides, 20 min) – What's changing, why, how to use new system
- Steering Committee Update (8 slides, 15 min) – Weekly KPI review, issues, decisions

---

## 🎯 Key Deliverables Summary

| Deliverable | Document | Purpose | Audience |
|-------------|----------|---------|----------|
| **Strategy & Opportunity** | Executive Summary | Board-level case for action | Board, CFO, COO |
| **Process Design** | Future State Workflow | How to redesign operations | Clinical, Ops |
| **Analytics** | Dashboard Scripts & Charts | Real-time KPI visibility | All leaders |
| **Financials** | Scenario Analysis | ROI & staffing trade-offs | Finance, CFO |
| **Execution Plan** | Pilot Charter | How to run 80-day pilot | Project, Clinical |
| **Change Mgmt** | Communications Plan | Staff engagement & adoption | HR, Comms |

---

## 💡 Critical Insights (Theory of Constraints)

### The Problem
**Throughput is NOT constrained by registration or triage—it's constrained by the doctor/treatment stage.**

- Doctor cycle time: 107.3 min (62% of total LOS)
- Post-triage wait: 38.6 min (queue forms due to slow downstream)
- Doctor utilization: Only 50% (despite busy patients)

**Why?** Manual patient-to-doctor assignment creates 2,179 idle-doctor events per quarter (14.5% of visits) where doctors are available but patients aren't routed to them.

### The Solution
**Don't hire more doctors. Fix the queue visibility & dispatch process.**

- Real-time queue board → Doctors see waiting patients instantly
- Auto-dispatch rules → System routes patient to available doctor
- Fast-track NP → Handles 20% of low-acuity cases (shorter cycle)
- Parallel processing → Lab/imaging ordered during wait

**Expected outcome:** Post-triage wait drops 73% (38.6 → 8-10 min); throughput rises 32% (6.9 → 9.1 patients/hour) without new hiring.

### The Math
```
Current: 3.2 doctors × (60 min/107.3 min cycle) = 1.8 patients/doctor/hr × 3.2 = 5.8 patients/hr avg
         (With 50% utilization in queue events, effective throughput ≈ 6.9 patients/hr observed)

Future:  3.2 doctors × (60 min/85 min cycle) = 2.12 patients/doctor/hr × 3.8 (with NP) = 8.1 patients/hr
         (With 75% utilization via queue visibility, actual ≈ 9.1 patients/hr)

Gain: +2.2 patients/hour (+32%) = 40–50 more patients/day = +$15M annual revenue
Investment: $840K → Payback in <3 weeks
```

---

## 📋 How to Use This Engagement Package

### Step 1: Executive Alignment (Week 1)
1. Share **Executive_Summary.md** with C-suite
2. Present **Staffing_Scenarios.md** (ROI analysis)
3. Secure approval for Scenario 2 (process fixes + 1 NP)
4. Allocate $840K budget for consulting, tech, and training

### Step 2: Clinical Design (Week 2)
1. Convene clinical steering committee
2. Review **Future_State_Workflow.md** with ER Medical Director
3. Design dispatch rules (clinical validation)
4. Finalize shift handoff playbook

### Step 3: Pilot Preparation (Weeks 3–4)
1. Procure queue management system (2–4 week lead time)
2. Hire/promote 1 NP for fast-track
3. Conduct staff training (use **Change_Communications_Plan.md** materials)
4. Set up KPI dashboards (run **bottleneck_analysis.py** script)

### Step 4: Pilot Execution (Weeks 5–10)
1. Launch day shift pilot (6 weeks)
2. Daily standups using **Pilot_Charter.md** governance
3. Weekly KPI reviews (track against success criteria)
4. Real-time issue escalation (Red/Orange/Yellow framework)
5. Weekly staff feedback surveys & huddles

### Step 5: Go/No-Go Decision (Week 10)
1. Analyze pilot results against success thresholds
2. Present Go/No-Go decision to executive sponsor
3. If Go: Proceed to Phase 3 (scale to all shifts)

### Step 6: Full Rollout (Weeks 11–20)
1. Cascade training to evening/night shifts
2. Deploy queue system hospital-wide
3. Adjust dispatch rules for low-volume periods
4. Transition governance to operations (monthly reviews vs. weekly)

### Step 7: Sustain & Optimize (Months 6+)
1. Monthly KPI scorecards (track sustained improvement)
2. Quarterly staff surveys (adoption, satisfaction)
3. Evaluate Phase 2 (staffing augmentation) based on demand
4. Plan tech upgrades (EHR integration, predictive staffing models)

---

## 🚀 Success Criteria (90-Day Pilot)

**Primary KPIs (Must achieve all to proceed to scale):**
| KPI | Current | Target | Status |
|-----|---------|--------|--------|
| Throughput (patients/hour) | 6.9 | 8.0+ | ❓ |
| Post-triage wait (minutes) | 38.6 | <12 | ❓ |
| Doctor utilization (%) | 50% | 70%+ | ❓ |
| Staff adoption rating (1–10) | – | 7+ | ❓ |
| Safety incidents | – | 0 | ❓ |

**Business outcomes:**
- Zero patient harm
- Patient satisfaction maintained or improved
- Staff engagement survey +10 points
- Annual revenue impact: +$15M (from pilot scale-up)

---

## 📞 Engagement Team

| Role | Responsibility | Escalation |
|------|-----------------|-----------|
| **Executive Sponsor** | Budget, blocker removal | Board |
| **Clinical Lead** | Workflow design, quality, safety | Medical Director |
| **Operations Lead** | Daily execution, KPI tracking | VP Operations |
| **IT Lead** | System setup, integrations | CIO |
| **NP Lead** | Fast-track protocols, staff training | Chief Nursing Officer |
| **Project Manager** | Timeline, comms, documentation | Executive Sponsor |

**Weekly Steering Committee:** Exec Sponsor + Clinical Lead + Operations Lead + Project Manager + CFO (to track financials)

---

## 📊 Recommended Next Actions (This Week)

**Week 1 Priorities:**
- [ ] **Monday:** Executive kickoff meeting (30 min, review Executive_Summary.md)
- [ ] **Tuesday:** Approve Scenario 2 (process fixes + 1 NP)
- [ ] **Wednesday:** Allocate $840K budget
- [ ] **Thursday:** Confirm pilot start date (target: Week 5, Nov 24, 2025)
- [ ] **Friday:** Begin queue system vendor evaluation (procurement team)

**Deliverables Due Week 2:**
- Signed pilot charter (Executive_Summary + Pilot_Charter.md)
- NP job description & recruiting plan
- Queue system vendor proposal (3–5 options)
- Clinical steering committee member list

---

## 📖 Reading Guide

**If you have 15 minutes:** Read **Executive_Summary.md** (Overview)  
**If you have 30 minutes:** Read Executive Summary + **Scenario_Analysis.md** (Business case)  
**If you have 1 hour:** Read Executive Summary + Scenario Analysis + **Pilot_Charter.md** (Implementation)  
**If you have 2 hours:** Read all of the above + **Future_State_Workflow.md** (Process deep-dive)  
**If you're leading the pilot:** Read everything in this folder + run **bottleneck_analysis.py** to generate dashboards

---

## 🎁 Included Tools & Templates

**Python Analytics:**
- `bottleneck_analysis.py` – Generate KPI summaries, distribution plots, scenario comparisons

**Markdown Documents:**
- Executive Summary, Future State Workflow, Staffing Scenarios, Pilot Charter, Communications Plan

**Laminated Quick-Ref Cards** (to be printed):
- Queue Board How-To
- Dispatch Rules Flowchart
- Shift Handoff Checklist

**Excel Templates** (to be created):
- KPI Tracking Dashboard
- Issue Log & Escalation Matrix
- Staff Feedback Survey
- Go/No-Go Decision Checklist

**Slide Decks** (to be created):
- C-Suite Presentation (15 slides)
- Operations Workshop (20 slides)
- Floor-Level Briefing (10 slides)

---

## 📞 Questions?

**For Strategic Questions:**
Contact: [Your Engagement Partner Name]
Email: [Your Email]
Phone: [Your Phone]

**For Operational Questions:**
Contact: [Your Project Manager Name]
Email: [Your Email]
Phone: [Your Phone]

---

## 📌 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 9, 2025 | Initial engagement package created; all core documents delivered |
| – | – | – |

---

## ✅ Engagement Checklist

**Pre-Pilot (Weeks 1–4):**
- [ ] Executive approval & budget allocation
- [ ] Clinical steering committee convened
- [ ] Queue system vendor selected & contract signed
- [ ] NP recruited/promoted
- [ ] Staff training curriculum finalized
- [ ] Dispatch rules clinically validated
- [ ] KPI dashboards tested

**Pilot Phase (Weeks 5–10):**
- [ ] Day shift pilot launched (Week 5)
- [ ] Daily standups initiated
- [ ] Real-time KPI tracking active
- [ ] Weekly steering committee updates
- [ ] Staff feedback loops active
- [ ] Go/No-Go gate review (Week 10)

**Rollout Phase (Weeks 11–20):**
- [ ] Go decision confirmed
- [ ] Evening shift training & deployment
- [ ] Night shift training & deployment
- [ ] Governance transitioned to operations
- [ ] Monthly KPI reviews initiated

---

**Next: Review this document with stakeholders, schedule kickoff, proceed to Step 1 above.**

---

*Prepared by: KPMG Consulting ER Transformation Practice*  
*Meridian City Hospital System*  
*November 2025*

