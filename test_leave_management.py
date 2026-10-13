
from module.leave_management import (
    calculate_leave_days,
    view_leave_requests,
)

print("--- LEAVE MANAGEMENT TEST ---")

print(
    "Three-day leave:",
    calculate_leave_days("2026-11-10", "2026-11-12")
)

print(
    "Single-day leave:",
    calculate_leave_days("2026-11-10", "2026-11-10")
)

try:
    calculate_leave_days("2026-11-12", "2026-11-10")
except ValueError as error:
    print("Invalid date range:", error)

print("All requests:", len(view_leave_requests()))
print("Pending requests:", len(view_leave_requests("pending")))

print("Leave management module loaded successfully.")
