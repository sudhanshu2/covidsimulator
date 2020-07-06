from datetime import datetime
import os
import logging
import time
import schedule
from crontab import CronTab

def check_mid_night():
    # function to check if the clock is at midnight
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    return seconds_since_midnight == 0

def fetch_data():
    '''
    function is run once everyday to fetch data from the updating
    kaggle dataset of region-wise datasets
    '''
    os.system('kaggle datasets download -d sudalairajkumar/novel-corona-virus-2019-dataset')
    os.system('rm -rf direct_data')
    os.system('unzip novel-corona-virus-2019-dataset.zip -d direct_data')
