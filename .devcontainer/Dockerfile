FROM python:3.11

# RUN apt-get -y update && \
#     apt-get install --no-install-recommends -y nodejs && \
#     apt-get -y autoclean && \
#     apt-get -y clean && \
#     rm -rf /var/lib/apt/lists/* 

RUN  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip --no-cache-dir install --upgrade requests_html pywencai tsfresh sktime notebook tqdm pandas akshare hikyuu mootdx tushare streamlit altair==4.0 plotly exchange_calendars apscheduler openpyxl lxml 