# Pilot Charter & Implementation Plan
## Meridian City ER Efficiency Pilot

---

## Pilot Objectives

### Primary Goals
1. **Validate process improvements** – Prove queue board + auto-dispatch reduces post-triage wait by 50%+
2. **Test NP fast-track model** – Confirm NP can safely handle 20% of low-acuity cases
3. **Build staff confidence** – Demonstrate workflow changes are intuitive & reduce provider burden
4. **Quantify throughput gain** – Confirm 25–35% throughput improvement is achievable
5. **Identify scalability barriers** – Uncover real-world constraints before full rollout

### Success Criteria (80-Day Pilot)
| Metric | Target | Threshold |
|--------|--------|-----------|
| **Post-triage wait time** | 8–10 min | Must achieve <15 min avg |
| **Doctor utilization** | 75%+ | Must achieve 70%+ |
| **Throughput** | 8.5–9 patients/hr | Must achieve 8+ patients/hr |
| **Staff adoption** | 85%+ comfort rating | Must score 7+/10 |
| **Patient satisfaction** | Baseline +5 points | At least maintain baseline |
| **Safety incidents** | Zero | No new safety issues |

---

## Pilot Scope

### What's Included
✓ **Day shift only** (7 AM–3 PM, highest volume, most controlled)  
✓ **All patient types** (but fast-track subset analyzed separately)  
✓ **Queue board + dispatch system**  
✓ **Shift handoff playbook**  
✓ **Room turnover SOP**  
✓ **1 NP for fast-track (pilot subset)**  
✓ **Real-time KPI dashboards**  

### What's Excluded (Full Rollout Phase)
✗ Night/evening shifts (in scope for Week 5–8 of pilot)  
✗ Fast-track facility expansion (use existing space)  
✗ EHR deep integration (basic queue data only)  
✗ Staffing increases beyond 1 NP (defer to Phase 2)  

---

## Timeline

### Pre-Pilot (Weeks 1–2)
| Week | Activity | Owner | Deliverable |
|------|----------|-------|-------------|
| 1 | System procurement & setup | IT + Vendor | Queue board hardware installed, software configured |
| 1 | Stakeholder alignment | Project Lead | Kickoff meeting, RACI confirmed |
| 2 | Dispatch rules design | Clinical Lead + IT | Rules documented, decision tree finalized |
| 2 | Staff training prep | HR + Clinical | Training decks ready, role assignments set |

### Pilot Execution (Weeks 3–8, 42 Days)
| Week | Phase | Activity | KPIs Tracked |
|------|-------|----------|---|
| 3 | **Launch** | Queue board goes live; staff trained on new workflow | Day 1–7: Baseline metrics, system issues |
| 4–5 | **Ramp-up** | Staff practice dispatch rules, identify edge cases; daily huddles | Days 8–21: Throughput, wait times, adoption % |
| 6–7 | **Steady State** | Run with minimal daily interventions; gather feedback | Days 22–35: Stabilized KPIs, staff feedback themes |
| 8 | **Optimization** | Refine dispatch rules, resolve top issues | Days 36–42: Final KPI lock, prepare scale plan |

### Post-Pilot (Weeks 9–10)
| Activity | Owner | Output |
|----------|-------|--------|
| Analyze pilot data | Analytics Team | Results report, variance analysis |
| Staff debrief | Clinical Lead | "What went well / what was hard" feedback |
| Stakeholder review | Project Lead | Go/No-Go decision for full scale-out |

---

## Staffing & Governance

### Pilot Team
| Role | Responsibility | Name/TBD |
|------|-----------------|----------|
| **Executive Sponsor** | Budget approval, remove blockers | Hospital COO |
| **Clinical Lead** | Workflow design, staff readiness, quality assurance | ER Medical Director |
| **Operations Lead** | Daily standup, issue resolution, KPI tracking | ER Operations Manager |
| **IT Lead** | System setup, troubleshooting, integrations | IT Director |
| **NP Lead** | Fast-track protocols, staff training, patient safety | Senior NP or PA |
| **Project Manager** | Timeline, communications, pilot documentation | KPMG Project Manager |

### Governance Cadence
- **Daily (9:30 AM)** – 15-min standup: blockers, KPIs, incidents
- **Weekly (Monday morning)** – 1-hr steering: progress, scope decisions, staff feedback
- **Bi-weekly (Tuesday)** – Stakeholder update: exec summary, go/no-go flags

---

## KPI Tracking & Dashboards

