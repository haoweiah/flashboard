#!/usr/bin/env python

from subprocess import *
import os, shutil
import time
import fire
import zipfile
import requests
import serial
from tqdm import tqdm 
requests.packages.urllib3.disable_warnings()

class flash_mrb(object):
    def __init__(self):
        if call(r"ls /dev/ttyUSB*", shell=True):
            raise Exception("not inset debug borad")
        call(r"pkill minicom", shell=True)
        self.ser = serial.Serial('/dev/ttyUSB2')
        self.filepath = os.getcwd() + os.sep + time.strftime('ww%W%w') + os.sep
        shutil.rmtree(self.filepath, ignore_errors=True)
        os.mkdir(self.filepath)

    def downfile(self, url):
        # wget = Popen(r"wget {url} --no-check-certificate  -P {filepath} --http-user=haowx --http-password='hw!QAZ1qaz' --no-proxy".format(filepath=self.filepath, url=url), shell=True)
        r = requests.get(url, auth=('haowx', 'hw!QAZ1qaz'), verify=False, stream=True)
        if r.status_code != 200:
            raise Exception("download file fail")
        length = float(r.headers['content-length'])/512
        pbar = tqdm(total=length)
        with open(self.filepath + 'test.zip', 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
                    pbar.update(1)
        pbar.close()
        with zipfile.ZipFile(self.filepath + 'test.zip') as f:
            f.extractall(self.filepath)

    # def

if __name__ == '__main__':
    fire.Fire(flash_mrb)
