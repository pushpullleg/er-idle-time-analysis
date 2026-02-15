# Doctor Idle Time & Queue Bottleneck Analysis
## Bottleneck Folder - Complete Guide

---

## 📁 Project Structure

```
/Users/mukeshravichandran/Datathon/Bottleneck/
│
├── 📄 README.md                      (you are here)
├── 📄 METHODOLOGY.md                 (detailed approach & reasoning)
├── 📄 FINDINGS.md                    (key discoveries - append here)
│
├── 📓 bottleneck_analysis.ipynb      (main analysis notebook - append all code here)
│
└── 📊 visualizations/                (saved charts - auto-generated)
    └── 01_wait_time_overview.png
```

---

## 🎯 Project Goal

**Understand and quantify bottlenecks in the Doctor Seen phase of ER flow.**

**Key Question:**  
*"Are doctors idle while patients wait? If yes, what's blocking flow?"*

**Secondary Questions:**
- Is it a bed shortage?
- Is it a doctor shortage?
- Is it a process coordination failure?
- Is it randomness we can't measure?

---

## 🚀 Getting Started

### For Running the Analysis

1. **Open the notebook:**
   ```
   /Bottleneck/bottleneck_analysis.ipynb
   ```

2. **Read the methodology first:**
   ```
   /Bottleneck/METHODOLOGY.md
   ```
   This explains:
   - Why we're doing this
   - What assumptions we're making
   - How we'll handle randomness
   - What "success" looks like

3. **Run cells sequentially:**
   - Don't skip ahead
   - Each section builds on previous
   - Watch for patterns emerging

4. **Track findings:**
   - Check `/Bottleneck/FINDINGS.md` for discoveries
   - This file grows as analysis progresses

---

## 📊 Analysis Phases

### **Phase 1: Data Exploration** ✅ READY
**File:** `bottleneck_analysis.ipynb` → Section 1

**What we do:**
- Load and understand the data
- Calculate wait time distributions
- Check for obvious patterns
- Correlate patient load with wait times

**Questions answered:**
- What's the average wait? Range?
- Does severity affect wait time?
- Do shifts show different patterns?
- Does "more patients per doctor" → "more waits"?

**Output:** Visualizations + summary statistics

---

### **Phase 2: Bed Occupancy Algorithm** 🔜 NEXT
**Will be added to:** `bottleneck_analysis.ipynb` → Section 2

**What we do:**
- Calculate bed occupancy at key moments
- Determine available beds during wait times
- Answer: "Is bed shortage the blocker?"

**Key Algorithm:**
```
For each patient at Triage End:
  occupied_beds = count(patients where Doctor_Seen <= now <= Exit_Time)
  available_beds = total_capacity - occupied_beds
  
  If (patient_waiting) AND (available_beds > 0) AND (doctor_available):
    → Not a bed problem
    → Likely coordination/process issue
```

---

### **Phase 3: Doctor Idle Detection** 🔜 THEN
**Will be added to:** `bottleneck_analysis.ipynb` → Section 3

**What we do:**
- Identify moments when doctor available but patient waiting
- Account for 10-min transition buffer after each patient
- Find specific bottleneck instances with timestamps

**Output:**
- Count of bottleneck events
- Average duration per event
- Which shifts/severities most affected

---

### **Phase 4: Root Cause Analysis** 🔜 AFTER
**Will be added to:** `bottleneck_analysis.ipynb` → Section 4

**What we do:**
- For each bottleneck: What's the likely cause?
  - Severity-driven (expected, not fixable immediately)
  - Resource-driven (need hiring/expansion)
  - Process-driven (fixable with workflow changes)
  - Random/Unmeasurable (need different approach)

**Output:**
- Categorization of bottlenecks
- % breakdown by cause
- Quantified impact by cause

---

### **Phase 5: Industry Approach Recommendation** 🔜 FINAL
**Will be added to:** `bottleneck_analysis.ipynb` → Section 5

**What we do:**
- If randomness is HIGH: Recommend Process Mining, Simulation, or ML
- If randomness is LOW: Recommend specific operational changes
- Provide clear next steps for management

---

## 🧠 Key Concepts

### **The 4 Factors Affecting Doctor Seen Phase**

