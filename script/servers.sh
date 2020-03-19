#!/usr/bin/bash
source /etc/profile


####### ####### ####### ####### ####### #######
if [ $# -lt 2 ]
then
    echo $0 " [all | ds_web | mysql_2kafka | kafka_2mqtt | train ]  [ps | start | stop] "
exit 0
fi
####### ####### ####### ####### ####### #######



####### ####### ####### ####### ####### #######
# [ps进程.函数], 间隔n秒查看一次，默认[5]秒. 
# [函数.参数1] 进程名.
# [函数.参数2] 项目名.
moni_ps()
{
    num=`ps -ef | grep -v "grep" | grep -v "\.sh" | grep "${1}" | grep "${2}" | wc -l`
    if [ ${num} -ge 1 ]
    then
        ps -ef | grep -v "grep" | grep -v "\.sh" | grep "${1}" | grep "${2}"
        #echo -e
    fi
    echo -e "进程=[${1}], 进程数=[${num}]..........................."
}

moni_ps_aux()
{
    num=`ps -ef | grep -v "grep" | grep -v "\.sh" | grep "${1}" | grep "${2}" | wc -l`
    if [ ${num} -ge 1 ]
    then
        ps aux | grep -v "grep" | grep -v "\.sh" | grep "${1}" | grep "${2}" 
        #echo -e
    fi
    echo -e "进程=[${1}], 进程数=[${num}]..........................."
}

# [kill进程.函数]. 
# [函数.参数1] 进程名.
# [函数.参数2] 项目名.
kill_ps()
{
    echo -e "进程=[${1}], 停止前....................."
    ps -ef | grep "${1}" | grep "${2}" | grep -v grep | grep -v "\.sh"
    
    echo -e "进程=[${1}], 开始停止..................."
    ps -ef | grep "${1}" | grep "${2}" | grep -v grep | grep -v "\.sh" | awk '{print $2}' | xargs kill -9
    
    echo -e "进程=[${1}], 停止后....................."
    ps -ef | grep "${1}" | grep "${2}" | grep -v grep |grep -v "\.sh"
}
####### ####### ####### ####### ####### #######

####### ####### ####### ####### ####### #######
# [参数1]代表[应用].
appName=$1

# [参数2]代表[动作].
actName=$2

# [项目名称].
projectName=app16


# [App路径].
APP_DIR=/root/works/src/BONC/app16/py/ma

App_ds_web_Path=${APP_DIR}/DService/web

App_dstream_opt_Path=${APP_DIR}/Dstream/optimAnalysis

App_train_Path=/root/works/ibin/app16_jar

# [输出目录].
Out_Dir=/root/works/idata/ma16_out
Log_Dir=/root/works/idata/ma16_log


# [更新.环境变量].
export PYTHONPATH=${APP_DIR}
export BONC_MA16_PATH=/root/works/ibin

# [日期].
ymd=`date +%Y%m%d`
###########  ###########  ###########

# [App名称 / python文件 / 输出].
# 【data service】数据服务.
App_ds_web=data_service_main
App_ds_web_PY=${App_ds_web_Path}/${App_ds_web}.py
App_ds_web_OUT=${Out_Dir}/${App_ds_web}_${ymd}.out

# 【mysql_2kafka】从mysql导入数据源
App_mysql_2kafka=opt_Data_mysql_2_kafka
App_mysql_2kafka_PY=${App_dstream_opt_Path}/${App_mysql_2kafka}.py
App_mysql_2kafka_OUT=${Out_Dir}/${App_mysql_2kafka}_${ymd}.out

# 【kafka_2mqtt】结果写入mqtt
App_kafka_2mqtt=opt_Result_Kafka_2_mqtt
App_kafka_2mqtt_PY=${App_dstream_opt_Path}/${App_kafka_2mqtt}.py
App_kafka_2mqtt_OUT=${Out_Dir}/${App_kafka_2mqtt}_${ymd}.py

# 【train】 训练
App_train=maTrain
App_train_JAR=${App_train_Path}/${App_train}.jar
App_train_OUT=${Out_Dir}/${App_train}_${ymd}.out


case ${appName} in

# 针对【所有】进程. 
all)
    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${App_ds_web}"  "${projectName}"
            echo -e ""

            moni_ps_aux "${App_mysql_2kafka}" "${projectName}"
            echo -e ""

            moni_ps_aux "${App_kafka_2mqtt}" "${projectName}"
			echo -e ""
			
			moni_ps_aux "${App_train}" "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        nohup /root/anaconda3/bin/python -u  ${App_ds_web_PY} >> ${App_ds_web_OUT} 2>&1 &
		nohup /root/anaconda3/bin/python -u  ${App_mysql_2kafka_PY} >> ${App_mysql_2kafka_OUT} 2>&1 &
		nohup /root/anaconda3/bin/python -u  ${App_kafka_2mqtt_PY} >> ${App_kafka_2mqtt_OUT} 2>&1 &
		 nohup java  -jar ${App_train_JAR} >> ${App_train_OUT} 2>&1 &
    ;;
    stop)
        kill_ps "${App_ds_web}"  "${projectName}"
		kill_ps "${App_mysql_2kafka}"  "${projectName}"
		kill_ps "${App_kafka_2mqtt}"  "${projectName}"
		kill_ps "${App_train}" "${projectName}"
    ;;
    *)
        echo -e "第[2]个参数输入错误! "
        exit 0
    ;;
    esac
