##################################################################
# uses GitHub API to collect monthly KPI stats
# * number of issues closed each month
# * number of contributors to the codebase
# * number of lines of code contributed by each contributor
##################################################################

import requests

APP_ROOT = "https://api.github.com/"
ORGS = APP_ROOT + "orgs/openactive"
MEMBERS = ORGS + "/members"
REPOS = ORGS + "/repos"
OWNER = "thill-odi"
LIMIT = 100 # max number of items per page



def page_through(endpoint_url, page_number=1):
    results = endpoint_url + "?per_page=" + str(LIMIT) + "&page=" + str(page_number)
    results_list = requests.get(results, auth=(uid,pwd)).json()
    if(len(results_list) == LIMIT):
        results_list.extend(page_through(endpoint_url, page_number + 1))
    return results_list


# get credentials

f = open("auth/tokens", "r").readlines()
uid = f[0].strip()
pwd = f[1].strip()

# get all members and repos

all_repos = page_through(REPOS)
all_members = page_through(MEMBERS)

member_contributions = {}
closed_issues_per_repo = {}
start_date = int("2021-11-01".replace("-", ""))
end_date = int("2021-11-25".replace("-", ""))

contributors = {} # key-value pairs will be username and integer of commits

while(all_repos):
    now_repo = all_repos.pop()
    repo_name = now_repo["name"]
    commits_url = APP_ROOT + "repos" + "/openactive/" + repo_name + "/commits"
    all_commits = requests.get(commits_url, auth=(uid,pwd)).json()
    while(all_commits):
        now_commit = all_commits.pop()
        commit_date = now_commit["commit"]["committer"]["date"]
        if(commit_date):
            commit_as_integer = int(str(commit_date)[:10].replace("-", ""))
            if(start_date <= commit_as_integer <= end_date):
                committer_id = now_commit["commit"]["author"]["email"]
                if(committer_id in contributors):
                    contributors[committer_id] += 1
                else:
                    contributors[committer_id] = 1


for contributor in contributors:
    print ("\n" + contributor + ": " + str(contributors[contributor]))
