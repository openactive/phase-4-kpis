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

while(all_repos):
    now_repo = all_repos.pop()
    repo_name = now_repo["name"]
    closed_issues_per_repo[repo_name]= []
    issues_url = APP_ROOT + "repos" + "/openactive/" + repo_name + "/issues?state=closed"
    all_repo_issues = requests.get(issues_url, auth=(uid,pwd)).json()
    while(all_repo_issues):
        now_issue = all_repo_issues.pop()
        closed_date = now_issue["closed_at"]
        if(closed_date):
            closed_as_integer = int(str(closed_date)[:10].replace("-", ""))
            if(start_date <= closed_as_integer <= end_date):
                closed_issues_per_repo[repo_name].append(now_issue["title"])


total_issues_closed = 0
for key in closed_issues_per_repo:
    print ("\n" + key + "\n------------------------")
    issues = closed_issues_per_repo[key]
    for issue in issues:
        print(issue)
    print("\n" + str(len(issues)) + " issues closed on " + key + "\n\n")
    total_issues_closed += len(issues)

print("TOTAL ISSUES CLOSED BETWEEN " + str(start_date) + " AND " + str(end_date) + ":" + str(total_issues_closed))
