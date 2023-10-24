import streamlit as st
import numpy as np
html_abnormal_mov = open('investin/Streamlit/utils/abnormal_mov.html', "r").read() 

def color_style(val):
    color = 'red' if val > 0 else 'green'
    return 'color: %s' % color
def color_abnormal(val):
    return 'color: gold'

def show_dataframe(df, market = None, language = '中文', source = None):
    
    if '市场' in df.values.tolist():
        pass
    else:
        df['市场'] = '-'
        
    df_sum = df.groupby(['市场'])[['总市值','成交额']].sum()
    df_sum['活跃度'] = df_sum['成交额'] / (np.log2(df_sum['总市值'] + 1) + 10) 
    df_sum['调整系数'] = 100 / (df_sum['活跃度'] + 1)

    df = df.merge(df_sum.reset_index()[['市场','调整系数']], how = 'left', on = '市场')
    df['异动值'] = df['异动值'] * df['调整系数']  
    
    
    # df_ind = df.groupby(['三级行业'])[['总市值','成交额']].sum()
    # df_ind['涨跌幅'] = df.groupby(['三级行业']).apply( lambda x : np.average(x['涨跌幅'], weights=x['成交额']))
    # df_ind['活跃度'] = df_ind['成交额'] / (np.log(df_ind['总市值'] + 1) + 1) 
    # df_ind['异动值'] = df_ind['成交额'] * df_ind['涨跌幅'].abs()/ (np.log(df_ind['总市值'] + 1) + 1) 
    # st.dataframe(df_ind.sort_values('异动值', ascending = False).style.format(precision=1))
   
    market_value = '流通市值' if market == '🇨🇳 A股' else '总市值'
    
    if language == '中文':
        industry = '二级行业' if market in ['🇨🇳 A股','🇭🇰 港股', '🇺🇸 美股', '🇬🇧 英股'] else '三级行业'
        symbol_name = '证券名称'
    else:
        industry = '二级行业' if market in ['🇨🇳 A股','🇭🇰 港股', '🇺🇸 美股', '🇬🇧 英股'] else 'industry'
        if source == 'tradingview':
            symbol_name = 'ticker_title'
        else:
            symbol_name = '证券名称'
            
        

    
    # df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df[market_value] + 1) + 1)
    
    df = df.drop_duplicates()
    df = df[(df['涨跌幅'].abs() > 0.5) & (df['异动值'] > 1) ].sort_values('异动值', ascending= False)\
        [['证券代码',symbol_name,'涨跌幅','异动值', market_value,'成交额', industry]].head(100)
        
        
    def markdown_fill(compare, values):
        values = values if language == '中文' else [i/10 for i in values]
        mv_text = str(int(values[0])) + compare + str(int(values[1]))  if compare == '-' else compare + str(int(values[0])) 
        markdown_text =  f'市场异动 (市值 {mv_text}亿)' if language == '中文' else f'Abnormal Movements (MarketValue {mv_text} Billion)' 
        return markdown_text
    
    
    def df_config():
        if language == '中文':
            config = None
        else:
            config = {
                    '证券代码':'Symbol',
                    symbol_name:'Name',
                    '涨跌幅':'Change%',
                    '异动值':'Ab_mov_index', 
                    market_value: 'MarketValue',
                    '成交额': 'Turnover', 
                    industry: 'Industry'
                    }
        return config
    
    
    
    col = st.columns([1, 1, 1])
    with col[0]:
        st.markdown(markdown_fill('>', [400]))
        st.dataframe(df[df[market_value] > 400].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .applymap(color_abnormal, subset=['异动值'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True,
            column_config= df_config()
            )
        # st.write(html_abnormal_mov, unsafe_allow_html= True)

    with col[1]:
        st.markdown(markdown_fill('-',[100,400]))
        st.dataframe(df[df[market_value].between(100,400)].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .applymap(color_abnormal, subset=['异动值'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True,
            column_config= df_config())
    
    with col[2]:
        st.markdown(markdown_fill('<',[100]))
        st.dataframe(df[df[market_value] < 100].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .applymap(color_abnormal, subset=['异动值'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True,
            column_config= df_config())
   
    