import logging
import warnings
import requests
import json
import sys 
import random 
import os 
import subprocess 
import time 
from time import sleep 
import threading 
from threading import Lock 
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob 
import configparser 
import shutil 
import copy 
from functools import partial 
from pathlib import Path 
import traceback 
import win32api 
import io 
import re
from typing import Dict, List, Union, Callable, Optional
import string 
import names 
import pyotp 
from tkinter import messagebox

os.makedirs('./logs', exist_ok=True)
warnings.filterwarnings("ignore", category=DeprecationWarning)

noisy_loggers = [
    'appium', 'urllib3', 'http.client', 'http', 'selenium',
    'selenium.webdriver.remote.remote_connection', 'webdriver_manager',
    'asyncio', 'PIL', 'geopy', 'geopy.adapters', 'requests', 'pytesseract']

for name in noisy_loggers:
    logger = logging.getLogger(name)
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False

logging.basicConfig(
    filename='./logs/logs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8')

__all__ = [
    'logging', 'warnings', 'requests', 'json',
    'sys', 'random', 'os', 'subprocess', 'time', 'sleep', 'threading', 'Lock',
    'datetime', 'timedelta', 'ThreadPoolExecutor', 'as_completed', 'glob',
    'configparser', 'shutil', 'copy', 'partial', 'Path', 'traceback', 'win32api',
    'io', 're', 'Dict', 'List', 'Union', 'Callable', 'Optional', 'string',
    'names', 'pyotp', 'messagebox'
]