;;
######## ######## ########



# [ 数据服务 ].
ds_web)
    appName=${App_ds_web}
    pyName=${App_ds_web_PY}
    outFile=${App_ds_web_OUT}

    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${appName}"  "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        if [[ $# -eq 3 ]] && [[ $3 == "front" ]] 
        then 
            echo "/root/anaconda3/bin  ${pyName} "
            /root/anaconda3/bin/python  ${pyName}
        else
            nohup /root/anaconda3/bin/python -u  ${pyName} >> ${outFile} 2>&1 &
        fi
    ;;
    stop)
        kill_ps "${appName}"  "${projectName}"
    ;;
    *)
        echo -e "第[2]个参数输入错误! "
        exit 0
    ;;
    esac
;;
######## ######## ########

# [ 从mysql导入数据 ].
mysql_2kafka)
    appName=${App_mysql_2kafka}
    pyName=${App_mysql_2kafka_PY}
    outFile=${App_mysql_2kafka_OUT}

    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${appName}"  "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        if [[ $# -eq 3 ]] && [[ $3 == "front" ]]
        then
            echo "/root/anaconda3/bin  ${pyName} "
            /root/anaconda3/bin/python  ${pyName}
        else
            nohup /root/anaconda3/bin/python -u  ${pyName} >> ${outFile} 2>&1 &
        fi
    ;;
    stop)
        kill_ps "${appName}"  "${projectName}"
    ;;
    *)
        echo -e "第[2]个参数输入错误! "
        exit 0
    ;;
    esac
;;
######## ######## ########

######## ######## ########
# [ 结果写入mqtt ].
kafka_2mqtt)
    appName=${App_kafka_2mqtt}
    pyName=${App_kafka_2mqtt_PY}
    outFile=${App_kafka_2mqtt_OUT}

    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${appName}"  "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        if [[ $# -eq 3 ]] && [[ $3 == "front" ]]
        then
            echo "/root/anaconda3/bin  ${pyName} "
            /root/anaconda3/bin/python  ${pyName}
        else
            nohup /root/anaconda3/bin/python -u  ${pyName} >> ${outFile} 2>&1 &
        fi
    ;;
    stop)
        kill_ps "${appName}"  "${projectName}"
    ;;
    *)
        echo -e "第[2]个参数输入错误! "
        exit 0
    ;;
    esac
;;
######## ######## ########
# [ 训练 ].
train)
    appName=${App_train}
    jarName=${App_train_JAR}
    outFile=${App_train_OUT}

    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${appName}" "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        cd ${App_train_Path}

        if [[ $# -eq 3 ]] && [[ $3 == "front" ]]
        then
            java  -jar ${jarName}
        else
            nohup java  -jar ${jarName} >> ${outFile} 2>&1 &
        fi
    ;;
    stop)
        kill_ps "${appName}" "${projectName}"
    ;;
    *)
        echo -e "第[2]个参数输入错误! "
        exit 0
    ;;
    esac
;;
######## ######## ########


*)
    echo -e "第[1]个参数输入错误!"
    exit 0
;;
esac

exit
