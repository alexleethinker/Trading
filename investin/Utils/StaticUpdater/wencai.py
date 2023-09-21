import pywencai


# query = '所属概念 公司亮点 所属同花顺行业 所属指数类'
query = '行业 概念 市值'
loop = True
query_type = 'hkstock'

'''
stock	股票
zhishu	指数
fund	基金
hkstock	港股
usstock	美股
threeboard	新三板
conbond	可转债
insurance	保险
futures	期货
lccp	理财
foreign_exchange	外汇
'''

r = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)

r.to_csv('hk_stock_details.csv', index = False)