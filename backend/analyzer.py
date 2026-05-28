import os 
import json 
from dotenv import load_dotenv
import anthropic 
from coral_queries import (
    get_user_repos,
    get_user_languages,
    get_recent_activity,
    get_company_repos,
    get_github_prs,
    get_github_commits,
    get_notion_pages,
    get_cross_source_insight,
    get_full_profile,
)

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "shivakumar2006")
MODEL = "claude-sonnet-4-6"

# analyze profile 
def analyze_profile() -> dict:
    """Fetch developer profile from GitHub + Notion via Coral"""
    repos = get_user_repos(GITHUB_USERNAME)
    languages = get_user_languages(GITHUB_USERNAME)
    # activity = get_recent_activity(GITHUB_USERNAME)
    # prs = get_github_prs(GITHUB_USERNAME)
    # commits = get_github_commits(GITHUB_USERNAME)
    notion = get_notion_pages()

    # commits = []
    # if repos:
    #     commits = get_github_commits(GITHUB_USERNAME, repos[0]['name'])

    return {
        "repos": repos,
        "languages": languages,
        "notion": notion,
        "github_username": GITHUB_USERNAME,
        # "activity": activity,
        # "prs": prs,
        # "commits": commits,
    }

# analysis 
def analyze_jd(jd: str, profile: dict, company_org: str = "") -> str: 
    """Analyze jd vs developers profile using claude"""

    company_intel = ""
    if company_org: 
        repos = get_company_repos(company_org)
        if repos: 
            company_intel = f"\n\nCompany Github Intelligence ({company_org}):\n{json.dumps(repos[:10], indent=2)}"

    prompt = f"""You are CareerCraft — an AI career agent for developers.
 
Analyze this job description against the developer's real GitHub profile data.
 
Provide a detailed analysis with:
 
1. MATCH SCORE (0-100) — with breakdown table by category
2. MATCHED SKILLS — with evidence from actual repos
3. SKILL GAPS — critical, important, minor gaps
4. COMPANY INSIGHTS — culture, tech stack, what they look for
5. TOP 3 PROJECTS TO HIGHLIGHT — from their actual repos, how to frame each
6. 30-DAY PREP PLAN — week by week with daily checkbox tasks
 
Job Description:
{jd}
 
Developer Profile:
GitHub Username: {profile['github_username']}
Repos: {json.dumps(profile['repos'][:20], indent=2)}
Languages: {json.dumps(profile['languages'], indent=2)}
Notion Pages: {json.dumps(profile['notion'][:5], indent=2)}
{company_intel}
 
Be specific, reference actual repo names, and make the prep plan actionable with checkbox tasks."""

    response = client.messages.create(
        model = MODEL,
        max_tokens = 4096,
        messages = [{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# generators 
def generate_resume(jd: str, profile: dict, analysis: str) -> str: 
    """Generate tailored HTML resume"""
    prompt = f"""Generate a complete, beautiful, modern HTML resume tailored for this job.
 
Use the developer's ACTUAL data — do not make up fake projects or skills.
 
Developer: {profile['github_username']}
Real Repos: {json.dumps(profile['repos'][:12], indent=2)}
Languages: {json.dumps(profile['languages'], indent=2)}
JD Summary: {jd[:600]}
Analysis: {analysis[:800]}
 
Design requirements:
- Dark theme: background #0d1117, cards #161b22
- Accent colors: blue #58a6ff, green #3fb950, purple #bc8cff
- JetBrains Mono for code elements, Inter for body
- Sections: Header, Summary, Skills, Projects (top 3), Experience, Education, Achievements
- Match score badge in header
- Hover effects on cards
- Print-friendly @media print styles
- Mobile responsive
 
Return ONLY a complete valid HTML file. No markdown fences."""

    response = client.messages.create(
        model = MODEL,
        max_tokens = 8096,
        messages = [{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def generate_cover_letter(jd: str, profile: dict, analysis: str) -> str: 
    """Generate personalized cover letter"""
    prompt = f"""Write a compelling, genuine cover letter for this job application.
 
Developer: {profile['github_username']}
Top projects: {[r['name'] for r in profile['repos'][:6]]}
Top languages: {[l['language'] for l in profile['languages'][:4]]}
JD: {jd[:600]}
Analysis highlights: {analysis[:500]}
 
Requirements:
- 3 strong paragraphs
- Reference specific real projects by name
- Show genuine enthusiasm for the company
- Professional but not robotic
- End with clear call to action
 
Return plain text only, no markdown."""

    response = client.messages.create(
        model = MODEL,
        max_tokens = 2000,
        messages = [{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def generate_interview_questions(jd: str, analysis: str) -> str: 
    """Generate 15 likely interview questions with hints"""
    prompt = f"""Generate 15 likely interview questions for this role with answer hints.
 
JD: {jd[:600]}
Candidate Analysis: {analysis[:600]}
 
Include:
- 5 technical questions specific to their tech stack
- 4 system design questions relevant to the role
- 3 behavioral questions (use STAR format hints)
- 2 company-specific questions
- 1 "why us" question
 
For each question provide:
Q: [question]
Hint: [2-3 sentence answer strategy]
 
Number them 1-15. Be specific to this role."""
 
    response = client.messages.create(
        model = MODEL,
        max_tokens = 2000,
        messages = [{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def generate_dashboard(company: str, jd: str, analysis: str, cover_letter: str, interview_questions: str, profile: dict) -> str:
    # Prompt chhota karo
    prompt = f"""Create complete interactive HTML dashboard.

Company: {company}
Candidate: {profile['github_username']}
Repos: {[r['name'] for r in profile['repos'][:6]]}
Languages: {[l['language'] for l in profile['languages'][:4]]}
Analysis: {analysis[:1500]}
Cover letter: {cover_letter[:500]}
Questions: {interview_questions[:800]}

Sections: navbar, hero with score ring, skill bars, 4-week prep checklist with localStorage, interview accordion, cover letter with copy button.

Design: bg #0a0a0f, accent #7c6ef7, green #1ddf8a, Inter font.
Return ONLY complete HTML."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=8096,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    result = response.content[0].text
    if not result.startswith("<!DOCTYPE"):
        result = "<!DOCTYPE html>" + result
    return result

# save files ₹
def save_all_files(company: str, resume: str, cover_letter: str, interview_questions: str, dashboard: str) -> list[str]: 
    """Save all generated files to output directory"""
    import os 
    os.makedirs("../output", exist_ok=True)

    files = []

    def save(name, content):
        path = f"../output/{name}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(name)
        print(f"  ✅ Saved: {name}")
 
    save(f"{company}_resume.html", resume)
    save(f"{company}_cover_letter.txt", cover_letter)
    save(f"{company}_interview_questions.txt", interview_questions)
    save(f"{company}_dashboard.html", dashboard)
 
    return files
