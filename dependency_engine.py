import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])


# --------------------------------------------------
# Find a Notion data source by name
# --------------------------------------------------

def get_data_source_id(name):
    results = notion.search(query=name)

    for result in results["results"]:
        if result["object"] == "data_source":
            ds = notion.data_sources.retrieve(
                data_source_id=result["id"]
            )

            if ds["title"][0]["plain_text"] == name:
                return result["id"]

    raise Exception(f"Could not find data source: {name}")


# --------------------------------------------------
# Read all rows from a data source
# --------------------------------------------------

def get_rows(data_source_id):
    response = notion.data_sources.query(
        data_source_id=data_source_id
    )

    return response["results"]


# --------------------------------------------------
# Extract text from a Notion property
# --------------------------------------------------

def get_text(properties, name):
    prop = properties.get(name)

    if not prop:
        return ""

    if prop["type"] == "title":
        items = prop["title"]
        return items[0]["plain_text"] if items else ""

    if prop["type"] == "rich_text":
        items = prop["rich_text"]
        return items[0]["plain_text"] if items else ""

    if prop["type"] == "select":
        return prop["select"]["name"] if prop["select"] else ""

    return ""


# --------------------------------------------------
# VERIFIED DEPENDENCY MAP
# --------------------------------------------------

SESSION_VOLUNTEERS = {
    "S001": ["VOL001", "VOL002"],
    "S002": ["VOL003", "VOL004", "VOL005"],
    "S003": []
}


# --------------------------------------------------
# Create a task in Notion
# --------------------------------------------------

def create_task(task_name, related_session, priority, task_number):

    tasks_source = get_data_source_id("Tasks")

    notion.pages.create(
        parent={
            "data_source_id": tasks_source
        },
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": task_name
                        }
                    }
                ]
            },
            "Task ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"AUTO-{related_session}-{task_number}"
                        }
                    }
                ]
            },
            "Owner": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Event Operations"
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": "Pending"
                }
            },
            "Priority": {
                "select": {
                    "name": priority
                }
            },
            "Related Item": {
                "rich_text": [
                    {
                        "text": {
                            "content": related_session
                        }
                    }
                ]
            }
        }
    )

    print(f"Task created: {task_name}")


# --------------------------------------------------
# Main impact analysis function
# --------------------------------------------------

def analyze_venue_change(old_venue, new_venue):

    sessions_source = get_data_source_id("Sessions")
    resources_source = get_data_source_id("Resources")

    session_rows = get_rows(sessions_source)
    resource_rows = get_rows(resources_source)

    affected_sessions = []
    affected_resources = []
    affected_volunteers = []
    generated_tasks = []

    # Find sessions using the old venue
    for page in session_rows:

        props = page["properties"]

        session_id = get_text(props, "Session ID")
        session_name = get_text(props, "Name")
        venue = get_text(props, "Venue")

        if venue == old_venue:

            affected_sessions.append({
                "session_id": session_id,
                "session_name": session_name,
                "old_venue": old_venue,
                "new_venue": new_venue
            })

            # Find affected volunteers
            for volunteer_id in SESSION_VOLUNTEERS.get(
                session_id, []
            ):
                affected_volunteers.append(volunteer_id)

            # Find affected resources
            for resource_page in resource_rows:

                resource_props = resource_page["properties"]

                resource_id = get_text(
                    resource_props,
                    "Resource ID"
                )

                assigned_session = get_text(
                    resource_props,
                    "Assigned Session"
                )

                resource_name = get_text(
                    resource_props,
                    "Name"
                )

                if assigned_session == session_id:

                    affected_resources.append({
                        "resource_id": resource_id,
                        "resource_name": resource_name,
                        "session_id": session_id
                    })

            # Generate operational tasks
            generated_tasks.append({
                "task": f"Update venue for {session_name}",
                "related_session": session_id,
                "priority": "High"
            })

            generated_tasks.append({
                "task": f"Update volunteer deployment for {session_name}",
                "related_session": session_id,
                "priority": "High"
            })

            generated_tasks.append({
                "task": f"Check equipment relocation for {session_name}",
                "related_session": session_id,
                "priority": "Medium"
            })

    # Remove duplicate volunteer IDs
    affected_volunteers = list(
        dict.fromkeys(affected_volunteers)
    )

    # --------------------------------------------------
    # Create generated tasks in Notion
    # --------------------------------------------------

    for index, task in enumerate(generated_tasks, start=1):

        create_task(
            task["task"],
            task["related_session"],
            task["priority"],
            index
        )

    return {
        "venue_change": {
            "old_venue": old_venue,
            "new_venue": new_venue
        },

        "affected_sessions": affected_sessions,

        "affected_volunteers": affected_volunteers,

        "affected_resources": affected_resources,

        "generated_tasks": generated_tasks
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    result = analyze_venue_change(
        "Auditorium A",
        "Auditorium B"
    )

    print("\n===== VERIFIED IMPACT ANALYSIS =====\n")

    print(result)