from sqlalchemy import create_engine
from time import time
import pandas as pd
import argparse
import requests
import gzip
import shutil
import os

def unzip(url):
    filename = 
    try:
        response = requests.get(url)
        print(f'Downloading {filename}')
