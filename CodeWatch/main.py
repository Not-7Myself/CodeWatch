from github import Github
from github import Auth
from datetime import date, datetime

import firebase_admin
from firebase_admin import db, credentials

import operator

cred = credentials.Certificate('CodeWatch\credentials.json')
firebase_admin.initialize_app(cred, {"databaseURL":"https://code-watch-default-rtdb.asia-southeast1.firebasedatabase.app/"})

auth = Auth.Token('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')
ref = db.reference('/')

g = Github(auth=auth)

def no_commit(user):
    total = 0
    for repo in g.get_user(user).get_repos():
            if user == repo.owner.login:
                total += repo.get_commits().totalCount
            #print(repo, repo.get_commits().totalCount)
    return total
ref.update({"No_commits_" + str("Not-7Myself"): str(no_commit("Not-7Myself"))})

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

ref.update({"lang"+str("Not-7Myself"): str(calc_language_percentage('Not-7Myself'))})

deadline = date.today()
mnth = datetime.now().month
month_Commit = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,}
mnth = [1,2,3,4,5,6,7,8,9,10,11,12]
target_year = 2023

strt_list = []
end_list = []

for i in range(len(mnth)):
    target_month = mnth[i]
    start_date = datetime(target_year, target_month, 1)
    strt_list.append(start_date)
for i in range(len(mnth)):
    target_month = mnth[i]
    end_date = datetime(target_year, target_month % 12 + 1, 1)
    end_list.append(end_date)
def date_commit(user):
    for repo in g.get_user(user).get_repos():
        for com in repo.get_commits():
            com_date = com.commit.author.date
            naive_Dt = com_date.replace(tzinfo=None)
            for j in range(len(mnth)):
                if strt_list[j] <= naive_Dt < end_list[j]:
                    month_Commit[str(j+1)]= 1
    return month_Commit
ref.update({"date_commits_" + str("Not-7Myself"): list(date_commit("Not-7Myself"))})

print(ref.get())
