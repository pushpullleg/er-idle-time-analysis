# Process Design: Current vs. Future State
## Meridian City ER Patient Flow

---

## Current-State Swimlane Diagram

```
┌────────────────┬──────────────┬─────────────┬──────────────┬─────────────────┐
│  PATIENT       │  REGISTRATION│   TRIAGE    │    DOCTOR    │  DISPOSITION    │
└────────────────┴──────────────┴─────────────┴──────────────┴─────────────────┘

  ARRIVAL              ↓
    ↓         Wait: 2 min
    ├─→ [Wait]       ↓
    │     (2 min) [Process] ← Manual check-in, insurance verification
    │       ↓       7.7 min
    │       └─→ [Register patient in system, print wristband]
    │             ↓
    │             [Move to triage area - no real-time queue signal]
    │             ↓
    │        [Triage nurse assigned manually]
    │             ↓
    │        [Assess & assign triage level]
    │             ↓
    │        [Patient waits in queue - ZERO VISIBILITY to doctors]
    │      12.6 min (process)
    │             ↓
    │        [No automated queue board → Doctors don't know who's waiting]
    │      38.6 min WAIT ← **BOTTLENECK**
    │      (Patients piled up, doctors unaware)
    │             ↓
    │        [Nurse pages doctor manually OR doctor asks "who's next?"]
    │             ↓
    │        [Manual room assignment]
    │             ↓
    │        [Doctor enters, reviews chart (slow EHR lookup)]
    │             ↓
    │        [Patient examination & decisions]
    │             ↓
    │        [Lab/imaging ordered (if needed)]
    │             ↓
    │        [Wait for results]
    │             ↓
    │        [Doctor treatment decisions]
    │       107.3 min ← Doctor cycle time (longest stage)
    │             ↓
    │        [Room cleanup & turnover]
    │      8+ min (patients not ready to leave; room not prepped for next)
    │             ↓
    │        [Patient exit/discharge or admission]
    │             ↓
    │        [Manual bed assignment for admits]
    │             ↓
    │        [Manual transport to floor]
    │
    └─→ **Total: 172 minutes average** ← Patient's entire ED experience

KEY PAIN POINTS (Current):
1. Manual patient-doctor assignment (no queue board)
2. Doctors unaware of waiting patients (information gap)
3. Slow EHR lookups (delays when seeing next patient)
4. Room turnover delays (no prep queue, sequential process)
5. Shift handoffs chaotic (no briefing structure)
6. No real-time bottleneck visibility (ops can't see queue growing)
```

---

## Future-State Swimlane Diagram (With Interventions)

