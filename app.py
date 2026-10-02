import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KBC — Event Command Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DEMO DATA
# ============================================================
# These datasets follow the agreed KBC data model.
# They can later be replaced by data returned from Aravind's
# backend / dependency engine.
# ============================================================

EVENTS = [
    {
        "event_id": "EVT001",
        "event_name": "TechFest 2026",
        "date": "2026-10-03",
        "status": "Active",
    }
]


VENUES = [
    {
        "venue_id": "VEN001",
        "venue_name": "Main Auditorium",
        "capacity": 500,
        "status": "Available",
    },
    {
        "venue_id": "VEN002",
        "venue_name": "Auditorium B",
        "capacity": 300,
        "status": "Available",
    },
    {
        "venue_id": "VEN003",
        "venue_name": "Innovation Hall",
        "capacity": 200,
        "status": "Available",
    },
]


SESSIONS = [
    {
        "session_id": "SES001",
        "session_name": "AI Keynote",
        "venue": "Main Auditorium",
        "start_time": "10:00",
        "end_time": "11:00",
        "speaker": "Dr. Rao",
        "status": "Scheduled",
    },
    {
        "session_id": "SES002",
        "session_name": "Robotics Workshop",
        "venue": "Main Auditorium",
        "start_time": "11:30",
        "end_time": "13:00",
        "speaker": "Prof. Mehta",
        "status": "Scheduled",
    },
    {
        "session_id": "SES003",
        "session_name": "Hardware Demo",
        "venue": "Main Auditorium",
        "start_time": "14:00",
        "end_time": "15:00",
        "speaker": "Arjun Labs",
        "status": "Scheduled",
    },
    {
        "session_id": "SES004",
        "session_name": "Startup Panel",
        "venue": "Innovation Hall",
        "start_time": "11:00",
        "end_time": "12:00",
        "speaker": "Industry Panel",
        "status": "Scheduled",
    },
    {
        "session_id": "SES005",
        "session_name": "Coding Challenge",
        "venue": "Auditorium B",
        "start_time": "13:00",
        "end_time": "15:00",
        "speaker": "TechFest Team",
        "status": "Scheduled",
    },
]


VOLUNTEERS = [
    {
        "volunteer_id": "VOL001",
        "name": "Rahul",
        "role": "Registration",
        "availability": "09:00-17:00",
        "status": "Assigned",
    },
    {
        "volunteer_id": "VOL002",
        "name": "Priya",
        "role": "Technical",
        "availability": "09:00-17:00",
        "status": "Assigned",
    },
    {
        "volunteer_id": "VOL003",
        "name": "Aman",
        "role": "Operations",
        "availability": "09:00-17:00",
        "status": "Assigned",
    },
    {
        "volunteer_id": "VOL004",
        "name": "Sneha",
        "role": "Volunteers",
        "availability": "10:00-18:00",
        "status": "Assigned",
    },
    {
        "volunteer_id": "VOL005",
        "name": "Karan",
        "role": "Technical",
        "availability": "09:00-16:00",
        "status": "Assigned",
    },
    {
        "volunteer_id": "VOL006",
        "name": "Ananya",
        "role": "Marketing",
        "availability": "09:00-17:00",
        "status": "Assigned",
    },
]


# Relationship:
# Session -> Volunteers
#
# We keep this as a separate mapping so that the six agreed
# entities keep their exact fields.

SESSION_VOLUNTEERS = {
    "SES001": ["VOL001", "VOL002", "VOL003"],
    "SES002": ["VOL003", "VOL004", "VOL005"],
    "SES003": ["VOL002", "VOL005"],
    "SES004": ["VOL006"],
    "SES005": ["VOL001", "VOL004"],
}


