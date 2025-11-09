# Executive Summary
## Meridian City ER Efficiency Challenge

**Engagement Owner:** KPMG Consulting  
**Date:** November 2025  
**Audience:** Hospital C-Suite, ER Leadership, Board of Directors

---

## The Challenge

Meridian City ER operates under significant capacity strain. Despite having adequate staffing levels, patients experience **long waits and providers appear underutilized**—a paradox that signals a **process problem, not a staffing problem**.

### Current State (Q1 2025)
- **15,000 patient visits** processed over 90 days
- **Average ED Length of Stay (LOS): 172 minutes** (nearly 3 hours)
- **Average post-triage wait: 38.6 minutes** before seeing a doctor
- **Doctor availability rate: Only ~50%** during peak bottleneck periods (vs. 75–80% industry target)
- **2,179 instances (14.5% of all visits)** where doctors were idle but patients waited

---

## The Root Cause: System Bottleneck (Not Staffing)

### Theory of Constraints Principle
*In any system, throughput = bottleneck capacity. Improving other stages doesn't help.*

**Meridian City's bottleneck:** The doctor/treatment phase.

| Stage | Mean Time | % of Total LOS | Queue? |
|-------|-----------|---|---|
| Wait for registration | 2.0 min | 1.2% | No |
| Registration | 7.7 min | 4.5% | No |
| Triage | 12.6 min | 7.3% | No |
| **Wait after triage** | **38.6 min** | **22.4%** | **YES ⚠️** |
| **Doctor → exit** | **107.3 min** | **62.3%** | **YES ⚠️** |
| Other | 4.0 min | 2.3% | No |

**Insight:** Patients queue AFTER triage (38.6 min avg) because the doctor stage is slow (107.3 min). The 38.6 min wait is **not** a triage problem—it's the price patients pay waiting for a slow downstream process.

### Current System Throughput: 6.9 patients/hour
This is capped by:
- 3.2 doctors on average per shift
- 107.3 minutes doctor+treatment cycle time per patient
- **Math:** 3.2 doctors × 60 min/hour ÷ 107.3 min/patient = **~1.8 patients/doctor/hour → 6.9 total**

---

## The Opportunity

### Thesis: Process Optimization, Not Hiring

Analysis reveals **2,179 bottleneck events** where:
- ✓ Patients were waiting post-triage
- ✓ Doctors were available (not actively treating)
- ✓ Yet no patient-doctor handoff occurred

**Why?** Manual assignment, no real-time queue visibility, handoff delays, room turnover friction.

### Addressable Issues
1. **Manual patient-doctor pairing** → No system tells doctors "next patient waiting in Room B"
2. **Lack of queue visibility** → Doctors can't see who's waiting or triage level
3. **Shift handoff inefficiencies** → Communication gaps during transitions
4. **Room turnover delays** → Patients not moved to available providers fast enough

---

## Financial Impact

### Cost of Bottleneck (Quantified)

| Factor | Value |
|--------|-------|
| Wasted patient-hours (Q1 2025) | 1,387 hours |
| Implied lost capacity | ~1,400 quick-visit equivalents |
| Annualized | **5,600 visits** |
| @ $800 avg ED visit revenue | **$4.48M** |
| Cost of patient dissatisfaction, LWBS, callbacks | **+$1–2M** estimate |
| **Total annual opportunity** | **$5–6M** |

### Upside Scenario: 25–35% Throughput Improvement

**Without adding staff**, with process fixes:

| Metric | Current | Target | Gain |
|--------|---------|--------|------|
| Throughput (patients/hour) | 6.9 | 8.5–9.2 | +23–33% |
| Patients/day | 167 | 204–220 | +37–53 |
| Annual visits | 61,000 | 74,500–80,300 | +13,500–19,300 |
| Revenue @ $800/visit | $48.8M | $59.6–64.2M | **+$10.8–15.4M** |
| Net cost to implement | – | – | **~$0.8M** (tech + training) |
| **Net benefit** | – | – | **+$10–14.6M annually** |

---

## Recommended Interventions

### Tier 1: High-Impact, Fast (Weeks 1–4)
1. **Real-time queue board** – Visual dashboard showing waiting patients, triage levels
2. **Auto-dispatch rules** – System assigns next patient to available doctor
3. **Shift handoff playbook** – Structured 15-min transitions with queue briefing
4. **Room turnover SOP** – Max 8-min room prep between patients

