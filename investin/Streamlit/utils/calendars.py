import pandas as pd
from datetime import datetime
import exchange_calendars as xcals
import plotly.express as px
from utils.config import data_dir


exchange_dir = '{data_dir}/static/exchanges.csv'.format(data_dir=data_dir)

def get_trading_calendars(language = '中文'):
    exchanges = xcals.get_calendar_names(include_aliases=False)
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    today_calendars = pd.DataFrame()
    for exchange in exchanges:
        cal = xcals.get_calendar(exchange)
        df = cal.schedule.loc[today:today]
        df['exchange'] = exchange
        df['is_open'] = cal.is_trading_minute(now)
        today_calendars = pd.concat([today_calendars, df], ignore_index=True)
    continuous = today_calendars[today_calendars['break_start'].isnull()][['open','close','exchange','is_open']]
    morning = today_calendars[~today_calendars['break_start'].isnull()][['open','break_start','exchange','is_open']].rename(columns={"break_start": "close"})
    afternoon = today_calendars[~today_calendars['break_start'].isnull()][['break_end','close','exchange','is_open']].rename(columns={"break_end": "open"})
    today_calendars = pd.concat([continuous, morning, afternoon], ignore_index=True)

    exchanges_info = pd.read_csv('{data_dir}/static/exchanges.csv'.format(data_dir=data_dir))
    today_calendars = today_calendars.merge(exchanges_info, how = 'left', left_on = 'exchange', right_on = 'ISO Code')
    today_calendars = today_calendars[today_calendars['Selected'].isin([1])]
    today_calendars = today_calendars.sort_values(['open','close']).reset_index(drop=True)

    country = '国家' if language == '中文' else 'Country'
    color_discrete_map = {True: 'lightskyblue', False: 'gray'}
    fig = px.timeline(today_calendars, x_start="open", x_end="close", y=country,color="is_open",
                      color_discrete_map=color_discrete_map,
                      hover_name= country,
                      custom_data=['open','close'],
                    )
    fig.update_yaxes(autorange="reversed",categoryorder='array', categoryarray=today_calendars['国家']) # otherwise tasks are listed from the bottom up

    fig.update_layout(
        xaxis = dict(side = 'top'),
        yaxis_title=None,
        xaxis_fixedrange = True,
        yaxis_fixedrange = True,
        dragmode=False,
        margin=dict(autoexpand=True,l=0,r=0,t=0,b=0),
        shapes=[
        dict(
        type='line',
        line=dict(color="White",width=2),
        yref='paper', y0=0, y1=1,
        xref='x', x0=now, x1=now,
        )
    ])
    fig.update_traces(hovertemplate= "%{label}",                 
                      marker_line_width = 0.5, 
                      showlegend=False
                      ) 
    return fig
