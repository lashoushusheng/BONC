import jpype

jvmPath = jpype.getDefaultJVMPath()
print(jvmPath)

jpype.startJVM(jvmPath)

jpype.java.lang.System.out.println("hello chijy")

jpype.shutdownJVM()