### Real-Time Dashboard (Updated Hourly)
```
┌─────────────────────────────────────────────────────────┐
│          MERIDIAN CITY ER PILOT DASHBOARD               │
│                    Day: Nov 20, 2025                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  THROUGHPUT                    QUEUE DEPTH              │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ 8.2 pts/hr   │ ↑ 15% vs avg │ 7 waiting    │ ↓ Good │
│  │ [Target: 8+] │              │ [Max: 12]    │        │
│  └──────────────┘              └──────────────┘        │
│                                                         │
│  POST-TRIAGE WAIT             DOCTOR UTIL              │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ 9.3 min      │ ✓ On target  │ 72%          │ ↑ Good │
│  │ [Target: <10]│              │ [Target: 75%]│        │
│  └──────────────┘              └──────────────┘        │
│                                                         │
│  STAFF ADOPTION                SAFETY INCIDENTS        │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ 87% comfort  │ ✓ On track   │ 0            │ ✓ Safe │
│  │ [Target: 85%]│              │ [Target: 0]  │        │
│  └──────────────┘              └──────────────┘        │
│                                                         │
│  Fast-Track Volume (NP): 24 patients (22% of total)    │
│  Avg NP cycle time: 42 min (vs. 107 min MD)            │
│                                                         │
│  Alerts:                                               │
│  • 11:00 AM: Queue spiked to 12 (discharged 2)        │
│  • 1:45 PM: Room C turnover took 9 min (goal: 5)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Weekly Report Card
| KPI | Target | Week 1 | Week 2 | Week 3 | Trend | Status |
|-----|--------|--------|--------|--------|-------|--------|
| Throughput (patients/hr) | 8.0+ | 7.2 | 7.8 | 8.4 | ↑↑ | 🟢 ON TRACK |
| Post-triage wait (min) | <10 | 14.2 | 11.5 | 9.1 | ↓↓ | 🟢 ON TRACK |
| Doctor utilization (%) | 75+ | 58 | 65 | 72 | ↑↑ | 🟡 IMPROVING |
| Staff comfort (1–10) | 8.0+ | 6.1 | 7.2 | 7.8 | ↑ | 🟡 IMPROVING |
| Safety incidents | 0 | 0 | 0 | 0 | – | 🟢 SAFE |

---

## Monitoring & Feedback Loops

### Daily Standup Script (15 min)
```
1. KPI snapshot (2 min)
   "Yesterday we hit 8.3 patients/hr, 9.2-min wait, 72% util. On track."

2. Blockers & issues (5 min)
   "Queue board lagged twice. Dispatch rule for ESI-4 needs tweaking."

3. Quick wins & learning (5 min)
   "Handoff meeting saved 3 min today. NP handled 6 fast-track patients."

4. Actions & owners (3 min)
   "IT investigating lag by EOD. Clinical revising ESI-4 rule by EOW."
