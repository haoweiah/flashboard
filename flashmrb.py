#!/usr/bin/env python
import sys
from subprocess import *
import os, shutil, re
import time
import fire
import zipfile, requests
import serial
import sh
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()


class flash_mrb(object):
    def __init__(self):
        if call(r"ls /dev/ttyUSB*", shell=True):
            raise Exception("not inset debug borad")
        # call(r"pkill minicom", shell=True)
        time.sleep(1)
        self.ser2 = serial.Serial('/dev/ttyUSB2')
        self.ser3 = serial.Serial('/dev/ttyUSB3')
        self.filepath = os.path.join(os.getcwd(), time.strftime('ww%W%w/'))
        json_file = "ifwi_gr_mrb_bi.bin"

    def downfile(self, url):
        # wget = Popen(r"wget {url} --no-check-certificate  -P {filepath} --http-user=haowx --http-password='hw!QAZ1qaz' --no-proxy".format(filepath=self.filepath, url=url), shell=True)
        if os.path.exists(self.filepath):
            shutil.rmtree(self.filepath[:-1] + ".old", ignore_errors=True)
            sh.mv(self.filepath, self.filepath[:-1] + ".old/")
        os.mkdir(self.filepath)
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
        with open(self.filepath + filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
                    chunk_len += 512
                    if time.time() - timenow > 0.05:
                        print("[{:.0%} ]downloadfile".format(chunk_len / length), end="\r")
                        timenow = time.time()
                    # sys.stdout.write("\r[{:.0f}%] downloadfile".format(chunk_len/length *100))
                    # sys.stdout.flush()
        with zipfile.ZipFile(os.path.join(self.filepath, filename)) as f:
            zip_list = f.namelist()
            for i, zname in enumerate(zip_list):
                f.extract(zname, self.filepath)
                print("[{}/{}] zip extrac".format(i + 1, len(zip_list)), end="\r")
            # f.extractall(self.filepath)

    def iocaplflash(self):
        ioc = sh.Command("/opt/intel/platformflashtool/bin/ioc_flash_server_app")
        apl = sh.Command("/opt/intel/platformflashtool/bin/ias-spi-programmer")
        zipname = sh.ls(self.filepath)
        binfile = "ifwi.bin" if "acrn" in zipname else "ifwi_gr_mrb_b1.bin"
        ioc("-s", "/dev/ttyUSB2", "-t", os.path.join(self.filepath, "ioc_firmware_gp_mrb_fab_e.ias_ioc"), _fg=True)
        self.ser2.write("r".encode())
        time.sleep(1)
        self.ser2.write("n1#".encode())
        time.sleep(1)
        apl("--write", os.path.join(self.filepath, binfile), _fg=True)

    def cflasher(self):
        if not self.ser2.isOpen():
            raise Exception("is not open")
        # self.ser2.write("r".encode())
        # if self.ser2.read().find("Logic Core Initialisation done"):
        # log_file = os.path.join(self.filepath,"")
        # while True:
        #    line = self.ser2.readline().decode()
        #    if line is None:
        #        break
        self.ser2.write("r".encode())
        time.sleep(1)
        self.ser2.write("n4#".encode())

        zipname = sh.ls(self.filepath)
        json = "SOS_and_AaaG" if "acrn" in zipname else "blank_gr_mrb_b1"
        jsonname = "flash_AaaG.json" if "acrn" in zipname else "flash.json"
        sh.cflasher("-f", self.filepath + jsonname, "-c", json, _fg=True)

    def write_and_except(self, data, except_data, timeout=20):
        pass


if __name__ == '__main__':
    fire.Fire(flash_mrb)
