#!/usr/bin/env python

from subprocess import *
import os, shutil
import time
import fire
import zipfile
import requests
import serial
import sh 
from tqdm import tqdm 
requests.packages.urllib3.disable_warnings()

class flash_mrb(object):
    def __init__(self):
        if call(r"ls /dev/ttyUSB*", shell=True):
            raise Exception("not inset debug borad")
        call(r"pkill minicom", shell=True)
        time.sleep(1)
        self.ser2 = serial.Serial('/dev/ttyUSB2')
        self.ser3 = serial.Serial('/dev/ttyUSB3')
        self.filepath = os.getcwd() + os.sep + time.strftime('ww%W%w') + os.sep

    def downfile(self, url):
        # wget = Popen(r"wget {url} --no-check-certificate  -P {filepath} --http-user=haowx --http-password='hw!QAZ1qaz' --no-proxy".format(filepath=self.filepath, url=url), shell=True)
        shutil.rmtree(self.filepath, ignore_errors=True)
        os.mkdir(self.filepath)
        r = requests.get(url, auth=('haowx', 'hw!QAZ1qaz'), verify=False, stream=True)
        if r.status_code != 200:
            raise Exception("download file fail")
        length = int(r.headers['content-length'])/512
        pbar = tqdm(total=length)
        with open(self.filepath + 'test.zip', 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
                    pbar.update(1)
        pbar.close()
        with zipfile.ZipFile(self.filepath + 'test.zip') as f:
            f.extractall(self.filepath)

    def cflasher(self):
        if not self.ser2.isOpen():
            raise Exception("is not open")
        self.ser2.write(b'r')
        if self.ser2.read().find("Logic Core Initialisation done"):
            self.ser2.write(b'n1#')



if __name__ == '__main__':
    fire.Fire(flash_mrb)
