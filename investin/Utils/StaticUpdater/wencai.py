import pywencai


query = '所属概念 公司亮点 所属同花顺行业 所属指数类'
loop = True
query_type = 'stock'

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

r = pywencai.get(query=query)

print(r)