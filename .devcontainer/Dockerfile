FROM python:3.9.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y nodejs && \
    apt-get -y autoclean && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* 

RUN pip --no-cache-dir install --upgrade notebook tqdm pandas akshare hikyuu mootdx tushare pandahouse clickhouse_driver streamlit altair==4.0 plotly exchange_calendars apscheduler openpyxl lxml &&\
    pip --no-cache-dir install git+https://github.com/alexleethinker/wencai.git
