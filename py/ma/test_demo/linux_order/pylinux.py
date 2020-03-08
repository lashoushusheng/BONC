import subprocess
import os
import time

def subprocess_():
    """
    subprocess模块执行linux命令
    :return:
    """
    subprocess.call("ps") # 执行ls命令

def popen_():
    """
    popen模块执行linux命令。返回值是类文件对象，获取结果要采用read()或者readlines()
    :return:
    """
    val = os.popen('jps | grep MaPredict_Main_opt | wc -l').read() # 执行结果包含在val中
    print(val)

    res = None
    if int(val) > 0:
        # res =  os.popen("jps | grep MaPredict_Main_opt | awk '{print $1}' | xargs kill -9")
        res = os.system("jps | grep MaPredict_Main_opt | awk '{print $1}' | xargs kill -9")
    if res == 0:
        print("success")
    else:
        print("faild")

def system_():
    """
    system模块执行linux命令
    :return:
    """
    # 使用system模块执行linux命令时，如果执行的命令没有返回值res的值是256
    # 如果执行的命令有返回值且成功执行，返回值是0
    modelname = "多氟多2点_all"
    res = os.system(f"nohup java -cp /root/works/src/git_test/rtc/poc_MAnalysis/scala/ma/target/poc-mAnalysis-0.1.1-jar-with-dependencies.jar rtcompute.RtcCompute.MaPredict_Main_opt 多氟多2点_all > myout 2>&1 &")
    # res = os.system("nohup java -jar /root/works/src/git_test/rtc/poc_MAnalysis/scala/ma/classes/artifacts/hellloworld/helloworld.jar &")
    print(res)

def start_predict_compute():
    # 检查当前是否有任务在执行
    val = os.popen('jps | grep MaPredict_Main_opt | wc -l').read()  # 执行结果包含在val中
    if int(val) > 0:
        print("当前有任务在运行，无法提交！")
        return

    # res = os.system(f"nohup java -cp {conf.OPT_JAR_DIR} rtcompute.RtcCompute.MaPredict_Main_opt {modelName} > myout 2>&1 &")
    res = os.system(
        f"nohup java -cp /root/works/src/git_test/rtc/poc_MAnalysis/scala/ma/target/poc-mAnalysis-0.1.1-jar-with-dependencies.jar rtcompute.RtcCompute.MaPredict_Main_opt 多氟多2点_all > myout 2>&1 &")
    if res == 0:
        print("提交成功！")

    else:
        print("提交失败！")


if __name__ == '__main__':
    # popen_()
    # time.sleep(1)
    # system_()
    start_predict_compute()