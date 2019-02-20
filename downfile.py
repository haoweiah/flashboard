#!/usr/bin/env python3
import sys
from subprocess import *
import os, shutil, re
import time
import fire
import zipfile, requests
import serial
import sh
#from tqdm import tqdm
requests.packages.urllib3.disable_warnings()



def urlpath( url):
    filepath = os.path.join(os.getcwd(), time.strftime('ww%W%w/'))
    if os.path.exists(filepath):
        shutil.rmtree(filepath[:-1] + ".old", ignore_errors=True)
        sh.mv(filepath, filepath[:-1] + ".old/")
    os.mkdir(filepath)
    r = requests.get(url, auth=('haowx', 'hw!QAZ1qaz'), verify=False, stream=True)
    # filename = re.search(r'(?<=userdebug/)(.*)', url).group(0)
    filename = url.split('/')[-1]
    print(filename)
    if r.status_code != 200:
        raise Exception("download file fail")

    length = int(r.headers['content-length'])
    chunk_len = 0
    timenow = time.time()

    print("[DEBUG]:Download file")

    with open(filepath + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
                chunk_len += 512
                if time.time() - timenow > 0.05:
                    print("[{:.0%} ]downloadfile".format(chunk_len / length), end="\r")
                    timenow = time.time()
    print("[DEBUG]: Download file over")

    with zipfile.ZipFile(os.path.join(filepath, filename)) as f:
        zip_list = f.namelist()
        for i, zname in enumerate(zip_list):
            f.extract(zname, filepath)
            print("[{}/{}] zip extrac".format(i + 1, len(zip_list)), end="\r")
    print("[DEBUG]: extract zip over")

if __name__ == '__main__':
    fire.Fire(urlpath)
