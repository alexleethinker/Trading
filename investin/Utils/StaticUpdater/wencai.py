import pywencai


query = '所属概念 公司亮点 所属同花顺行业 所属指数类'



r = pywencai.get(query=query, sort_key='退市@退市日期', sort_order='asc')

print(r)