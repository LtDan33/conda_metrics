from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from .models import Message, MessageSerializer
from django.core.serializers.json import DjangoJSONEncoder

import requests

import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import config
import datetime
import time
import operator
from github import Github
from pprint import pprint

import config

# Serve Vue Application
# index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

def traffic():

    traffic_date = {}

    g = Github(config.GITHUB_TOKEN)
    repo = g.get_repo("{}/{}".format('conda','conda'))
    clones = repo.get_clones_traffic(per="day")
    views = repo.get_views_traffic(per="day")

    best_day = max(*list((day.count, day.timestamp) for day in views["views"]), key=operator.itemgetter(0))

    traffic_date['clones_count'] = clones['count']
    traffic_date['clones_uniq'] = clones['uniques']
    traffic_date['best_day_date'] = best_day[1]
    traffic_date['best_day_views'] = best_day[0]

    return traffic_date


# Obatin issues
def get_issues(repo='conda', owner='conda',max_issues_hundreds=2):
    github_api = "https://api.github.com"
    
    gh_session = requests.Session()
    gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)

    issues = []
    next = True
    i = 1
    while i < max_issues_hundreds:
    # while next == True:
        url = github_api + '/repos/{}/{}/issues?page={}&per_page=100'.format(owner, repo, i)
        issue_pg = gh_session.get(url = url)
        issue_pg_list = [dict(item, **{'repo_name':'{}'.format(repo)}) for item in issue_pg.json()]    
        issue_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in issue_pg_list]
        issues = issues + issue_pg_list
        if 'Link' in issue_pg.headers:
            if 'rel="next"' not in issue_pg.headers['Link']:
                next = False
        i = i + 1

    # issues = issues.sort_values(by='comments', ascending=False)


    # issues['user'] = issues.pop('user.login')
    return issues

def issue_by_author(data):
    issue_by_author = data.groupby('user.login')[['number']].count()
    issue_by_author = issue_by_author.rename(columns = {'user.login': 'user'})
    issue_by_author = issue_by_author.sort_values(by='number', ascending=False)
    top_authors = issue_by_author.head(25)
    return top_authors

def get_git():
    issues = json_normalize(get_issues('conda', 'conda',2))

    # Creates a csv on local
    # issues.to_csv('issues.csv',index=False)
    data = issues[['number','title','state','comments','owner','user.login','html_url']]



    data['date'] =  pd.to_datetime(issues['created_at'])
    data['date'] =  pd.to_datetime(data['date'], utc=True)
    data['issue_date'] = data['date'].dt.date
    data['issue_week'] = data['date'].dt.week
    data['issue_hour'] = data['date'].dt.hour
    data['issue_month'] = data['date'].dt.month
    data['issue_year'] = data['date'].dt.year

    return data

# Throwing in data and mutating , not a great idea (Hack day all day)
def priority(data):
    # data.drop(['issue_date_dt'], axis=1, inplace=True)

    # Determine age of an issue 
    today = datetime.date.today() 
    dt = pd.to_datetime('today', format='%Y-%m-%d')
    data['days_old'] = ''
    for i in range(0,len(data['issue_date'])):
        x = pd.to_datetime(data['issue_date'][i], format='%Y-%m-%d')
        data['days_old'][i] = ((dt-x).days)

    data['priority_score'] = ''
    for i in range(0,len(data['comments'])):
        data['priority_score'][i] = ((data['comments'][i])*10) + data['days_old'][i]


    issue_by_author = data.sort_values(by='priority_score', ascending=False)

    return issue_by_author.head(25)

def index_view(request):

    start_time = time.time()
    git_data = get_git()
    # print("--- %s seconds ---" % (time.time() - start_time))

    # Get the top Authors
    top_authors = issue_by_author(git_data)
    top_authors_json = top_authors.reset_index().to_json(orient ='records')
    top_authors_json = json.loads(top_authors_json)


    priority_data = priority(git_data)

    # Needs to be in correct json format to show correctly in html  
    priority_json = priority_data.reset_index().to_json(orient ='records')
    priority_json = json.loads(priority_json)

    # parsing the DataFrame in json format.
    json_records = git_data.head(20).reset_index().to_json(orient ='records')
    data = json.loads(json_records)

    traffic_date = traffic()

    # Should be able to reference the dict by key in the template/html, but can't for some 
    # reason. Going 1x1 to get around

    context = {
        'all_issues': data,
        'priority': priority_json,
        'top_authors' : top_authors_json,
        'traffic_data' : json.dumps(traffic_date, cls=DjangoJSONEncoder),
        'clones_count':traffic_date['clones_count'],
        'clones_uniq':traffic_date['clones_uniq'],
        'best_day_date':traffic_date['best_day_date'],
        'best_day_views':traffic_date['best_day_views'],
    }

    return render(request, 'indexdist.html', context)