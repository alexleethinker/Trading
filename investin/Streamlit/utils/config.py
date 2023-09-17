import streamlit as st
from datetime import datetime
import pytz
import os



data_dir = os.getenv('DATA_DIR') 


# def page_config():
#     hide_streamlit_style = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     body {border-color: white; border-style: solid;}
#     footer {visibility: hidden;}
#     </style>
#     # """
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def page_config(
        max_width: int = 1100, max_width_100_percent: bool = True,
        padding_top: int = 0, padding_right: int = 1, padding_left: int = 1, padding_bottom: int = 1,
        color: str = 'black', background_color: str = 'black',
    ):
    st.set_page_config(layout= 'wide')
    if max_width_100_percent:
        max_width_str = f'max-width: 100%;'
    else:
        max_width_str = f'max-width: {max_width}px;'
    st.markdown(
        f'''
        <style>
            #MainMenu {{visibility: hidden;}}
            body {{border-color: white; border-style: solid;}}
            footer {{visibility: hidden;}}
            .reportview-container .sidebar-content {{
                padding-top: {padding_top}rem;
            }}
            .reportview-container .main .block-container {{
                {max_width_str}
                padding-top: {padding_top}rem;
                padding-right: {padding_right}rem;
                padding-left: {padding_left}rem;
                padding-bottom: {padding_bottom}rem;
            }}
            .reportview-container .main {{
                color: {color};
                background-color: {background_color};

            }}
        </style>
        ''',
        unsafe_allow_html=True,
        )


def update_at(data_path, timezone):
    text = '更新时间： ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S') +  ' ({timezone})'.format(timezone=timezone)
    st.markdown(text)  