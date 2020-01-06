#!/usr/bin/env python
import PySimpleGUI as sg
from multiprocessing import Process
import psutil
import time
import platform
from datetime import datetime
import wmi
import pythoncom
import urllib.request
import socket

sg.theme('Dark Blue')  # Please always add color to your window
bar_count = 0

# percent of loaded virtual memory
mem = psutil.virtual_memory()
percent = mem.percent
# running time of system
data = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
data2 = datetime.fromtimestamp(psutil.boot_time())
now_time = datetime.now()

time_past = now_time - data2
time_past = str(time_past)
time_past = time_past[0:-7]
computer = wmi.WMI()


def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        return host_ip
    except:
        print("Unable to get Hostname and IP")


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def info_proceses():
    global bar_count, mem, percent, time_past
    print("in Info process")
    bar_count = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    percent = mem.percent
    now_time2 = datetime.now()
    time_past = now_time2 - data2
    time_past = str(time_past)
    time_past = time_past[0:-5]


def info_processor():
    global computer
    print("in Info procesor")
    pythoncom.CoInitialize()

    cpufreq = psutil.cpu_freq()
    cpus = psutil.cpu_percent(percpu=True, interval=1)
    proc_info = computer.Win32_Processor()[0]
    proc_name = proc_info.Name
    proc_L2Cache = proc_info.L2CacheSize
    proc_L3Cache = proc_info.L3CacheSize
    return [psutil.cpu_count(logical=False), cpufreq.max, cpufreq.current, psutil.cpu_percent(), cpus, proc_name,
            proc_L2Cache, proc_L3Cache]


def info_memory():
    print("in Info memory")
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return [get_size(svmem.total), get_size(svmem.available), get_size(svmem.used), svmem.percent,
            get_size(swap.total), get_size(swap.free), get_size(swap.used), swap.percent]


