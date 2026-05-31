import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_databases() -> list[dict]:
    """Search for all databases in Notion"""
    try:
        res = requests.post(
            "https://api.notion.com/v1/search",
            headers=HEADERS,
            json={"filter": {"value": "database", "property": "object"}},
        )
        print("Search Response:")
        print(res.status_code)
        print(res.text)

        data = res.json()
        return data.get("results", [])
    except Exception as e:
        print(f"Notion search error: {e}")
        return []


def create_prep_database(company: str) -> str | None:
    """
    Create a new Notion database for the prep plan.
    Returns the database ID.
    """
    # First find a parent page to create the DB in
    try:
        res = requests.post(
            "https://api.notion.com/v1/search",
            headers=HEADERS,
            json={"filter": {"value": "page", "property": "object"}, "page_size": 1},
        )
        print("Search Response:")
        print(res.status_code)
        print(res.text)
    
        pages = res.json().get("results", [])
        if not pages:
            print("No Notion pages found to create DB in")
            return None

        parent_id = pages[0]["id"]

        db_payload = {
            "parent": {"type": "page_id", "page_id": parent_id},
            "title": [{"type": "text", "text": {"content": f"CareerCraft — {company} Prep Plan"}}],
            "properties": {
                "Task": {"title": {}},
                "Week": {"select": {"options": [
                    {"name": "Week 1", "color": "blue"},
                    {"name": "Week 2", "color": "green"},
                    {"name": "Week 3", "color": "yellow"},
                    {"name": "Week 4", "color": "red"},
                ]}},
                "Day": {"number": {}},
                "Status": {"select": {"options": [
                    {"name": "Todo", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Done", "color": "green"},
                ]}},
                "Priority": {"select": {"options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "gray"},
                ]}},
                "Company": {"rich_text": {}},
            },
        }

        res = requests.post(
            "https://api.notion.com/v1/databases",
            headers=HEADERS,
            json=db_payload,
        )
        print("Database Create Response:")
        print(res.status_code)
        print(res.text)

        data = res.json()
        return data.get("id")

    except Exception as e:
        print(f"Notion create DB error: {e}")
        return None


def add_tasks_to_notion(company: str, prep_plan: str) -> bool:
    """
    Parse the 30-day prep plan and add tasks to Notion database.
    Returns True if successful.
    """
    if not NOTION_TOKEN:
        print("NOTION_TOKEN not set")
        return False

    db_id = create_prep_database(company)
    if not db_id:
        return False

    # Parse prep plan into tasks
    tasks = parse_prep_plan(prep_plan, company)

    success_count = 0
    for task in tasks:
        try:
            payload = {
                "parent": {"database_id": db_id},
                "properties": {
                    "Task": {"title": [{"text": {"content": task["title"]}}]},
                    "Week": {"select": {"name": task["week"]}},
                    "Day": {"number": task["day"]},
                    "Status": {"select": {"name": "Todo"}},
                    "Priority": {"select": {"name": task["priority"]}},
                    "Company": {"rich_text": [{"text": {"content": company}}]},
                },
            }
            res = requests.post(
                "https://api.notion.com/v1/pages",
                headers=HEADERS,
                json=payload,
            )
            if res.status_code in [200, 201]:
                success_count += 1
            else:
                print("Task Create Error:")
                print(res.status_code)
                print(res.text)
        except Exception as e:
            print(f"Task add error: {e}")

    print(f"✅ Added {success_count}/{len(tasks)} tasks to Notion")
    return success_count > 0


def parse_prep_plan(prep_plan: str, company: str) -> list[dict]:
    """Parse the AI-generated prep plan into structured tasks"""
    tasks = []
    lines = prep_plan.split("\n")

    current_week = "Week 1"
    day_counter = 1
    week_map = {
        "week 1": "Week 1", "week 2": "Week 2",
        "week 3": "Week 3", "week 4": "Week 4",
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect week
        line_lower = line.lower()
        for key, val in week_map.items():
            if key in line_lower and ("##" in line or "**" in line):
                current_week = val
                break

        # Detect day
        if "day" in line_lower and any(str(i) in line for i in range(1, 31)):
            for i in range(1, 31):
                if f"day {i}" in line_lower or f"days {i}" in line_lower:
                    day_counter = i
                    break

        # Detect tasks (checkbox items)
        if line.startswith("- [ ]") or line.startswith("* [ ]"):
            task_text = line.replace("- [ ]", "").replace("* [ ]", "").strip()
            task_text = task_text.replace("**", "").replace("*", "").strip()
            if task_text and len(task_text) > 5:
                # Determine priority
                priority = "Medium"
                if any(kw in task_text.lower() for kw in ["critical", "must", "important", "required"]):
                    priority = "High"
                elif any(kw in task_text.lower() for kw in ["bonus", "optional", "nice"]):
                    priority = "Low"

                tasks.append({
                    "title": task_text[:100],  # Notion title limit
                    "week": current_week,
                    "day": day_counter,
                    "priority": priority,
                })

        # Also catch bullet tasks without checkboxes
        elif line.startswith("- ") and len(line) > 10 and not line.startswith("- **"):
            task_text = line[2:].strip()
            task_text = task_text.replace("**", "").strip()
            if task_text and len(task_text) > 10:
                tasks.append({
                    "title": task_text[:100],
                    "week": current_week,
                    "day": day_counter,
                    "priority": "Medium",
                })

    return tasks[:30]  # Max 30 tasks