```
┌────────────────┬──────────────┬─────────────┬──────────────┬─────────────────┐
│  PATIENT       │  REGISTRATION│   TRIAGE    │    DOCTOR    │  DISPOSITION    │
└────────────────┴──────────────┴─────────────┴──────────────┴─────────────────┘

  ARRIVAL
    ↓
    ├─→ [Quick registration kiosk OR mobile tablet]  ← Faster, self-service
    │       ↓
    │   Wait: 1 min (vs. 2 min)
    │       ↓
    │   Process: 5 min (vs. 7.7 min) ← Streamlined form, auto-insurance lookup
    │       ↓
    │   [Wristband generated, patient auto-routed]
    │       ↓
    │   [Triage START immediately - parallel with registration prep]
    │       ↓
    │   [Triage nurse assigned from real-time queue]
    │       ↓
    │   [Patient assessment, triage level assigned]
    │       ↓
    │   Process: 10–12 min (vs. 12.6 min) ← Focused process
    │       ↓
    │   [REAL-TIME QUEUE BOARD ACTIVATED] ← Game changer!
    │   ├─ Patients auto-sorted by triage level
    │   ├─ Available doctors see waiting queue on dashboard
    │   └─ Next patient + room assignment push-notified
    │       ↓
    │   Wait: 8–10 min (vs. 38.6 min) ← Massive reduction!
    │   Why? Doctors see patients NOW vs. asking "who's next?"
    │       ↓
    │   [AUTO-DISPATCH RULE]
    │   ├─ System: "Doctor available + Room B empty + Patient ready"
    │   ├─ Action: Doctor routed to Room B, patient moved by tech
    │   └─ Time: <2 min vs. 5 min manual coordination
    │       ↓
    │   [Patient in room, doctor charts already pre-loaded on tablet]
    │   ← EHR integration (vs. slow lookup)
    │       ↓
    │   [Doctor assessment & clinical decisions]
    │   ├─ Parallel: Nurse drawing labs, tech prepping imaging
    │   └─ Time: 70–80 min (vs. 107.3 min) ← Compressed via parallelism
    │       ↓
    │   [Results returned faster - orders placed earlier]
    │       ↓
    │   [Doctor final decisions & disposition order]
    │       ↓
    │   [FAST-TRACK PATHWAY (if low-acuity)]
    │   ├─ Nurse practitioners handle minor injuries
    │   ├─ Time: 40–50 min (vs. 107 min for MD)
    │   └─ Frees doctors for complex cases
    │       ↓
    │   [Room turnover - TECH-ASSISTED]
    │   ├─ Cleaning crew alerted via system
    │   ├─ Next patient routed once room ready
    │   └─ Time: 5 min (vs. 8+ min sequential wait)
    │       ↓
    │   [Patient exit with clear next steps]
    │   ├─ Discharge paperwork auto-printed
    │   └─ Transport for admits coordinated in real-time
    │
    └─→ **Target: 130–140 minutes average** ← 20–25% LOS reduction

IMPROVEMENTS (Future State):
✓ Registration: 2 min → 1 min (self-service kiosk)
✓ Registration process: 7.7 → 5 min (streamlined)
✓ Triage process: 12.6 → 10–12 min (focused)
✓ Post-triage wait: 38.6 → 8–10 min (queue board + auto-dispatch)
✓ Doctor cycle: 107.3 → 70–80 min (parallel processing, NP for low-acuity)
✓ Room turnover: 8+ → 5 min (system alerts, prep queue)
✓ Shift handoffs: chaotic → structured 15-min briefing
✓ Utilization: 50% → 75–80% (doctors always have next patient queued)
```

---

## Key Process Improvements

### 1. Real-Time Queue Board (Central Dashboard)

**Purpose:** Eliminate information gap between patients and doctors

**Features:**
- Visual list of all waiting patients (name, age, triage level, wait time)
- Color-coded triage levels (Red=urgent, Yellow=semi-urgent, Green=routine)
- Room availability status (clean, occupied, turning over)
- Doctor availability (active, transitioning, on break)

**Placement:** 
- Main ED wall (visible to all providers)
- Doctor/nurse tablet (push notifications for assignments)
- ER leadership dashboard (monitor queue depth, throughput)

**Technology:** Off-the-shelf queue management system (e.g., Waiting Room Solutions, Qmatic)

**Impact:** Reduces manual assignment friction; doctors see queue instantly

---

### 2. Automated Dispatch Rules

**Logic:**
```
IF (Doctor.available == True 
    AND Room.clean == True 
    AND Patient.ready == True)
THEN 
    Assign Patient → Doctor + Room
    Notify Doctor via pager/tablet
    Move Patient to room
END
```

**Rules by priority:**
1. **Red (Urgent)** – Highest priority, any available doctor
2. **Yellow (Semi-urgent)** – Next available general doctor
3. **Green (Routine)** – Nurse practitioner or fast-track lane preferred

**Implementation:** EHR module or standalone queue management system

**Impact:** Eliminates 2–5 min delay per patient from manual coordination

---

### 3. Structured Shift Handoff Playbook

**Current:** Informal, chaotic, information loss

**Future:** 15-minute structured briefing

