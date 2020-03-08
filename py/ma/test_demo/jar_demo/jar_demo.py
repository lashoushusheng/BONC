import jpype
from jpype import *
import codecs

def openjar():
    jvmpath = jpype.get_default_jvm_path()
    print(jvmpath)
    jpype.startJVM(jvmpath,"-Djava.class.path=/root/works/src/git_test/rtc/poc_MAnalysis/scala/ma/target/poc-mAnalysis-0.1.1-jar-with-dependencies.jar")
    jpype.java.lang.System.out.println("hello")


def get_text():
    # clasanme = JClass('rtcompute.RtcCompute.MaPredict_Main_opt')
    clasanme = JClass('test_demo.test.helloWorld')
    cn = clasanme()
    result = cn.getFunctionname()
    print(result)


if __name__ == '__main__':
    openjar()
    get_text()
    jpype.shutdownJVM()