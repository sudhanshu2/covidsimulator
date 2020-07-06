from flask import Flask
from datetime import datetime
import os
import logging
import time
from fetch_data import *

# this file still needs work, just take a look at parse.py

app = Flask(__name__)

@app.route("/")
def main():
    fetch_data()
    
if __name__ == "__main__":
  app.run()
