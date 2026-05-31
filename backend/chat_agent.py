import os 
import json 
import anthropic 
from dotenv import load_dotenv
from coral_queries import (
    get_user_repos,
    get_user_languages,
    get_company_repos,
    get_github_commits,
    get_github_prs,
    get_largest_projects,
    get_most_starred_projects,
    get_projects_with_topics,
    get_public_projects,
    get_repo_health,
    get_resume_projects,
    get_recently_maintained_projects,
    get_go_portfolio,
    get_best_showcase_projects,
    get_recent_featured_projects,
    get_recent_projects,
    get_go_projects,
    get_javascript_projects,
    get_showcase_projects,
    get_language_distribution,
    get_latest_project,
    get_top_projects,
    get_notion_pages,
    get_cross_source_insight,
    get_linear_issues,
    get_pending_tasks,
    get_completed_tasks,
    get_high_priority_tasks,
    get_linear_projects,
    get_linear_users,
    get_linear_summary,
    get_linear_teams,
    get_careercraft_context,
    get_full_profile,
    get_project_portfolio,
    get_recent_active_projects,
    get_deployed_projects,
    get_portfolio_projects,
    get_recruiter_view,

    get_project_intelligence,
    get_repo_root,
    get_backend_structure,
    get_frontend_structure,
    get_package_json,
    get_requirements,
    get_readme,
    get_recent_commits,
    get_repo_prs,
    get_repo_issues,
    get_repo_contributors,
    get_repo_topics,
    get_repo_releases,
    get_repo_workflows,
    get_repo_action_runs,
    get_repo_branches,
    get_repo_deployments,
    get_repo_checks,
    get_repo_status,

    get_calendar_events,
    get_all_calendar_events,
    get_calendar_schedule,
    get_work_events,
    get_gym_events,
    get_college_events,
    get_content_events,
    get_upcoming_events,
    get_event_links,
    get_calendar_analytics,
    get_daily_planning_context,
    get_calendar_intelligence,
    get_interview_schedule_context,

    get_gmail_messages,
    get_gmail_message_details,
    get_gmail_intelligence,
    get_email_context,
    get_important_emails,
    get_inbox_emails,
    get_update_emails,
    get_security_emails,
    get_career_emails,
    get_recruiter_emails,

    get_full_career_context,
)

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "shivakumar2006")
MODEL = "claude-sonnet-4-6"

def detect_intent(message: str) -> str: 
    """Detect what user is asking about"""
    msg = message.lower()

    if any(w in msg for w in [
        "careercraft",
        "architecture",
        "review project",
        "project review",
        "engineering manager review",
        "analyze project"
    ]):
        return "project_intelligence"

    if any(w in msg for w in [
        "career manager",
        "overview",
        "full briefing",
        "analyze everything",
        "personal assistant",
        "careercraft"
    ]):
        return "full_context"

    if any(w in msg for w in [
        "careercraft",
        "architecture",
        "review project",
        "project review",
        "engineering manager review",
        "analyze project"
    ]):
        return "project_intelligence"

    if any(w in msg for w in [
        "calendar",
        "schedule",
        "event",
        "meeting",
        "gym",
        "college",
        "today schedule",
        "my day",
        "free time"
    ]):
        return "calendar"

    if any(w in msg for w in [
        "gmail",
        "email",
        "mail",
        "inbox",
        "message",
        "emails",
        "unread",
        "recruiter",
        "interview",
        "hiring",
        "job mail"
    ]):
        return "gmail"

    if any(w in msg for w in ["aaj", "today", "task", "karna", "todo", "plan"]): 
        return "today_task"

    if any(w in msg for w in ["best", "top", "rank", "resume", "highlight", "sabse"]):
        if any(w in msg for w in ["go", "golang", "project", "repo"]): 
            return "rank_go_projects"
        return "rank_projects"

    if any(w in msg for w in ["skill", "gap", "missing", "learn", "improve"]):
        return "skill_gap"
    
    if any(w in msg for w in ["github", "repo", "commit", "language", "tech"]): 
        return "github_summary"

    if any(w in msg for w in ["notion", "note", "page", "doc"]): 
        return "notion_summary"

    if any(w in msg for w in ["week", "hafte", "progress", "done", "complete"]): 
        return "weekly_summary"

    if any(w in msg for w in ["company", "zerodha", "razorpay", "visa", "intel"]): 
        return "company_intel"

    if any(w in msg for w in ["linear", "issue", "ticket"]):
        return "linear_tasks"

    if any(w in msg for w in ["recent", "latest", "new project"]):
        return "recent_projects"

    if any(w in msg for w in ["showcase", "strongest", "best project"]):
        return "best_projects"
    
    if any(w in msg for w in ["recruiter", "hire", "portfolio review"]):
        return "recruiter_review"

    if any(w in msg for w in ["deploy", "deployed", "live project"]):
        return "deployed_projects"

    if any(w in msg for w in ["portfolio", "project portfolio"]):
        return "portfolio_projects"

    return "general"

