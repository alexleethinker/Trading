import plotly.express as px



def fig_render(fig, hovertemplate):
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'margin': dict(autoexpand=True,l=0,r=0,t=0,b=0),
        })
    fig.update_coloraxes(showscale=False)
    fig.update_traces(  marker_line_width = 0.5,
                        marker_line_color = "white",
                        textposition = 'middle center', 
                        textinfo = 'label', 
                        textfont = dict(color='white'),
                        texttemplate = "%{label}<br>%{customdata[0]:.2f}%<br>",
                        hovertemplate = hovertemplate)
    return fig



def treemap(df, path, values, color, range_color, custom_data, hovertemplate):
    fig = px.treemap(df, 
                    path=path,  # 指定层次结构，每一个层次都应该是category型的变量
                    values=values, # 需要聚合的列名
                    color=color, 
                    range_color=[-range_color,range_color], # 色彩范围最大最小值
                    custom_data=custom_data,
                    color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                    color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                    )
    fig = fig_render(fig, hovertemplate)  
    return fig

