#!/usr/bin/env python
import PySimpleGUI as sg
from multiprocessing import Process
import psutil
from datetime import datetime
import wmi
import urllib.request
import socket
import time


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

def info_proceses_bar():
    bar_count = psutil.cpu_percent(interval=1)
    return bar_count
def info_proceses_mem():
    mem = (psutil.virtual_memory())
    percent = mem.percent
    return percent

def info_proceses_time():
    now_time2= datetime.now()
    time_past = now_time2 - data2
    time_past = str(time_past)
    time_past = time_past[0:-5]
    return time_past

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


def info_processor_cpu():
    core = psutil.cpu_count(logical=False)
    return core

def info_processor_cpumax():

    cpufreq = psutil.cpu_freq()
    cpumax = cpufreq.max
    return cpumax

def info_processor_current():
    cpufreq = psutil.cpu_freq()
    cpufre = cpufreq.current
    return cpufre

def info_processor_percent():
    cpuperc = psutil.cpu_percent()
    return cpuperc

def info_processor_freq():
    global cpufreq
    cpufreq = psutil.cpu_freq()
    return cpufreq

def info_processor_cpu_percent():
    cpus = psutil.cpu_percent(percpu=True, interval=1)
    return cpus

def info_processor_name():
    global computer, proc_name
    proc_info = computer.Win32_Processor()[0]
    proc_name = proc_info.Name
    return proc_name

def info_processor_L2():
    global computer, proc_L2Cache
    proc_info = computer.Win32_Processor()[0]
    proc_L2Cache = proc_info.L2CacheSize
    return proc_L2Cache

def info_processor_L3():
    global computer, proc_L3Cache
    proc_info = computer.Win32_Processor()[0]
    proc_L3Cache = proc_info.L3CacheSize
    return proc_L3Cache

def info_memory_total():
    svmem = psutil.virtual_memory()
    return get_size(svmem.total)

def info_memory_available():
    svmem = psutil.virtual_memory()
    return get_size(svmem.available)

def info_memory_used():
    svmem = psutil.virtual_memory()
    return get_size(svmem.used)


def info_memory_percent():
    svmem = psutil.virtual_memory()
    return svmem.percent

def info_swap_total():
    swap = psutil.swap_memory()
    return get_size(swap.total)

def info_swap_free():
    swap = psutil.swap_memory()
    return get_size(swap.free)

def info_swap_used():
    swap = psutil.swap_memory()
    return get_size(swap.used)

def info_swap_percent():
    swap = psutil.swap_memory()
    return get_size(swap.used)




