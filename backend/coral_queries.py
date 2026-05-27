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
        LIMIT 50
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


def get_recent_activity(username: str) -> list[dict]:
    return run_coral(f"""
        SELECT type, repo__name, created_at
        FROM github.activity
        WHERE actor__login = '{username}'
        LIMIT 20
    """)


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
        SELECT title, state, created_at, merged_at
        FROM github.repo_pull_requests
        WHERE owner = '{username}'
        LIMIT 20
    """)


def get_github_commits(username: str, repo: str) -> list[dict]:
    return run_coral(f"""
        SELECT sha, message, author__date
        FROM github.repo_git_commits
        WHERE owner = '{username}'
        AND repo = '{repo}'
        LIMIT 10
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


# full profile

def get_full_profile(username: str) -> dict:
    """Fetch complete developer profile from all sources"""
    repos = get_user_repos(username)
    languages = get_user_languages(username)
    notion = get_notion_pages()
    cross = get_cross_source_insight(username)

    return {
        "repos": repos,
        "languages": languages,
        "notion_pages": notion,
        "cross_source": cross,
        "github_username": username,
        "total_repos": len(repos),
        "top_language": languages[0]["language"] if languages else "Unknown",
    }