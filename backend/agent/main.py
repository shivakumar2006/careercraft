import os
import json
from dotenv import load_dotenv
import anthropic
from coral_queries import (
    get_user_repos,
    get_user_languages,
    get_recent_activity,
    get_notion_pages,
    get_company_repos
)

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "shivakumar2006")

def analyze_profile() -> dict:
    """Fetch user profile data from all sources via Coral"""
    print("🔍 Fetching your GitHub repos...")
    repos = get_user_repos(GITHUB_USERNAME)
    
    print("💻 Analyzing your tech stack...")
    languages = get_user_languages(GITHUB_USERNAME)
    
    print("📋 Fetching your Notion pages...")
    notion = get_notion_pages()

    return {
        "repos": repos,
        "languages": languages,
        "notion": notion,
        "github_username": GITHUB_USERNAME
    }

def analyze_jd_vs_profile(jd: str, profile: dict, company_org: str = None) -> str:
    """Use Claude to analyze JD against user profile"""
    
    company_intel = ""
    if company_org:
        print(f"🏢 Fetching {company_org} GitHub intelligence...")
        company_repos = get_company_repos(company_org)
        company_intel = f"\n\nCompany GitHub Intelligence:\n{json.dumps(company_repos, indent=2)}"

    prompt = f"""
You are CareerCraft — an AI career agent for developers.

Analyze this job description against the developer's profile and provide:

1. MATCH SCORE (0-100) — how well does the profile match
2. MATCHED SKILLS — what they already have
3. SKILL GAPS — what's missing
4. COMPANY INSIGHTS — based on their GitHub (if available)
5. TOP 3 PROJECTS TO HIGHLIGHT — from their repos
6. PREPARATION PLAN — 30 days, week by week

Job Description:
{jd}

Developer Profile:
GitHub Repos: {json.dumps(profile['repos'], indent=2)}
Tech Stack: {json.dumps(profile['languages'], indent=2)}
Notion Pages: {json.dumps(profile['notion'], indent=2)}
{company_intel}

Be specific, actionable, and encouraging. Format clearly with sections.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def generate_resume(jd: str, profile: dict, analysis: str) -> str:
    """Generate tailored HTML resume"""
    
    prompt = f"""
Generate a beautiful, modern HTML resume tailored for this job description.

Use this developer's actual data:
- GitHub Username: {profile['github_username']}
- Repos: {json.dumps(profile['repos'][:10], indent=2)}
- Languages: {json.dumps(profile['languages'], indent=2)}

Job Description: {jd}
Analysis: {analysis}

Requirements:
- Complete HTML file with embedded CSS
- Dark theme, modern design
- Highlight relevant projects
- Include skills section based on actual repos
- Professional formatting
- Ready to download and send

Return ONLY the complete HTML, nothing else.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def generate_cover_letter(jd: str, profile: dict, analysis: str) -> str:
    """Generate tailored cover letter"""
    
    prompt = f"""
Write a compelling cover letter for this job application.

Developer: {profile['github_username']}
Key projects: {[r['name'] for r in profile['repos'][:5]]}
Top languages: {[l['language'] for l in profile['languages'][:3]]}

Job Description: {jd}
Profile Analysis: {analysis}

Make it:
- Personal and genuine
- Highlight specific relevant projects
- Show enthusiasm for the company
- 3 paragraphs max
- Ready to send
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def generate_interview_questions(jd: str, analysis: str) -> str:
    """Generate likely interview questions"""
    
    prompt = f"""
Generate 15 likely interview questions for this role.

Job Description: {jd}
Candidate Analysis: {analysis}

Include:
- 5 technical questions specific to their stack
- 5 system design questions
- 3 behavioral questions
- 2 company-specific questions

For each question, provide a brief answer hint.
Format clearly and number each question.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def generate_dashboard(jd: str, analysis: str, cover_letter: str, 
                       interview_questions: str, profile: dict) -> str:
    
    # Analysis se sirf key points nikalo
    analysis_short = analysis[:2000]  # pura mat bhejo
    
    prompt = f"""
Create a complete single-file HTML dashboard for a job application.
Dark theme, accent color #6366f1, Inter font.

Data:
- Candidate: {profile['github_username']}
- Top repos: {[r['name'] for r in profile['repos'][:8]]}
- Languages: {[l['language'] for l in profile['languages'][:5]]}
- Analysis summary: {analysis_short}
- Cover letter: {cover_letter[:800]}
- Interview questions (first 5): {interview_questions[:1000]}

Include these sections:
1. Header — company name, match score, candidate name
2. Skill bars — matched vs missing (from analysis)
3. 30-day prep checklist — interactive checkboxes, 4 weeks
4. Top 3 interview questions with hint answers — accordion
5. Cover letter — formatted nicely with copy button

Requirements:
- All CSS and JS embedded in single HTML file
- Interactive checkboxes that save state
- Smooth animations
- Mobile responsive
- Professional dark design

Return ONLY complete valid HTML. No markdown, no explanation.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def save_files(resume: str, cover_letter: str, dashboard: str, company: str):
    """Save all generated files"""
    import os
    os.makedirs("output", exist_ok=True)
    
    with open(f"output/{company}_resume.html", "w") as f:
        f.write(resume)
    
    with open(f"output/{company}_cover_letter.txt", "w") as f:
        f.write(cover_letter)
    
    with open(f"output/{company}_dashboard.html", "w") as f:
        f.write(dashboard)
    
    print(f"\n✅ Files saved in output/ folder:")
    print(f"   📄 {company}_resume.html")
    print(f"   ✉️  {company}_cover_letter.txt")
    print(f"   🎯 {company}_dashboard.html")

def main():
    print("\n🚀 CareerCraft — Your AI Career Agent")
    print("=" * 50)
    
    # Get job description
    print("\nPaste the Job Description (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    jd = "\n".join(lines[:-1])
    
    # Get company info
    company = input("\nCompany name (for file naming): ").strip()
    company_org = input("Company GitHub org (optional, press Enter to skip): ").strip()
    
    print("\n" + "=" * 50)
    
    # Step 1 — Fetch profile
    print("\n📊 Step 1: Analyzing your profile via Coral...")
    profile = analyze_profile()
    print(f"✅ Found {len(profile['repos'])} repos, {len(profile['languages'])} languages")
    
    # Step 2 — Analyze
    print("\n🧠 Step 2: Analyzing JD vs your profile...")
    analysis = analyze_jd_vs_profile(jd, profile, company_org if company_org else None)
    print("✅ Analysis complete")
    print("\n" + analysis)
    
    # Step 3 — Generate resume
    print("\n📄 Step 3: Generating tailored resume...")
    resume = generate_resume(jd, profile, analysis)
    print("✅ Resume generated")
    
    # Step 4 — Cover letter
    print("\n✉️  Step 4: Writing cover letter...")
    cover_letter = generate_cover_letter(jd, profile, analysis)
    print("✅ Cover letter written")
    
    # Step 5 — Interview questions
    print("\n❓ Step 5: Generating interview questions...")
    interview_q = generate_interview_questions(jd, analysis)
    print("✅ Interview questions ready")
    
    # Step 6 — Dashboard
    print("\n🎯 Step 6: Building your career dashboard...")
    dashboard = generate_dashboard(jd, analysis, cover_letter, interview_q, profile)
    print("✅ Dashboard ready")
    
    # Step 7 — Save
    print("\n💾 Step 7: Saving all files...")
    save_files(resume, cover_letter, dashboard, company)
    
    print("\n🎉 CareerCraft complete!")
    print(f"Open output/{company}_dashboard.html in your browser")

if __name__ == "__main__":
    main()