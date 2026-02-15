# Doctor Idle Time & Queue Bottleneck Analysis
## Methodology & Approach

**Date:** November 11, 2025  
**Focus:** Understanding wait times in Doctor Seen phase (Triage End → Doctor Seen)  
**Data Period:** Q1 2025

---

## Executive Summary of Approach

We face a complex problem with incomplete information:
- **What we know:** Timestamps, severity, staff counts, bed capacity
- **What we don't know:** Real-time bed occupancy, test status, exact room assignments
- **Challenge:** High randomness from multiple factors affecting queue

**Our Strategy:** Use deterministic rules with documented assumptions, then layer probabilistic analysis to address randomness.

---

## Part 1: The Randomness Problem & Industry Solutions

### Why This Is Tricky

When multiple factors affect queue (Severity, Tests, Beds, Staff Workload), simple analysis breaks down:

```
Patient Wait Time = f(Severity, Test Results, Bed Availability, Staff Load)

Example Problem:
- Patient A waits 45 minutes
- Patient B waits 5 minutes
- Both same severity, same shift, same number of doctors

Why the difference?
Option 1: Patient A needed tests (not doctor's fault)
Option 2: Patient A was waiting for bed (not doctor's fault)
Option 3: Patient A had coordination delay (process failure)
Option 4: Random chance (timing of arrivals, test turnaround)

We can't tell which one from timestamps alone.
```

### How Industry Solves This

#### **Approach 1: Deterministic Rules (Our Starting Point)**
- Define clear rules: "Doctor is idle IF doctor available + waiting patient + no bed constraint"
- Acknowledge limitations: "This misses factors we can't measure"
- **Pros:** Simple, interpretable, defensible
- **Cons:** Likely over-reports idle time (blames doctor for bed delays, test delays)

#### **Approach 2: Process Mining (Recommended for Next Phase)**
- Track individual patients end-to-end
- Identify which transition takes longest: Triage→Queue? Queue→Doctor? Doctor→Exit?
- Find the **actual bottleneck** (may not be doctor!)
- **Used by:** Hospitals, airlines, call centers
- **Tools:** Discovery algorithms (ProM, Disco, CyberOps)

#### **Approach 3: Queuing Theory / Simulation (When Determinism Fails)**
- Model ER as M/M/c queue (Poisson arrivals, exponential service, c servers)
- Calculate theoretical capacity
- Compare actual vs theoretical
- **Pros:** Handles randomness mathematically
- **Cons:** Requires validating model assumptions
- **Used by:** Healthcare operations research

#### **Approach 4: Machine Learning (When You Have Training Data)**
- Train model: Given {severity, shift, bed_count, doctor_count, time_of_day} → predict wait_time
- Compare predictions to actual waits
- Residuals = unexplained variance = potential process failures
- **Pros:** Captures complex interactions
- **Cons:** Requires large training set, hard to interpret
- **Used by:** Modern hospitals with integrated systems

---

## Part 2: Critical Caveat - Doctor "Idleness" is a CONDITIONAL Function

### ⚠️ DO NOT assume: "Doctor finished + 10min + Patient waiting = Doctor Idle"

**INSTEAD, check ALL of these SIMULTANEOUSLY:**

```
Is this REALLY a coordination failure (fixable with process)?
  ✓ Yes IF: Doctor Available AND Patient Waiting AND Beds Available
  ✗ No IF:  Any of these fail → Resource problem (not process)
```

**Example Scenarios:**

| Doctor Available? | Patient Waiting? | Bed Available? | Conclusion |
|---|---|---|---|
| YES | YES | YES | ✅ Coordination failure (process fixable) |
| NO | YES | YES | ❌ Doctor shortage (need hiring) |
| YES | YES | NO | ❌ Bed shortage (need capacity) |
| YES | NO | YES | ❌ No problem (or queue cleared by then) |

**This is why we build the full detection algorithm, not just surface-level metrics.**

---

