# -*- coding:utf-8 -*-
import subprocess
import chardet
import sys

class Demo(object):
    """
    """
    def process(self):
        jarPath = r"E:\code\Athena\taurus\scala\ZxyyRtc\out\artifacts\ZxyyRtc_jar\ZxyyRtc.jar"
        command = "java -jar %s" %(jarPath)

        stdout,stderr = subprocess.Popen(
            command,stdout=subprocess.PIPE,stderr=subprocess.PIPE
        ).communicate()
        print("============", stdout)
        print("============", stderr)

        encoding = chardet.detect(stdout)["encoding"]
        result = stdout.decode(encoding)
        return result


if __name__ == '__main__':
    Demo = Demo()
    res = Demo.process()
    print("============", res)

