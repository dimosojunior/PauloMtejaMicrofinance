from apscheduler.schedulers.background import BackgroundScheduler
from .no_rejesho_scheduler import check_and_update_rejesho

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_update_rejesho, 'cron', hour=18)  # Runs every day at 6:00 PM
    scheduler.start()
