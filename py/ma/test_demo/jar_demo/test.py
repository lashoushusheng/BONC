command = "java -jar aes.jar"
arg0 = "待解密的字符串"
arg1 = "密钥"

cmd = [command,arg0,arg1]

new_cmd = " ".join(cmd)
print(new_cmd)