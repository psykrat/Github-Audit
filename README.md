# GitHub Organization Audit

This Python script is designed to extract detailed data from a GitHub organization, including teams, members, and repositories. It uses GitHub's REST API for fetching data and stores the results into CSV files.

The script creates separate CSV files for each team's members and repositories, along with CSV files for all the teams and repositories in the organization. 

## Setup

To run this script, you need to have Python 3.6 or later installed on your machine. You also need the following Python packages, which can be installed via pip:

- requests
- python-dotenv
- tqdm

Install these packages using pip:

```
pip install requests python-dotenv tqdm
```

## Configuration

1. Create a `.env` file in the root of the project.
2. In the `.env` file, specify your GitHub personal access token and the GitHub organization name. For example:

```
GITHUB_PERSONAL_ACCESS_TOKEN=your_personal_access_token
GITHUB_ORG_NAME=your_organization_name
```

To generate a personal access token on GitHub, follow the guide on this [link](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Usage

You can run the script using Python from your command line:

```
python github_audit.py
```

This will start the data extraction process. Progress will be shown in the command line for each team and repository being processed.

## Output

The script generates the following CSV files:

- A `teams.csv` file, containing all the teams in the organization, including their id, name, slug, and description.
- A `repos.csv` file, containing all the repositories in the organization.
- Individual CSV files for each team's members, named `{team_slug}_members.csv`.
- Individual CSV files for each team's repositories, named `{team_slug}_repos.csv`.

All files are stored in a folder named `Github Audit`, with subfolders `team users` and `team repos` for the individual team's members and repositories, respectively.
