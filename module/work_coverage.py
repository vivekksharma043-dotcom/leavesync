
import json
import os

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FOLDER, ".."))
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")

def load_json(file_name):
    """Read a JSON file from the data folder and return its contents."""
    file_path = os.path.join(DATA_FOLDER, file_name)
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_name} was not found in {DATA_FOLDER}")
        return []
    except json.JSONDecodeError:
        print(f"Error: {file_name} is not valid JSON (check commas and brackets)")
        return []


def save_json(file_name, data):
    """Write data into a JSON file in the data folder. Returns True if it worked."""
    file_path = os.path.join(DATA_FOLDER, file_name)
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        print(f"Error: could not save {file_name}")
        return False


def load_employees():
    return load_json("employees.json")


def load_tasks():
    return load_json("tasks.json")


def load_leave_requests():
    return load_json("leave_requests.json")


def load_notifications():
    return load_json("notifications.json")

def find_approved_leaves():
    """Return a list of all leave requests whose status is 'approved'."""
    leave_requests = load_leave_requests()
    approved = []
    for leave in leave_requests:
        if leave.get("status") == "approved":
            approved.append(leave)
    return approved


def find_employee_by_id(employee_id):
    """Return the employee dictionary with this ID, or None if not found."""
    employees = load_employees()
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    return None



def process_approved_leaves():
    """Go through every approved leave and start work coverage for each."""
    approved_leaves = find_approved_leaves()
    print("Approved leaves found:", len(approved_leaves))

    for leave in approved_leaves:
        employee_id = leave["employee_id"]
        employee = find_employee_by_id(employee_id)

        if employee is None:
            print(f"Warning: employee ID {employee_id} not found, skipping leave {leave['id']}")
            continue

        print(f"{employee['name']} is on leave from {leave['from_date']} to {leave['to_date']} -> unavailable")
        automate_work_coverage(employee_id)

def find_pending_tasks(employee_id):
    """Return a list of pending tasks assigned to the given employee."""
    tasks = load_tasks()
    pending_tasks = []

    for task in tasks:
        if task.get("assigned_to") == employee_id and task.get("status") == "pending":
            pending_tasks.append(task)

    return pending_tasks


def find_available_employees(absent_employee_id):
    """Return employees who can cover for the absent employee:
    same domain, available is true, and not the absent employee."""
    absent_employee = find_employee_by_id(absent_employee_id)

    if absent_employee is None:
        print(f"Warning: employee ID {absent_employee_id} not found")
        return []

    absent_domain = absent_employee["domain"]
    employees = load_employees()
    candidates = []

    for employee in employees:
        if employee["id"] == absent_employee_id:
            continue
        if employee.get("available") != True:
            continue
        if employee.get("domain") != absent_domain:
            continue
        candidates.append(employee)

    return candidates

#skill match
def calculate_skill_match(required_skills, employee_skills):
    """Return the percentage (0 to 100) of required skills the employee has."""
    # If the task needs no special skills, anyone matches fully
    if len(required_skills) == 0:
        return 100

    # Make everything lowercase so "python" and "Python" count as the same skill
    employee_skills_lower = []
    for skill in employee_skills:
        employee_skills_lower.append(skill.lower())

    matched = 0
    for skill in required_skills:
        if skill.lower() in employee_skills_lower:
            matched = matched + 1

    percentage = (matched / len(required_skills)) * 100
    return percentage

# Employees at or above this workload (in percent) must NOT receive extra work
MAX_WORKLOAD = 80

def calculate_workload_score(workload):
    """Return a score from 0 to 100. Lower workload gives a higher score.
    Returns 0 if the employee is overloaded (at or above MAX_WORKLOAD)."""
    if workload < 0:
        workload = 0

    if workload >= MAX_WORKLOAD:
        return 0

    return 100 - workload

# How important each part is in the final score (together they add up to 1.0)
DOMAIN_WEIGHT = 0.40
SKILL_WEIGHT = 0.40
WORKLOAD_WEIGHT = 0.20


def calculate_coverage_score(domain_score, skill_score, workload_score):
    """Combine the three scores (each 0 to 100) into one final score."""
    final_score = (
        domain_score * DOMAIN_WEIGHT
        + skill_score * SKILL_WEIGHT
        + workload_score * WORKLOAD_WEIGHT
    )
    return round(final_score, 2)


NO_SUITABLE_EMPLOYEE = "No suitable employee found"


def get_score(item):
    """Helper used for sorting: returns the score stored in one entry."""
    return item["score"]


