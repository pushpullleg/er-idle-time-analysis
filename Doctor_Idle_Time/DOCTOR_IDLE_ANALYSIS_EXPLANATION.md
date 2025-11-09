# How I Calculated Idle Doctor Time

## 🎯 **The Core Question**

**"Is a doctor idle while patients are waiting?"**

To answer this, I need to define three fundamental states:

## 📐 **STEP 1: Define the Basic States**

### **State A: When is a doctor BUSY?**
```
A doctor is BUSY if:
  They saw a patient at time T1 (Doctor Seen)
  AND that patient hasn't left yet at time T2 (Exit Time)
  AND we're checking a time T between T1 and T2
```

**Visual Example:**
```
Timeline:  9:00    9:15    9:30    9:45    10:00
Doctor:    [Doctor Sees Patient]--------[Patient Exits]
           ^                                   ^
        Doctor Seen                        Exit Time

At 9:30, doctor is BUSY because patient is still there
```

### **State B: When is a patient WAITING?**
```
A patient is WAITING if:
  They finished triage at time T1 (Triage End)
  AND haven't seen doctor yet at time T2 (Doctor Seen)
  AND we're checking a time T between T1 and T2
```

**Visual Example:**
```
Timeline:  9:00    9:15    9:30    9:45    10:00
Patient:   [Triage End]----WAITING----[Doctor Seen]
           ^                              ^
       Triage End                    Doctor Seen

At 9:30, patient is WAITING (finished triage, not yet seen)
```

### **State C: When is a doctor IDLE?**
```
A doctor is IDLE if:
  They are on duty (we know this from "Doctors On Duty")
  AND they are NOT in State A (not busy with a patient)
```

## 🔍 **STEP 2: The Actual Calculation Logic**

Let me trace through **ONE SPECIFIC EXAMPLE** from the data:

### **Example Patient Record:**
```python
Visit ID: V112722
Hospital: MC_ER_EAST
Triage End: 2025-03-07 12:23:00
Doctor Seen: 2025-03-07 12:38:00
Exit Time: 2025-03-07 14:09:00
Doctors On Duty: 4
```

### **Question: Was a doctor idle while this patient waited?**

**Patient's wait time:**
```
Doctor Seen - Triage End = 12:38 - 12:23 = 15 minutes
```

**Now check at the moment triage ended (12:23):**

#### **Step 2.1: Count Active Doctors at 12:23**

```python
def count_active_doctors_at_time(all_visits, check_time):
    active = all_visits[
        (all_visits['Doctor Seen'] <= check_time) &    # Doctor already saw them
        (all_visits['Exit Time'] > check_time)         # They haven't left yet
    ]
    return len(active)
```

**Translation:** Find all patients who at time 12:23:
- Already saw a doctor (Doctor Seen ≤ 12:23)
- Haven't exited yet (Exit Time > 12:23)

**This gives us the number of doctors actively treating patients at 12:23**

Let's say we find **1 patient** meeting these criteria → **1 doctor is busy**

#### **Step 2.2: Calculate Idle Doctors**

```python
doctors_on_duty = 4  # From the staffing data
active_doctors = 1   # From Step 2.1
idle_doctors = doctors_on_duty - active_doctors = 4 - 1 = 3
```

**Result: 3 doctors are idle at 12:23**

#### **Step 2.3: Count Waiting Patients at 12:23**

```python
def count_waiting_patients_at_time(all_visits, check_time):
    waiting = all_visits[
        (all_visits['Triage End'] <= check_time) &     # Finished triage
        (all_visits['Doctor Seen'] > check_time)       # Haven't seen doctor yet
    ]
    return len(waiting)
```

**Translation:** Find all patients who at time 12:23:
- Finished triage (Triage End ≤ 12:23)
- Haven't seen doctor yet (Doctor Seen > 12:23)

Let's say we find **4 patients** → **4 patients waiting**

#### **Step 2.4: Detect Inefficiency**

```python
if idle_doctors > 0 and waiting_patients > 0:
    # This is an inefficiency!
    # 3 doctors are idle while 4 patients are waiting
```

## 📊 **STEP 3: The Timeline Visualization**

Let me show you what the data looks like at 12:23:

```
Time: 12:23:00

Patient A: [Triage: 11:50]--WAITING--[Doctor: 12:25]
Patient B: [Triage: 12:10]--WAITING--[Doctor: 12:30]
Patient C: [Triage: 12:20]--WAITING--[Doctor: 12:35]
Patient D: [Triage: 12:23]--WAITING--[Doctor: 12:38] ← Our patient
                    ^
                 Check here

Patient X: [Doctor: 11:45]--BEING TREATED--[Exit: 12:30]

Doctors on duty: 4
Active (busy): 1 (treating Patient X)
Idle: 3
Waiting: 4 (Patients A, B, C, D)

PROBLEM DETECTED! ⚠️
```

## 🧮 **STEP 4: The Mathematical Formula**

For each time point T:

```
Active_Doctors(T) = COUNT(
    patients WHERE 
        Doctor_Seen ≤ T AND 
        Exit_Time > T
)

Waiting_Patients(T) = COUNT(
    patients WHERE 
        Triage_End ≤ T AND 
        Doctor_Seen > T
)

Idle_Doctors(T) = Doctors_On_Duty - Active_Doctors(T)

Inefficiency_Exists(T) = (Idle_Doctors(T) > 0) AND (Waiting_Patients(T) > 0)
```

## 🔬 **STEP 5: Why This Works (Assumptions)**

This calculation makes these **key assumptions**:

### ✅ **Valid Assumptions:**
1. **One patient = One doctor** during treatment
   - When a patient is between "Doctor Seen" and "Exit Time", one doctor is occupied
   
2. **Doctors are interchangeable** (within reason)
   - Any available doctor can see the next waiting patient
   - (This isn't always true in reality - specialties matter)

3. **Triage End = Ready for Doctor**
   - Once triage is complete, patient is medically cleared and ready
   
4. **Doctors On Duty = Available Pool**
   - All doctors on duty can potentially see patients
   - (Doesn't account for breaks, meetings, etc.)

### ⚠️ **Limitations:**
1. **Doesn't track individual doctors** - We see system-level patterns, not specific doctor behavior
2. **Doesn't account for:**
   - Doctor specialties (cardiologist can't help orthopedic patient)
   - Doctors in meetings, on break, doing paperwork
   - Room availability
   - Equipment availability
   - Patient complexity (some take longer)

## 💡 **STEP 6: Real Code Walkthrough**

Let me show you the exact code path:

```python
# For each patient who waited...
for idx, patient in shift_df.iterrows():
    triage_end = patient['Triage End']      # When they finished triage
    doctor_seen = patient['Doctor Seen']    # When they saw doctor
    wait_time = (doctor_seen - triage_end).total_seconds() / 60  # Minutes waited
    
    if wait_time > 5:  # Only look at waits > 5 minutes
        
        # AT THE MOMENT TRIAGE ENDED, check the system state
        active_doctors = count_active_doctors_at_time(shift_df, triage_end)
        waiting_patients = count_waiting_patients_at_time(shift_df, triage_end)
        idle_doctors = doctors_on_duty - active_doctors
        
        # If doctors were idle while patients waited = INEFFICIENCY
        if idle_doctors > 0 and waiting_patients > 0:
            # Record this as a problem!
            idle_scenarios.append({...})
```

## 📈 **STEP 7: Aggregation**

Once we identify all inefficiency instances, we aggregate:

```python
# Sum all wait times from inefficient periods
total_wasted_time = sum(wait_time for each inefficient instance)

# Average metrics
avg_wait = mean(wait_time for each inefficient instance)
avg_idle_docs = mean(idle_doctors for each inefficient instance)
```

## 🎯 **The Bottom Line**

**What we're really calculating:**

> "For each moment a patient finished triage and then waited to see a doctor, 
> how many doctors were sitting idle at that exact moment, 
> and was there a queue of patients waiting?"

If **idle doctors > 0** AND **waiting patients > 0** → **System inefficiency detected!**

The **2,240 instances** we found means this happened 2,240 times in your 15,000 visits - that's about **15% of all visits** had this problem.

---

## 📊 **Key Findings Summary**

### Main Results:
- **2,240 instances** of idle doctors while patients waited
- **1,423 hours** of total wasted patient wait time
- **38.1 minutes** average unnecessary wait per affected patient
- **2.8 doctors** average idle during these incidents

### By Shift:
| Shift   | Incidents | Avg Wait | Worst Case |
|---------|-----------|----------|------------|
| DAY     | 965       | 36.4 min | 87 min     |
| EVENING | 880       | 40.9 min | 99 min     |
| NIGHT   | 395       | 36.1 min | 78 min     |

### Root Causes (Hypotheses):
1. Scheduling gaps between patient handoffs
2. Doctors finishing with one patient but not immediately getting next
3. Possible lack of real-time queue visibility
4. Triage-to-doctor assignment delays
5. Shift change inefficiencies

### Recommendations:
1. **Real-time Queue Dashboard**: Give doctors visibility into waiting patients
2. **Automated Assignment**: Auto-assign next patient when doctor becomes available  
3. **Shift Overlap**: Have incoming shift start seeing patients before outgoing shift ends
4. **Fast Track Utilization**: Better use of fast track for lower acuity patients
5. **Monitor Utilization**: Track doctor utilization % as KPI (target: 75-80%)

---

## 📁 **Files**

- **Analysis Script**: `ML/doctor_idle_analysis.py`
- **Data Source**: `final_data.csv`
- **This Documentation**: `ML/DOCTOR_IDLE_ANALYSIS_EXPLANATION.md`

---

*Analysis Date: November 8, 2025*
*Data Period: January 1 - March 31, 2025*
*Hospital: MC_ER_EAST*
