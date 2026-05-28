import os 
import json 
import anthropic 
from dotenv import load_dotenv
from coral_queries import (
    get_user_repos,
    get_user_languages,
    get_notion_pages,
    get_company_repos,
    get_cross_source_insight,
)

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "shivakumar2006")
MODEL = "claude-sonnet-4-6"

def detect_intent(message: str) -> str: 
    """Detect what user is asking about"""
    msg = message.lower()

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

    return "general"

def fetch_for_intent(intent: str, message: str) -> str: 
    """Fetch relevant Coral data based on intent"""
    data = {}

    if intent in ["today_task", "weekly_summary", "general"]:
        data["notion"] = get_notion_pages()
        data["repos"] = get_user_repos(GITHUB_USERNAME)
 
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
 
    return data

SYSTEM_PROMPT = f"""You are CareerCraft AI — a personal career agent for developer {GITHUB_USERNAME}.
 
You have real-time access to their GitHub profile and Notion workspace via Coral SQL.
 
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
- For skill gaps: give a concrete 1-week action plan"""

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
        "Which skills are missing for zerodha?",
    ]
 
    history = []
    for q in test_questions:
        print(f"\nQ: {q}")
        response = chat(q, history)
        print(f"A: {response}")
        history.append({"role": "user", "content": q})
        history.append({"role": "assistant", "content": response})
        print("-" * 40)
 