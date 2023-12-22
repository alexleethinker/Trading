from st_pages import Page, Section, show_pages, add_page_title
from utils.config import get_args
args = get_args()
language = args.language

# add_page_title() # By default this also adds indentation
# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be

if language == '中文':
    show_pages(
        [
            Page("investin/Streamlit/pages/exchange_clock.py", "开盘时钟", "⏰"),
            Page("investin/Streamlit/pages/1_Main Markets.py", "主要市场", "💴"),
            Page("investin/Streamlit/pages/0_Global Markets.py", "全球市场", "🌎"),
            Page("investin/Streamlit/pages/2_Indutries.py", "行业对比", "⚙️"),
            Page("investin/Streamlit/pages/5_Time Machine.py", "历史切面", "🕙"),
            Page("investin/Streamlit/pages/indices.py", "指数", "🕙"),
            # Page("investin/Streamlit/pages/6_ 📈_量化回测.py", "Backtest Engine", "📈"),
        ]
    )    
else:
    show_pages(
        [
            Page("investin/Streamlit/pages/exchange_clock.py", "Exchange Clocks", "⏰"),
            Page("investin/Streamlit/pages/0_Global Markets.py", "Global Markets", "🌎"),
            Page("investin/Streamlit/pages/1_Main Markets.py", "Main Markets", "💴"),
            Page("investin/Streamlit/pages/2_Indutries.py", "Indutries", "⚙️"),
            Page("investin/Streamlit/pages/5_Time Machine.py", "Time Machine", "🕙"),
            # Page("investin/Streamlit/pages/6_ 📈_量化回测.py", "Backtest Engine", "📈"),
        ]
    ) 