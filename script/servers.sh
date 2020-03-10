#!/usr/bin/bash
source /etc/profile


####### ####### ####### ####### ####### #######
if [ $# -lt 2 ]
then
    echo $0 " [all | ds_web | product | update_ds]  [ps | start | stop] "
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
# APP_DIR=/root/works/src/git_test/rtc/poc_MAnalysis/py/ma
APP_DIR=/root/works/src/BONC/app16/py/ma

App_ds_web_Path=${APP_DIR}/DService/web

App_ds_Real_data_Path=${APP_DIR}/Real_data


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

# 【data product】造数据
App_data_product=Data_product
App_data_product_PY=${App_ds_Real_data_Path}/${App_data_product}.py
App_data_product_OUT=${Out_Dir}/${App_data_product}_${ymd}.out

# 【update_ds】更新数据源
App_update_ds=update_datasource
App_update_ds_PY=${App_ds_Real_data_Path}/${App_update_ds}.py
App_update_ds_OUT=${Out_Dir}/${App_update_ds}_${ymd}.py


case ${appName} in

# 针对【所有】进程. 
all)
    case ${actName} in
    ps)
        while [ 1 ]
        do
            moni_ps "${App_ds_web}"  "${projectName}"
            echo -e ""

            moni_ps_aux "${App_data_product}" "${projectName}"
            echo -e ""

            moni_ps_aux "${App_update_ds}" "${projectName}"
            echo "☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺"
            sleep 10
        done
    ;;
    start)
        nohup /root/anaconda3/bin/python -u  ${App_ds_web_PY} >> ${App_ds_web_OUT} 2>&1 &
		nohup /root/anaconda3/bin/python -u  ${App_data_product_PY} >> ${App_data_product_OUT} 2>&1 &
		nohup /root/anaconda3/bin/python -u  ${App_update_ds_PY} >> ${App_update_ds_OUT} 2>&1 &
    ;;
    stop)
        kill_ps "${App_ds_web}"  "${projectName}"
		kill_ps "${App_data_product}"  "${projectName}"
		kill_ps "${App_update_ds}"  "${projectName}"

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

# [ 产生数据 ].
product)
    appName=${App_data_product}
    pyName=${App_data_product_PY}
    outFile=${App_data_product_OUT}

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

# [ 更新数据源 ].
update_ds)
    appName=${App_update_ds}
    pyName=${App_update_ds_PY}
    outFile=${App_update_ds_OUT}

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

*)
    echo -e "第[1]个参数输入错误!"
    exit 0
;;
esac

exit
