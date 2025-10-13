from apscheduler.schedulers.background import BackgroundScheduler
from .no_rejesho_scheduler import check_and_update_rejesho


def start():
    scheduler = BackgroundScheduler()
    # Once a day at 6:00 PM
    scheduler.add_job(check_and_update_rejesho, 'cron', hour=21, minute=0)
    
    # Uncomment the following line to schedule task every 10 seconds
    #scheduler.add_job(check_and_update_rejesho, 'interval', seconds=10)
    
    scheduler.start()