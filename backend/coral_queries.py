import subprocess
import json


def run_coral(sql: str) -> list[dict]:
    """Run a Coral SQL query and return results as list of dicts"""
    result = subprocess.run(
        ["coral", "sql", "--format", "json", sql],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Coral error: {result.stderr}")
        return []
    try:
        return json.loads(result.stdout)
    except Exception as e:
        print(f"JSON parse error: {e}")
        return []


# Github 

def get_user_repos(username: str) -> list[dict]:
    return run_coral("""
        SELECT name, language, description, stargazers_count
        FROM github.user_repos
        LIMIT 60
    """)


def get_user_languages(username: str) -> list[dict]:
    return run_coral("""
        SELECT language, COUNT(*) as repo_count
        FROM github.user_repos
        WHERE language IS NOT NULL
        GROUP BY language
        ORDER BY repo_count DESC
        LIMIT 10
    """)


# def get_recent_activity(username: str) -> list[dict]:
#     # return run_coral(f"""
#     #     SELECT activity_type, actor__login
#     #     FROM github.activity
#     #     WHERE owner = '{username}'
#     #     LIMIT 20
#     # """)
#     return []


def get_company_repos(org: str) -> list[dict]:
    return run_coral(f"""
        SELECT name, language, description,
               stargazers_count, open_issues_count
        FROM github.org_repos
        WHERE org = '{org}'
        ORDER BY stargazers_count DESC
        LIMIT 15
    """)


def get_github_prs(username: str) -> list[dict]:
    return run_coral(f"""
        SELECT name, open_issues_count, language
        FROM github.user_repos
        WHERE open_issues_count > 0
        LIMIT 20
    """)


def get_github_commits(username: str, repo: str) -> list[dict]:
    return run_coral(f"""
        SELECT
            sha,
            commit_sha,
            html_url
        FROM github.repo_git_commits
        WHERE owner = '{username}'
        AND repo = '{repo}'
        LIMIT 10
    """)

def get_largest_projects():
    return run_coral("""
        SELECT
            name,
            language,
            size,
            pushed_at
        FROM github.user_repos
        ORDER BY size DESC
        LIMIT 10
    """)

def get_most_starred_projects():
    return run_coral("""
        SELECT
            name,
            language,
            stargazers_count,
            forks_count
        FROM github.user_repos
        ORDER BY stargazers_count DESC
        LIMIT 10
    """)

def get_projects_with_topics():
    return run_coral("""
        SELECT
            name,
            topics,
            language
        FROM github.user_repos
        WHERE topics IS NOT NULL
        LIMIT 20
    """)

def get_public_projects():
    return run_coral("""
        SELECT
            name,
            language,
            visibility,
            pushed_at
        FROM github.user_repos
        WHERE visibility = 'public'
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_repo_health():
    return run_coral("""
        SELECT
            name,
            open_issues_count,
            has_issues,
            has_projects,
            has_discussions
        FROM github.user_repos
        LIMIT 20
    """)

def get_resume_projects():
    return run_coral("""
        SELECT
            name,
            language,
            size,
            pushed_at,
            forks_count,
            stargazers_count
        FROM github.user_repos
        WHERE language IS NOT NULL
        ORDER BY size DESC
        LIMIT 15
    """)

def get_recently_maintained_projects():
    return run_coral("""
        SELECT
            name,
            language,
            pushed_at,
            updated_at
        FROM github.user_repos
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_go_portfolio():
    return run_coral("""
        SELECT
            name,
            size,
            pushed_at
        FROM github.user_repos
        WHERE language = 'Go'
        ORDER BY size DESC
        LIMIT 20
    """)

def get_best_showcase_projects():
    return run_coral("""
        SELECT
            name,
            language,
            size,
            pushed_at,
            stargazers_count
        FROM github.user_repos
        WHERE language IS NOT NULL
        ORDER BY size DESC
        LIMIT 10
    """)

def get_recent_featured_projects():
    return run_coral("""
        SELECT
            name,
            language,
            stargazers_count,
            forks_count,
            pushed_at
        FROM github.user_repos
        WHERE language IS NOT NULL
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_recent_projects():
    return run_coral("""
        SELECT
            name,
            language,
            pushed_at
        FROM github.user_repos
        ORDER BY pushed_at DESC
        LIMIT 15
    """)

def get_go_projects():
    return run_coral("""
        SELECT
            name,
            language,
            pushed_at
        FROM github.user_repos
        WHERE language = 'Go'
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_javascript_projects():
    return run_coral("""
        SELECT
            name,
            language,
            pushed_at
        FROM github.user_repos
        WHERE language IN ('JavaScript', 'Typescript')
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_showcase_projects():
    return run_coral("""
        SELECT
            name,
            language,
            pushed_at
        FROM github.user_repos
        WHERE
            name ILIKE '%finance%'
            OR name ILIKE '%resilient%'
            OR name ILIKE '%metadata%'
            OR name ILIKE '%career%'
        ORDER BY pushed_at DESC
    """)

def get_language_distribution():
    return run_coral("""
        SELECT
            language,
            COUNT(*) as repo_count
        FROM github.user_repos
        WHERE language IS NOT NULL
        GROUP BY language
        ORDER BY repo_count DESC
    """)

def get_latest_project():
    return run_coral("""
        SELECT
            name,
            language,
            pushed_at
        FROM github.user_repos
        ORDER BY pushed_at DESC
        LIMIT 1
    """)

def get_top_projects():
    return run_coral("""
        SELECT
            name,
            language,
            description,
            stargazers_count,
            pushed_at
        FROM github.user_repos
        WHERE language IS NOT NULL
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_project_portfolio():
    return run_coral("""
        SELECT
            name,
            language,
            description,
            size,
            topics,
            homepage,
            stargazers_count,
            forks_count,
            open_issues_count,
            pushed_at
        FROM github.user_repos
        ORDER BY size DESC
        LIMIT 50
    """)

def get_recent_active_projects():
    return run_coral("""
        SELECT
            name,
            language,
            description,
            pushed_at,
            updated_at,
            size
        FROM github.user_repos
        ORDER BY pushed_at DESC
        LIMIT 15
    """)

def get_deployed_projects():
    return run_coral("""
        SELECT
            name,
            homepage,
            language,
            description
        FROM github.user_repos
        WHERE homepage IS NOT NULL
        LIMIT 20
    """)

def get_portfolio_projects():
    return run_coral("""
        SELECT
            name,
            language,
            size,
            stargazers_count,
            forks_count,
            homepage,
            topics,
            pushed_at
        FROM github.user_repos
        WHERE size > 5000
        ORDER BY pushed_at DESC
        LIMIT 20
    """)

def get_recruiter_view():
    return run_coral("""
        SELECT
            name,
            language,
            size,
            homepage,
            stargazers_count,
            forks_count,
            description,
            pushed_at
        FROM github.user_repos
        ORDER BY pushed_at DESC
        LIMIT 30
    """)

def get_repo_root(repo: str):
    return run_coral(f"""
        SELECT
            name,
            path,
            type
        FROM github.contents
        WHERE owner = 'shivakumar2006'
        AND repo = '{repo}'
        AND path = ''
    """)

def get_backend_structure(repo: str):
    return run_coral(f"""
        SELECT
            name,
            path,
            type
        FROM github.contents
        WHERE owner = 'shivakumar2006'
        AND repo = '{repo}'
        AND path = 'backend'
    """)

def get_frontend_structure(repo: str):
    return run_coral(f"""
        SELECT
            name,
            path,
            type
        FROM github.contents
        WHERE owner = 'shivakumar2006'
        AND repo = '{repo}'
        AND path = 'frontend'
    """)

def get_package_json(repo: str):
    return run_coral(f"""
        SELECT content_text
        FROM github.contents
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        AND path='frontend/package.json'
    """)

def get_requirements(repo: str):
    return run_coral(f"""
        SELECT content_text
        FROM github.contents
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        AND path='backend/requirements.txt'
    """)

def get_readme(repo: str):
    return run_coral(f"""
        SELECT content_text
        FROM github.contents
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        AND path='README.md'
    """)

def get_recent_commits(repo: str):
    return run_coral(f"""
        SELECT
            sha,
            commit__message,
            commit__author__date
        FROM github.commits
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 15
    """)

def get_repo_prs(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.pulls
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 20
    """)

def get_repo_issues(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.issues
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 20
    """)

def get_repo_contributors(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_contributors
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
    """)

def get_repo_topics(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_topics
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
    """)

def get_repo_releases(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.releases
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 10
    """)

def get_repo_workflows(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.workflows
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
    """)

def get_repo_action_runs(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_action_runs
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 20
    """)

def get_repo_branches(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_branches
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
    """)

def get_repo_deployments(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_deployments
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
    """)

def get_repo_checks(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_check_runs
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 20
    """)

def get_repo_status(repo: str):
    return run_coral(f"""
        SELECT *
        FROM github.repo_commit_statuses
        WHERE owner='shivakumar2006'
        AND repo='{repo}'
        LIMIT 20
    """)




# Notion

def get_notion_pages() -> list[dict]:
    return run_coral("""
        SELECT id, url, created_time, last_edited_time
        FROM notion.search
        LIMIT 20
    """)


# Corss source

def get_cross_source_insight(username: str) -> list[dict]:
    """GitHub + Notion joined — Coral ka superpower"""
    return run_coral(f"""
        SELECT
            g.name as repo_name,
            g.language,
            g.stargazers_count,
            n.url as notion_page
        FROM github.user_repos g
        LEFT JOIN notion.search n
            ON n.url ILIKE '%' || g.name || '%'
        WHERE g.language IS NOT NULL
        ORDER BY g.stargazers_count DESC
        LIMIT 20
    """)

# LINEAR 

def get_linear_issues() -> list[dict]:
    return run_coral("""
        SELECT
            identifier,
            title,
            state_name,
            priority_label,
            assignee_name,
            created_at,
            updated_at
        FROM linear.issues
        ORDER BY created_at DESC
        LIMIT 50
    """)

def get_pending_tasks() -> list[dict]:
    return run_coral("""
        SELECT
            identifier,
            title,
            state_name,
            priority_label
        FROM linear.issues
        WHERE completed_at IS NULL
        ORDER BY created_at DESC
        LIMIT 50
    """)

def get_completed_tasks() -> list[dict]:
    return run_coral("""
        SELECT
            identifier,
            title,
            completed_at
        FROM linear.issues
        WHERE completed_at IS NOT NULL
        ORDER BY completed_at DESC
        LIMIT 50
    """)

def get_high_priority_tasks() -> list[dict]:
    return run_coral("""
        SELECT
            identifier,
            title,
            priority_label,
            state_name
        FROM linear.issues
        WHERE priority_label != 'No priority'
        LIMIT 50
    """)

def get_linear_projects() -> list[dict]:
    return run_coral("""
        SELECT
            name,
            state,
            progress,
            team_name
        FROM linear.projects
        LIMIT 20
    """)

def get_linear_teams() -> list[dict]:
    return run_coral("""
        SELECT
            key,
            name,
            description,
            private
        FROM linear.teams
        LIMIT 20
    """)

def get_linear_users() -> list[dict]:
    return run_coral("""
        SELECT
            name,
            display_name,
            email,
            active,
            admin
        FROM linear.users
        LIMIT 20
    """)

def get_linear_summary() -> dict:
    return {
        "issues": get_linear_issues(),
        "pending": get_pending_tasks(),
        "completed": get_completed_tasks(),
        "projects": get_linear_projects(),
        "teams": get_linear_teams(),
        "users": get_linear_users(),
    }

# google calendar 

def get_calendar_events():
    return run_coral("""
    SELECT *
    FROM calendar.events
    LIMIT 100
    """)

def get_all_calendar_events():
    return run_coral("""
    SELECT *
    FROM calendar.events
    LIMIT 100
    """)

def get_calendar_schedule():
    return run_coral("""
    SELECT
        summary,
        start,
        end,
        status
    FROM calendar.events
    LIMIT 100
    """)

def get_work_events():
    return run_coral("""
    SELECT *
    FROM calendar.events
    WHERE summary LIKE '%Work%'
    LIMIT 100
    """)

def get_gym_events():
    return run_coral("""
    SELECT *
    FROM calendar.events
    WHERE summary LIKE '%Gym%'
    LIMIT 100
    """)

def get_college_events():
    return run_coral("""
    SELECT *
    FROM calendar.events
    WHERE summary LIKE '%College%'
    LIMIT 100
    """)

def get_content_events():
    return run_coral("""
    SELECT *
    FROM calendar.events
    WHERE summary LIKE '%Content%'
    LIMIT 100
    """)

def get_upcoming_events():
    return run_coral("""
    SELECT
        summary,
        start,
        end
    FROM calendar.events
    LIMIT 50
    """)

def get_event_links():
    return run_coral("""
    SELECT
        summary,
        htmlLink
    FROM calendar.events
    LIMIT 100
    """)

def get_calendar_analytics():
    return run_coral("""
    SELECT
        summary,
        start,
        end,
        status
    FROM calendar.events
    LIMIT 100
    """)

def get_daily_planning_context():
    return run_coral("""
    SELECT *
    FROM calendar.events
    LIMIT 100
    """)

def get_interview_schedule_context():
    return run_coral("""
    SELECT
        summary,
        start,
        end
    FROM calendar.events
    LIMIT 100
    """)

def get_calendar_intelligence():
    return run_coral("""
    SELECT *
    FROM calendar.events
    LIMIT 200
    """)

# gmail 

def get_gmail_messages():
    return run_coral("""
    SELECT *
    FROM gmail.messages
    LIMIT 100
    """)

def get_gmail_message_details():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    LIMIT 100
    """)

def get_email_context():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    LIMIT 20
    """)

def get_important_emails():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    WHERE labelIds LIKE '%IMPORTANT%'
    LIMIT 50
    """)

def get_inbox_emails():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    WHERE labelIds LIKE '%INBOX%'
    LIMIT 50
    """)

def get_update_emails():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    WHERE labelIds LIKE '%CATEGORY_UPDATES%'
    LIMIT 50
    """)

def get_security_emails():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    WHERE snippet LIKE '%security%'
       OR snippet LIKE '%access%'
       OR snippet LIKE '%Google Account%'
    LIMIT 50
    """)

def get_career_emails():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    WHERE snippet LIKE '%job%'
       OR snippet LIKE '%career%'
       OR snippet LIKE '%interview%'
       OR snippet LIKE '%application%'
    LIMIT 50
    """)

def get_recruiter_emails():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    WHERE snippet LIKE '%recruiter%'
       OR snippet LIKE '%hiring%'
       OR snippet LIKE '%position%'
       OR snippet LIKE '%opportunity%'
    LIMIT 50
    """)

