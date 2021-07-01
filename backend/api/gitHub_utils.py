import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import config
import datetime
import time

# import plotly
# import chart_studio.plotly as py
# import plotly.graph_objs as go
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import config

def get_git():
    issues = json_normalize(issues_of_repo('conda', 'conda'))
    issues.columns
    issues.to_csv('issues.csv',index=False)
    data = issues[['number','title','state','comments','owner','user.login']]
    data['date'] =  pd.to_datetime(issues['created_at'])
    data['date'] =  pd.to_datetime(data['date'], utc=True)
    data['issue_date'] = data['date'].dt.date
    data['issue_week'] = data['date'].dt.week
    data['issue_hour'] = data['date'].dt.hour
    data['issue_month'] = data['date'].dt.month
    data['issue_year'] = data['date'].dt.year
    return data.head()


# Obatin issues
def issues_of_repo(repo, owner):
    github_api = "https://api.github.com"
    
    gh_session = requests.Session()
    gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)

    issues = []
    next = True
    i = 1
    while next == True:
        url = github_api + '/repos/{}/{}/issues?page={}&per_page=100'.format(owner, repo, i)
        issue_pg = gh_session.get(url = url)
        issue_pg_list = [dict(item, **{'repo_name':'{}'.format(repo)}) for item in issue_pg.json()]    
        issue_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in issue_pg_list]
        issues = issues + issue_pg_list
        if 'Link' in issue_pg.headers:
            if 'rel="next"' not in issue_pg.headers['Link']:
                next = False
        i = i + 1
    return issues
