import logging
import os
import subprocess
import time

from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from pathlib import Path
from threading import Thread

import dmPython
import psycopg2
import pymssql
from secmind.rpa_v2 import common, WinRMWrapper, SSHWrapper
import paramiko
import pymysql
from ldap3 import Server, Connection, ALL, NTLM
import cx_Oracle

john_path = '/root/john-1.9.0-Jumbo-1/run/john'
codebook_path = '/root/service/codebook/'

def do_task(data_map):

    userNameList = data_map['user']
    dataBaseList = data_map['database']
    job_id = data_map['password']
    protocol = data_map['protocol']
    #关闭库日志
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger("dmPython").disabled = True
    logging.getLogger("psycopg2").disabled = True
    logging.getLogger("pymssql").disabled = True
    logging.getLogger("secmind.rpa_v2").disabled = True
    logging.getLogger("pymysql").disabled = True
    logging.getLogger("cx_Oracle").disabled = True
    result = []
    try:
        # 判断是否用自定义密码本
        wordlist = f'{codebook_path}codebook.txt'
        if os.path.exists(f'{codebook_path}{job_id}.txt'):
            print(f"本地存在密码本，路径为：{codebook_path}{job_id}.txt")
            wordlist = f'{codebook_path}{job_id}.txt'
        else:
            if codebook(job_id):
                wordlist = f'{codebook_path}{job_id}.txt'
    except Exception as e:
        logging.error(e)
    dir_path = f'{codebook_path}{job_id}.txt'
    with open(dir_path, 'r', encoding='utf-8') as file:
        passWordList = file.read()
    start = datetime.now()
    result_queue = Queue()
    #设置为守护进程，主线程终止监测进程立刻终止避免资源浪费
    t = Thread(target=monitor_runtime, args=(start, result_queue), daemon=True)
    t.start()
    if protocol == 'oracle':
        detect_oracle(userNameList, passWordList, data_map, result, dataBaseList, result_queue)
    elif protocol == 'mysql' or protocol == 'db_kundb':
        detect_mysql(userNameList, passWordList, data_map, result, result_queue)
    elif protocol == 'dameng':
        detect_dameng(userNameList, passWordList, data_map, result, result_queue)
    elif protocol == 'sqlserver':
        detect_sqlserver(userNameList, passWordList, data_map, result, result_queue)
    elif protocol == 'postgresql' or protocol == 'kingbase8':
        detect_postgre(userNameList, passWordList, data_map, result, dataBaseList, result_queue)
    elif protocol == 'rdp':
        detect_windows(userNameList, passWordList, data_map, result, result_queue)
    elif protocol == 'ssh':
        detect_linux(userNameList, passWordList, data_map, result, result_queue)
    # end = datetime.now()
    # total_seconds = (end - start).total_seconds()
    # print(f"总耗时：{total_seconds} 秒")
    return str(result)

def codebook(id):
    import requests
    print("请求密码本")
    response = requests.post(f'http://xpam-runner-core:33100/account/device/codebook?jobId={id}')

    # 检查请求是否成功
    if response.status_code == 200:
        print("请求成功")
        if response.text:
            # 打开本地文件进行写入
            with open(f'{codebook_path}{id}.txt', 'w') as f:
                f.write(response.text)
            return True
    else:
        common.logger.error('请求失败，状态码：', response.status_code)
    return False

def monitor_runtime(start_time, q):
    print(f"[监测进程启动] PID: {os.getpid()}")
    while True:
        now = datetime.now()
        elapsed = now - start_time
        print(f"[监测进程] 已运行时间：{elapsed}")

        if elapsed > timedelta(minutes=60*2):
            q.put(f"{elapsed}")
            print(f"[监测进程] 检测超时，脚本运行时间：{elapsed}")
        time.sleep(60 * 10)  # 每10分钟检测一次

def detect_mysql(userNameList, passWordList, data_map, result, result_queue):
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            try:
                connect = pymysql.connect(
                    host=data_map['location'],
                    user=username,
                    password=password)
                cursor = connect.cursor()
                info = 'ip:' + data_map['location'] + ' username:' + username + ' password:' + password
                result.append(info)
            except Exception as ex:
                pass

def detect_dameng(userNameList, passWordList, data_map, result, result_queue):
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    for username in userNameList:
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            try:
                connect = dmPython.connect(
                    server=data_map['location'],
                    port=int(data_map['port']),
                    user=username,
                    password=password)
                cursor = connect.cursor()
                info = 'ip:' + data_map['location'] + ' username:' + username + ' password:' + password
                result.append(info)
            except Exception as ex:
                pass