def fetch_for_intent(intent: str, message: str) -> str: 
    """Fetch relevant Coral data based on intent"""
    data = {}

    if intent == "full_context":
        data["github"] = get_project_intelligence("careercraft")

        data["linear"] = get_linear_summary()
        data["notion"] = get_notion_pages()

        data["calendar"] = get_calendar_intelligence()

        data["gmail"] = get_gmail_intelligence()

    if intent in ["today_task", "weekly_summary", "general"]:
        data["notion"] = get_notion_pages()
        data["repos"] = get_user_repos(GITHUB_USERNAME)
        data["pending_tasks"] = get_pending_tasks()
        data["high_priority"] = get_high_priority_tasks()
 
    if intent in ["rank_go_projects", "rank_projects", "github_summary"]:
        data["repos"] = get_user_repos(GITHUB_USERNAME)
        data["languages"] = get_user_languages(GITHUB_USERNAME)
 
    if intent == "skill_gap":
        data["repos"] = get_user_repos(GITHUB_USERNAME)
        data["languages"] = get_user_languages(GITHUB_USERNAME)
        data["notion"] = get_notion_pages()
 
    if intent == "notion_summary":
        data["notion"] = get_notion_pages()
        data["cross"] = get_cross_source_insight(GITHUB_USERNAME)

    if intent == "company_intel":
        companies = ["zerodha", "razorpay", "visa", "google", "amazon",
                     "microsoft", "flipkart", "swiggy", "zomato", "cred"]
        for company in companies:
            if company in message.lower():
                data["company_repos"] = get_company_repos(company + "tech")
                data["company_name"] = company
                break
        data["repos"] = get_user_repos(GITHUB_USERNAME)
        data["languages"] = get_user_languages(GITHUB_USERNAME)
 
    if intent == "general":
        data["repos"] = get_user_repos(GITHUB_USERNAME)
        data["languages"] = get_user_languages(GITHUB_USERNAME)
        data["notion"] = get_notion_pages()

    if intent == "best_projects":
        data["best_projects"] = get_best_showcase_projects()
        data["resume_projects"] = get_resume_projects()

    if intent == "recent_projects":
        data["recent_projects"] = get_recent_projects()

    if intent == "linear_tasks":
        data["pending_tasks"] = get_pending_tasks()
        data["completed_tasks"] = get_completed_tasks()
        data["high_priority"] = get_high_priority_tasks()
    
    if intent == "general":
        data["context"] = get_careercraft_context(GITHUB_USERNAME)

    if intent == "recruiter_review":
        data["recruiter_view"] = get_recruiter_view()

    if intent == "deployed_projects":
        data["deployed_projects"] = get_deployed_projects()

    if intent == "portfolio_projects":
        data["portfolio_projects"] = get_project_portfolio()
        data["recent_active"] = get_recent_active_projects()

    if intent == "project_intelligence":
        repo = "careercraft"

        data["project_root"] = get_repo_root(repo)
        data["backend_structure"] = get_backend_structure(repo)
        data["frontend_structure"] = get_frontend_structure(repo)

        data["package_json"] = get_package_json(repo)
        data["requirements"] = get_requirements(repo)

        data["readme"] = get_readme(repo)
        data["commits"] = get_recent_commits(repo)

        data["topics"] = get_repo_topics(repo)
        data["contributors"] = get_repo_contributors(repo)

        data["prs"] = get_repo_prs(repo)
        data["issues"] = get_repo_issues(repo)

        data["branches"] = get_repo_branches(repo)
        data["workflows"] = get_repo_workflows(repo)

        data["deployments"] = get_repo_deployments(repo)

    if intent == "calendar":
        data["calendar"] = get_calendar_intelligence()

    if intent == "calendar":
        data["calendar"] = get_calendar_intelligence()
        print("CALENDAR FETCHED:")
        print(data["calendar"])

    if intent == "general":
        data["calendar"] = get_calendar_intelligence()

    if intent == "gmail":
        data["gmail"] = get_gmail_messages()
        data["gmail_details"] = get_gmail_message_details()

        data["important_emails"] = get_important_emails()
        data["inbox_emails"] = get_inbox_emails()
        data["update_emails"] = get_update_emails()
        data["security_emails"] = get_security_emails()
        data["career_emails"] = get_career_emails()
        data["recruiter_emails"] = get_recruiter_emails()
 
    return data

