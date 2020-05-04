import pandas as pd
import numpy as np
import plotly.graph_objects as go

def percentages(factor, df):
    p_list = factor.tolist()
    new_list = []
    for num in p_list:
        new_list.append(('{:.2%}'.format((num / len(df)))))
    return new_list

def create_updrs_data(df, options):
    data = [go.Bar()]
    for option in options:
        x = df.groupby([option, 'status_decode'])['status'].count().reset_index(name="count")
        data.append(go.Bar(name='PD',
                           x=x[x.status_decode=='PD'][option],
                           y=x[x.status_decode=='PD']['count'],
                           marker=dict(color="orange")))
        data.append(go.Bar(name='RBD',
                           x=x[x.status_decode=='RBD'][option],
                           y=x[x.status_decode=='RBD']['count'],
                           marker=dict(color="purple")))
    return data
                               
def create_updrs_menu(options):
    menus = [{'label': '',
              'method': 'update',
              'args': [{'visible': [True]+([False]*54)}, 
              {'title': 'UPDRS Scale Items by Score'}]}]
    for opt in options:
        menu ={'label': opt,
               'method': 'update',
               'args': [{'visible': []}, 
               {'title': opt +' Score Count'}]}
        
        x = list(np.repeat([opt == option for option in options], 2))
        menu['args'][0]['visible'] = [False] + x
        menus.append(menu)
    return menus

def create_speech_mean_data(df,options):
    data = [go.Bar()]
    for feature in options:
        x = df.groupby(['status_decode']).mean()[feature]
        colors=['green','orange','purple']
        data.append(go.Bar( name='Mean',x=x,
                           y=x.index,
                           orientation='h',
                           marker=dict(color=colors)))
    return data


def create_speech_mean_menu(options):
    menus = [{'label': '',
              'method': 'update',
              'args': [{'visible': [True] + ([False] * 24)},
                       {'title': 'Speech Examination Scores'}]}]
    for opt in options:
        menu = {'label': opt,
                'method': 'update',
                'args': [{'visible': []},
                         {'title': opt + ' Score Mean by Status'}]}

        x = list([opt == option for option in options])
        menu['args'][0]['visible'] = [False] + x
        menus.append(menu)
    return menus