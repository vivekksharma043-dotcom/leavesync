
import json
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"


def load_json(file_name):
    """Load a JSON file from the data folder."""
    file_path = DATA_FOLDER / file_name

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_name, data):
    """Save JSON data and report whether saving succeeded."""
    file_path = DATA_FOLDER / file_name

    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError as error:
        print(f"Could not save {file_name}: {error}")
        return False


def get_next_id(records):
    """Generate the next record ID."""
    return max((record["id"] for record in records), default=0) + 1


def calculate_leave_days(from_date, to_date):
    """Calculate leave duration, including both start and end dates."""
    start = date.fromisoformat(from_date)
    end = date.fromisoformat(to_date)

    if end < start:
        raise ValueError("End date cannot be before start date.")

    return (end - start).days + 1


def apply_leave(employee_id, from_date, to_date, reason):
    """Create a pending leave request after basic validation."""
    try:
        days = calculate_leave_days(from_date, to_date)
    except ValueError as error:
        return {"success": False, "message": str(error)}

    if date.fromisoformat(from_date) < date.today():
        return {
            "success": False,
            "message": "Leave cannot start in the past."
        }

    if not reason.strip():
        return {"success": False, "message": "Reason is required."}

    employees = load_json("employees.json")
    leaves = load_json("leave_requests.json")

    employee = next(
        (item for item in employees if item["id"] == employee_id),
        None
    )

    if employee is None:
        return {"success": False, "message": "Employee not found."}

    balance = employee.get("leave_balance", 0)

    if days > balance:
        return {
            "success": False,
            "message": "Insufficient leave balance."
        }

    # Do not allow overlapping pending or approved requests.
    for leave in leaves:
        if leave["employee_id"] != employee_id:
            continue

        if leave["status"] not in ("pending", "approved"):
            continue

        existing_start = date.fromisoformat(leave["from_date"])
        existing_end = date.fromisoformat(leave["to_date"])
        requested_start = date.fromisoformat(from_date)
        requested_end = date.fromisoformat(to_date)

        if requested_start <= existing_end and requested_end >= existing_start:
            return {
                "success": False,
                "message": "This request overlaps an existing leave request."
            }

    request = {
        "id": get_next_id(leaves),
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "from_date": from_date,
        "to_date": to_date,
        "days": days,
        "reason": reason.strip(),
        "status": "pending"
    }

    leaves.append(request)

    if not save_json("leave_requests.json", leaves):
        return {
            "success": False,
            "message": "Could not save the leave request."
        }

    return {
        "success": True,
        "message": "Leave request submitted successfully.",
        "request": request
    }


def view_leave_requests(status=None):
    """Return all requests, optionally filtered by status."""
    leaves = load_json("leave_requests.json")

    if status is None:
        return leaves

    return [
        leave for leave in leaves
        if leave["status"].lower() == status.lower()
    ]


def review_leave(request_id, decision, reviewer_role=None):
    """Approve or reject a pending request; managers/admins only."""

    if reviewer_role not in {"manager", "admin"}:
        return {
            "success": False,
            "message": "Only managers and admins can review leave requests."
        }

    decision = decision.strip().lower()
    """Approve or reject a pending request."""
    decision = decision.strip().lower()

    if decision not in ("approved", "rejected"):
        return {"success": False, "message": "Invalid decision."}

    employees = load_json("employees.json")
    leaves = load_json("leave_requests.json")

    request = next(
        (leave for leave in leaves if leave["id"] == request_id),
        None
    )

    if request is None:
        return {"success": False, "message": "Leave request not found."}

    if request["status"] != "pending":
        return {
            "success": False,
            "message": "This request has already been reviewed."
        }

    employee = next(
        (
            item for item in employees
            if item["id"] == request["employee_id"]
        ),
        None
    )

    if employee is None:
        return {"success": False, "message": "Employee not found."}

    days = request.get(
        "days",
        calculate_leave_days(request["from_date"], request["to_date"])
    )

    if decision == "approved":
        balance = employee.get("leave_balance", 0)

        if days > balance:
            return {
                "success": False,
                "message": "Insufficient leave balance at approval."
            }

        employee["leave_balance"] = balance - days

        # Save the balance first. Do not mark the request approved
        # if this write fails.
        if not save_json("employees.json", employees):
            return {
                "success": False,
                "message": "Could not update leave balance."
            }

    request["status"] = decision

    if not save_json("leave_requests.json", leaves):
        return {
            "success": False,
            "message": (
                "Could not save the review. Check the data files "
                "before retrying."
            )
        }

    return {
        "success": True,
        "message": f"Leave request {decision}.",
        "request": request
    }
