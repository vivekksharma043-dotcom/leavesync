

from module.leave_management import (
    apply_leave,
    view_leave_requests as get_leave_requests,
    review_leave,
)


from module.work_coverage import (
    load_employees,
    load_tasks,
    load_leave_requests,
    load_notifications,
    automate_work_coverage,
)


def view_employees():
    """Display all employees."""
    employees = load_employees()

    print("\n--- EMPLOYEE DIRECTORY ---")

    if not employees:
        print("No employees found.")
        return

    for employee in employees:
        print(
            f"ID: {employee['id']} | "
            f"Name: {employee['name']} | "
            f"Domain: {employee['domain']} | "
            f"Workload: {employee['workload']}%"
        )


def view_leave_requests():
    """Display all leave requests."""
    leaves = load_leave_requests()

    print("\n--- LEAVE REQUESTS ---")

    if not leaves:
        print("No leave requests found.")
        return

    for leave in leaves:
        print(
            f"ID: {leave['id']} | "
            f"Employee: {leave['employee_name']} | "
            f"From: {leave['from_date']} | "
            f"To: {leave['to_date']} | "
            f"Status: {leave['status']}"
        )


def view_tasks():
    """Display all tasks."""
    tasks = load_tasks()

    print("\n--- TASKS ---")

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(
            f"ID: {task['id']} | "
            f"Title: {task['title']} | "
            f"Assigned to: {task['assigned_to']} | "
            f"Status: {task['status']}"
        )


def view_notifications():
    """Display all notifications."""
    notifications = load_notifications()

    print("\n--- NOTIFICATIONS ---")

    if not notifications:
        print("No notifications found.")
        return

    for notification in notifications:
        print(
            f"ID: {notification['id']} | "
            f"Employee ID: {notification['employee_id']} | "
            f"Status: {notification['status']} | "
            f"Message: {notification['message']}"
        )


def run_coverage():
    """Run existing work-coverage automation for an employee."""
    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Invalid input. Enter a numeric employee ID.")
        return

    employees = load_employees()

    if not any(employee["id"] == employee_id for employee in employees):
        print("Employee not found.")
        return

    confirm = input(
        "This may change tasks.json and notifications.json. "
        "Continue? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Coverage process cancelled.")
        return

    result = automate_work_coverage(employee_id)

    print("\n--- COVERAGE SUMMARY ---")
    print("Reassigned:", len(result["reassigned"]))
    print("Unassigned:", len(result["unassigned"]))

    
def apply_leave_menu():
    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Invalid employee ID. Enter a number.")
        return

    from_date = input("Leave start date (YYYY-MM-DD): ").strip()
    to_date = input("Leave end date (YYYY-MM-DD): ").strip()
    reason = input("Reason for leave: ").strip()

    result = apply_leave(employee_id, from_date, to_date, reason)
    print(result["message"])

    if result.get("success"):
        print("Request ID:", result["request"]["id"])


def view_leave_menu():
    print("\n1. View all requests")
    print("2. View pending requests")
    print("3. View approved requests")
    print("4. View rejected requests")

    choice = input("Choose an option: ").strip()

    statuses = {
        "1": None,
        "2": "pending",
        "3": "approved",
        "4": "rejected",
    }

    if choice not in statuses:
        print("Invalid choice.")
        return

    requests = get_leave_requests(statuses[choice])

    if not requests:
        print("No leave requests found.")
        return

    for request in requests:
        print(
            f"ID: {request['id']} | "
            f"Employee: {request['employee_name']} | "
            f"Dates: {request['from_date']} to {request['to_date']} | "
            f"Status: {request['status']}"
        )


def review_leave_menu():
    requests = get_leave_requests("pending")
    if not requests:
        print("No pending requests to review.")
        return

    for request in requests:
        print(
            f"ID: {request['id']} | "
            f"Employee: {request['employee_name']} | "
            f"Status: {request['status']}"
        )

    try:
        request_id = int(input("Enter request ID: "))
    except ValueError:
        print("Invalid request ID.")
        return

    print("1. Approve")
    print("2. Reject")

    decision = input("Choose an action: ").strip()
    decisions = {"1": "approved", "2": "rejected"}

    if decision not in decisions:
        print("Invalid action.")
        return

    result = review_leave(request_id, decisions[decision])
    print(result["message"])



def main():
    """Run the WorkMesh terminal application."""

    while True:
        print("\n" + "=" * 40)
        print("       WORKMESH")
        print(" Employee Leave & Work Coverage")
        print("=" * 40)
        print("1. View Employees")
        print("2. View Leave Requests")
        print("3. View Tasks")
        print("4. View Notifications")
        print("5. Run Work Coverage")
        print("6. Apply for Leave")
        print("7. View Leave Requests")
        print("8. Review Leave Request")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_employees()
        elif choice == "2":
            view_leave_requests()
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            view_notifications()
        elif choice == "5":
            run_coverage()
        elif choice == "0":
            print("Exiting WorkMesh. Goodbye!")
        elif choice == "6":
            apply_leave_menu()
        elif choice == "7":
            view_leave_menu()
        elif choice == "8":
            review_leave_menu()    
            break
        else:
            print("Invalid choice. Please select a listed option.")


if __name__ == "__main__":
    main()

    
def apply_leave_menu():
    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Invalid employee ID. Enter a number.")
        return

    from_date = input("Leave start date (YYYY-MM-DD): ").strip()
    to_date = input("Leave end date (YYYY-MM-DD): ").strip()
    reason = input("Reason for leave: ").strip()

    result = apply_leave(employee_id, from_date, to_date, reason)
    print(result["message"])

    if result.get("success"):
        print("Request ID:", result["request"]["id"])
        print("Status: pending")


def view_leave_menu():
    print("\n1. View all requests")
    print("2. View pending requests")
    print("3. View approved requests")
    print("4. View rejected requests")

    choice = input("Choose an option: ").strip()

    statuses = {
        "1": None,
        "2": "pending",
        "3": "approved",
        "4": "rejected",
    }

    if choice not in statuses:
        print("Invalid choice.")
        return

    requests = view_leave_requests(statuses[choice])

    if not requests:
        print("No leave requests found.")
        return

    for request in requests:
        print(
            f"ID: {request['id']} | "
            f"Employee: {request['employee_name']} | "
            f"Dates: {request['from_date']} to {request['to_date']} | "
            f"Days: {request.get('days', 'N/A')} | "
            f"Status: {request['status']}"
        )


def review_leave_menu():
    requests = view_leave_requests("pending")

    if not requests:
        print("No pending requests to review.")
        return

    for request in requests:
        print(
            f"ID: {request['id']} | "
            f"Employee: {request['employee_name']} | "
            f"Dates: {request['from_date']} to {request['to_date']} | "
            f"Days: {request.get('days', 'N/A')}"
        )

    try:
        request_id = int(input("Enter request ID to review: "))
    except ValueError:
        print("Invalid request ID.")
        return

    print("1. Approve")
    print("2. Reject")

    decision = input("Choose an action: ").strip()

    decisions = {"1": "approved", "2": "rejected"}

    if decision not in decisions:
        print("Invalid action.")
        return

    result = review_leave(request_id, decisions[decision])
    print(result["message"])

