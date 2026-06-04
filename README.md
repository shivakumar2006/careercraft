# CareerCraft — Your AI-Powered Personal Career Agent

> **"Stop switching tabs. Your entire career OS, powered by Coral SQL."**

![Track](https://img.shields.io/badge/Track-T2%20Personal%20Agent-7c6ef7)
![Hackathon](https://img.shields.io/badge/Hackathon-Pirates%20of%20CoralBean-1ddf8a)
![Sources](https://img.shields.io/badge/Sources-7%20Connected-22d9f3)
![Stack](https://img.shields.io/badge/Stack-React%20%2B%20FastAPI%20%2B%20Coral-ff4d6a)

---

## The Problem

A developer's life is scattered across 7+ tools.

- GitHub for code
- Linear for tasks
- Notion for notes
- Gmail for opportunities
- Google Calendar for schedule
- Job boards for openings

Every morning you context-switch between all of them just to answer one question: **"What should I actually do today?"**

And when you find a job you want — you spend hours manually tailoring your resume, writing cover letters, and guessing what the interview will look like.

**CareerCraft fixes all of this. One agent. One query language. Everything connected.**

---

## What CareerCraft Does

CareerCraft is an AI-powered personal career agent that uses **Coral SQL** to query your real data across 7 sources and gives you intelligent, actionable answers — through a conversational chat interface or a full JD analyzer.

### 🤖 Ask Your Agent Anything

```
"What should I work on today?"
→ Fetches Linear tasks + Google Calendar events + Notion pages
→ Gives you a prioritized plan for the day

"Which is my best Go project for a Zerodha application?"
→ Queries 50+ GitHub data points — size, recency, architecture
→ Ranks your projects with specific reasons

"What emails did I miss today?"
→ Queries Gmail labels, snippets, dates via Coral
→ Surfaces only what matters

"Am I overbooked this week?"
→ Queries Google Calendar events
→ Tells you which days are heavy and what to reschedule
```

### 📋 JD Analyzer — Full Career Pack in 60 Seconds

Paste any job description. CareerCraft:

1. **Queries your GitHub** — 50+ SQL queries across repos, languages, architecture
2. **Analyzes your fit** — match score, skill gaps, company insights
3. **Generates tailored resume** — beautiful HTML, your actual projects
4. **Writes cover letter** — specific to the role, references real work
5. **Prepares interview questions** — 15 questions with answer strategies
6. **Builds interactive dashboard** — 30-day prep plan with checkboxes
7. **Posts tasks to Notion** — your prep plan, automatically organized

---

## The Coral Advantage

Every answer CareerCraft gives is backed by **real SQL queries** across live sources — not cached data, not mock responses.

### Cross-Source Joins — The Killer Feature

```sql
-- "What should I focus on today?"
SELECT
    l.title as task,
    l.priority_label,
    c.summary as meeting,
    c.start__date_time as meeting_time,
    n.url as relevant_note
FROM linear.issues l
LEFT JOIN google_calendar.events c
    ON c.start__date_time >= CURRENT_DATE
LEFT JOIN notion.search n
    ON n.url ILIKE '%' || l.title || '%'
WHERE l.completed_at IS NULL
ORDER BY l.priority_label ASC
LIMIT 10
```

```sql
-- "Rank my Go projects for this role"
SELECT
    name,
    language,
    size,
    pushed_at,
    stargazers_count
FROM github.user_repos
WHERE language = 'Go'
ORDER BY size DESC, pushed_at DESC
LIMIT 10
```

```sql
-- "What emails came in today?"
SELECT
    subject,
    snippet,
    date,
    label_ids
FROM gmail.messages
WHERE date >= CURRENT_DATE
ORDER BY date DESC
LIMIT 20
```

### Sources Connected

| Source | Tables | What It Unlocks |
|--------|--------|-----------------|
| **GitHub** | 50+ queries | Repos, languages, architecture, package.json, size, recency |
| **Linear** | issues, projects, teams, users | Tasks, priorities, deadlines, team structure |
| **Notion** | pages, search | Notes, docs, project context |
| **Google Calendar** | events, schedule | Today's meetings, week overview, scheduling density |
| **Gmail** | messages, snippets, labels, dates | Important emails, opportunities, follow-ups |

---

## Demo

### Chat Agent

```
You: "What should i work in today?"

CareerCraft: Based on your real data:

📋 Linear — 3 high priority tasks pending:
   • Fix auth bug in CareerCraft API (High)
   • Write README for hackathon submission (Urgent)
   • Deploy to Railway (High)

📅 Calendar — 2 meetings today:
   • 11:00 AM — Team standup (30 min)
   • 3:00 PM — Interview prep session (1 hr)

📝 Notion — Related notes found:
   • "CareerCraft deployment checklist"

Start with the auth bug — you have a clear window 9-11 AM.
```

```
You: "Which is the best Go project for my resume?"

CareerCraft: Querying your GitHub via Coral SQL...

Top 3 Go projects for your resume:

🥇 OpenMetaDataCommandLineTool (omctl)
   → Largest Go codebase (most recent push)
   → CLI tool — demonstrates real-world Go patterns
   → Frame as: "Built omctl — CLI for OpenMetadata with 8 commands,
     scanned 1,276 tables, bulk-tagged 545 PII columns"

🥈 resilientLab
   → API resilience patterns — Circuit Breaker, Rate Limiting
   → Strong system design signal for backend roles

🥉 auto-checkpoint
   → Kubernetes + Go — cloud-native experience
   → Rare skill for a fresher

Lead with omctl. It has the best story.
```

### JD Analyzer

```
1. Paste job description → Visa Software Engineer
2. CareerCraft queries your GitHub via Coral SQL
3. Returns: Match Score 78/100
4. Generates: resume.html, cover_letter.txt, dashboard.html
5. Posts 30-day prep plan to your Notion — automatically
6. Opens interactive dashboard with week-by-week checklist
```

---

## Architecture

```
careercraft/
├── backend/
│   ├── main.py              ← FastAPI + streaming endpoints
│   ├── analyzer.py          ← Claude API — analysis & generation
│   ├── coral_queries.py     ← 30+ Coral SQL queries
│   ├── chat_agent.py        ← Conversational agent with intent detection
│   ├── notion_integration.py← Auto-post 30-day plan to Notion
│   └── specs/
│       └── google_calendar.yaml ← Custom Coral source spec
│
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Home.jsx     ← Landing page
│       │   ├── Analyze.jsx  ← JD input + real-time terminal + file viewer
│       │   └── Chat.jsx     ← Conversational AI agent
│       └── store/
│           └── careerSlice.js ← Redux state
│
└── output/                  ← Generated resumes, dashboards, cover letters
```

**Stack:** React + Tailwind + Redux · FastAPI · Coral SQL · Claude AI · GitHub + Linear + Notion + Calendar + Gmail

---

## Quick Start

### Prerequisites

- [Coral CLI](https://withcoral.com/docs/getting-started/installation) installed
- Python 3.11+
- Node.js 18+

### Setup

```bash
# Clone
git clone https://github.com/shivakumar2006/careercraft
cd careercraft

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env

# Connect sources
coral source add --interactive github
coral source add --interactive linear
coral source add --interactive notion
coral source add --file specs/google_calendar.yaml

# Run backend
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

### Environment Variables

```env
ANTHROPIC_API_KEY=your_key
GITHUB_USERNAME=your_github_username
NOTION_TOKEN=your_notion_token
```

---

## Judging Criteria — How CareerCraft Scores

| Criteria | CareerCraft |
|----------|-------------|
| **Potential Impact** | Every developer job-hunts. Every developer loses time to scattered tools. This solves both. |
| **Creativity & Originality** | Career intelligence + multi-source agent — no one else built this angle |
| **Best Use of Coral** | 5 sources, 83 queries, cross-source JOINs, custom source spec |
| **Technical Implementation** | Streaming FastAPI, Redux state, real-time terminal UI, Notion write-back |
| **Aesthetics & UX** | Dark terminal UI, animated score ring, interactive prep checklist |
| **Learning & Growth** | First time using Coral, custom source spec, multi-source agent architecture |

---

## Built For

**Pirates of the CoralBean Hackathon** — Track 2: Personal Agent

> *"Build an agent that makes your personal workflow more productive. Connect the tools you use every day. Coral handles the rest."*

---

## Author

**Shiva** — [@shivakumar2006](https://github.com/shivakumar2006)
**Linkedin** - [Linkedin](https://www.linkedin.com/in/shiva-shiva-8a48002a7/)
**Email** - [Email](official.shivakumar06@gmail.com)

Hackathon builder · Go developer

*WeMakeDevs × Coral · May 2026*