def select_best_employee(task, candidates):
    """Return the best employee dictionary for this task,
    or NO_SUITABLE_EMPLOYEE if nobody qualifies."""
    scored_candidates = []

    for employee in candidates:
        # Rule: never give extra work to an overloaded employee
        if employee["workload"] >= MAX_WORKLOAD:
            continue

        skill_score = calculate_skill_match(task.get("required_skills", []), employee["skills"])
        workload_score = calculate_workload_score(employee["workload"])
        coverage_score = calculate_coverage_score(100, skill_score, workload_score)

        scored_candidates.append({"employee": employee, "score": coverage_score})

    if len(scored_candidates) == 0:
        return NO_SUITABLE_EMPLOYEE

    scored_candidates.sort(key=get_score, reverse=True)
    return scored_candidates[0]["employee"]


def assign_task(task_id, employee_id):
    """Reassign a pending task to a new employee and save tasks.json.
    Returns the updated task, or None if nothing was changed."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            # Safety rule: only pending tasks can be reassigned
            if task["status"] != "pending":
                print(f"Warning: task {task_id} is not pending (status: {task['status']}), not reassigned")
                return None

            task["previous_assignee"] = task["assigned_to"]
            task["assigned_to"] = employee_id
            task["status"] = "reassigned"

            if save_json("tasks.json", tasks):
                return task
            return None

    print(f"Warning: task {task_id} not found")
    return None

def get_next_notification_id(notifications):
    """Return the next free notification ID (highest existing ID + 1)."""
    highest = 0
    for notification in notifications:
        if notification["id"] > highest:
            highest = notification["id"]
    return highest + 1


def create_notification(employee_id, task):
    """Add an unread notification telling the employee about their new task.
    Returns the new notification, or None if saving failed."""
    notifications = load_notifications()

    new_notification = {
        "id": get_next_notification_id(notifications),
        "employee_id": employee_id,
        "message": f"You have been assigned the task: {task['title']}",
        "task_id": task["id"],
        "status": "unread"
    }

    notifications.append(new_notification)

    if save_json("notifications.json", notifications):
        return new_notification
    return None


def view_notifications(employee_id):
    """Return all notifications that belong to this employee."""
    notifications = load_notifications()
    my_notifications = []

    for notification in notifications:
        if notification["employee_id"] == employee_id:
            my_notifications.append(notification)

    return my_notifications

def mark_notification_as_read(notification_id, employee_id=None):
    """Mark a notification as read, optionally verifying employee ownership."""
    notifications = load_notifications()

    for notification in notifications:
        if str(notification.get("id")) == str(notification_id):

            # If an employee ID is supplied, verify notification ownership.
            if employee_id is not None:
                if str(notification.get("employee_id")) != str(employee_id):
                    print("Warning: notification ownership check failed")
                    return False

            notification["status"] = "read"
            return save_json("notifications.json", notifications)

    print(f"Warning: notification {notification_id} not found")
    return False

    
    # How much extra workload (in percent) one reassigned task adds to a person
WORKLOAD_PER_TASK = 10


def automate_work_coverage(employee_id):
    """Reassign all pending tasks of an absent employee to the best available
    colleagues, and notify them. Returns a summary dictionary."""
    result = {"employee_id": employee_id, "reassigned": [], "unassigned": []}

    print(f"Starting work coverage for employee ID {employee_id}")

    pending_tasks = find_pending_tasks(employee_id)
    print("Pending tasks found:", len(pending_tasks))
    if len(pending_tasks) == 0:
        return result

    candidates = find_available_employees(employee_id)
    print("Candidates found:", len(candidates))

    for task in pending_tasks:
        best = select_best_employee(task, candidates)

        if best == NO_SUITABLE_EMPLOYEE:
            print(f"Task '{task['title']}' -> {NO_SUITABLE_EMPLOYEE}")
            result["unassigned"].append(task["id"])
            continue

        updated_task = assign_task(task["id"], best["id"])
        if updated_task is None:
            print(f"Task '{task['title']}' -> could not be assigned")
            result["unassigned"].append(task["id"])
            continue

        create_notification(best["id"], updated_task)

        # Count the new task in this person's workload for the rest of this run
        best["workload"] = best["workload"] + WORKLOAD_PER_TASK

        result["reassigned"].append({"task_id": task["id"], "new_employee_id": best["id"]})
        print(f"Task '{task['title']}' -> assigned to {best['name']}")

    return result