## Part 2: The Hybrid Approach (Deterministic + Probabilistic)

### Phase 1: Deterministic Analysis (What We CAN Measure)

**Step 1A: Understand Current State**
- Distribution of wait times
- Wait times by severity, shift, date
- Correlation: Do certain times/shifts have worse waits?

**Step 1B: Build Bed Occupancy Algorithm**
- Calculate max concurrent patients at any moment
- Compare to available beds
- Flag: "Patients waiting but all beds occupied" vs "Beds available, patients still waiting"

**Step 1C: Identify Queue Dynamics**
- At each snapshot (Triage End), count:
  - Waiting patients (not yet with doctor)
  - Available doctors (finished + 10-min buffer)
  - Available beds
- Flag cases: `(waiting_patients > 0) AND (available_doctors > 0) AND (available_beds > 0)` = Process failure

**Step 1D: Acknowledge Randomness**
- For remaining waits we can't explain, note: "Likely due to factors outside our dataset (test results, procedure time variability, clinical decisions)"

### Phase 2: Probabilistic Analysis (If Randomness Persists)

If Step 1 finds many unexplained waits, we'll use:

**Option A: Queue Simulation**
- Assume Poisson patient arrivals, exponential service times
- Simulate ER queue under current conditions
- "Theoretical wait" vs "actual wait" = process inefficiency

**Option B: Residual Analysis**
- Build simple model: `Wait Time = f(Severity, Shift, Doctors On Duty)`
- Residuals (actual - predicted) show which cases are outliers
- Investigate outliers for pattern

**Option C: Time-Series Clustering**
- Identify "normal" vs "abnormal" wait patterns
- When does the system behave differently?
- ML clustering to find common characteristics of bad days/shifts

---

## Part 3: Bed Occupancy Algorithm - Assumptions & Reasoning

### The Challenge

We DON'T have real-time occupancy data. We only know:
- Total bed capacity (100 beds, 20 ICU, 10 fast-track)
- Which patients were in ER at which times

### The Algorithm (Deterministic Approach)

