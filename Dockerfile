FROM nikolaik/python-nodejs:python3.11-nodejs20

RUN pip --no-cache-dir install --upgrade lib-pybroker mootdx pandas pywencai streamlit altair==4.0 plotly exchange_calendars apscheduler zhconv lxml openpyxl streamlit-autorefresh
RUN pip --no-cache-dir install --upgrade tables
# RUN pip --no-cache-dir install --upgrade cloudscraper cryptography==38.0.4 selenium requests-html

# ADD ./ /home
# WORKDIR /home