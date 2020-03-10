#!/usr/bin/bash
source /etc/profile


####### ####### ####### ####### ####### #######
if [ $# -lt 2 ]
then
    echo $0 " [all | update_pstate | train | predict]  [ps | start | stop] "
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
projectName=MAnalysis


# [App路径].
APP_DIR=/root/works/src/git_test/rtc/poc_MAnalysis/py/ma

App_ds_web_Path=${APP_DIR}/DService/web

App_ds_Real_data_Path=${APP_DIR}/Real_data

App_train_Path=/root/works/ibin/real_MAnalysis_jar/
App_predict_Path=/root/works/ibin/real_MAnalysis_jar/


# [输出目录].
Out_Dir=/root/works/idata/ma16_out
Log_Dir=/root/works/idata/ma16_log


# [更新.环境变量].
export PYTHONPATH=${APP_DIR}
export BONC_MA16_PATH=/root/works/ibin

# [日期].
ymd=`date +%Y%m%d`
###########  ###########  ###########

# 【update_pstate】更新训练状态
App_update_pstate=soft_update_predictState
App_update_pstate_PY=${App_ds_Real_data_Path}/${App_update_pstate}.py
App_update_pstate_OUT=${Out_Dir}/${App_update_pstate}_${ymd}.py

# 【train】 训练
App_train=maTrain_soft
App_train_JAR=${App_train_Path}/${App_train}.jar
App_train_OUT=${Out_Dir}/${App_train}_${ymd}.out

# 【predict】 预测
App_predict=maPredict_soft
App_predict_JAR=${App_predict_Path}/${App_predict}.jar
App_predict_OUT=${Out_Dir}/${App_predict}_${ymd}.out
###########  ###########  ###########

case ${appName} in

# 针对【所有】进程. 
all)
    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${App_update_pstate}"  "${projectName}"
            echo -e ""

            moni_ps_aux "${App_train}" "${projectName}"
            echo -e ""

            moni_ps_aux "${App_predict}" "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        nohup /root/anaconda3/bin/python -u  ${App_update_pstate_PY} >> ${App_update_pstate_OUT} 2>&1 &

        nohup java  -jar ${App_train_JAR} >> ${App_train_OUT} 2>&1 &

        nohup java  -jar ${App_predict_JAR} >> ${App_predict_OUT} 2>&1 &
    ;;
    stop)
        kill_ps "${App_update_pstate}"  "${projectName}"

        kill_ps "${App_train}" "${projectName}"
       
        kill_ps "${App_predict}" "${projectName}"
    ;;
    *)
        echo -e "第[2]个参数输入错误! "
        exit 0
    ;;
    esac
;;
######## ######## ########

######## ######## ########

# [ 更新训练状态 ].
update_pstate)
    appName=${App_update_pstate}
    pyName=${App_update_pstate_PY}
    outFile=${App_update_pstate_OUT}

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



# [ 预测 ].
predict)
    appName=${App_predict}
    jarName=${App_predict_JAR}
    outFile=${App_predict_OUT}
    
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