```
Patient Wait Time = f(
    Severity,              ← Triage Level (1=Critical, 4=Minor)
    Test Turnaround,       ← Results ready? (NOT in our data)
    Room Availability,     ← Beds free? (WE'LL CALCULATE)
    Staff Workload         ← Doctors available? (WE'LL CHECK)
)
```

### **Doctor "Idle"**
- Doctor is available (finished previous patient + 10-min buffer)
- Patient is waiting (triage done, not with doctor yet)
- Beds/tests aren't blocking (OR we can't verify)
- = **Process failure** (coordination, communication, or assignment delay)

### **Randomness Problem**
- Many factors affect wait time simultaneously
- Some factors we can measure, others we can't
- Simple analysis may find "idle doctors" that are actually blocked by:
  - Test results (delayed lab work)
  - Room turnover (not in our data)
  - Clinical decisions (complex cases take longer)
  
- **Solution:** Document assumptions, run sensitivity analysis, propose advanced methods if needed

---

## 📋 Key Assumptions (See METHODOLOGY.md for Details)

**About Beds:**
- Patient occupies bed from `Doctor Seen` to `Exit Time`
- Beds freed immediately after exit (unrealistic but conservative)
- Bed assignment by severity (ICU→Critical, Regular→Urgent, Fast-Track→Minor)

**About Doctors:**
- Doctors can see any patient (no specialization constraints)
- 10-minute buffer after patient exit for transition/notes
- All doctors equally capable

**About Data:**
- Timestamps are accurate and complete
- No external events affecting flow (disasters, equipment failures)
- Single hospital (MC_ER_EAST)

---

## 🔍 How to Read Results

### **Wait Time Statistics**
```
Mean: 25 minutes      ← Average wait
Median: 18 minutes    ← 50th percentile (better than mean = long-tail outliers)
Std Dev: 22 minutes   ← Variability
P90: 60 minutes       ← 90% of waits are under this
```

### **Correlation** (Load vs Wait)
```
0.85 = Strong positive (more patients → more waits, likely capacity problem)
0.45 = Moderate (multiple factors involved)
0.15 = Weak (other factors dominate, check process/randomness)
```

### **Bottleneck Classification**
```
Severity-Driven:     Patient low priority, waits expected
Resource-Driven:     Few doctors/beds, classic capacity problem
Process-Driven:      Enough resources, coordination failure
Random/Unknown:      Can't explain from available data
```

---

## ⚠️ Limitations & Uncertainties

1. **No test result timing** - We can't know if patient is waiting for lab work
2. **No room assignment logs** - We estimate bed usage, not exact assignments
3. **No explicit doctor-patient matching** - We assume doctors available, don't know actual assignments
4. **Randomness not quantified** - We'll estimate unexplained variance

**Mitigation:** We'll document these and propose advanced methods if randomness is >30%

---

## 📈 Success Criteria

### **Phase 1 Success** (Data Exploration)
✅ Understand wait time distribution  
✅ Identify key patterns  
✅ Find correlation with patient load  

### **Phase 2 Success** (Bed Analysis)
✅ Calculate occupancy algorithm  
✅ Determine if beds are constraint  
✅ Identify "bed-free but patient waiting" instances  

### **Phase 3 Success** (Doctor Idle)
✅ Count bottleneck events  
✅ Quantify wasted time  
✅ Identify worst shifts/times  

### **Phase 4 Success** (Root Cause)
✅ Categorize causes  
✅ Explain >70% of variance  
✅ Identify fixable vs structural issues  

### **Phase 5 Success** (Recommendations)
✅ Clear next steps  
✅ Industry best practice  
✅ Management-ready presentation  

---

## 🛠️ Tools & Technologies

- **Python**: Pandas, NumPy, Matplotlib, Seaborn
- **Analysis**: Descriptive statistics, time-series analysis, queuing theory
- **Next (if needed)**: Process Mining, Simulation, Machine Learning

---

## 📞 Quick Reference

**Main Analysis File:** `/Bottleneck/bottleneck_analysis.ipynb`  
**Methodology:** `/Bottleneck/METHODOLOGY.md`  
**Findings:** `/Bottleneck/FINDINGS.md` (append results here)  
**Data Source:** `/final_data.csv` + `/Cleaned_Datasets/Hospital_facility_out.csv`

---

**Project Start Date:** November 11, 2025  
**Status:** Phase 1 Complete, Phase 2 Ready  
**Next:** Run notebook Section 1 to explore data

