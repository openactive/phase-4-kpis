import requests

APP_ROOT = "https://api.github.com/"
ORGS = APP_ROOT + "orgs/openactive"
MEMBERS = ORGS + "/members"
REPOS = ORGS + "/repos"
LIMIT = 100 # max number of items per page

# uses GitHub API to collect monthly KPI stats

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

# get all members, all repos

all_repos = page_through(REPOS)
all_members = page_through(MEMBERS)
