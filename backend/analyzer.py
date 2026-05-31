import os 
import json 
from dotenv import load_dotenv
import anthropic 
from coral_queries import (
    get_user_repos,
    get_user_languages,
    # get_recent_activity,
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
    prompt = f"""
You are an elite resume writer and senior technical recruiter.

Your task is to create a world-class ATS-optimized software engineer resume tailored specifically for the provided job description.

IMPORTANT RULES:

* Use ONLY information from the developer's actual GitHub profile data.
* Never invent companies, jobs, internships, achievements, certifications, or technologies.
* If information is missing, omit the section instead of hallucinating.
* Prioritize projects that best match the job description.
* Make the candidate look as strong as possible using real evidence.

Developer Profile:
Username: {profile['github_username']}

GitHub Repositories:
{json.dumps(profile['repos'][:20], indent=2)}

Languages:
{json.dumps(profile['languages'], indent=2)}

Job Description:
{jd}

Career Analysis:
{analysis}

Generate a COMPLETE professional HTML resume.

Required Sections:

1. HERO HEADER

   - Full Name
   - Professional Title
   - GitHub
   - LinkedIn (placeholder if unavailable)
   - Email (placeholder if unavailable)
   - Match Score Badge

2. PROFESSIONAL SUMMARY

   - 4-6 lines
   - Tailored specifically to the role
   - Mention strongest technologies
   - Mention strongest project domains

3. TECHNICAL SKILLS
   Categories:

   - Languages
   - Frontend
   - Backend
   - Databases
   - Cloud & DevOps
   - Tools & Platforms

4. FEATURED PROJECTS

   - Select the BEST 3 projects
   - Explain why each project is relevant
   - Include:

     - Project Name
     - Description
     - Technologies
     - Business Impact
     - Key Features
     - Challenges Solved

5. ADDITIONAL PROJECTS

   - Display remaining relevant projects

6. EXPERIENCE

   - If no professional experience exists:
     "Independent Software Developer"
   - Showcase project experience professionally

7. EDUCATION

8. ACHIEVEMENTS

   - GitHub statistics
   - Open source contributions
   - Project count
   - Language expertise

9. WHY THIS CANDIDATE FITS THIS ROLE

   - 3-5 bullet points

10. ATS KEYWORDS

- Naturally incorporate keywords from JD

Design Requirements:

- Premium modern SaaS style
- Dark theme
- Background: #0d1117
- Cards: #161b22
- Accent: #7c6ef7
- Secondary Accent: #58a6ff
- Success: #1ddf8a

UI Requirements:

- Beautiful hero section
- Glassmorphism cards
- Progress bars for skills
- Project cards
- ATS score badge
- Responsive design
- Mobile friendly
- Print friendly
- Professional typography
- Clean spacing

Technical Requirements:

- Return a COMPLETE standalone HTML document
- Include all CSS inside <style>
- No external dependencies
- No markdown
- No code fences
- Must be immediately viewable in browser

Output ONLY valid HTML.
"""


    response = client.messages.create(
        model = MODEL,
        max_tokens = 12096,
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
        max_tokens=18000,
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