```

### Weekly Staff Feedback (Anonymous Survey)
```
1. How clear were the new dispatch rules? (1–10)
2. Did the queue board help you understand patient volume? (Yes/No)
3. What was hardest to adapt to?
4. What surprised you positively?
5. One thing we should change immediately?
```

### Weekly Clinician Huddle (30 min)
- Review KPI trends
- Surface workflow pain points
- Iterate dispatch rules
- Discuss patient safety observations

---

## Issue Resolution & Escalation

### Issue Severity Levels

**🔴 Red (Immediate, patient safety)**
- Example: Queue system down, dispatch errors leading to wrong provider assignment
- Action: Stop pilot, return to manual, notify exec sponsor
- Owner: Clinical Lead + IT Lead, escalate to COO

**🟠 Orange (High, threatens pilot success)**
- Example: Post-triage wait not improving; staff adoption <50%
- Action: Weekly steering meeting, implement contingency (add manual dispatch)
- Owner: Operations Lead + Project Manager

**🟡 Yellow (Medium, iterative fix)**
- Example: Room turnover SOP taking 8 min instead of 5; one dispatch rule underperforming
- Action: Daily standup resolution, process tweak
- Owner: Clinical Lead

**🟢 Green (Low, continuous improvement)**
- Example: Staff suggestions for dashboard improvements; minor timing tweaks
- Action: Backlog for post-pilot optimization
- Owner: Project Manager

---

## Pilot Success Scenarios

### Go Scenario ✓ (Proceed to Full Scale-Out)
- ✓ Throughput reaches 8.0+ patients/hr
- ✓ Post-triage wait achieves <12 min average
- ✓ Doctor utilization hits 70%+
- ✓ Staff adoption rating 7+/10
- ✓ Zero safety incidents
- ✓ No critical system failures

**Decision:** Approve full hospital rollout (all shifts, all areas)

### Conditional Go Scenario (~) (Proceed with Conditions)
- ~ Throughput: 7.5–7.9 patients/hr (95% of target)
- ~ Post-triage wait: 12–15 min (approach target)
- ~ Doctor utilization: 65–69% (trending to target)
- ~ 1–2 minor safety observations (no patient harm)
- ~ Staff adoption 6–7/10 (needs more training)

**Decision:** Extend pilot 2 weeks, add targeted interventions, re-gate

### No-Go Scenario ✗ (Halt & Redesign)
- ✗ Throughput plateaus <7 patients/hr after Week 4
- ✗ Post-triage wait remains >18 min
- ✗ Staff adoption <50% (high resistance)
- ✗ Safety incident occurs
- ✗ Critical system failure impacts patient flow

**Decision:** Pause rollout, root-cause analysis, design alternatives

---

## Rollout Plan (Conditional on Pilot Success)

### Phase 1: Cascade to All Day Shifts (Week 9–11)
- Extend queue board + dispatch to all day shifts
- Train additional day-shift teams
- Expected outcome: Consistent 8+ patients/hr across all days

### Phase 2: Add Evening Shifts (Week 12–14)
- Deploy to 3–11 PM shift
- Adapt staffing/dispatch for lower evening volume
- Expected outcome: 7.5–8 patients/hr evening (lower base volume)

### Phase 3: Add Night Shifts (Week 15–17)
- Deploy to 11 PM–7 AM shift (lowest volume, easiest to manage)
- Integrated NP/fast-track if volume warrants
- Expected outcome: 5–6 patients/hr night (but optimized for low volume)

### Full Hospital (Week 18+)
- All shifts, all areas operating with unified queue & dispatch system
- Governance transitions from pilot mode to operations BAU
- Quarterly KPI reviews to maintain improvements

---

## Sustainability & Handoff

### Transition to Operations (Post-Pilot)
- **KPI ownership** transferred from Project Manager → Operations Lead
- **System maintenance** transferred to IT Help Desk (24/7 support)
- **Governance** shifts to monthly exec steering vs. weekly
- **Change management** transitions to ER leadership (no external consultants)

### Sustaining Improvements
1. **Monthly KPI reviews** – Track throughput, utilization, wait times
2. **Quarterly staff surveys** – Monitor adoption, satisfaction, process refinements
3. **Continuous dispatch rule updates** – Refine based on 3 months of real data
4. **Annual benchmarking** – Compare Meridian vs. peer hospitals
5. **Investment in tech** – Plan Phase 2 upgrades (EHR integration, predictive staffing)

---

## Budget & Resource Allocation

| Cost Category | Amount | Notes |
|---------------|--------|-------|
| **Queue board system (annual license)** | $80K | Software + hardware + support |
| **System integration (one-time)** | $120K | EHR hookup, testing, validation |
| **KPMG consulting (16 weeks)** | $400K | Design, pilot oversight, training |
| **NP salary (1 FTE, 6 months pilot)** | $75K | Prorated; part of Phase 1 investment |
| **Staff training & change mgmt** | $50K | Curriculum, materials, facilitation |
| **Contingency (10%)** | $82.5K | – |
| **Total Pilot Investment** | **$807.5K** | Payback in <2 months via throughput gains |

---

## Key Documents & Templates (To Be Developed)

- [ ] Dispatch rules decision tree (Excel flowchart)
- [ ] Shift handoff meeting template (PDF, laminated)
- [ ] Room turnover SOP checklist (laminated, posted in rooms)
- [ ] Staff training deck (PowerPoint)
- [ ] KPI dashboard query (BI tool query definition)
- [ ] Daily standup tracker (shared spreadsheet)
- [ ] Feedback survey (Qualtrics or similar)
- [ ] Issue log (shared tracker with escalation matrix)
- [ ] Go/No-Go decision checklist (based on success criteria)

---

## Approval & Sign-Off

**This charter is approved by:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Hospital Executive Sponsor (COO) | _____________ | _____________ | _____ |
| Clinical Lead (ER Medical Director) | _____________ | _____________ | _____ |
| Operations Lead (ER Ops Manager) | _____________ | _____________ | _____ |
| Project Lead (KPMG PM) | _____________ | _____________ | _____ |

---

**Next Step:** Schedule pilot kickoff meeting for Week 1, distribute training materials, procure queue board system.

