
import streamlit as st

from module.work_coverage import (
    load_employees,
    load_tasks,
    load_leave_requests,
    load_notifications,
    automate_work_coverage,
)

st.set_page_config(
    page_title="LeaveSync",
    page_icon="🏢",
    layout="wide",
)

st.title("Employee Leave & Work Coverage System")
st.caption("Automated task reassignment and employee notifications")

# Load current data
employees = load_employees()
tasks = load_tasks()
leaves = load_leave_requests()
notifications = load_notifications()

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Employees", len(employees))
col2.metric("Tasks", len(tasks))
col3.metric("Leave Requests", len(leaves))
col4.metric("Notifications", len(notifications))

st.divider()

# Approved leave requests
approved_leaves = [
    leave for leave in leaves
    if str(leave.get("status", "")).lower() == "approved"
]

st.subheader("Automatic Work Coverage")

st.write(
    "Run the coverage process for approved leave requests. "
    "The system will look for pending tasks and suitable replacement employees."
)

st.write("Approved leave requests:", len(approved_leaves))

if not approved_leaves:
    st.info("There are no approved leave requests to process.")

if st.button(
    "Run Automatic Work Coverage",
    type="primary",
    disabled=not approved_leaves,
):
    results = []

    with st.spinner("Checking tasks and available employees..."):
        for leave in approved_leaves:
            employee_id = leave.get("employee_id")

            result = automate_work_coverage(employee_id)
            results.append({
                "employee_id": employee_id,
                "reassigned": result["reassigned"],
                "unassigned": result["unassigned"],
            })

    st.session_state["coverage_results"] = results
    st.success("Work coverage process completed.")

# Show the last run's results
if "coverage_results" in st.session_state:
    st.subheader("Latest Run Results")

    for result in st.session_state["coverage_results"]:
        st.write("Employee ID:", result["employee_id"])
        st.write("Tasks reassigned:", len(result["reassigned"]))
        st.write("Tasks without a replacement:", len(result["unassigned"]))

        if result["reassigned"]:
            st.write("Reassigned task details:")
            st.json(result["reassigned"])

        if result["unassigned"]:
            st.warning("Some tasks could not be assigned.")
            st.json(result["unassigned"])

        st.divider()

# Navigation
section = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Employees", "Tasks", "Leave Requests", "Notifications"],
)

if st.sidebar.button("Refresh Data"):
    st.rerun()

if section == "Dashboard":
    st.subheader("Overview")
    st.metric(
        "Pending Tasks",
        sum(1 for task in tasks if task.get("status") == "pending"),
    )
    st.metric(
        "Approved Leaves",
        len(approved_leaves),
    )

elif section == "Employees":
    st.subheader("Employee Directory")
    st.json(employees)

elif section == "Tasks":
    st.subheader("Task Assignments")
    st.json(load_tasks())

elif section == "Leave Requests":
    st.subheader("Leave History")
    st.json(load_leave_requests())

elif section == "Notifications":
    st.subheader("Employee Notifications")
    st.json(load_notifications())
