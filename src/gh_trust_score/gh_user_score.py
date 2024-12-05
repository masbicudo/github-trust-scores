import requests

# Replace with your GitHub token
TOKEN = "your_personal_access_token"

# GitHub API base URL
BASE_URL = "https://api.github.com"

def get_user_trust_level(username):
    headers = {"Authorization": f"token {TOKEN}"}
    
    # Fetch user data
    user_url = f"{BASE_URL}/users/{username}"
    response = requests.get(user_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return None
    user_data = response.json()

    # Collect metrics
    followers = user_data.get("followers", 0)
    public_repos = user_data.get("public_repos", 0)
    created_at = user_data.get("created_at", "Unknown")  # Account age

    # Fetch repository data
    repos_url = f"{BASE_URL}/users/{username}/repos"
    repos_response = requests.get(repos_url, headers=headers)
    repos_data = repos_response.json() if repos_response.status_code == 200 else []

    # Aggregate metrics
    stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    forks = sum(repo.get("forks_count", 0) for repo in repos_data)

    # Example trust level calculation
    trust_score = followers * 2 + public_repos + stars + forks
    return {
        "username": username,
        "followers": followers,
        "public_repos": public_repos,
        "stars": stars,
        "forks": forks,
        "trust_score": trust_score,
        "account_created": created_at,
    }

if __name__ == "__main__":
    username = input("Enter GitHub username: ").strip()
    user_trust = get_user_trust_level(username)
    if user_trust:
        print(f"User Trust Level: {user_trust}")