def detect_oracle(userNameList, passWordList, data_map, result, dataBaseList, result_queue):
    lock_flag = False
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    if dataBaseList is None or len(dataBaseList) == 0:
        dataBaseList = data_map['database']
    if isinstance(dataBaseList, str):
        dataBaseList = dataBaseList.splitlines()
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                 raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            print(password)
            for database in dataBaseList:
                try:
                    url = "{0}/{1}@{2}:{3}/{4}".format(username, password, data_map['location'], data_map['port'],
                                                       database)
                    connect = cx_Oracle.connect(url)
                    cursor = connect.cursor()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:' + database
                    result.append(info)
                except Exception as ex:
                    if ex.args[0].code == 28000:
                        print("当前账户被锁定")
                        lock_flag = True
                        # break;
                    pass
            if lock_flag:
                break
        if lock_flag:
            lock_flag = False
            continue

def detect_sqlserver(userNameList, passWordList, data_map, result, dataBaseList, result_queue):
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    if dataBaseList is None or len(dataBaseList) == 0:
        dataBaseList = data_map['database']
    if isinstance(dataBaseList, str):
        dataBaseList = dataBaseList.splitlines()
    for username in userNameList:
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            for database in dataBaseList:
                try:
                    connect = pymssql.connect(
                        host=data_map['location'],
                        port=data_map['port'],
                        database=database,
                        user=username,
                        password=password)
                    cursor = connect.cursor()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:' + database
                    result.append(info)
                except Exception as ex:
                    pass

def detect_postgre(userNameList, passWordList, data_map, result, dataBaseList, result_queue):
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    if dataBaseList is None or len(dataBaseList) == 0:
        dataBaseList = data_map['database']
    if isinstance(dataBaseList, str):
        dataBaseList = dataBaseList.splitlines()
    for username in userNameList:
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            for database in dataBaseList:
                try:
                    conn_params = {
                        "dbname": database,
                        "user": username,
                        "password": password,
                        "host": data_map['location'],
                        "port": data_map['port']
                    }
                    connect = psycopg2.connect(**conn_params)
                    cursor = connect.cursor()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:' + database
                    result.append(info)
                except Exception as ex:
                    pass

def detect_windows(userNameList, passWordList, data_map, result, result_queue):
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
                try:
                    winrm_wrapper = WinRMWrapper(host=data_map['location'], username=username, password=password)
                    winrm_wrapper.connect()
                    info = 'ip:' + data_map[
                        'location'] + ' username:' + username + ' password:' + password + ' database:'
                    result.append(info)
                except Exception as ex:
                    pass

def detect_windowsAD(userNameList, passWordList, data_map, result, result_queue, domain):
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    for username in userNameList:
        if "\\" not in username:
            username = domain + "\\" + username
        checked.append(username)
        print(
            f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            try:
                server = Server(data_map['location'], get_info=ALL)
                conn = Connection(server, user=username, password=password, authentication=NTLM, auto_bind=True)
                conn.unbind()
                info = 'ip:' + data_map[
                    'location'] + ' username:' + username + ' password:' + password + ' database:'
                result.append(info)
            except Exception as ex:
                pass

def detect_linux(userNameList, passWordList, data_map, result, result_queue):
    client = paramiko.SSHClient()
    checked = []
    if isinstance(userNameList, str):
        userNameList = userNameList.splitlines()
    if isinstance(passWordList, str):
        passWordList = passWordList.splitlines()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for username in userNameList:
        checked.append(username)
        print(f"===资产探测中====当前用户：{username}, 进度：{(len(checked) / len(userNameList.splitlines())) * 100:.2f}%")
        if not result_queue.empty():
            result = result_queue.get()
            if result:
                raise RuntimeError(f"脚本执行超时，任务已自动终止，执行时间：{result}")
        for password in passWordList:
            try:
                client.connect(
                    hostname=data_map['location'],
                    port=data_map['port'],
                    username=username,
                    password=password,
                    timeout=10,
                    banner_timeout=15,
                    allow_agent=False,
                    look_for_keys=False
                )
                info = 'ip:' + data_map['location'] + ' username:' + username + ' password:' + password
                result.append(info)
            except paramiko.AuthenticationException:
                pass
            except paramiko.SSHException as e:
                print(f"SSH连接过于频繁：{e}")
                pass
            except Exception as ex:
                pass
            finally:
                client.close()

if __name__ == '__main__':
    common.go(do_task)