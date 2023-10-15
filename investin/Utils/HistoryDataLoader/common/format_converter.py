import pandas as pd
from tqdm import tqdm
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
from datetime import datetime
import exchange_calendars as xcals


market = 'china'

h5_dir = f'{data_dir}/history/stock/{market}.h5'
store = pd.HDFStore(h5_dir, 'r')   
stock_list = [x.replace('/','') for x in store.keys()]   


def history_spot():
    df = pd.DataFrame()
    for symbol in tqdm(stock_list):
        try:
            dfi = store[symbol]
            # dfi = dfi[dfi.index == date]
            dfi.insert(loc=0, column='证券代码', value=symbol)
            df = pd.concat([df, dfi], ignore_index=True)
        except:
            pass
    return df


def get_date_list():
    xshg = xcals.get_calendar("XSHG")
    date_list = xshg.schedule.index.date
    date_list = [ x.strftime('%Y-%m-%d') for x in date_list if x < datetime.today().date() ]
    return date_list


def write_snapshot(df, date):
    df.to_feather(f'{data_dir}/history/snapshot/{market}/{date}.feather')

date_list = get_date_list()
df = history_spot()

for date in tqdm(date_list):
    dfi = df[df.index == date]
    write_snapshot(dfi, date)


store.close()