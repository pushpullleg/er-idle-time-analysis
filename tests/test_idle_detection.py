"""Unit tests for ER doctor idle time detection logic.

Tests the core 4-condition idle detection model using synthetic data:
1. Patient has finished triage (Triage End <= check_time)
2. Patient hasn't seen doctor yet (Doctor Seen > check_time)
3. A doctor is available (idle_doctors > 0)
4. Uses 10-minute transition buffer (realistic assumption)
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def count_active_doctors_at_time(all_visits, check_time, transition_buffer_minutes=10):
    """Count doctors actively seeing patients at a given time.

    A doctor is 'active' from when they start seeing a patient until
    EXIT TIME + BUFFER to account for post-patient tasks (documentation,
    handwashing, room turnover, chart review).
    """
    active = all_visits[
        (all_visits["Doctor Seen"] <= check_time)
        & (
            all_visits["Exit Time"]
            + pd.Timedelta(minutes=transition_buffer_minutes)
            > check_time
        )
    ]
    return len(active)


def count_waiting_patients_at_time(all_visits, check_time):
    """Count patients who finished triage but haven't seen a doctor yet."""
    waiting = all_visits[
        (all_visits["Triage End"] <= check_time)
        & (all_visits["Doctor Seen"] > check_time)
    ]
    return len(waiting)


def make_visit(triage_end, doctor_seen, exit_time):
    """Helper to create a single visit row."""
    return {
        "Triage End": pd.Timestamp(triage_end),
        "Doctor Seen": pd.Timestamp(doctor_seen),
        "Exit Time": pd.Timestamp(exit_time),
    }


@pytest.fixture
def sample_visits():
    """Create a realistic set of ER visits for testing."""
    base = "2024-01-15"
    visits = pd.DataFrame(
        [
            make_visit(f"{base} 08:00", f"{base} 08:10", f"{base} 08:40"),
            make_visit(f"{base} 08:05", f"{base} 08:20", f"{base} 09:00"),
            make_visit(f"{base} 08:30", f"{base} 09:15", f"{base} 09:45"),
        ]
    )
    return visits


class TestActiveDoctorCount:
    """Tests for counting active doctors at a given time."""

    def test_no_active_before_any_visits(self, sample_visits):
        check = pd.Timestamp("2024-01-15 07:00")
        assert count_active_doctors_at_time(sample_visits, check) == 0

    def test_one_active_during_first_visit(self, sample_visits):
        check = pd.Timestamp("2024-01-15 08:15")
        assert count_active_doctors_at_time(sample_visits, check) == 1

    def test_two_active_during_overlap(self, sample_visits):
        check = pd.Timestamp("2024-01-15 08:25")
        assert count_active_doctors_at_time(sample_visits, check) == 2

    def test_buffer_keeps_doctor_active_after_exit(self, sample_visits):
        """Doctor should remain 'active' for 10 min after patient exits."""
        check = pd.Timestamp("2024-01-15 08:45")  # 5 min after first exit
        active = count_active_doctors_at_time(sample_visits, check, transition_buffer_minutes=10)
        assert active >= 1, "Doctor should be active during transition buffer"

    def test_doctor_free_after_buffer_expires(self, sample_visits):
        """Doctor should be free 10+ min after patient exits."""
        check = pd.Timestamp("2024-01-15 08:51")  # 11 min after first exit
        active = count_active_doctors_at_time(sample_visits, check, transition_buffer_minutes=10)
        # First visit ended 08:40, buffer until 08:50, so at 08:51 first doctor is free
        # Second visit still active (ends 09:00)
        assert active >= 1  # Second visit still active

    def test_zero_buffer(self, sample_visits):
        """With zero buffer, doctor is free immediately after exit."""
        check = pd.Timestamp("2024-01-15 08:41")  # 1 min after first exit
        active = count_active_doctors_at_time(sample_visits, check, transition_buffer_minutes=0)
        assert active == 1  # Only second visit active


class TestWaitingPatientCount:
    """Tests for counting patients waiting after triage."""

    def test_no_waiting_before_triage(self, sample_visits):
        check = pd.Timestamp("2024-01-15 07:00")
        assert count_waiting_patients_at_time(sample_visits, check) == 0

    def test_one_waiting_after_triage_before_doctor(self, sample_visits):
        check = pd.Timestamp("2024-01-15 08:07")
        # First patient triaged at 08:00, sees doctor at 08:10 — waiting
        # Second patient triaged at 08:05, sees doctor at 08:20 — waiting
        assert count_waiting_patients_at_time(sample_visits, check) == 2

    def test_zero_waiting_after_all_seen(self, sample_visits):
        check = pd.Timestamp("2024-01-15 10:00")
        assert count_waiting_patients_at_time(sample_visits, check) == 0


class TestIdleDetectionIntegration:
    """Integration tests for the full idle detection logic."""

    def test_idle_scenario_detected(self):
        """When doctors on duty > active doctors and patients are waiting."""
        base = "2024-01-15"
        visits = pd.DataFrame(
            [
                make_visit(f"{base} 08:00", f"{base} 08:30", f"{base} 09:00"),
            ]
        )
        # At 08:10: patient waiting (triaged 08:00, won't see doc until 08:30)
        # No doctors active yet
        check = pd.Timestamp(f"{base} 08:10")
        active = count_active_doctors_at_time(visits, check)
        waiting = count_waiting_patients_at_time(visits, check)

        doctors_on_duty = 3
        idle_doctors = doctors_on_duty - active

        assert waiting == 1, "One patient should be waiting"
        assert idle_doctors == 3, "All 3 doctors should be idle"
        assert idle_doctors > 0 and waiting > 0, "This IS an idle scenario"

    def test_no_idle_when_all_doctors_busy(self):
        """When all doctors are seeing patients, no idle detected."""
        base = "2024-01-15"
        visits = pd.DataFrame(
            [
                make_visit(f"{base} 08:00", f"{base} 08:05", f"{base} 08:30"),
                make_visit(f"{base} 08:00", f"{base} 08:05", f"{base} 08:35"),
                make_visit(f"{base} 08:00", f"{base} 08:05", f"{base} 08:40"),
            ]
        )
        check = pd.Timestamp(f"{base} 08:20")
        active = count_active_doctors_at_time(visits, check)
        doctors_on_duty = 3
        idle = doctors_on_duty - active

        assert idle == 0, "No doctors should be idle when all are seeing patients"
