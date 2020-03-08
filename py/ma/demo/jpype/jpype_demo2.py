# -*- coding:utf-8 -*-
import jpype

jvmPath = jpype.getDefaultJVMPath()
print(jvmPath)

jarPath = r" -jar E:\code\Athena\taurus\scala\ZxyyRtc\out\artifacts\ZxyyRtc_jar\ZxyyRtc.jar"

jpype.startJVM(jvmPath, jarPath)

# Zxyy = jpype.JClass('rtc.DPublic')
# Zxyy.now()

jpype.shutdownJVM()