def get_ip_addresses(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == -1:
                mac = snic.address
            if snic.family == 2:
                yield interface, snic.address, snic.netmask, mac


def info_internet_external( ):
    try:
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        return external_ip
    except:
        external_ip = '0.0.0.0'
        return external_ip

def info_internet_internal( ):
    internal_ip = get_Host_name_IP()
    return internal_ip


    ##TODO loop for checking if it is ETHernet or WiFi connection


def info_internet_connection():
    ipv4 = list(get_ip_addresses(socket.AF_INET))
    con = str(ipv4[0][0])
    return con

def info_internet_mask():
    ipv4 = list(get_ip_addresses(socket.AF_INET))
    mask = str(ipv4[0][2])
    return mask

def info_internet_mac():
    ipv4 = list(get_ip_addresses(socket.AF_INET))
    mac = str(ipv4[0][3])
    return mac


def gui():
    print("in Info gui")
    # The tab 1, 2, 3 layouts - what goes inside the tab
    info = [
            [sg.Text('CPU usage %', size=(20, 1)), sg.Text(info_proceses_bar(), size=(3, 1), key='CPU'),
             sg.ProgressBar(max_value=100, orientation='h', border_width=1, size=(12, 5),
                            bar_color=('#199FD0', '#FFFFFF'), key='BAR')],
            [sg.Text('Memory usage %', size=(20, 1)), sg.Text(info_proceses_mem(), size=(3, 1), key='MEM'),
             sg.ProgressBar(max_value=100, orientation='h', border_width=1, size=(12, 5), bar_color=('#199FD0',
                                                                                                     '#FFFFFF'),
                            key='MEM2')],
            [sg.Text('Start Time', size=(20, 1)), sg.Text(data, size=(20, 1), key='START')],
            [sg.Text('Running Time', size=(20, 1)), sg.Text(info_proceses_time(), size=(20, 1), key='RUN')]]

    tab_cpu = [
        [sg.Text('Name ', size=(20, 1)), sg.Text(info_processor_name(), key='CPU_NAME')],
        [sg.Text("Physical cores", size=(20, 1)), sg.Text(info_processor_cpu(), key='CPU_CORES')],
        [sg.Text("Max Frequencys", size=(20, 1)), sg.Text(info_processor_cpumax(), key='CPU_MAX')],
        [sg.Text("Current Frequency", size=(20, 1)), sg.Text(info_processor_current(), key='CPU_FRQ')],
        [sg.Text("Total CPU load", size=(20, 1)), sg.Text(info_processor_freq(), key='CPU_LOAD', size=(6,1)), sg.Text("%")],
        [sg.Text("Each core load", size=(20, 1)), sg.Text(info_processor_cpu_percent(), key='CPU_CLOAD', size=(15,1)), sg.Text("%")],
        [sg.Text("L2 Cache", size=(20, 1)), sg.Text(info_processor_L2(), key='L2Cache')],
        [sg.Text("L3 Cache", size=(20, 1)), sg.Text(info_processor_L3(), key='L3Cache')],
    ]
    tab_gpu = [[sg.Text('GPU')]]

    tab_net = [
        [sg.Text('External IPv4', size=(20, 1)), sg.Text(info_internet_external(), key='EX_IP4')],
        [sg.Text('Internal IPv4', size=(20, 1)), sg.Text(info_internet_internal(), key='IN_IP4')],
        [sg.Text('Connection types', size=(20, 1)), sg.Text(info_internet_connection(), key='IP_Con')],
        [sg.Text('Mask', size=(20, 1)), sg.Text(info_internet_mask(), key='Mask')],
        [sg.Text('MAC', size=(20, 1)), sg.Text(info_internet_mac(), key='MAC')],
    ]

    tab_mem = [
        [sg.Text('Total ', size=(22, 1)), sg.Text(info_memory_total(), key='Total_mem')],
        [sg.Text('Available ', size=(22, 1)), sg.Text(info_memory_available(), key='MEM_ava')],
        [sg.Text('Used ', size=(22, 1)), sg.Text(info_memory_used(), key='MEM_USED')],
        [sg.Text('Percentage ', size=(22, 1)), sg.Text(info_memory_percent(), key='MEM_PER')],
        [sg.Text('Total SWAP Memory', size=(22, 1)), sg.Text(info_swap_total(), key='TOT_SWAP')],
        [sg.Text('Free SWAP Memory', size=(22, 1)), sg.Text(info_swap_free(), key='FREE_SWAP')],
        [sg.Text('Used SWAP Memory', size=(22, 1)), sg.Text(info_swap_used(), key='USED_SWAP')],
        [sg.Text('Percentage  SWAP Memory', size=(22, 1)), sg.Text(info_swap_percent(), key='SWAP_PER')]
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
            a = time.time()
            mem_percent = info_proceses_mem()
            window['MEM2'].update_bar(current_count=mem_percent)

            cpufre = info_processor_current()
            window['CPU_FRQ'].update(cpufre)

            cpuperc = info_processor_percent()
            window['CPU_LOAD'].update(cpuperc)

            cpus = info_processor_cpu_percent()
            window['CPU_CLOAD'].update(cpus)

            bar_count = info_proceses_bar()
            window['BAR'].update_bar(current_count=bar_count)

            window['CPU'].update(bar_count)
            window['MEM'].update(percent)

            time_past = info_proceses_time()
            window['RUN'].update(time_past)

            memory_ava = info_memory_available()
            window['MEM_ava'].update(memory_ava)

            memory_used = info_memory_used()
            window['MEM_USED'].update(memory_used)

            memory_per = info_memory_percent()
            window['MEM_PER'].update(memory_per)

            swap_free = info_swap_free()
            window['FREE_SWAP'].update(swap_free)

            swap_used = info_swap_used()
            window['FREE_SWAP'].update(swap_used)

            swap_perce = info_swap_percent()
            window['FREE_SWAP'].update(swap_perce)
            b = time.time()
            print(b-a)
            event, values = window.read(timeout=500)
            if event in (None, 'Cancel'):
                print('break inner')
                break

        if event in (None, 'Cancel'):
            print('break outer')
            break
    window.close()





if __name__ == '__main__':
    print("main")
    gui()