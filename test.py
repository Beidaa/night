import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os




def get_ciba():
    url = "https://api.tianapi.com/tiangou/index?key=4bd63a1e9f1b96e518d2a9857359a3f1"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["newslist"]
    
    # note_ch = r.json()["note"]
    return  note_en