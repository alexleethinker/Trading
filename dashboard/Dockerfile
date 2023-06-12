FROM python:3.9.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y nodejs && \
    apt-get -y autoclean && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* 

RUN pip --no-cache-dir install --upgrade pandas streamlit altair==4.0 plotly exchange_calendars apscheduler zhconv
# RUN pip --no-cache-dir install --upgrade cloudscraper cryptography==38.0.4 selenium requests-html



# ADD ./ /home
# WORKDIR /home