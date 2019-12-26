import PySimpleGUI as sg
from threading import Thread
import psutil
from datetime import datetime

bar_count = 0
active = True
#percent of loaded virtual memory
mem = psutil.virtual_memory()
percent = mem.percent
#running time of system
data= datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
data2 = datetime.fromtimestamp(psutil.boot_time())
now_time = datetime.now()
time_past = now_time - data2



def some_external_process():
    global bar_count, active, mem , percent, time_past

    bar_count = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    percent = mem.percent
    now_time2 = datetime.now()
    time_past = now_time2 - data2




def gui():
    sg.change_look_and_feel('Dark')
    layout = [
        [sg.Text('CPU usage %', size=(20, 1)), sg.Text(bar_count, size=(20, 1),key='CPU'),
        sg.ProgressBar(max_value=100, orientation='h', border_width=1, size=(5, 5),
                        bar_color=('#199FD0', '#FFFFFF'), key='BAR')],
        [sg.Text('Memory usage %',size=(20,1)), sg.Text(percent,size=(20,1), key='MEM'), sg.ProgressBar(max_value=100,
                orientation='h', border_width=1, size=(5, 5), bar_color=('#199FD0', '#FFFFFF'), key='MEM2')],
        [sg.Text('Start Time',size=(20,1)), sg.Text(data,size=(20,1), key='START')] ,
        [sg.Text('Running Time',size=(20,1)), sg.Text(time_past,size=(20,1), key='RUN')],
        [sg.Cancel()]
    ]
    window = sg.Window('Widget', layout, no_titlebar=False, element_justification='center',
         size=(500, 150), margins=(0, 0), alpha_channel=1, grab_anywhere=True, keep_on_top=True, finalize=True)
    while True:
        global active
        event, values = window.Read(timeout=50)

        while active:
            some_external_process()
            window['BAR'].update_bar(current_count=bar_count)
            window['MEM2'].update_bar(current_count=percent)
            window['CPU'].update([bar_count])
            window['MEM'].update([percent])
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
    t1 = Thread(target=some_external_process, daemon=True)
    t1.start()
    window = gui()


if __name__ == '__main__':
    main()
