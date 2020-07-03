from flask import Flask
from datetime import datetime
import os
import logging
import time

# this file still needs work, just take a look at parse.py

def fetch_data():
    '''
    function is run once everyday to fetch data from the updating
    kaggle dataset of region-wise datasets
    '''
    os.system('kaggle datasets download -d sudalairajkumar/novel-corona-virus-2019-dataset')

app = Flask(__name__)

@app.route("/")
def main():
    fetch_data()
    return "hello world"

if __name__ == "__main__":
  app.run()
