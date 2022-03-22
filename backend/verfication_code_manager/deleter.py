from apscheduler.schedulers.background import BackgroundScheduler
from verfication_code_manager import deleter_script



def start():
    delete_process = BackgroundScheduler()
    delete_process.add_job(deleter_script.delete_invalid_verification_codes, 'interval', minutes=60)
    delete_process.start()