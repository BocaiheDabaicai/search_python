import os
import shutil
import time
import easygui as eg
import sys
import string
import win32api, win32con
import threading


# 全局对象，存放所有文件名称
all_search_file = []
disk_count = 0
dir_count = 0
file_count = 0

# 初始化路径
reg_root = win32con.HKEY_CURRENT_USER
reg_class = win32con.HKEY_CLASSES_ROOT
reg_machine = win32con.HKEY_LOCAL_MACHINE
reg_user = win32con.HKEY_USERS
reg_config = win32con.HKEY_CURRENT_CONFIG

def get_disk():
    global disk_count
    # 获取磁盘文件
    disk_list = []
    for disk in string.ascii_uppercase:
        disk = disk + ':\\'
        if os.path.exists(disk):
            disk_list.append(disk)
    print(disk_list, len(disk_list))
    disk_count += len(disk_list)
    return disk_list


def searchDirs(root, name, dirs):
    global dir_count
    # 搜索包含关键字的目录
    for _dir in dirs:
        dir_count += len(dirs)
        if -1 != _dir.find(name) and _dir[0] != '$':
            AllDir = os.path.join(root, _dir)
            all_search_file.append(AllDir)


def searchfiles(root, name, files):
    global file_count
    # 搜索包含关键字的文件
    for file in files:
        file_count += len(files)
        if name in file:
            AllFile = os.path.join(root, file)
            all_search_file.append(AllFile)


def search(name):
    # 执行搜索功能
    curdisks = get_disk()
    print("程序正在执行，请耐心等待")
    try:
        for disk in curdisks:
            for root, dirs, files in os.walk(disk, True):
                searchDirs(root, name, dirs)
                searchfiles(root, name, files)
    except Exception as e:
        print(e)
        sys.exit(0)

def delete_data(name):
    # 删除文件或文件夹
    if os.path.isfile(name):
        try:
            os.remove(name)
            print('删除成功')
        except Exception as e:
            print(e)
            print('删除失败')
    else:
        try:
            shutil.rmtree(name)
            print('删除成功')
        except Exception as e:
            print(e)
            print('删除失败')

def get_all_registry_software():
    # 配置具体搜索路径
    reg_paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                 r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]
    # 搜集器
    all_list = []
    for path in reg_paths:
        # 取出具体路径，获取具体路径键值

        pkey = win32api.RegOpenKeyEx(reg_machine, path)
        for item in win32api.RegEnumKeyEx(pkey):
            # 取出键名，做匹配
            print(item[0])
            try:
                # 指明需要删除的名称，删除操作需要管理员权限才可以实现
                if(item[0] == 'adobe'):
                    all_list.append(item[0])
                    win32api.RegDeleteKey(pkey,item[0])
            except Exception as e:
                print(e)
                print('IMPORTANTERROR')
                pass
        win32api.RegCloseKey(pkey)
    return all_list


def main():
    eg.msgbox(title="文件检索", msg="查找的文件名为:adobe\n请耐心等待程序运行完毕，预计在五分钟左右\n\n\n\n请点击ok")
    start_time = time.time()
    search("adobe")
    end_time = time.time()
    timeout = end_time - start_time
    while all_search_file:
        choice = eg.multchoicebox(title="搜索结果",
                                  msg="一共搜索 " + str(disk_count) + " 块磁盘\n一共搜索 " + str(dir_count) + " 个目录\n一共搜索 " + str(file_count) + " 个文件\n一共用时: " + str(timeout)[:7] + " 秒\n请选择您需要删除的文件或文件夹\n并点击确认进行删除",
                                  choices=all_search_file)
        if choice:
            for item in choice:
                all_search_file.remove(item)
                delete_data(item)
        else:
            print('点击取消')
            break
    else:
        eg.msgbox(title="结果",msg="未查找到此文件 或 对应文件已全部被删除，查找完毕\n接下来进行注册表删除,请点击ok")
        test = get_all_registry_software()
        print(test)
        print('文件、文件夹、注册表信息已全部删除完毕，请关闭控制台。')
        time.sleep(1000)


if __name__ == '__main__':
    main()