def get_ip_addresses(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == -1:
                mac = snic.address
            if snic.family == 2:
                yield interface, snic.address, snic.netmask, mac


def info_internet():
    try:
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except:
        external_ip = '0.0.0.0'

    internal_ip = get_Host_name_IP()
    ipv4 = list(get_ip_addresses(socket.AF_INET))

    ##TODO loop for checking if it is ETHernet or WiFi connection
    if ipv4[0][1] == internal_ip:
        print("in Info intenet")
    con = str(ipv4[0][0])
    ip = str(ipv4[0][1])
    mask = str(ipv4[0][2])
    mac = str(ipv4[0][3])
    return [external_ip, internal_ip, con, ip, mask, mac]


def gui():
    print("in Info gui")
    # The tab 1, 2, 3 layouts - what goes inside the tab
    info = [[sg.Text('Info')],
            [sg.Text('CPU usage %', size=(20, 1)), sg.Text(bar_count, size=(3, 1), key='CPU'),
             sg.ProgressBar(max_value=100, orientation='h', border_width=1, size=(12, 5),
                            bar_color=('#199FD0', '#FFFFFF'), key='BAR')],
            [sg.Text('Memory usage %', size=(20, 1)), sg.Text(percent, size=(3, 1), key='MEM'),
             sg.ProgressBar(max_value=100, orientation='h', border_width=1, size=(12, 5), bar_color=('#199FD0',
                                                                                                     '#FFFFFF'),
                            key='MEM2')],
            [sg.Text('Start Time', size=(20, 1)), sg.Text(data, size=(20, 1), key='START')],
            [sg.Text('Running Time', size=(20, 1)), sg.Text(time_past, size=(20, 1), key='RUN')]]

    tab_cpu = [
        [sg.Text('Name ', size=(20, 1)), sg.Text(info_processor()[5], key='CPU_NAME')],
        [sg.Text("Physical cores", size=(20, 1)), sg.Text(info_processor()[0], key='CPU_CORES')],
        [sg.Text("Max Frequencys", size=(20, 1)), sg.Text(info_processor()[1], key='CPU_MAX')],
        [sg.Text("Current Frequency", size=(20, 1)), sg.Text(info_processor()[2], key='CPU_FRQ')],
        [sg.Text("Total CPU load", size=(20, 1)), sg.Text(info_processor()[3], key='CPU_LOAD')],
        [sg.Text("Each core load", size=(20, 1)), sg.Text(info_processor()[4], key='CPU_CLOAD')],
        [sg.Text("L2 Cache", size=(20, 1)), sg.Text(info_processor()[6], key='L2Cache')],
        [sg.Text("L3 Cache", size=(20, 1)), sg.Text(info_processor()[7], key='L3Cache')],
    ]
    tab_gpu = [[sg.Text('GPU')]]

    tab_net = [
        [sg.Text('External IPv4', size=(20, 1)), sg.Text(info_internet()[0], key='EX_IP4')],
        [sg.Text('Internal IPv4', size=(20, 1)), sg.Text(info_internet()[1], key='IN_IP4')],
        [sg.Text('Connection types', size=(20, 1)), sg.Text(info_internet()[2], key='IP_Con')],
        [sg.Text('Mask', size=(20, 1)), sg.Text(info_internet()[4], key='Mask')],
        [sg.Text('MAC', size=(20, 1)), sg.Text(info_internet()[5], key='MAC')],
    ]

    tab_mem = [
        [sg.Text('Total ', size=(22, 1)), sg.Text(info_memory()[0], key='Total_mem')],
        [sg.Text('Available ', size=(22, 1)), sg.Text(info_memory()[1], key='MEM_ava')],
        [sg.Text('Used ', size=(22, 1)), sg.Text(info_memory()[2], key='MEM_USED')],
        [sg.Text('Percentage ', size=(22, 1)), sg.Text(info_memory()[3], key='MEM_PER')],
        [sg.Text('Total SWAP Memory', size=(22, 1)), sg.Text(info_memory()[4], key='TOT_SWAP')],
        [sg.Text('Free SWAP Memory', size=(22, 1)), sg.Text(info_memory()[5], key='FREE_SWAP')],
        [sg.Text('Used SWAP Memory', size=(22, 1)), sg.Text(info_memory()[6], key='USED_SWAP')],
        [sg.Text('Percentage  SWAP Memory', size=(22, 1)), sg.Text(info_memory()[7], key='SWAP_PER')]
    ]

    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [
        [sg.Tab('INFO', info, font='Courier 15', key='INFO'),
         sg.Tab('CPU', tab_cpu, key='CPU2'),
         sg.Tab('GPU', tab_gpu, key='GPU'),
         sg.Tab('Internet', tab_net, key='NET'),
         sg.Tab('Memory', tab_mem, key='RAM')]]

    # The window layout - defines the entire window
    layout = [[sg.TabGroup(tab_group_layout,
                           selected_title_color='blue',
                           selected_background_color='red',
                           tab_background_color='green',
                           enable_events=True,
                           # font='Courier 18',
                           key='-TABGROUP-')],
              ]
    print("start gui")
    window = sg.Window('Task Manager', layout, no_titlebar=False)

    while True:
        event, values = window.read(timeout=10)  # type: str, dict

        while True:
            print("in While loop")
            info_proceses()
            info_internet()
            info_memory()
            info_processor()
            window['BAR'].update_bar(current_count=bar_count)
            window['MEM2'].update_bar(current_count=percent)
            window['CPU'].update(bar_count)
            window['MEM'].update(percent)
            window['START'].update(data)
            window['RUN'].update(time_past)

            event, values = window.read(timeout=500)
            if event in (None, 'Cancel'):
                print('break inner')
                break

        if event in (None, 'Cancel'):
            print('break outer')
            break
    window.close()


def main():
    print("before gui")
    # gui()
    threads = []
    t0 = Process(target=gui, daemon=True)
    print("after gui")
    t1 = Process(target=info_proceses, daemon=False)
    print("after process")
    t2 = Process(target=info_memory, daemon=False)
    print("after memory")
    t3 = Process(target=info_processor, daemon=False)
    print("after procesor")
    t4 = Process(target=info_internet, daemon=False)
    print("after internet")
    threads.append(t0)
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)
    print(" append")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("after join")


if __name__ == '__main__':
    print("main")
    main()
