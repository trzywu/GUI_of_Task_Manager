import PySimpleGUI as sg
from threading import Thread
from time import sleep
import psutil
import datetime
import gpustat

bar_count = 0
active = True
# average system load over the last 1, 5 and 15 minutes
average = psutil.getloadavg()
print(average[0])
#percent of loaded virtual memory
mem = psutil.virtual_memory()
percent = mem.percent
#running time of system
data= datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
data2 = datetime.datetime.fromtimestamp(psutil.boot_time())
now_time = datetime.datetime.now()
time_past = now_time - data2
#


def some_external_process():
    """ put whatever you want here """
    global bar_count, active, mem , percent, time_past
    while True:
        bar_count = psutil.getloadavg()[0]
        mem = psutil.virtual_memory()
        percent = mem.percent
        now_time2 = datetime.datetime.now()
        time_past = now_time2 - data2
        print(bar_count)
        sleep(1)



def splash_gui():
    layout = [
        [sg.Text('CPU usage %', size=(20, 1)), sg.Text(bar_count, size=(20, 1),key='CPU')],
        [sg.ProgressBar(max_value=100, orientation='h', border_width=1, size=(25, 25),
                        bar_color=('#199FD0', '#FFFFFF'), key='BAR')],
        [sg.Text('Memory usage %',size=(20,1)), sg.Text(percent,size=(20,1), key='MEM')],
        [sg.Text('Start Time',size=(20,1)), sg.Text(data,size=(20,1), key='START')] ,
        [sg.Text('Running Time',size=(20,1)), sg.Text(time_past,size=(20,1), key='RUN')],
        [sg.Cancel()]
    ]

    return sg.Window('splash', layout, keep_on_top=True)


def gui_event_loop(window):
    global bar_count, active
    while active:

        window.read(timeout=10)


        window['BAR'].update_bar(current_count=bar_count)
        window['CPU'].update([bar_count])
        window['MEM'].update([percent])
        window['START'].update(data)
        window['RUN'].update(time_past)


    window.close()


def main():
    t1 = Thread(target=some_external_process)
    t1.start()
    window = splash_gui()
    sg.change_look_and_feel('Dark Blue 3')
    gui_event_loop(window)


if __name__ == '__main__':
    main()



