from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from data_loader_china_a import update_spot_data_a
from data_loader_hk import update_spot_data_hk
from data_loader_us import update_spot_data_us
from data_loader_worldwide import update_spot_data_global
import datetime
import exchange_calendars as xcals


def update_spot_data_at_trading_a():    

    xshg = xcals.get_calendar("XSHG") #获取A股交易日期
    if xshg.is_trading_minute(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        update_spot_data_a()
    else:
        pass
        # print('not a trading date')



def start_cronjob():
    job_defaults = {
                'coalesce': False,
                'max_instances': 3
               }
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler(job_defaults=job_defaults)

    # scheduler.add_job(save_data, 'interval', minutes=1, id='load_data')
    scheduler.add_job(update_spot_data_at_trading_a, 'cron', day_of_week='mon-fri',hour='1-6',minute='*')
    scheduler.add_job(update_spot_data_a, 'cron', day_of_week='mon-fri',hour='7',minute='1')

    scheduler.add_job(update_spot_data_hk, 'cron', day_of_week='mon-fri',hour='1-8',minute='0/15')
    scheduler.add_job(update_spot_data_us, 'cron', day_of_week='mon-fri',hour='13-22',minute='0/15')
    scheduler.add_job(update_spot_data_global, 'cron', day_of_week='mon-fri',hour='0-21',minute='0/15')
    scheduler.start()

if __name__ == "__main__":
    print('Started scheduler')
    
    start_cronjob()