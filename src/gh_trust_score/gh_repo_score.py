import requests
from datetime import datetime

# Replace with your GitHub token
TOKEN = "your_personal_access_token"

# GitHub API base URL
BASE_URL = "https://api.github.com"

def calculate_repo_trust_score(owner, repo):
    headers = {"Authorization": f"token {TOKEN}"}
    
    # Fetch repository details
    repo_url = f"{BASE_URL}/repos/{owner}/{repo}"
    response = requests.get(repo_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return None
    repo_data = response.json()

    # Metrics
    stars = repo_data.get("stargazers_count", 0)
    forks = repo_data.get("forks_count", 0)
    watchers = repo_data.get("subscribers_count", 0)
    open_issues = repo_data.get("open_issues_count", 0)
    created_at = datetime.strptime(repo_data.get("created_at"), "%Y-%m-%dT%H:%M:%SZ")
    last_pushed_at = datetime.strptime(repo_data.get("pushed_at"), "%Y-%m-%dT%H:%M:%SZ")

    # Derived metrics
    repo_age_days = (datetime.utcnow() - created_at).days
    days_since_last_commit = (datetime.utcnow() - last_pushed_at).days

    # Example trust score calculation (adjust weights as needed)
    trust_score = (
        stars * 5 +
        forks * 3 +
        watchers * 2 -
        open_issues * 2 -
        days_since_last_commit * 0.1 +
        repo_age_days * 0.05
    )

    return {
        "repository": f"{owner}/{repo}",
        "stars": stars,
        "forks": forks,
        "watchers": watchers,
        "open_issues": open_issues,
        "repo_age_days": repo_age_days,
        "days_since_last_commit": days_since_last_commit,
        "trust_score": max(trust_score, 0),  # Ensure score is non-negative
    }

if __name__ == "__main__":
    owner = input("Enter repository owner: ").strip()
    repo = input("Enter repository name: ").strip()
    repo_trust = calculate_repo_trust_score(owner, repo)
    if repo_trust:
        print(f"Repository Trust Score: {repo_trust}")