def get_gmail_intelligence():
    return run_coral("""
    SELECT *
    FROM gmail.message_details
    LIMIT 100
    """)



# full profile

def get_full_profile(username: str) -> dict:
    """Fetch complete developer profile from all sources"""
    repos = get_user_repos(username)
    languages = get_user_languages(username)
    notion = get_notion_pages()
    cross = get_cross_source_insight(username)

    linear = get_linear_summary()

    recent_projects = get_recent_projects()
    showcase_projects = get_showcase_projects()

    return {
        "repos": repos,
        "languages": languages,
        "notion_pages": notion,
        "cross_source": cross,

        "linear": linear,

        "recent_projects": recent_projects,
        "showcase_projects": showcase_projects,

        "github_username": username,
        "total_repos": len(repos),
        "top_language": languages[0]["language"] if languages else "Unknown",
    }


def get_careercraft_context(username: str):
    return {
        "repos": get_user_repos(username),
        "languages": get_language_distribution(),
        "recent_projects": get_recent_projects(),
        "showcase_projects": get_showcase_projects(),
        "best_projects": get_best_showcase_projects(),
        "go_projects": get_go_portfolio(),
        "linear_tasks": get_pending_tasks(),
    }

def get_project_intelligence(repo: str):
    return {
        "root": get_repo_root(repo),
        "backend": get_backend_structure(repo),
        "frontend": get_frontend_structure(repo),
        "dependencies": get_package_json(repo),
        "requirements": get_requirements(repo),
        "readme": get_readme(repo),
        "commits": get_recent_commits(repo),
    }

def get_full_career_context():
    data = {}

    data["github"] = get_project_intelligence()
    data["linear"] = get_linear_intelligence()
    data["notion"] = get_notion_intelligence()
    data["calendar"] = get_calendar_intelligence()
    data["gmail"] = get_gmail_intelligence()

    return data