RESOURCES = [
    {
        "resource_id": "RES001",
        "resource": "Projector",
        "type": "Equipment",
        "assigned_session": "SES001",
        "status": "Assigned",
    },
    {
        "resource_id": "RES002",
        "resource": "Wireless Microphones",
        "type": "Equipment",
        "assigned_session": "SES001",
        "status": "Assigned",
    },
    {
        "resource_id": "RES003",
        "resource": "Robotics Kit",
        "type": "Equipment",
        "assigned_session": "SES002",
        "status": "Assigned",
    },
    {
        "resource_id": "RES004",
        "resource": "Display System",
        "type": "Equipment",
        "assigned_session": "SES003",
        "status": "Assigned",
    },
    {
        "resource_id": "RES005",
        "resource": "Stage Microphones",
        "type": "Equipment",
        "assigned_session": "SES003",
        "status": "Assigned",
    },
    {
        "resource_id": "RES006",
        "resource": "Projector",
        "type": "Equipment",
        "assigned_session": "SES004",
        "status": "Assigned",
    },
]


TASKS = [
    {
        "task_id": "TASK001",
        "task": "Confirm keynote venue",
        "owner": "Operations Team",
        "deadline": "09:00",
        "status": "Completed",
        "priority": "Medium",
        "related_item": "SES001",
    },
    {
        "task_id": "TASK002",
        "task": "Move projector to Main Auditorium",
        "owner": "Technical Team",
        "deadline": "09:30",
        "status": "Pending",
        "priority": "High",
        "related_item": "SES001",
    },
    {
        "task_id": "TASK003",
        "task": "Prepare robotics equipment",
        "owner": "Technical Team",
        "deadline": "10:30",
        "status": "Pending",
        "priority": "Medium",
        "related_item": "SES002",
    },
    {
        "task_id": "TASK004",
        "task": "Update session location signage",
        "owner": "Operations Team",
        "deadline": "10:00",
        "status": "Pending",
        "priority": "High",
        "related_item": "SES002",
    },
    {
        "task_id": "TASK005",
        "task": "Notify participants about venue",
        "owner": "Marketing Team",
        "deadline": "09:45",
        "status": "Blocked",
        "priority": "High",
        "related_item": "SES001",
    },
    {
        "task_id": "TASK006",
        "task": "Prepare registration desk",
        "owner": "Registration Team",
        "deadline": "09:15",
        "status": "Completed",
        "priority": "Medium",
        "related_item": "SES005",
    },
    {
        "task_id": "TASK007",
        "task": "Confirm volunteer shifts",
        "owner": "Volunteer Team",
        "deadline": "09:30",
        "status": "Pending",
        "priority": "Medium",
        "related_item": "SES002",
    },
    {
        "task_id": "TASK008",
        "task": "Check emergency access route",
        "owner": "Operations Team",
        "deadline": "10:00",
        "status": "Pending",
        "priority": "High",
        "related_item": "VEN001",
    },
]


# ============================================================
# SESSION STATE
# ============================================================

if "generated_tasks" not in st.session_state:
    st.session_state.generated_tasks = []

if "last_impact" not in st.session_state:
    st.session_state.last_impact = None


# ============================================================
# DATA HELPERS
# ============================================================

def all_tasks():
    """Return original tasks + tasks generated during this session."""
    return TASKS + st.session_state.generated_tasks


def session_lookup():
    return {session["session_id"]: session for session in SESSIONS}


def volunteer_lookup():
    return {vol["volunteer_id"]: vol for vol in VOLUNTEERS}


def find_affected_sessions(old_venue):
    """Demo implementation of venue -> session dependency."""

    return [
        session
        for session in SESSIONS
        if session["venue"] == old_venue
    ]


def find_affected_volunteers(affected_sessions):
    """Demo implementation of session -> volunteer dependency."""

    volunteer_ids = set()

    for session in affected_sessions:
        ids = SESSION_VOLUNTEERS.get(session["session_id"], [])
        volunteer_ids.update(ids)

    lookup = volunteer_lookup()

    return [
        lookup[volunteer_id]
        for volunteer_id in volunteer_ids
        if volunteer_id in lookup
    ]