SYSTEM_PROMPT = f"""You are CareerCraft AI — a personal career agent for developer {GITHUB_USERNAME}.
 
You have real-time access to their GitHub profile, Linear and Notion workspace via Coral SQL.
 
Your personality:
- Smart, direct, encouraging
- Reference actual repo names and data
- Give actionable advice, not generic tips
- Keep responses concise but specific
- Use emojis sparingly for clarity
 
When answering:
- Always reference actual data provided to you
- Rank/compare things with clear reasoning
- For tasks: be specific about what to do today
- For projects: explain WHY a project is good for a role
- For skill gaps: give a concrete 1-week action plan

When project architecture data is available:

- Analyze repository structure
- Analyze frontend dependencies
- Analyze backend dependencies
- Analyze commit history
- Analyze engineering maturity
- Analyze scalability
- Analyze maintainability

Never say "architecture information is unavailable"
if repository structure or dependency information is provided.

"""

def chat(message: str, history: list[dict]) -> str:
    """
    Process a chat message and return AI response.
    
    Args:
        message: User's message
        history: List of {role, content} dicts (conversation history)
    
    Returns:
        AI response string
    """
    # Detect intent
    intent = detect_intent(message)
 
    # Fetch relevant Coral data
    coral_data = fetch_for_intent(intent, message)
 
    # Build context from Coral data
    context_parts = []
 
    if "repos" in coral_data:
        repos = coral_data["repos"]
        go_repos = [r for r in repos if r.get("language") == "Go"]
        context_parts.append(f"GitHub Repos ({len(repos)} total):\n{json.dumps(repos[:15], indent=2)}")
        if go_repos:
            context_parts.append(f"Go Repos specifically:\n{json.dumps(go_repos, indent=2)}")
 
    if "languages" in coral_data:
        context_parts.append(f"Language Distribution:\n{json.dumps(coral_data['languages'], indent=2)}")
 
    if "notion" in coral_data and coral_data["notion"]:
        context_parts.append(f"Notion Pages:\n{json.dumps(coral_data['notion'][:10], indent=2)}")
 
    if "cross" in coral_data and coral_data["cross"]:
        context_parts.append(f"GitHub-Notion Cross Analysis:\n{json.dumps(coral_data['cross'][:10], indent=2)}")
 
    if "company_repos" in coral_data:
        context_parts.append(f"Company GitHub ({coral_data.get('company_name', 'target')}):\n{json.dumps(coral_data['company_repos'][:8], indent=2)}")

    if "best_projects" in coral_data:
        context_parts.append(
            f"Best Projects:\n{json.dumps(coral_data['best_projects'], indent=2)}"
        )

    if "recent_projects" in coral_data:
        context_parts.append(
            f"Recent Projects:\n{json.dumps(coral_data['recent_projects'], indent=2)}"
        )

    if "pending_tasks" in coral_data:
        context_parts.append(
            f"Pending Tasks:\n{json.dumps(coral_data['pending_tasks'], indent=2)}"
        )
    
    if "recruiter_view" in coral_data:
        context_parts.append(
            f"Recruiter View:\n{json.dumps(coral_data['recruiter_view'], indent=2)}"
        )

    if "deployed_projects" in coral_data:
        context_parts.append(
            f"Deployed Projects:\n{json.dumps(coral_data['deployed_projects'], indent=2)}"
        )

    if "portfolio_projects" in coral_data:
        context_parts.append(
            f"Portfolio Projects:\n{json.dumps(coral_data['portfolio_projects'], indent=2)}"
        )

    if "recent_active" in coral_data:
        context_parts.append(
            f"Recent Active Projects:\n{json.dumps(coral_data['recent_active'], indent=2)}"
        )

    if "project_root" in coral_data:
        context_parts.append(
            f"Repository Root:\n{json.dumps(coral_data['project_root'], indent=2)}"
        )

    if "backend_structure" in coral_data:
        context_parts.append(
            f"Backend Structure:\n{json.dumps(coral_data['backend_structure'], indent=2)}"
        )

    if "frontend_structure" in coral_data:
        context_parts.append(
            f"Frontend Structure:\n{json.dumps(coral_data['frontend_structure'], indent=2)}"
        )

    if "package_json" in coral_data:
        context_parts.append(
            f"Frontend Dependencies:\n{json.dumps(coral_data['package_json'], indent=2)}"
        )

    if "requirements" in coral_data:
        context_parts.append(
            f"Backend Dependencies:\n{json.dumps(coral_data['requirements'], indent=2)}"
        )

    if "commits" in coral_data:
        context_parts.append(
            f"Recent Commits:\n{json.dumps(coral_data['commits'], indent=2)}"
        )

    if "topics" in coral_data:
        context_parts.append(
            f"Topics:\n{json.dumps(coral_data['topics'], indent=2)}"
        )

    if "contributors" in coral_data:
        context_parts.append(
            f"Contributors:\n{json.dumps(coral_data['contributors'], indent=2)}"
        )

    if "prs" in coral_data:
        context_parts.append(
            f"Pull Requests:\n{json.dumps(coral_data['prs'], indent=2)}"
        )

    if "issues" in coral_data:
        context_parts.append(
            f"Issues:\n{json.dumps(coral_data['issues'], indent=2)}"
        )

    if "calendar" in coral_data:
        context_parts.append(
            f"Calendar Events:\n{json.dumps(coral_data['calendar'], indent=2)}"
        )

    if "gmail" in coral_data:
        context_parts.append(
            f"Gmail Messages:\n{coral_data['gmail']}"
        )

    if "gmail_details" in coral_data:
        context_parts.append(
            f"Gmail Details:\n{coral_data['gmail_details']}"
        )

    if "important_emails" in coral_data:
        context_parts.append(
            f"Important Emails:\n{coral_data['important_emails']}"
        )

    if "inbox_emails" in coral_data:
        context_parts.append(
            f"Inbox Emails:\n{coral_data['inbox_emails']}"
        )

    if "career_emails" in coral_data:
        context_parts.append(
            f"Career Emails:\n{coral_data['career_emails']}"
        )

    if "recruiter_emails" in coral_data:
        context_parts.append(
            f"Recruiter Emails:\n{coral_data['recruiter_emails']}"
        )

    print("Fetched Keys:", list(coral_data.keys()))
    
    coral_context = "\n\n---\n".join(context_parts) if context_parts else "No data fetched."
    
    # Build messages
    messages = []
 
    # Add history (last 6 messages for context)
    for h in history[-6:]:
        messages.append({"role": h["role"], "content": h["content"]})
 
    # Add current message with Coral data
    user_content = f"""User question: {message}
 
Real-time data fetched via Coral SQL:
{coral_context}
 
Answer based on the actual data above. Be specific and actionable."""
 
    messages.append({"role": "user", "content": user_content})
 
    # Call Claude
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
 
    return response.content[0].text
 
 
# ── QUICK TEST ───────────────────────────────────────────────
 
if __name__ == "__main__":
    print("CareerCraft Chat Agent — Test Mode")
    print("=" * 40)
 
    test_questions = [
        "Which is the best golang project for my resume?",
        "What i need to do today?",
        "Which skills are missing for ____ company?",
    ]
 
    history = []
    for q in test_questions:
        print(f"\nQ: {q}")
        response = chat(q, history)
        print(f"A: {response}")
        history.append({"role": "user", "content": q})
        history.append({"role": "assistant", "content": response})
        print("-" * 40)
 