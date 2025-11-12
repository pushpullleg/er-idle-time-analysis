# Doctor Idle Time - Precise Definition & Conditional Logic

## The Problem We're Solving

**Question:** "Are doctors idle while patients wait?"

**Why it's hard:** This is NOT a simple binary measurement. It's a **conditional function** that depends on multiple simultaneous factors.

---

## What "Doctor Idle" ACTUALLY Means

### ❌ WRONG Definitions (Too Simple)

- "Patient sees doctor 30 minutes after triage" ← Could be bed shortage, not doctor idle
- "Doctor On Duty value is 4" ← Doesn't mean 4 doctors are idle
- "Doctor finished patient + 10 minutes have passed + patient still waiting" ← Could be bed shortage or other blockers

### ✅ CORRECT Definition (Conditional)

**A doctor is considered "idle" (in a problematic way) at moment T if ALL of these are TRUE:**

1. **Doctor has capacity to see next patient:**
   - Count doctors currently active: `Patients in treatment (with 10-min buffer)`
   - Available doctors: `Doctors On Duty - Active Doctors`
   - If `Available Doctors > 0` ✓

2. **Patient is waiting (ready to be seen):**
   - Patient finished triage but not yet with doctor
   - Time window: `Triage End ≤ T < Doctor Seen`
   - At least one other patient waiting (not counting this patient)
   - If `Waiting Patients > 0` ✓

3. **Bed IS available (not the blocker):**
   - Count occupied beds: `Patients in treatment (Doctor Seen ≤ T ≤ Exit Time)`
   - Available beds: `Total Capacity - Occupied`
   - If `Available Beds > 0` for that severity ✓

4. **Treatment area is EMPTY (no one is currently being seen):**
   - All doctors have completed with their current patients
   - No one actively in "Doctor Seen" phase (all have exited)
   - This is the strongest signal of doctor idle
   - Count active patients: `Patients where Doctor Seen ≤ T < Doctor Busy Until`
   - If `Active Patients = 0` ✓ (Doctor Seen area is empty)
   
5. **Tests are NOT blocking (assumption):**
   - We can't measure test result timing directly
   - We assume tests don't block initial doctor assessment
   - Acknowledge this as a LIMITATION

---

## The 10-Minute Transition Buffer (CRITICAL DETAIL)

### Why Include It?

A doctor is NOT truly "idle" immediately after a patient exits. They need:
- 3 min: Documentation and charting
- 2 min: Room sanitization
- 2 min: Hand washing
- 1 min: Mental reset
- 2 min: Review next patient's chart
- **Total: ~10 minutes**

### How We Apply It

```
Doctor is "busy until" = Patient Exit Time + 10 minutes
```

**This prevents false positives:**
- Without buffer: Every patient seen at 10:31 would show doctor "idle" at 10:32
- With buffer: Realistic—doctor is actually prepping next patient

### Result

