from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from data_loader import update_spot_data

def update_spot_data_at_trading():    
    import datetime
    import exchange_calendars as xcals
    xshg = xcals.get_calendar("XSHG") #获取A股交易日期
    if xshg.is_trading_minute(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        update_spot_data()
    else:
        pass
        # print('not a trading date')



def start_cronjob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()

    # scheduler.add_job(save_data, 'interval', minutes=1, id='load_data')
    scheduler.add_job(update_spot_data_at_trading, 'cron', day_of_week='mon-fri',hour='1-6',minute='*')
    scheduler.add_job(update_spot_data, 'cron', day_of_week='mon-fri',hour='7',minute='1')
    scheduler.start()

if __name__ == "__main__":

    print('Started scheduler')

    start_cronjob()