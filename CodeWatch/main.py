from github import Github
from github import Auth
from datetime import date, datetime

import firebase_admin
from firebase_admin import db, credentials

import operator

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {"databaseURL":"https://code-watch-default-rtdb.asia-southeast1.firebasedatabase.app/"})

auth = Auth.Token('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')
ref = db.reference('/')

g = Github(auth=auth)

def no_commit(user):
    total = 0
    fake = 0
    for repo in g.get_user(user).get_repos():
            if user == repo.owner.login:
                total += repo.get_commits().totalCount
            #print(repo, repo.get_commits().totalCount)
    return total
ref.update({"No_commits_" + str("Not-7Myself"): str(no_commit("Not-7Myself"))})

print(ref.get())
def calc_language_percentage(user):
    repos = g.get_user(user).get_repos()
    lang_dict = {}
    for repo in repos:
        for lang, num in repo.get_languages().items():
            if lang not in lang_dict:
                lang_dict[lang] = num
            else:
                lang_dict[lang] += num
    total = sum(lang_dict.values()) * 0.01
    sorted_lang_dict = dict(sorted(lang_dict.items(),key=operator.itemgetter(1),reverse=True))
    percentages = {}
    for key, value in sorted_lang_dict.items():
        percentages[key] = f"{value / total:.2f}%"
    return percentages

ref.update({"lang": str(calc_language_percentage('aouxwoux'))})

deadline = date.today()
mnth = datetime.now().month
def date_commit(user):
    d = []
    da = []
    for repo in g.get_user(user).get_repos():
        for com in repo.get_commits():
            d.append(com.commit.author.date)
        for i in range(len(d)):
            for j in range(13):
                if d[i].month == j:
                    da.append(d[i])
        
ref.update({"date_commits_" + str("Not-7Myself"): list(date_commit("Not-7Myself"))})
'''
Date of commits: "Line Graph"
Languages Used: "Bar Graph based on overall language used"
No. of commits Made: "Stats for commit page"
'''