Including the buffer is MORE REALISTIC, so:
- Fewer false positives (doctors marked idle when they're not)
- More credible analysis (management will trust it)
- Potentially finds REAL coordination failures (when doctors ARE idle despite 10-min buffer)

---

## The Full Detection Algorithm

### For Each Patient (At the moment they finish triage):

```python
CONDITION 1: Doctor Available?
  active_doctors = count(patients where Doctor_Seen ≤ now ≤ Doctor_Busy_Until)
  idle_doctors = Doctors_On_Duty - active_doctors
  doctor_available = (idle_doctors > 0)

CONDITION 2: Patient Waiting?
  waiting_patients = count(other patients where Triage_End ≤ now < Doctor_Seen)
  patient_waiting = (waiting_patients > 0)

CONDITION 3: Bed Available?
  bed_type = assign_by_severity(patient.severity)
  occupied_beds = count(patients in treatment with same bed type)
  available_beds = total_capacity[bed_type] - occupied_beds
  bed_available = (available_beds > 0)

CONDITION 4: Treatment Area is EMPTY?
  ⭐ STRONGEST SIGNAL OF DOCTOR IDLE
  active_patients = count(patients where Doctor_Seen ≤ now < Doctor_Busy_Until)
  treatment_area_empty = (active_patients == 0)
  ✓ if treatment_area_empty

BOTTLENECK DETECTION:
  if (doctor_available AND patient_waiting AND bed_available AND treatment_area_empty):
    → CLEAR COORDINATION FAILURE (process fixable)
    → Strongest evidence: Doctor is demonstrably idle
    → Action: Fix assignment/workflow immediately
    
  else if (doctor_available AND patient_waiting AND bed_available):
    → POSSIBLE COORDINATION FAILURE (doctor in transition buffer)
    → Less definitive but still a problem
    → Action: Investigate workflow
    
  else:
    → RESOURCE CONSTRAINT (needs capital/hiring)
    → Determine which: Doctor shortage? Bed shortage? Test delays?
    → Action: Hire/expand/improve diagnostics
```

---

## The Four Conditions Explained

| Condition | What It Means | Why It Matters |
|-----------|--------------|----------------|
| Doctor Available | At least 1 idle doctor (Doctors On Duty > Active) | Without this, can't be doctor's fault |
| Patient Waiting | At least 1 patient ready (Triage End ≤ now < Doctor Seen) | Without this, no one to help anyway |
| Bed Available | At least 1 free bed (for that severity) | Without this, bed shortage, not doctor issue |
| **Treatment Area Empty** | **No one being actively treated** | **Strongest proof doctor is idle** |

**Why the 4th condition matters:**
- Conditions 1-3 show "could be idle"
- Condition 4 shows "definitely idle" (no one even in treatment)
- With all 4: Undeniable evidence of coordination failure

---

## Example Walkthrough

### Scenario
- **Time:** 2:30 PM
- **Patient:** Jane just finished triage
- **Doctors On Duty:** 4
- **Setup:**
  - Patient Bob: Saw doctor 2:00 PM, exited 2:20 PM (in 10-min buffer until 2:30 PM)
  - Patient Alice: Saw doctor 2:10 PM, still in exam (exits 2:45 PM)
  - Patient Mike: Saw doctor 2:25 PM, still in exam (exits 3:15 PM)
  - Jane: Just finished triage at 2:30 PM
  - Others: Tom finished triage at 2:25 PM, still waiting; Carmen finished at 2:15 PM, still waiting

### Analysis at Jane's Triage End (2:30 PM)

**CONDITION 1: Doctor Available?**
```
Active doctors at 2:30 PM:
  - Bob: Saw doctor 2:00, exit 2:20, busy until 2:30 ✓ (in buffer period)
  - Alice: Saw doctor 2:10, in exam, busy until 2:45 ✓
  - Mike: Saw doctor 2:25, in exam, busy until 3:15 ✓
  - (No one else in treatment range)

Active doctors = 3
Idle doctors = 4 - 3 = 1
✓ Doctor Available (1 idle)
```

**CONDITION 2: Patient Waiting?**
```
Other patients waiting at 2:30 PM:
  - Tom: Triage end 2:25, not yet with doctor, doctor_seen > 2:30 ✓
  - Carmen: Triage end 2:15, not yet with doctor, doctor_seen > 2:30 ✓

Waiting patients (excluding Jane) = 2
✓ Patient Waiting (at least 1 other)
```

**CONDITION 3: Bed Available?**
```
Jane's severity = Level 2 (Urgent) → Regular beds

Occupied beds at 2:30 PM (only count Doctor_Seen ≤ now ≤ Exit):
  - Alice (L2): In exam, 2:10 ≤ 2:30 ≤ 2:45 ✓
  - Mike (L1): In exam but ICU, not counted here
  - (No other L2/L3 patients in treatment)

Occupied regular beds = 1
Available regular beds = 70 - 1 = 69
✓ Bed Available (plenty)
```

**CONDITION 4: Treatment Area Empty?** ⭐ STRONGEST SIGNAL
```
Active patients at 2:30 PM (Doctor_Seen ≤ now < Doctor_Busy_Until):
  - Alice: In exam (2:10 ≤ 2:30 ≤ 2:45) ✓ (1 patient)
  - Mike: In exam (2:25 ≤ 2:30 ≤ 3:15) ✓ (1 patient)

Active patients = 2
Treatment area NOT empty (2 patients being treated)
✗ Treatment Area Empty? NO
```

### CONCLUSION - Scenario A (With Treatment Area Full)

```
Doctor Available: ✓ YES (1 idle)
Patient Waiting: ✓ YES (2 others)
Bed Available: ✓ YES (69 free)
Treatment Area Empty: ✗ NO (2 patients in exam)

→ POSSIBLE COORDINATION FAILURE (3 of 4 conditions met)
→ Doctor in 10-min transition buffer, not completely free
→ Action: Investigate workflow, but less urgent
```

---

### SCENARIO B (When Treatment Area IS Empty)

**Same time (2:30 PM), but different setup:**
- Alice exited at 2:20 PM (busy until 2:30 PM, NOW DONE)
- Mike exited at 2:25 PM (busy until 2:35 PM, still in buffer)
- No one else in treatment

**CONDITION 4 Check:**
```
Active patients at 2:30 PM (Doctor_Seen ≤ now < Doctor_Busy_Until):
  - Mike: In buffer (2:25 ≤ 2:30 ≤ 2:35) ✓ (1 patient)

Active patients = 1
Treatment area NOT completely empty
```

**SCENARIO C (When Treatment Area IS TRULY Empty):**

**Time (2:35 PM), after all buffers expire:**
- Alice exited at 2:20 PM (busy until 2:30 PM, NOW FULLY DONE)
- Mike exited at 2:25 PM (busy until 2:35 PM, NOW DONE)
- No one in treatment

**CONDITION 4 Check:**
```
Active patients at 2:35 PM (Doctor_Seen ≤ now < Doctor_Busy_Until):
  - No one!

Active patients = 0
✓ Treatment Area Empty (DEFINITIVE IDLE SIGNAL)
```

**CONCLUSION - Scenario C (Treatment Area EMPTY)**

```
Doctor Available: ✓ YES (4 idle, no one in treatment)
Patient Waiting: ✓ YES (Jane, Tom, Carmen all waiting)
Bed Available: ✓ YES (plenty free)
Treatment Area Empty: ✓ YES (no one being treated)

→ CLEAR COORDINATION FAILURE (ALL 4 CONDITIONS MET)
→ STRONGEST POSSIBLE EVIDENCE OF DOCTOR IDLE
→ Doctors are demonstrably not helping waiting patients
→ Action: URGENT - Fix assignment workflow immediately
```

---

## What If NOT All Conditions Met?

### Example: Bed IS the Bottleneck

```
Same scenario (2:35 PM, treatment area empty) BUT:
Regular beds are 70 total
Only 2 regular beds available (68 occupied)

CONDITION 3 fails: Bed NOT Available

Conclusion:
  Doctor idle (yes) + Patient waiting (yes) + Bed FULL (not available)
  → NOT a coordination failure
  → BED SHORTAGE is the bottleneck
  → Action: Get more regular beds or faster discharge
```

### Example: Doctor IS the Bottleneck

```
Same time, but only 1 doctor on duty

CONDITION 1 fails: No doctor available

Active doctors = 1 (Bob in 10-min buffer)
Idle doctors = 1 - 1 = 0

Conclusion:
  No idle doctors → DOCTOR SHORTAGE
  → Action: Hire more doctors or redistribute staffing
```

---

## Why This Matters for Your Analysis

1. **Credibility:** Management will see the rigor, not just "doctors are idle"
2. **Accuracy:** Distinguishes between coordination (fixable) vs. resources (needs money)
3. **Actionability:** Different solutions for different bottlenecks
4. **Completeness:** Every patient wait is categorized as one of:
   - ✅ Coordination failure → Process improvement
   - ❌ Doctor shortage → Hiring
   - ❌ Bed shortage → Capacity expansion
   - ❌ Test delays → Diagnostics improvement
   - ❌ Unexplained → Randomness (need advanced methods)

---

## Limitations We'll Document

1. **No test timing:** Assume tests don't block initial doctor assessment
2. **No room assignment logs:** We infer from occupancy, not actual assignments
3. **No clinician identities:** Can't track specific doctor movements
4. **Bed turnover time:** We assume instant cleaning (unrealistic, creates upper bound)
5. **Staff skill matching:** We treat all doctors equally (some may have specialty gaps)

**These limitations should be listed but don't invalidate findings—they just provide context for interpretation.**

---

## Implementation in Notebook

**Section 2** of `bottleneck_analysis.ipynb` implements this exact logic:

1. Define bed assignment strategy
2. Build helper functions (count active doctors, waiting patients, available beds)
3. For each patient, check all 3 conditions
4. Flag as bottleneck only if ALL true
5. Analyze non-bottleneck cases (why didn't conditions meet?)
6. Report both findings and limitations

This approach handles the complexity properly instead of oversimplifying.
