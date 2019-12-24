import PySimpleGUI as sg
import psutil
import datetime
import gpustat

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

#TODO gpu stats 

sg.change_look_and_feel('Dark Blue 3')
# All the stuff inside window.
layout = [  [sg.Text('CPU usage %',size=(20,1)),sg.Text(average[0],size=(20,1))],
            [sg.Text('Memory usage %',size=(20,1)), sg.Text(percent,size=(20,1))],
            [sg.Text('Start Time',size=(20,1)), sg.Text(data,size=(20,1))] ,
            [sg.Text('Running Time',size=(20,1)), sg.Text(time_past,size=(20,1))],
            [sg.Cancel()]]

# Create the Window
window = sg.Window('Window Title', layout)

while True:
    event, values = window.read(timeout=10)
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        break


window.close()






# progress_bar.UpdateBar(0, 5)
# #adding time.sleep(length in Seconds) has been used to Simulate adding your script in between Bar Updates
# time.sleep(.5)
#
# progress_bar.UpdateBar(1, 5)
# time.sleep(.5)
#
# progress_bar.UpdateBar(2, 5)
# time.sleep(.5)
#
# progress_bar.UpdateBar(3, 5)
# time.sleep(.5)
#
# progress_bar.UpdateBar(4, 5)
# time.sleep(.5)
#
# progress_bar.UpdateBar(5, 5)
# time.sleep(.5)
# #I paused for 3 seconds at the end to give you time to see it has completed before closing the window
# time.sleep(3)
