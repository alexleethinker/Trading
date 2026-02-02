import pywencai
import pandas as pd
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'



def calculate_PEG(loop = True):
    # 分红比例 ~= 股利支付率
    #query = 'PE 扣非PE PB 扣非ROE 扣非净利润同比增长率 每股分红 股利支付率 销售净利率 销售毛利率 商誉占净资产比例 ROA  ROE EPS 货币资金/流动市值 股息率 资产负债率 过去三年平均营收增速'
    query = 'PE 扣非PE PB 扣非ROE 扣非净利润同比增长率 股利支付率 ROA  ROE 货币资金/流动市值 股息率 资产负债率 过去三年平均营收增速'
    loop = loop
    query_type = 'stock'
    r = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)
    
    # r = r.rename(columns= {"[1]/[2]":"现金"})
    r.columns = [x.split('[')[0] for x in r.columns.tolist()]
    # print(r.columns)
    result = r[['股票代码','股票简称','市盈率(pe)','市盈率(pe,扣非ttm)','市净率(pb)','净资产收益率roe-扣除非经常损益','净资产收益率roe(加权,公布值)','总资产报酬率roa','股息率(股票获利率)','股利支付率','归属母公司股东的净利润-扣除非经常损益(同比增长率)','营业收入(同比增长率)平均','资产负债率','{(}货币资金']]
    result.columns = ['股票代码','股票简称','PE','扣非PE','PB','扣非ROE','ROE','ROA','股息率','分红比例','扣非净利润增速','营收增速','资产负债率','现金']
    result = result.apply(pd.to_numeric, errors='ignore').rename(columns={"股票代码":"证券代码"})

    result['扣非PEG']  = (result['扣非PE'] / result['营收增速'])

    def dividend_correct(x):
        if x >= 0.5:
            n = 1
        elif x < 0.25:
            n = 2
        else:
            n = 0.5/x
        return n

    result['分红比例'] = result['分红比例'].fillna(0)
    result['扣非市赚率'] = result['扣非PE'] / result['扣非ROE'] * result['分红比例'].apply(dividend_correct)
    result['市赚率'] =result['PE'] / result['ROE'] * result['分红比例'].apply(dividend_correct)
    result['财务健康度'] = (1 / result['扣非市赚率']) + result['现金'].fillna(0)
    result.loc[(result['扣非PE']> 0) & (result['扣非ROE']<0) & (result['PB']>0),'财务健康度']  = (1 / result['市赚率']) + result['现金'].fillna(0)
    result.loc[(result['PB']<0),'财务健康度']  = -10
    result.loc[(result['扣非PE']< 0) & (result['扣非ROE']<0) ,'财务健康度']  = -1 + result['现金'].fillna(0)
    result['财务健康度'] = result['财务健康度'].fillna(0)
    result.loc[(result['财务健康度'] == 0),'财务健康度']   = (1 / result['市赚率']) + result['现金'].fillna(0)

    df = result.fillna('').apply(pd.to_numeric, errors='ignore').round(2).copy()

    # 市赚率
    # PE<0 ROE > 0, 亏损
    # 扣非PE<0 扣非ROE>0, 扣非亏损
    # ROE<0 资不抵债

    df.loc[(df['PE']< 0) & (df['ROE']<0),'市赚率'] = '亏损'
    df.loc[(df['PE']> 0) & (df['ROE']<0) & (df['PB']<0),'市赚率'] = '强烈警报'
    df.loc[(df['PE']< 0) & (df['ROE']>0),'市赚率'] = '危险信号'

    df.loc[(df['扣非PE']< 0) & (df['扣非ROE']<0),'扣非市赚率'] = '扣非亏损'
    df.loc[(df['扣非PE']> 0) & (df['扣非ROE']<0) & (df['PB']<0),'扣非市赚率'] = '强烈警报'
    df.loc[(df['扣非PE']< 0) & (df['扣非ROE']>0),'扣非市赚率'] = '危险信号'
    df.loc[(df['扣非PE']> 0) & (df['扣非ROE']<0) & (df['PE']< 0),'扣非市赚率'] = '困境反转'

    df.loc[df['扣非PE']< 0,'扣非PEG'] = '扣非亏损'
    # 分红比例 < 0
    # PE 或 盈利增速 < 0
    df.to_csv(data_dir + '/static/EM/China/a_stock_PE_values.csv', index =False)
    # print(df)


if __name__ == '__main__':
    calculate_PEG(loop = True)