**Expected gain:** 10–15% throughput lift, ~50-minute LOS reduction

### Tier 2: Medium-Impact, Medium Effort (Weeks 5–8)
5. **Fast-track expansion** – Dedicated lane for minor injuries/illnesses
6. **Nurse practitioners/PAs** – Extended provider model for low-acuity cases
7. **Parallel processing** – Compress pre-doc steps (registration + triage during waiting)

**Expected gain:** Additional 8–12% throughput

### Tier 3: Operational Excellence (Weeks 9+)
8. **EHR integration** – Seamless patient handoff and documentation
9. **Predictive staffing model** – Adjust coverage based on time-of-day, day-of-week demand
10. **Feedback loops** – Weekly KPI reviews, continuous micro-improvements

**Expected gain:** 3–5% ongoing optimization

---

## Implementation Roadmap

```
Week 1–2: Diagnostic & Design
  ├─ Validate findings with ops team
  ├─ Process mapping (current state)
  └─ Design future-state workflows

Week 3–4: Pilot Planning
  ├─ Procure queue board tech
  ├─ Draft auto-dispatch rules
  └─ Staff training (pilot cohort)

Week 5–7: Pilot Execution (1 shift, 3 weeks)
  ├─ Monitor real-time KPIs
  ├─ Gather feedback daily
  └─ Iterate on workflows

Week 8–12: Scale & Rollout
  ├─ Roll out to all shifts
  ├─ Train full staff complement
  └─ Monitor sustained improvement

Week 13+: Governance & Sustain
  ├─ Weekly scorecard reviews
  ├─ Continuous process refinement
  └─ Quarterly business reviews
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Staff resistance to change | Early engagement, clear comms on "why," training, feedback loops |
| Tech implementation delays | Phased pilot first; proven off-the-shelf queue systems |
| Bottleneck shifts upstream | Monitor triage/registration during pilot; adjust staffing if needed |
| Unsustainable gains | Governance structure, weekly KPI reviews, accountability |

---

## Investment Required

| Category | Cost | Notes |
|----------|------|-------|
| Queue board software (annual) | $80K | Includes hardware, installation, support |
| EHR integration (one-time) | $150K | Custom development + testing |
| Training & change management | $60K | Curriculum, materials, facilitation |
| KPMG consulting & support (16 weeks) | $400K | Diagnostic, design, pilot oversight |
| **Total** | **$690K** | ROI breakeven in ~2.5 months at $5–6M annual upside |

---

## Success Looks Like (90-Day Targets)

✓ **ED LOS reduced to 140 minutes** (from 172)  
✓ **Post-triage wait reduced to 15–20 minutes** (from 38.6)  
✓ **Doctor utilization improved to 70–75%** (from 50%)  
✓ **Throughput increased to 8.5 patients/hour** (from 6.9)  
✓ **Patient satisfaction (HCAHPS) improves 10+ points**  
✓ **LWBS rate drops below 2%**  
✓ **Staff engagement survey shows +15 points**  

---

## Next Steps (This Week)

1. **Schedule kickoff** with ER leadership, CFO, and clinical team
2. **Review process design** artifacts (swimlanes, dispatch rules, handoff playbook)
3. **Confirm pilot scope** – which shift, which week, which metrics to track
4. **Approve investment** – budget allocation for tech, training, consulting
5. **Identify internal sponsor** – clinical champion + ops owner to lead implementation

---

## Key Takeaways

| Insight | Implication |
|---------|-------------|
| **Doctor stage is bottleneck** | Don't optimize registration/triage; fix doctor flow |
| **Process, not people** | Problem is not staffing; it's queue visibility & assignment |
| **$5–6M annual opportunity** | 25–35% throughput gain without hiring = massive ROI |
| **Fast to implement** | 12 weeks to see results, 6 months to full sustained improvement |
| **De-risks patient safety** | More patients, same or better quality—less provider fatigue |

---

## Questions for Leadership

1. **Is a 25–35% throughput improvement without new hires compelling?**
2. **What are your top 3 constraints today** (staffing, space, processes, tech)?
3. **What is your risk tolerance** for a pilot that may reveal workflow gaps?
4. **Who will be the internal executive sponsor** for this initiative?
5. **What is your timeline** for ROI realization?

---

**Prepared by:** KPMG Consulting ER Transformation Practice  
**Contact:** [Your engagement leader]  
**Date:** November 2025