**Handoff Meeting Agenda:**
- **2 min:** Queue status (# patients waiting, by triage level)
- **3 min:** Patient snapshots (critical patients, complex cases, boarding admits)
- **5 min:** Staffing & resources (doctors available, NPs, beds, lab capacity)
- **3 min:** Lessons learned from outgoing shift (what slowed things down, wins)
- **2 min:** Goals for incoming shift (# patients target, bottleneck focus)

**Attendees:** Incoming shift lead, outgoing shift lead, charge nurse

**Output:** Handoff log (timestamp, attendees, key notes) for accountability

**Impact:** Reduces confusion, ensures continuity, prevents workflow gaps

---

### 4. Room Turnover SOP (8-Minute Max)

**Current Process:**
1. Patient exits room
2. Doctor documents (slow)
3. Nurse notifies housekeeping (manual call)
4. Housekeeping cleans when available (could be 15+ min wait)
5. Next patient enters

**Future Process:**
1. Patient exits room → System auto-signals room status as "needs cleaning"
2. Cleaning team receives alert on mobile device (push notification)
3. Cleaner arrives within 3 min, completes cleaning in 5 min
4. System updates room status to "ready" → Next patient routed
5. While room is being cleaned, patient documentation is automated/templated

**Tools:**
- Room status dashboard (real-time)
- Mobile alerts for housekeeping
- Cleaning time tracking (identify bottlenecks)

**SLA:** 8-minute max room turnover (vs. current 8–12 min average)

**Impact:** Reduces wait for next patient by 2–3 min; improves room utilization

---

### 5. Fast-Track Pathway for Low-Acuity Cases

**Criteria for Fast-Track:**
- Triage level 4–5 (minor injuries/illnesses)
- No lab/imaging needed (initial assessment)
- Chief complaints: Minor lacerations, simple fractures, URI, ankle sprains, etc.

**Fast-Track Model:**
- Dedicated lane with Nurse Practitioner (NP) or Physician Assistant (PA)
- Patients flow: Registration → Brief triage → NP exam → Discharge
- Typical LOS: 40–50 min (vs. 107+ min with MD in main ED)

**Staffing:**
- 1 NP on all shifts (cost ~$150K/year vs. MD)
- Reduces main ED volume by 20–25% (freeing MDs for complex cases)

**Impact:** Increases throughput by 10–15%; improves patient satisfaction for simple cases

---

### 6. Parallel Processing During Patient Wait

**Current:** Patients wait post-triage with zero activity

**Future:**
- Labs ordered by triage nurse (before doctor assessment) for likely diagnoses
- Imaging requisitions pre-filled based on chief complaint
- Vitals rechecked, flu screens done
- Medication history & allergy verification automated in background

**Benefit:** When doctor sees patient, preliminary data is ready; reduces doctor's cycle time

---

## Implementation Sequence

### Week 1–2: Foundation
1. Install queue management software (hardware, integration with EHR)
2. Design auto-dispatch rules with clinical team
3. Draft shift handoff playbook with operations

### Week 3: Pilot Training
1. Train pilot shift on queue board system
2. Dry-run dispatch rules with role-play
3. Practice handoff meeting

### Week 4–6: Pilot Execution
1. Run on one shift for 3 weeks
2. Monitor KPIs daily (wait times, utilization, workflow issues)
3. Gather feedback, iterate playbooks

### Week 7–8: Scale
1. Roll out to all shifts
2. Train full ER staff
3. Continuous process monitoring

### Week 9+: Optimization
1. Add NP fast-track
2. Optimize dispatch rules based on real data
3. Integrate advanced EHR features

---

## Expected Outcomes

| Stage | Current | Target | Rationale |
|-------|---------|--------|-----------|
| Reg wait | 2.0 | 1.0 | Kiosk self-service |
| Reg process | 7.7 | 5.0 | Streamlined form |
| Triage process | 12.6 | 11.0 | Focused workflow |
| **Post-triage wait** | **38.6** | **8–10** | **Queue board + auto-dispatch** ← Primary lever |
| Doctor cycle | 107.3 | 75–85 | Parallel processing, NP fast-track |
| Room turnover | 8+ | 5 | System alerts, structured cleaning |
| **Total LOS** | **172** | **130–140** | **20–25% reduction** |
| **Throughput** | **6.9/hr** | **8.5–9.2/hr** | **25–33% lift** |

---

**Next:** Review with ER leadership; confirm process changes and staffing model.