def find_affected_resources(affected_sessions):
    """Demo implementation of session -> resource dependency."""

    session_ids = {
        session["session_id"]
        for session in affected_sessions
    }

    return [
        resource
        for resource in RESOURCES
        if resource["assigned_session"] in session_ids
    ]


def find_affected_tasks(affected_sessions):
    """Demo implementation of session -> task dependency."""

    session_ids = {
        session["session_id"]
        for session in affected_sessions
    }

    return [
        task
        for task in all_tasks()
        if task["related_item"] in session_ids
    ]


def analyze_demo_impact(old_venue, new_venue):
    """
    Temporary local demo dependency engine.

    IMPORTANT:
    In the final integrated version, this function should call
    Aravind's backend/dependency engine instead of calculating
    dependencies here.
    """

    affected_sessions = find_affected_sessions(old_venue)

    affected_volunteers = find_affected_volunteers(
        affected_sessions
    )

    affected_resources = find_affected_resources(
        affected_sessions
    )

    affected_tasks = find_affected_tasks(
        affected_sessions
    )

    return {
        "old_venue": old_venue,
        "new_venue": new_venue,
        "sessions": affected_sessions,
        "volunteers": affected_volunteers,
        "resources": affected_resources,
        "tasks": affected_tasks,
    }


def generate_follow_up_tasks(impact):
    """
    Create frontend demo tasks from the detected impact.

    In the integrated version, Aravind's backend should create
    the official tasks and synchronize them to Notion.
    """

    new_tasks = []

    for session in impact["sessions"]:
        session_id = session["session_id"]
        session_name = session["session_name"]

        new_tasks.append(
            {
                "task_id": f"IMPACT-{session_id}-VENUE",
                "task": f"Update venue for {session_name}",
                "owner": "Operations Team",
                "deadline": "Before session",
                "status": "Pending",
                "priority": "High",
                "related_item": session_id,
            }
        )

        new_tasks.append(
            {
                "task_id": f"IMPACT-{session_id}-COMMS",
                "task": f"Notify participants about {session_name} venue",
                "owner": "Marketing Team",
                "deadline": "ASAP",
                "status": "Pending",
                "priority": "High",
                "related_item": session_id,
            }
        )

    for volunteer in impact["volunteers"]:
        new_tasks.append(
            {
                "task_id": f"IMPACT-{volunteer['volunteer_id']}",
                "task": f"Confirm reassignment for {volunteer['name']}",
                "owner": "Volunteer Team",
                "deadline": "Before session",
                "status": "Pending",
                "priority": "Medium",
                "related_item": volunteer["volunteer_id"],
            }
        )

    for resource in impact["resources"]:
        new_tasks.append(
            {
                "task_id": f"IMPACT-{resource['resource_id']}",
                "task": f"Move {resource['resource']} to {impact['new_venue']}",
                "owner": "Technical Team",
                "deadline": "Before session",
                "status": "Pending",
                "priority": "High",
                "related_item": resource["resource_id"],
            }
        )

    return new_tasks


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎯 KBC Command Center")

role = st.sidebar.selectbox(
    "Operational Role",
    [
        "Leadership",
        "Operations",
        "Technical",
        "Marketing",
        "Registration",
        "Volunteers",
    ],
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Sessions",
        "Venues",
        "Volunteers",
        "Resources",
        "Tasks",
        "Impact Analysis",
    ],
)

st.sidebar.divider()

