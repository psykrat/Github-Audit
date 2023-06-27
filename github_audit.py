import csv
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm

# Load the .env file
load_dotenv()

# Get the access token and org name from the .env file
access_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
org_name = os.getenv("GITHUB_ORG_NAME")

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {access_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_paginated_results(url):
    results = []

    while url:
        response = requests.get(url, headers=headers)
        results.extend(response.json())
        if 'next' in response.links.keys():
            url = response.links['next']['url']
        else:
            url = None

    return results

# Create a directory to save the CSV files
os.makedirs('Github Audit/team users', exist_ok=True)
os.makedirs('Github Audit/team repos', exist_ok=True)

# Fetch all teams for the organization
teams = get_paginated_results(f'https://api.github.com/orgs/{org_name}/teams')

# Create a CSV file for the teams
with open('Github Audit/teams.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'slug', 'description'])

    # Iterate over the teams in the organization
    for team in tqdm(teams, desc="Processing teams"):
        # Write the team details to the CSV file
        writer.writerow([team['id'], team['name'], team['slug'], team['description']])

        # Fetch all members for the current team
        members = get_paginated_results(f'https://api.github.com/orgs/{org_name}/teams/{team["slug"]}/members')

        # Create a CSV file for the current team
        with open(f'Github Audit/team users/{team["slug"]}_members.csv', mode='w', newline='') as member_file:
            member_writer = csv.writer(member_file)
            member_writer.writerow(['login'])

            # Iterate over the members that the team has
            for member in tqdm(members, desc=f"Processing members for team {team['slug']}", leave=False):
                # Write the member's username to the CSV file
                member_writer.writerow([member['login']])

        # Fetch all repos for the current team
        team_repos = get_paginated_results(f'https://api.github.com/orgs/{org_name}/teams/{team["slug"]}/repos')

        # Create a CSV file for the current team
        with open(f'Github Audit/team repos/{team["slug"]}_repos.csv', mode='w', newline='') as repo_file:
            repo_writer = csv.writer(repo_file)

            # Write the header to the CSV file
            if team_repos:
                repo_writer.writerow(team_repos[0].keys())

            # Iterate over the repos that the team has access to
            for repo in tqdm(team_repos, desc=f"Processing repos for team {team['slug']}", leave=False):
                # Write the repo details to the CSV file
                repo_writer.writerow(repo.values())

# Fetch all repositories for the organization
repos = get_paginated_results(f'https://api.github.com/orgs/{org_name}/repos')

# Create a CSV file for the repositories
with open('Github Audit/repos.csv', mode='w', newline='') as file:
    # Prepare the CSV writer
    writer = csv.writer(file)

    # Write the header to the CSV file
    if repos:
        writer.writerow(repos[0].keys())

    # Iterate over the repositories in the organization
    for repo in tqdm(repos, desc="Processing repositories"):
        # Write the repository details to the CSV file
        writer.writerow(repo.values())
