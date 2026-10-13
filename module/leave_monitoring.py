from module.leave_management import load_json
from datetime import date


def view_leave_history(employee_id):
    leaves = load_json("leave_requests.json")

    employee_leaves = [
        leave for leave in leaves
        if leave["employee_id"] == employee_id
    ]

    print("\n===== LEAVE HISTORY =====")

    if not employee_leaves:
        print("No leave history found.")
        return

    for leave in employee_leaves:
        print("Employee:", leave["employee_name"])
        print("From:", leave["from_date"])
        print("To:", leave["to_date"])
        print("Reason:", leave["reason"])
        print("Status:", leave["status"])
        print("-" * 30)


def view_currently_on_leave():
    employees = load_json("employees.json")
    leaves = load_json("leave_requests.json")

    today = date.today()
    found = False

    print("\n===== EMPLOYEES CURRENTLY ON LEAVE =====")

    for leave in leaves:
        if leave["status"].lower() != "approved":
            continue

        start = date.fromisoformat(leave["from_date"])
        end = date.fromisoformat(leave["to_date"])

        if start <= today <= end:
            employee = next(
                (
                    emp for emp in employees
                    if emp["id"] == leave["employee_id"]
                ),
                None
            )

            if employee:
                print(employee["name"], "-", start, "to", end)
                found = True

    if not found:
        print("No employees currently on leave.")


def view_pending_requests():
    leaves = load_json("leave_requests.json")

    print("\n===== PENDING LEAVE REQUESTS =====")

    found = False

    for leave in leaves:
        if leave["status"].lower() == "pending":
            print("Request ID:", leave["id"])
            print("Employee:", leave["employee_name"])
            print("From:", leave["from_date"])
            print("To:", leave["to_date"])
            print("Reason:", leave["reason"])
            print("-" * 30)
            found = True

    if not found:
        print("No pending requests.")


def view_leave_summary(employee_id):
    leaves = load_json("leave_requests.json")

    employee_leaves = [
        leave for leave in leaves
        if leave["employee_id"] == employee_id
    ]

    print("\n===== LEAVE SUMMARY =====")
    print("Total Requests:", len(employee_leaves))
    print(
        "Approved:",
        sum(leave["status"].lower() == "approved"
            for leave in employee_leaves)
    )
    print(
        "Rejected:",
        sum(leave["status"].lower() == "rejected"
            for leave in employee_leaves)
    )
    print(
        "Pending:",
        sum(leave["status"].lower() == "pending"
            for leave in employee_leaves)
    )