st.sidebar.caption("TechFest 2026")
st.sidebar.caption("Event Operations Control")
st.sidebar.caption("KBC-NOTION-03")


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    event = EVENTS[0]
    tasks = all_tasks()

    completed = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    pending = sum(
        1 for task in tasks
        if task["status"] == "Pending"
    )

    blocked = sum(
        1 for task in tasks
        if task["status"] == "Blocked"
    )

    at_risk = sum(
        1 for task in tasks
        if task["priority"] == "High"
        and task["status"] == "Pending"
    )

    st.title("🎯 KBC — Event Command Center")

    st.caption(
        f"{event['event_name']} • "
        f"{event['date']} • "
        f"Role: {role}"
    )

    st.divider()

    # -------------------------
    # STATUS
    # -------------------------

    st.subheader("Operational Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Completed",
            completed,
        )

    with col2:
        st.metric(
            "Pending",
            pending,
        )

    with col3:
        st.metric(
            "Blocked",
            blocked,
        )

    with col4:
        st.metric(
            "At Risk",
            at_risk,
        )

    st.divider()

    # -------------------------
    # EVENT COUNTS
    # -------------------------

    st.subheader("Event Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Sessions",
            len(SESSIONS),
        )

    with col2:
        st.metric(
            "Venues",
            len(VENUES),
        )

    with col3:
        st.metric(
            "Volunteers",
            len(VOLUNTEERS),
        )

    with col4:
        st.metric(
            "Resources",
            len(RESOURCES),
        )

    st.divider()

    # -------------------------
    # PRIORITY TASKS
    # -------------------------

    st.subheader("High-Priority Operations")

    high_priority = [
        task
        for task in tasks
        if task["priority"] == "High"
        and task["status"] != "Completed"
    ]

    if high_priority:

        task_df = pd.DataFrame(high_priority)

        st.dataframe(
            task_df[
                [
                    "task_id",
                    "task",
                    "owner",
                    "deadline",
                    "status",
                    "priority",
                    "related_item",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.success("No high-priority pending operations.")


# ============================================================
# SESSIONS
# ============================================================

elif page == "Sessions":

    st.title("📅 Sessions")

    st.caption(
        "All scheduled event sessions and their operational dependencies."
    )

    sessions_df = pd.DataFrame(SESSIONS)

    st.dataframe(
        sessions_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Session Details")

    selected_session_name = st.selectbox(
        "Select a session",
        [
            session["session_name"]
            for session in SESSIONS
        ],
    )

    selected_session = next(
        session
        for session in SESSIONS
        if session["session_name"] == selected_session_name
    )

    st.write(
        f"**Session ID:** {selected_session['session_id']}"
    )

    st.write(
        f"**Speaker:** {selected_session['speaker']}"
    )

    st.write(
        f"**Venue:** {selected_session['venue']}"
    )

    st.write(
        f"**Time:** "
        f"{selected_session['start_time']} – "
        f"{selected_session['end_time']}"
    )

    st.write(
        f"**Status:** {selected_session['status']}"
    )


# ============================================================
# VENUES
# ============================================================

elif page == "Venues":

    st.title("🏢 Venues")

    st.caption(
        "Event locations and their operational capacity."
    )

    venues_df = pd.DataFrame(VENUES)

    st.dataframe(
        venues_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Venue Utilization")

    for venue in VENUES:

        sessions_here = [
            session
            for session in SESSIONS
            if session["venue"] == venue["venue_name"]
        ]

        with st.expander(
            f"{venue['venue_name']} — "
            f"{len(sessions_here)} session(s)"
        ):

            st.write(
                f"Capacity: **{venue['capacity']}**"
            )

            st.write(
                f"Status: **{venue['status']}**"
            )

            if sessions_here:

                for session in sessions_here:
                    st.write(
                        f"• {session['session_name']} "
                        f"({session['start_time']}–"
                        f"{session['end_time']})"
                    )

            else:
                st.write("No sessions assigned.")


# ============================================================
# VOLUNTEERS
# ============================================================

elif page == "Volunteers":

    st.title("👥 Volunteers")

    st.caption(
        "Volunteer assignments and operational availability."
    )

    volunteers_df = pd.DataFrame(VOLUNTEERS)

    st.dataframe(
        volunteers_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Volunteer Workload")

    volunteer_lookup_data = volunteer_lookup()
    session_lookup_data = session_lookup()

    workload = []

    for volunteer in VOLUNTEERS:

        assigned_sessions = []

        for session_id, volunteer_ids in SESSION_VOLUNTEERS.items():

            if volunteer["volunteer_id"] in volunteer_ids:

                session = session_lookup_data.get(session_id)

                if session:
                    assigned_sessions.append(
                        session["session_name"]
                    )

        workload.append(
            {
                "Volunteer": volunteer["name"],
                "Role": volunteer["role"],
                "Sessions": len(assigned_sessions),
                "Assigned Sessions": ", ".join(
                    assigned_sessions
                ),
            }
        )

    workload_df = pd.DataFrame(workload)

    st.dataframe(
        workload_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# RESOURCES
# ============================================================

elif page == "Resources":

    st.title("🧰 Resources")

    st.caption(
        "Equipment and resources assigned to sessions."
    )

    resources_df = pd.DataFrame(RESOURCES)

    display_resources = resources_df.copy()

    display_resources["Session Name"] = (
        display_resources["assigned_session"]
        .map(
            {
                session["session_id"]: session["session_name"]
                for session in SESSIONS
            }
        )
    )

    st.dataframe(
        display_resources[
            [
                "resource_id",
                "resource",
                "type",
                "assigned_session",
                "Session Name",
                "status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TASKS
# ============================================================

elif page == "Tasks":

    st.title("✅ Task & Escalation Center")

    st.caption(
        f"Showing tasks relevant to the {role} role."
    )

    tasks = all_tasks()

    # Role -> owner filtering

    role_owner_map = {
        "Leadership": None,
        "Operations": "Operations Team",
        "Technical": "Technical Team",
        "Marketing": "Marketing Team",
        "Registration": "Registration Team",
        "Volunteers": "Volunteer Team",
    }

    owner_filter = role_owner_map[role]

    if owner_filter is None:
        visible_tasks = tasks
    else:
        visible_tasks = [
            task
            for task in tasks
            if task["owner"] == owner_filter
        ]

    if visible_tasks:

        task_df = pd.DataFrame(visible_tasks)

        st.dataframe(
            task_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            f"No tasks currently assigned to {role}."
        )

    st.divider()

    st.subheader("Task Summary")

    visible_completed = sum(
        1 for task in visible_tasks
        if task["status"] == "Completed"
    )

    visible_pending = sum(
        1 for task in visible_tasks
        if task["status"] == "Pending"
    )

    visible_blocked = sum(
        1 for task in visible_tasks
        if task["status"] == "Blocked"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Completed",
            visible_completed,
        )

    with c2:
        st.metric(
            "Pending",
            visible_pending,
        )

    with c3:
        st.metric(
            "Blocked",
            visible_blocked,
        )


# ============================================================
# IMPACT ANALYSIS
# ============================================================

elif page == "Impact Analysis":

    st.title("⚡ Venue Change Impact Analysis")

    st.caption(
        "Organizer changes a venue → dependency engine identifies downstream impact."
    )

    st.divider()

    # -------------------------
    # VENUE CHANGE INPUT
    # -------------------------

    st.subheader("1. Change Venue")

    venue_names = [
        venue["venue_name"]
        for venue in VENUES
    ]

    old_venue = st.selectbox(
        "Old Venue",
        venue_names,
        index=0,
    )

    available_new_venues = [
        venue
        for venue in venue_names
        if venue != old_venue
    ]

    new_venue = st.selectbox(
        "New Venue",
        available_new_venues,
    )

    st.write(
        f"**Change:** {old_venue} → {new_venue}"
    )

    analyze_button = st.button(
        "🔍 ANALYZE IMPACT",
        type="primary",
        use_container_width=True,
    )

    # -------------------------
    # RUN ANALYSIS
    # -------------------------

    if analyze_button:

        impact = analyze_demo_impact(
            old_venue,
            new_venue,
        )

        st.session_state.last_impact = impact

        generated = generate_follow_up_tasks(
            impact
        )

        # Prevent duplicate task generation
        existing_ids = {
            task["task_id"]
            for task in st.session_state.generated_tasks
        }

        for task in generated:

            if task["task_id"] not in existing_ids:

                st.session_state.generated_tasks.append(
                    task
                )

        st.success(
            "Impact analysis completed successfully."
        )

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------

    impact = st.session_state.last_impact

    if impact:

        st.divider()

        st.subheader("🚨 IMPACT DETECTED")

        old = impact["old_venue"]
        new = impact["new_venue"]

        st.warning(
            f"Venue change detected: **{old} → {new}**"
        )

        # ----------------------------------
        # SUMMARY COUNTS
        # ----------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Affected Sessions",
                len(impact["sessions"]),
            )

        with c2:
            st.metric(
                "Affected Volunteers",
                len(impact["volunteers"]),
            )

        with c3:
            st.metric(
                "Affected Resources",
                len(impact["resources"]),
            )

        with c4:
            st.metric(
                "Affected Tasks",
                len(impact["tasks"]),
            )

        st.divider()

        # ----------------------------------
        # AFFECTED SESSIONS
        # ----------------------------------

        st.subheader("📅 Affected Sessions")

        if impact["sessions"]:

            session_df = pd.DataFrame(
                impact["sessions"]
            )

            st.dataframe(
                session_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.success(
                "No sessions are affected."
            )

        # ----------------------------------
        # AFFECTED VOLUNTEERS
        # ----------------------------------

        st.subheader("👥 Affected Volunteers")

        if impact["volunteers"]:

            volunteer_df = pd.DataFrame(
                impact["volunteers"]
            )

            st.dataframe(
                volunteer_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.success(
                "No volunteers are affected."
            )

        # ----------------------------------
        # AFFECTED RESOURCES
        # ----------------------------------

        st.subheader("🧰 Affected Resources")

        if impact["resources"]:

            resource_df = pd.DataFrame(
                impact["resources"]
            )

            st.dataframe(
                resource_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.success(
                "No resources are affected."
            )

        # ----------------------------------
        # AFFECTED TASKS
        # ----------------------------------

        st.subheader("✅ Affected Tasks")

        if impact["tasks"]:

            task_df = pd.DataFrame(
                impact["tasks"]
            )

            st.dataframe(
                task_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.success(
                "No existing tasks are affected."
            )

        # ----------------------------------
        # GENERATED FOLLOW-UP TASKS
        # ----------------------------------

        st.divider()

        st.subheader("⚡ Generated Follow-Up Actions")

        generated_for_impact = [
            task
            for task in st.session_state.generated_tasks
            if task["task_id"].startswith("IMPACT-")
        ]

        if generated_for_impact:

            generated_df = pd.DataFrame(
                generated_for_impact
            )

            st.dataframe(
                generated_df,
                use_container_width=True,
                hide_index=True,
            )

        # ----------------------------------
        # OPERATIONAL SUMMARY
        # ----------------------------------

        st.divider()

        st.subheader("📋 Operational Impact Summary")

        st.info(
            f"""
The organizer changed the venue from **{old}** to **{new}**.

The system detected:

• **{len(impact['sessions'])} session(s)** requiring venue updates  
• **{len(impact['volunteers'])} volunteer(s)** potentially requiring reassignment  
• **{len(impact['resources'])} resource(s)** requiring movement or reassignment  
• **{len(impact['tasks'])} existing task(s)** related to the affected sessions  

Follow-up actions have been generated for Operations, Technical,
Marketing, and Volunteer teams.

In the integrated version, the dependency engine and task records
will come from Aravind's backend and the operational records will
synchronize with Notion.
"""
        )

    else:

        st.info(
            "Select the old and new venue, then click "
            "**ANALYZE IMPACT** to simulate the organizer's change."
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "KBC-NOTION-03 • Intelligent Team Operations"
)

st.sidebar.caption(
    "Frontend prototype • Rudra"
)