**Assumption 1: A patient occupies a bed from Doctor Seen to Exit**
- Reasoning: Before Doctor Seen, patient is in triage area (doesn't need exam bed)
- After Exit, patient has left (bed is free)
- Risk: May undercount occupancy (some triage patients may use beds), but conservative

**Assumption 2: Bed types matched to patient severity (Simple Assignment)**
- Triage Level 1 (Critical) → ICU beds first
- Triage Level 2-3 (Urgent) → Regular beds
- Triage Level 4 (Minor) → Fast-track beds (or Regular if full)
- Reasoning: Realistic ER triage-to-bed assignment
- Risk: Actual assignment may differ, affecting accuracy

**Assumption 3: At any snapshot time T, count occupancy**
- Occupancy(T) = count of patients where `Doctor Seen <= T <= Exit`
- Available Beds(T) = Total Beds - Occupancy(T)
- Reasoning: Standard queue theory occupancy definition
- Risk: Patients may stay in rooms after exit (not freed immediately)

### Algorithm Pseudocode

```python
For each unique timestamp T in dataset (at each Triage End):
    
    # Find all patients who are currently with doctor (occupying beds)
    occupying_patients = patients where (Doctor_Seen <= T) AND (Exit_Time >= T)
    
    # Categorize by severity/bed type
    icu_occupied = count of occupying_patients where Triage_Level == 1
    regular_occupied = count of occupying_patients where Triage_Level in [2,3]
    fasttrack_occupied = count of occupying_patients where Triage_Level == 4
    
    # Calculate availability
    icu_available = 20 - icu_occupied
    regular_available = 70 - regular_occupied
    fasttrack_available = 10 - fasttrack_occupied
    
    # Check if waiting patient can get a bed
    waiting_patients = patients where (Triage_End <= T) AND (Doctor_Seen > T)
    
    can_bed_be_assigned = (
        regular_available > 0 OR 
        fasttrack_available > 0 OR 
        icu_available > 0
    )
    
    # Flag if process is blocking despite available beds
    if (waiting_patients > 0) AND (can_bed_be_assigned) AND (doctors_available > 0):
        FLAG: "Process Bottleneck - Patient waiting despite available doctor + bed"
```

### Limitations & Uncertainties

1. **Bed Type Assignment Unknown**
   - We assume severity-based assignment, but actual assignment may differ
   - Impact: Could misclassify "bed unavailable" vs "doctor unavailable"
   - Mitigation: Run sensitivity analysis (what if assignment is different?)

2. **No Transition Time Between Triage and Bed**
   - Patient finishes triage, needs time to get to bed/room
   - We assume this is instant (conservative assumption)
   - Impact: Slight undercount of wait time variability

3. **Tests Are Unknown**
   - If patient needs imaging/labs, they may not go to bed immediately
   - We can't detect this from data
   - Impact: We may blame "bed shortage" when really "test waiting"

4. **Room Turnover Time Unknown**
   - After patient exits, bed needs cleaning/prep
   - We assume instant availability (unrealistic)
   - Impact: Overcount of available beds, undercount of true bed shortage

---

## Part 4: Expected Outcomes & Next Steps

### What We'll Find (Predictions)

**Scenario A: Beds are the bottleneck**
- Finding: High occupancy, full beds during peak hours
- Wait times high during high occupancy periods
- Implication: Need more beds or faster patient processing

**Scenario B: Doctors are the bottleneck**
- Finding: Many beds available, but few doctors on duty
- High patients-per-doctor ratio during peak
- Implication: Need more doctors or redistribute staffing

**Scenario C: Process is the bottleneck**
- Finding: Doctors available, beds available, but patients still waiting
- Suggests: Coordination/assignment delays, communication gaps
- Implication: Fix workflow, not staffing

**Scenario D: Multiple bottlenecks (Most Likely)**
- Different bottlenecks at different times
- Will require targeted interventions

### How We'll Address Randomness

**If deterministic analysis explains >70% of variance:**
- Good! Randomness is manageable
- Focus on the 70% (controllable factors)

**If deterministic analysis explains <50% of variance:**
- Signal: Important factors are missing
- Next step: Implement Process Mining or Queuing Simulation
- Consider: Test result timing, actual bed assignments, room turnover

---

## Part 5: Analysis Structure

### Notebook Structure (Single File, Appended)

**Section 1: Data Loading & Exploration**
- Load final_data.csv and Hospital_facility_out.csv
- Understand data distributions

**Section 2: Bed Occupancy Algorithm**
- Implement occupancy calculation
- Visualize occupancy over time

**Section 3: Wait Time Analysis**
- By severity, shift, date
- Identify patterns

**Section 4: Bottleneck Detection**
- Apply deterministic rules
- Find specific instances of doctor idle + patient waiting

**Section 5: Root Cause Analysis**
- For each bottleneck: What was blocking?
- Severity? Beds? Staffing?

**Section 6: Industry Approaches & Recommendations**
- If randomness is high, propose next steps (Process Mining? Simulation?)

### Markdown File Structure

- This methodology (what we're doing and why)
- Key findings section (to be appended)
- Assumptions & limitations (for management review)
- Recommendations (management-ready)

---

## Part 6: What Success Looks Like

### For This Phase
✅ Clear understanding of wait time distributions  
✅ Identification of which bottleneck matters most  
✅ Specific examples with timestamps and reasons  
✅ Acknowledgment of what we can't measure  

### For Management
✅ Proof that bottleneck exists (if it does)  
✅ Which factor is primary (bed/doctor/process)  
✅ Quantified impact ("X hours wasted" or "Y% of waits are avoidable")  
✅ Realistic next steps (don't over-promise what one analysis can show)  

---

## Ready to Begin

We'll start with **descriptive statistics** (What does the data show?) before jumping to **causal analysis** (Why does it happen?).

Proceed to notebook for Step 1: Data Loading & Exploration.

