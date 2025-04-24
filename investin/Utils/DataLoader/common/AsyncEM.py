import asyncio
from typing import Dict, List

import aiohttp
import pandas as pd



em_fields = {
    'f2':'最新价',
    'f3':'涨跌幅',
    'f6':'成交额',
    'f7':'振幅',
    'f8':'换手率',
    'f12':'证券代码',
    'f14':'证券名称',
    'f20':'总市值',
    'f21':'流通市值',
    'f9':'市盈率',
    'f23':'市净率',
    'f37':'ROE',
    'f41':'总营收同比',
    'f46':'净利润同比',
    'f49':'毛利率',
    'f57':'资产负债率',
    'f58':'净资产',
    'f102':'地区板块',
    'f112':'EPS',
    'f113':'每股净资产',
    'f133':'股息率',
    'f103':'东财概念'
}
fields = [ i for i in em_fields]
fields = ','.join(fields)





async def fetch_single_page(
    session: aiohttp.ClientSession, url: str, params: Dict
) -> Dict:
    """异步获取单页数据"""
    async with session.get(url, params=params, ssl=False) as response:
        return await response.json()


async def fetch_all_pages_async(url: str, base_params: Dict) -> List[Dict]:
    """异步获取所有页面数据"""
    # 首先获取总数以计算页数
    first_page_params = base_params.copy()
    first_page_params["pn"] = "1"

    async with aiohttp.ClientSession() as session:
        first_page_data = await fetch_single_page(session, url, first_page_params)

        # 检查是否成功获取数据
        if first_page_data.get("rc") != 0 or not first_page_data.get("data"):
            return [first_page_data]  # 返回错误信息

        total = first_page_data["data"]["total"]
        page_size = int(base_params["pz"])
        total_pages = (total + page_size - 1) // page_size

        # 限制页数，避免过大请求
        total_pages = min(total_pages, 150)

        # 创建所有页面的任务
        tasks = []
        for page in range(1, total_pages + 1):
            page_params = base_params.copy()
            page_params["pn"] = str(page)
            tasks.append(fetch_single_page(session, url, page_params))

        # 并发执行所有任务
        results = await asyncio.gather(*tasks)
        return results


def process_data(page_results: List[Dict]) -> pd.DataFrame:
    """处理获取到的数据，转换为DataFrame"""
    all_data = []

    # 保存每个页面的结果和页码
    page_number = 1
    items_per_page = 100  # 假设每页100条

    for result in page_results:
        if result.get("rc") == 0 and result.get("data") and result["data"].get("diff"):
            page_data = result["data"]["diff"]
            for item in page_data:
                item["page_number"] = page_number
                item["page_index"] = page_data.index(item)
            all_data.extend(page_data)
            page_number += 1
    if not all_data:
        return pd.DataFrame()
    df = pd.DataFrame(all_data)
    df["序号"] = df.apply(
        lambda row: (row["page_number"] - 1) * items_per_page + row["page_index"] + 1,
        axis=1,
    )
    df.drop(columns=["page_number", "page_index"], inplace=True, errors="ignore")
    df = df.rename(columns = em_fields)

    df['流通市值'] = (pd.to_numeric(df['流通市值'], errors="coerce")/100000000).round(2).fillna(0) 
    df['总市值'] = (pd.to_numeric(df['总市值'], errors="coerce")/100000000).round(2).fillna(0) 
    df['成交额'] = (pd.to_numeric(df['成交额'], errors="coerce")/100000000).round(2).fillna(0) 

    df['EPS'] = (pd.to_numeric(df['EPS'], errors="coerce")).round(2).fillna(0) 
    df['每股净资产'] = (pd.to_numeric(df['每股净资产'], errors="coerce")).round(2).fillna(0) 
    df['资产负债率'] = (pd.to_numeric(df['资产负债率'], errors="coerce")).round(2).fillna(0) 
    df['股息率'] = (pd.to_numeric(df['股息率'], errors="coerce")).round(2).fillna(0) 

    df['最新价'] = pd.to_numeric(df['最新价'], errors="coerce")
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors="coerce")
    df['振幅'] = pd.to_numeric(df['振幅'], errors="coerce")
    df['换手率'] = pd.to_numeric(df['换手率'], errors="coerce")
    df['毛利率'] = pd.to_numeric(df['毛利率'], errors="coerce").round(2).fillna(0) 
    df['净利润同比'] = pd.to_numeric(df['净利润同比'], errors="coerce").round(2).fillna(0) 
    df['总营收同比'] = pd.to_numeric(df['总营收同比'], errors="coerce").round(2).fillna(0) 
    df['地区板块'] = df['地区板块'].str.replace('板块','')

    df = df[['证券代码','证券名称','地区板块','流通市值','总市值','最新价', '涨跌幅','振幅','成交额','换手率','市盈率','市净率','EPS','每股净资产','ROE','毛利率','总营收同比','净利润同比','股息率','资产负债率','东财概念']]

    df = df[df['流通市值'] > 0]
    df = df[df['总市值'] > 0]
    df = df[df['成交额'] > 0]

    df.sort_values(by="涨跌幅", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["序号"] = df.index + 1
    return df


async def stock_zh_a_spot_em_async(market) -> pd.DataFrame:
    """
    异步获取东方财富网-沪深京 A 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    if market == 'China':
        fs = 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048'
    elif market == 'HK':
        fs = 'm:128 t:3,m:128 t:4,m:128 t:1,m:128 t:2'
    elif market == 'US':
        fs = 'm:105,m:106,m:107'       
    elif market == 'UK':
        fs = 'm:155 t:1,m:155 t:2,m:155 t:3,m:156 t:1,m:156 t:2,m:156 t:5,m:156 t:6,m:156 t:7,m:156 t:8'       
    else:
        raise('Market not support')

    url = "https://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": fs,
        "fields": fields,
    }
    results = await fetch_all_pages_async(url, params)
    return process_data(results)


def fetch_spot_em(market) -> pd.DataFrame:
    """
    东方财富网-沪深京 A 股-实时行情 (同步接口)
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    import nest_asyncio

    nest_asyncio.apply()
    return asyncio.run(stock_zh_a_spot_em_async(market))


if __name__ == "__main__":
    stock_zh_a_spot_em_df = fetch_spot_em(market='China')
    print(stock_zh_a_spot_em_df)