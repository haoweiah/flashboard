#!/usr/bin/env python
# coding=utf-8
import sh
import fire
import os
import re


def Findcase(name):
    """
    find case and execute
    :param name:
    :return:
    """
    filepaths = {"/home/hw/acs/acs_test_suites/OTC/TC/TP/tests/Graphics_Display",
                 "/home/hw/acs/acs_test_suites/OTC/TC/TP/tests/Graphics_RenderApp",
                 "/home/hw/acs/acs_test_suites/OTC/TC/TP/tests/Graphics_System"
                 }
    nosestr = ""

    def ClassName(rfile, i):

        for line in reversed(rfile[:i]):
            if "class " in line:
                classname = re.search(r"(?<=class ).*?(?=\()", line).group()
                if classname:
                    return classname
                else:
                    raise Exception("not find classname")

    filelist = [os.path.join(root, file) for filepath in filepaths for root, dirs, files in os.walk(filepath) for file
                in files if "init" not in file]
    for file in filelist:
        with open(file, errors="ignore") as f:
            file_str = f.readlines()
            name_list = [i for i, fname in enumerate(file_str) if name + "(" in fname]
            if name_list:
                classname = ClassName(file_str, name_list[0])
                print("classname -----", classname)
                nosestr = "{file}:{classname}.{name}".format(file=file, classname=classname, name=name)
                domain = re.search(r'(?<=tests/)(.*?)/', file).group()
                print("domain----- {}".format(domain))
                os.environ['TEST_DATA_ROOT'] = "/home/hw/acs/acs_test_suites/OTC/TC/TP/testplan/{domain}".format(
                    domain=domain)
                break
    nose = sh.Command("nosetests")
    if nosestr == "": raise Exception("dont have nosestr")
    try:
        nose("-s", nosestr, _fg=True)
    except:
        pass


if __name__ == '__main__':
    fire.Fire(Findcase)
# Findcase("test_VK_ubo_random")
