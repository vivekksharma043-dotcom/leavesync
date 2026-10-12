from module.work_coverage import (
    load_employees,
    load_tasks,
    load_leave_requests,
    load_notifications,
    save_json,
)

employees = load_employees()
tasks = load_tasks()
leaves = load_leave_requests()
notifications = load_notifications()

print("Employees loaded:", len(employees))
print("Tasks loaded:", len(tasks))
print("Leave requests loaded:", len(leaves))
print("Notifications loaded:", len(notifications))

print("First employee:", employees[0]["name"])
print("First task:", tasks[0]["title"])

# Save test: write notifications back unchanged (safe, nothing changes)
print("Save worked:", save_json("notifications.json", notifications))

from module.work_coverage import process_approved_leaves
#phase 2
print("--- Phase 2 test ---")
#process_approved_leaves()

from module.work_coverage import find_pending_tasks

print("--- Phase 3 test ---")
pending = find_pending_tasks(1)
print("Pending tasks for employee 1:", len(pending))
for task in pending:
    print("-", task["id"], task["title"])

print("Pending tasks for employee 99:", len(find_pending_tasks(99)))
#aviable employee

from module.work_coverage import find_available_employees

print("--- Phase 4 test ---")
candidates = find_available_employees(1)
print("Candidates found:", len(candidates))
for person in candidates:
    print("-", person["name"], "(ID", person["id"], ")")

print("Candidates for Priya (Frontend):", len(find_available_employees(4)))
from module.work_coverage import calculate_skill_match

from module.work_coverage import calculate_skill_match

print("--- Phase 5 test ---")
required = ["Python", "FastAPI"]

print("Candidate with Python, SQL:", calculate_skill_match(required, ["Python", "SQL"]))
print("Candidate with Python, FastAPI, SQL:", calculate_skill_match(required, ["Python", "FastAPI", "SQL"]))
print("Candidate with HTML, CSS:", calculate_skill_match(required, ["HTML", "CSS"]))
print("Lowercase skills:", calculate_skill_match(required, ["python", "fastapi"]))
print("Task needing no skills:", calculate_skill_match([], ["Python"]))

from module.work_coverage import calculate_workload_score

print("--- Phase 6 test ---")
for load in [0, 20, 39, 40, 60, 79, 80, 95]:
    print("Workload", load, "-> score", calculate_workload_score(load))

    from module.work_coverage import calculate_coverage_score

print("--- Phase 7 test ---")
print("Roadmap example (100, 80, 70):", calculate_coverage_score(100, 80, 70))
print("Perfect candidate (100, 100, 100):", calculate_coverage_score(100, 100, 100))
print("No skills (100, 0, 100):", calculate_coverage_score(100, 0, 100))

# Compare two real candidates for a task needing Python and FastAPI
required = ["Python", "FastAPI"]

amit_skill = calculate_skill_match(required, ["Python", "FastAPI"])
amit_load = calculate_workload_score(35)
print("Amit:", calculate_coverage_score(100, amit_skill, amit_load))

rohan_skill = calculate_skill_match(required, ["Python", "SQL"])
rohan_load = calculate_workload_score(60)
print("Rohan:", calculate_coverage_score(100, rohan_skill, rohan_load))

from module.work_coverage import select_best_employee

print("--- Phase 8 test ---")
candidates = find_available_employees(1)
for task in find_pending_tasks(1):
    best = select_best_employee(task, candidates)
    if best == "No suitable employee found":
        print(task["title"], "->", best)
    else:
        print(task["title"], "-> Best:", best["name"])

# Overloaded candidate should be ignored
overloaded = [{"id": 9, "name": "Busy", "skills": ["Python", "FastAPI"], "workload": 85}]
print("Overloaded only:", select_best_employee(find_pending_tasks(1)[0], overloaded))

# No candidates at all
print("Empty list:", select_best_employee(find_pending_tasks(1)[0], []))

from module.work_coverage import assign_task

print("--- Phase 9 test ---")
original_tasks = load_tasks()   # backup, so this test leaves tasks.json unchanged

updated = assign_task(101, 2)
print("Reassigned task:", updated["id"], updated["title"])
print("assigned_to:", updated["assigned_to"])
print("previous_assignee:", updated["previous_assignee"])
print("status:", updated["status"])

print("Second attempt:", assign_task(101, 3))
print("Unknown task:", assign_task(999, 2))

save_json("tasks.json", original_tasks)   # restore the original data
print("tasks.json restored")

from module.work_coverage import create_notification, view_notifications, mark_notification_as_read

print("--- Phase 10 test ---")
original_notifications = load_notifications()   # backup, restored at the end
all_tasks = load_tasks()

n1 = create_notification(2, all_tasks[0])
n2 = create_notification(2, all_tasks[1])
print("Created notification", n1["id"], "for employee 2")
print("Created notification", n2["id"], "for employee 2")

mine = view_notifications(2)
print("Notifications for employee 2:", len(mine))
for n in mine:
    print("-", n["id"], n["status"], "|", n["message"])

print("Notifications for employee 3:", len(view_notifications(3)))

print("Marked as read:", mark_notification_as_read(n1["id"]))
for n in view_notifications(2):
    print("-", n["id"], n["status"])
print("Unknown notification:", mark_notification_as_read(999))

save_json("notifications.json", original_notifications)   # restore
print("notifications.json restored")

from module.work_coverage import automate_work_coverage

print("--- Phase 11 test ---")
backup_tasks = load_tasks()
backup_notifications = load_notifications()

summary = automate_work_coverage(1)
print("Reassigned:", len(summary["reassigned"]), "| Unassigned:", len(summary["unassigned"]))

print("Amit's notifications:", len(view_notifications(2)))
print("Rohan's notifications:", len(view_notifications(3)))
for task in load_tasks():
    print("-", task["id"], task["title"], "->", task["assigned_to"], task["status"])

print("Running again:")
automate_work_coverage(1)

print("Employee with no tasks:")
automate_work_coverage(99)

save_json("tasks.json", backup_tasks)
save_json("notifications.json", backup_notifications)
print("Data restored")