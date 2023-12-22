from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from investin.Utils.DataLoader.China import StockSpotChinaA
from investin.Utils.DataLoader.US import StockSpotUS
from investin.Utils.DataLoader.UK import StockSpotUK
from investin.Utils.DataLoader.HK import StockSpotHKEX
from investin.Utils.DataLoader.Euronext import StockSpotEuronext
from investin.Utils.DataLoader.Xetra import StockSpotXetra
from investin.Utils.DataLoader.TradingView import StockSpotTradingView
from investin.Utils.IntradayDataLoader.indices import indices_intraday, indices_intraday_china, indices_intraday_hk, indices_intraday_india, indices_intraday_apac, indices_intraday_europe, indices_intraday_US


import datetime
import exchange_calendars as xcals


def update_spot_data_at_trading_a():    

    xshg = xcals.get_calendar("XSHG") #获取A股交易日期
    if xshg.is_trading_minute(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        StockSpotChinaA().run()
        indices_intraday_china()
    else:
        pass
        # print('not a trading date')

def update_spot_europe_at_trading():    

    xams = xcals.get_calendar("XAMS") #获取A股交易日期
    if xams.is_trading_minute(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        StockSpotEuronext().run()
        StockSpotXetra().run()
        StockSpotUK().run()
        indices_intraday_europe()
    else:
        pass


def start_cronjob():
    job_defaults = {
                'coalesce': False,
                'max_instances': 3
               }
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler(job_defaults=job_defaults)

    # scheduler.add_job(save_data, 'interval', minutes=1, id='load_data')
    scheduler.add_job(update_spot_data_at_trading_a, 'cron', day_of_week='mon-fri',hour='0-7',minute='*',second='30')
    scheduler.add_job(StockSpotChinaA().run, 'cron', day_of_week='mon-fri',hour='7',minute='1')
    scheduler.add_job(indices_intraday_china(), 'cron', day_of_week='mon-fri',hour='7',minute='1')

    scheduler.add_job(update_spot_europe_at_trading, 'cron', day_of_week='mon-fri',hour='7-16',minute='0/1',second='30')
    scheduler.add_job(StockSpotEuronext().run, 'cron', day_of_week='mon-fri',hour='16',minute='36,55')
    scheduler.add_job(StockSpotXetra().run, 'cron', day_of_week='mon-fri',hour='16',minute='36,55')
    scheduler.add_job(StockSpotUK().run, 'cron', day_of_week='mon-fri',hour='16',minute='36,55')
    scheduler.add_job(indices_intraday_europe(), 'cron', day_of_week='mon-fri',hour='16',minute='36,55')

    
    scheduler.add_job(StockSpotHKEX().run, 'cron', day_of_week='mon-fri',hour='0-8',minute='0/1')
    scheduler.add_job(indices_intraday_hk(), 'cron', day_of_week='mon-fri',hour='0-8',minute='0/1')
    scheduler.add_job(StockSpotUS().run, 'cron', day_of_week='mon-fri',hour='14-22',minute='0/1')
    scheduler.add_job(indices_intraday_US().run, 'cron', day_of_week='mon-fri',hour='14-22',minute='0/1')    
    scheduler.add_job(StockSpotTradingView().run, 'cron', day_of_week='mon-fri',hour='0-22',minute='0/1')
    scheduler.add_job(indices_intraday_apac(), 'cron', day_of_week='mon-fri',hour='1-8',minute='0/1')
    scheduler.add_job(indices_intraday_india(), 'cron', day_of_week='mon-fri',hour='3-11',minute='0/1')
    
    scheduler.add_job(indices_intraday(), 'cron', day_of_week='mon-fri',hour='22',minute='1')
    scheduler.start()

if __name__ == "__main__":
    print('Started scheduler')
    
    start_cronjob()