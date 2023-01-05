# imports
import tkinter as tk
import os
import time
from tkinter import *
import sys
from tkinter import ttk
import traceback

# if library is not built in then install it
try:
    import winsound
except:
    os.system('pip install winsound')

try:
    import platform
except:
    os.system('pip install platform')

try:
    import psutil
except:
    os.system('pip install psutil')

try:
    import threading
except:
    os.system('pip install threading')

# Create the main root
root = tk.Tk()
root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')
root.attributes('-fullscreen', True)
root.title('SkyOS')
root.config(cursor='none', bg='black')

# variables
terminal_text = False
install = False
shell = False
touched = False
code = False
edit_src = False
task_display = False
srcv = False
touch_file = False
skyos_label = False
touch_file = False
save_file = False
open_file = False
task_displayed = False
rootdirs = False
homedirs = False
dirname = False
terminalVar = True
rootVar = False
cpu_freq_label = False
cpu_label = False,
cpu_usage = False
cpu_usage_label = False
memory = False
memory_percent = False
memory_used = False
memory_usage_label = False
disk_percent = False
disk_total = False
disk_usage = False
disk_usage_label = False
disk_used = False
shell_label = False
error_label = False
opened = False
saved_file = False
drivename = os.getcwd()[0:2]
paths = ['', 'root', 'home']
PathVar = 2
path = '/'+paths[1]+'/'+paths[2]

# directories
dirs = {
    'C': {
        'skylog': '',
        'root': {
            'home': {}
            }
    }
}

# Calculate the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create the text widget to display the boot messages
boot_text = tk.Text(root, bg='black', fg='white', width=screen_width, height=screen_height, font=('Terminal', 11), cursor='none', selectbackground='black')
boot_text.pack()

# Flag to track whether the OS installation is in progress
installation_in_progress = False

# Function to display the "LOADING..." message
def load_boot():
    global install
    boot_text.insert(1.0, f'LOADING...\n')
    install = True

# Function to display the CPU frequency and count
def display_cpu_info():
    boot_text.insert('end', f'\nCPU FREQUENCY: {psutil.cpu_freq()[0]}')
    boot_text.insert('end', f'\nCPU COUNT: {os.cpu_count()}')

# Function to display the CPU name
def display_cpu_name():
    boot_text.insert('end', f'\nCPU: {platform.processor()}\n')

# Function to display the machine name and prompt the user to install the OS
def display_machine_name_and_prompt_install():
    global root
    boot_text.insert('end', f'\nMACHINE: {platform.machine()}')
    boot_text.insert('end', f'\nDO YOU WANT TO INSTALL SKYOS (Y/N): ')
    root.after(1, prompt_for_install)

# Function to bind key events to install or skip the OS installation
def prompt_for_install():
    global install, root
    if install:
        root.bind('<Key-y>', install_os)
        root.bind('<Key-n>', skip_install)

# Function to start the OS installation process
def install_os(event):
    boot_text.delete('end-1l linestart', 'end')
    boot_text.insert('end', f'\nDO YOU WANT TO INSTALL SKYOS (Y/N):\n')
    global installation_in_progress
    installation_in_progress = True
    update_installation_progress(0)

# Function to skip the OS installation and boot the OS
def skip_install(event):
    global install, root
    if install:
        if event.keysym == 'n':
            root.after(1000, bootupmessages)
            root.after(4000, boot_skyos)
            install = False
# messages on booting
def bootupmessages():
    boot_text.insert('end', '\n\nInitializing processor...\nInitializing memory...')
    boot_text.insert('end', '\n\n\nBOOTING SKYOS...')

# Function to update the installation progress bar
def update_installation_progress(percentage):
    global install, root, installation_in_progress
    if install:
        boot_text.delete('end-1l linestart', 'end')
        boot_text.insert('end', f'\n[{"#" * int(percentage / 2)}{"-" * (50 - int(percentage / 2))}]  {percentage}%')

        if installation_in_progress:
            if percentage < 50:
                root.after(1000, update_installation_progress, percentage + 1)
            else:
                boot_text.delete('end-1l linestart', 'end')
                boot_text.insert('end', '\n[##################################################]  %100')
                root.after(1000, bootupmessages)
                root.after(4000, boot_skyos)
                install = False

# commands for skyos

# print data
def Println(arg):
    global terminal_text
    root.update_idletasks()
    terminal_text.insert(END, f'{arg}')

# change background / foreground color
def change_color(type, color):
    global root, terminal_text, task_display, open_file, touch_file
    root.update_idletasks()
    try:
        if type == 'bg':
            root.config(bg=color)
        elif type == 'fg':
            terminal_text.config(fg=color)
    except:
        pass

# shutdown skyos
def shutdown():
    time.sleep(2)
    sys.exit()

# reboot skyos
def reboot():
    global terminal_text
    terminal_text.insert(END, 'Rebooting...')
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

# print working directory
def pwd():
    global terminal_text, drivename, path
    terminal_text.insert(END, f'{drivename+path}')

# clear terminal
def clear():
    global terminal_text
    try:
        terminal_text.delete(1.0, END)
    except:
        pass

# change directory    
def cd(dir):
    global PathVar, path, rootVar, terminal_text, paths
    if dir == 'home' and PathVar == 1:
        PathVar = 2
        rootVar = False
        path = '/'+paths[1]+'/'+paths[2]
    if dir == 'root' and PathVar == 0:
        rootVar = True
        PathVar = 1
        path = '/'+paths[PathVar]
    if dir == 'home' and PathVar == 0:
        terminal_text.insert(END, 'Directory not found')
    if dir == '..':
        PathVar -= 1
        if PathVar < 0:
            PathVar = 0
        path = '/'+paths[PathVar]
    if PathVar == 1:
        rootVar = True
    if PathVar == 2:
        rootVar = False
    if PathVar == 0:
        rootVar = False

# create virtual file        
def touch(new_dir):
    global touch_file,  save_file, task_display, touched, dirs, touch_file, dirname, opened
    dirname = new_dir
    if rootVar:
        touch_file = Text(root, cursor='xterm', insertbackground='yellow', insertwidth=15, bg='white', fg='blue', height=screen_height-850, width=100, selectbackground='light blue', highlightcolor='red', highlightthickness=3, highlightbackground='red')
        touch_file.pack(side=RIGHT)
        dirs['C']['root'][new_dir] = touch_file.get(1.0, END)
        touched = True
    if PathVar == 2:
        touch_file = Text(root, cursor='xterm', insertbackground='yellow', insertwidth=15, bg='white', fg='blue', height=screen_height-850, width=100, selectbackground='light blue', highlightcolor='red', highlightthickness=3, highlightbackground='red')
        touch_file.pack(side=RIGHT)
        dirs['C']['root']['home'][new_dir] = touch_file.get(1.0, END)
        touched = True
    if PathVar == 0:
        terminal_text.insert(END, 'Cannot create files in system directory')
        touched = False
# open file [file]
def Open(file):
    global dirs, dirname, PathVar, terminal_text, open_file, opened
    if rootVar:
        if file in dirs['C']['root']:
            opened = True
            open_file = Text(root, cursor='xterm', insertbackground='yellow', insertwidth=15, bg='white', fg='blue', height=screen_height-850, width=100, selectbackground='light blue', highlightcolor='red', highlightthickness=3, highlightbackground='red')
            open_file.pack(side=RIGHT) 
            rootdir = dirs['C']['root'][file]
            open_file.insert(END, rootdir)
        else:
            terminal_text.insert(END, 'File not found')
            opened = False
    elif PathVar == 2:
        if file in dirs['C']['root']['home']:
            opened = True
            open_file = Text(root, cursor='xterm', insertbackground='yellow', insertwidth=15, bg='white', fg='blue', height=screen_height-850, width=100, selectbackground='light blue', highlightcolor='red', highlightthickness=3, highlightbackground='red')
            open_file.pack(side=RIGHT)
            homedir = dirs['C']['root']['home'][file]
            open_file.insert(END, homedir)
        else:
            terminal_text.insert(END, 'File not found')
            opened = False
    if PathVar == 0:
        terminal_text.insert(END, 'Cannot open system directory files')
        opened = False
# help command / command list    
def Help():
    global terminal_text
    terminal_text.insert(END, '\nHelp() - command list\ntouch() - create directory [virtual directory name, computer directory name]\nkill() - kill task [task name]\ncd() - change directory [directory name or .. to go to previous directory]\nclear() - clear terminal\npwd() - print working directory\nreboot() - reboot\nshutdown() - shutdown\nchange_color() [type, color]\nPrintln - print arguments [argument]\nsrc() - source code\nSave_src() - save edited source code\nSave() - save files [file]\ntasks_display() - display tasks\nplay_sound() - play sound [frequency, duration]\nrm - remove directory [directory]\ndir - show directories\nskylog_start() - start skylog\n')

# show source code
def src():
    global srcv, terminal_text, edit_src, rootVar
    this_path = os.getcwd()+'\\skyos.pyw'
    if rootVar == False:
        terminal_text.insert(END, 'Source code not found')
        srcv = False
    else:
        srcv = True
        edit_src = Text(root, cursor='xterm', insertbackground='yellow', insertwidth=15, bg='white', fg='blue', height=screen_height-850, width=100, selectbackground='light blue', highlightcolor='red', highlightthickness=3, highlightbackground='red')
        edit_src.pack(side=RIGHT)
        f = open(this_path, 'r')
        edit_src.insert(END, f'\n{f.read()}\n\n')
        f.close()

# save edited source code
def Save_src():
    global rootVar, terminal_text, srcv
    this_path = os.getcwd()+'\\skyos.py'
    if rootVar == False:
        terminal_text.insert(END, 'Source code not found')
        srcv = False
    else:
        f = open(this_path, 'w')
        f.write(edit_src.get(1.0, END))
        f.close() 

# save touched file
def Save():
    global saved_file, touch_file, dirs, terminal_text, PathVar
    saved_file = touch_file.get(1.0, END)
    if rootVar:
        dirs['C']['root'][dirname] = saved_file
    if PathVar == 2:
        dirs['C']['root']['home'][dirname] = saved_file
    if PathVar == 0:
        terminal_text.insert(END, 'Cannot create files in system directory')
# kill task command
def kill(task):
    global edit_src, opened, srcv, touched, terminal_text, terminalVar
    try:
        task.destroy()
        if task == edit_src:
            srcv = False
            root.after(1, task_update)
        if task == touch_file:
            touched = False
            root.after(1, task_update)
        if task == open_file:
            opened = False
            root.after(1, task_update)
    except:
        terminal_text.insert(END, 'Cannot kill task')

# play sound [frequency, duration]
def play_sound(freq, dur):
    winsound.Beep(freq, dur)

# remove file [file]
def rm(dir):
    global rootVar, dirs, terminal_text, PathVar
    try:
        if rootVar:
            dirs['C']['root'].pop(dir)
        if PathVar == 2:
            dirs['C']['root']['home'].pop(dir)
        if PathVar == 0:
            terminal_text.insert(END, 'Cannot remove system directory')
    except:
        terminal_text.insert(END, 'File/Directory not found')

# show directories
def dir():
    global terminal_text, dirs, PathVar
    if rootVar:
        rootdir = f'''
{drivename}/root:
├──src
├──tasks_display
├──touch_file
│
'''
        terminal_text.insert(END, f'{rootdir}\n')
        for i in dirs['C']['root']:
            rootdirs = terminal_text.insert(END, f'├──{i}\n')
        terminal_text.insert(END, '└────────')
    if PathVar == 2:
        homedir = f'''
{drivename}/root/home:
│
'''
        terminal_text.insert(END, f'{homedir}\n')
        for i in dirs['C']['root']['home']:
            homedirs = terminal_text.insert(END, f'├──{i}\n')
        terminal_text.insert(END, '└────────')
    if PathVar == 0:
        cdir = f'''
{drivename}
├──skylog
├──root
└────────
'''
        terminal_text.insert(END, f'{cdir}\n')
# execute commands
def execute_command(cmd):
    global code, terminal_text
    try:
        code = exec(terminal_text.get(1.0, END))
    except Exception as e:
        terminal_text.insert(END, f'{e}')
# tasks display
def tasks_display(event=None):
    global task_display, srcv, touched, dirs, opened, terminalVar, task_displayed
    task_displayed = True
    if task_displayed:
        task_display = Listbox(root, height=screen_height, width=100, fg='blue', bg='white', selectbackground='light blue', highlightbackground='red', highlightcolor='red', highlightthickness=3, cursor='top_left_arrow')
        task_display.pack(side=RIGHT)

        # tasks
        task_display.insert(0, 'edit_src [not running]')
        task_display.insert(1, 'touch_file [not running]')
        task_display.insert(2, 'open_file [not running]')
        task_display.insert(3, 'root [running]')
        task_display.insert(4, 'home [running]')
        task_display.insert(5, 'task_display [running]')
        task_display.insert(6, 'skylog [running]')

        # edit tasks
        if srcv:
            task_display.delete(0)
            task_display.insert(0, 'edit_src [running]')
        if srcv == False:
            task_display.delete(0)
            task_display.insert(0, 'edit_src [not running]')
        if touched:
            task_display.delete(1)
            task_display.insert(1, 'touch_file [running]')
        if touched == False:
            task_display.delete(1)
            task_display.insert(1, 'touch_file [not running]')
        if opened:
            task_display.delete(2)
            task_display.insert(2, 'open_file [running]')
        if opened == False:
            task_display.delete(2)
            task_display.insert(2, 'open_file [not running]')
        root.update()
        root.update_idletasks()

# update task display
def task_update(event=None):
    global task_display, srcv, touched, opened, terminalVar, task_displayed
    root.update()
    root.update_idletasks()
    if task_displayed:
        if srcv == True:
            task_display.delete(0)
            task_display.insert(0, 'edit_src [running]')
        if srcv == False:
            task_display.delete(0)
            task_display.insert(0, 'edit_src [not running]')
        if touched:
            task_display.delete(1)
            task_display.insert(1, 'touch_file [running]')
        if touched == False:
            task_display.delete(1)
            task_display.insert(1, 'touch_file [not running]')
        if opened:
            task_display.delete(2)
            task_display.insert(2, 'open_file [running]')
        if opened == False:
            task_display.delete(2)
            task_display.insert(2, 'open_file [not running]')
    root.after(500, task_update)

# skylog

# skylog labels
def skylog_labels():
    root.update_idletasks()
    global cpu_freq_label, cpu_label, cpu_usage, cpu_usage_label, memory, memory_percent, memory_usage_label, memory_used, disk_percent, disk_total, disk_usage, disk_usage_label, disk_used, shell_label, error_label
    memory = psutil.virtual_memory()
    memory_used = memory.total - memory.available
    memory_percent = memory.percent
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage = psutil.disk_usage('/')
    disk_used = disk_usage.used
    disk_total = disk_usage.total
    disk_percent = disk_usage.percent
    cpu_label = Label(root, bg='blue', fg='white', text=f'CPU count: {os.cpu_count()}', font='System')
    cpu_freq_label = Label(root, bg='blue', fg='white', text=f'CPU frequency: {psutil.cpu_freq()[0]}', font='System')
    memory_usage_label = Label(root, bg='blue', fg='white', text=f'Memory used: {memory_used / 1024**2:.2f} MB ({memory_percent}%)', font='System')
    cpu_usage_label = Label(root, bg='blue', fg='white', text=f'CPU usage: {cpu_usage}%', font='System')
    disk_usage_label = Label(root, bg='blue', fg='white', text=f'Disk usage: {disk_used / 1024**3:.2f} GB / {disk_total / 1024**3:.2f} GB ({disk_percent}%)', font='System')
    shell_label = Label(root, bg='blue', fg='white', text='Shell: True', font='System')
    error_label = Label(root, bg='dark blue', fg='white', text=f'{traceback.print_exc()}', font='System')
    cpu_label.lower()
    cpu_freq_label.lower()
    memory_usage_label.lower()
    cpu_usage_label.lower()
    disk_usage_label.lower()
    shell_label.lower()
    error_label.lower()
    error_label.place(x=200, y=380)
    shell_label.place(x=200, y=320)
    disk_usage_label.place(x=200, y=290)
    cpu_usage_label.place(x=200, y=260)
    memory_usage_label.place(x=200, y=230)
    cpu_freq_label.place(x=200, y=200)
    cpu_label.place(x=200, y=170)

def update_skylog():
    global cpu_freq_label, cpu_label, cpu_usage, cpu_usage_label, memory, memory_percent, memory_usage_label, memory_used, disk_percent, disk_total, disk_usage, disk_usage_label, disk_used, shell_label, error_label
    while True:
        root.update()
        memory = psutil.virtual_memory()
        memory_used = memory_used = memory.total - memory.available
        memory_percent = memory.percent
        cpu_usage = psutil.cpu_percent(interval=1)
        disk_usage = psutil.disk_usage('/')
        disk_used = disk_usage.used
        disk_total = disk_usage.total
        disk_percent = disk_usage.percent
        cpu_label.lower()
        cpu_freq_label.lower()
        memory_usage_label.lower()
        cpu_usage_label.lower()
        disk_usage_label.lower()
        shell_label.lower()
        error_label.lower()
        cpu_label.config(text=f'CPU count: {os.cpu_count()}')
        cpu_freq_label.config(text=f'CPU frequency: {psutil.cpu_freq()[0]}')
        memory_usage_label.config(text=f'Memory used: {memory_used / 1024**2:.2f} MB ({memory_percent}%)')
        cpu_usage_label.config(text=f'CPU usage: {cpu_usage}%')
        disk_usage_label.config(text=f'Disk usage: {disk_used / 1024**3:.2f} GB / {disk_total / 1024**3:.2f} GB ({disk_percent}%)')
        error_label.config(text=f'{traceback.print_exc()}')
def skylog_start():
    t = threading.Thread(target=update_skylog)
    t.start()
def skylog():
    root.after(600, skylog_labels)
# Show or hide terminal and task display
def show_skylog(event=None):
    root.update_idletasks()
    global terminal_text, task_display, task_displayed
    if terminalVar:
        # Terminal is being displayed, bind Control-h to toggle display
        root.bind('<Control-h>', toggle_terminal_and_task_display)
    else:
        # Terminal is not being displayed, unbind Control-h
        root.unbind('<Control-h>')
# Toggle display of terminal and task display
def toggle_terminal_and_task_display(event=None):
    global terminal_text, task_display, task_displayed, open_file, touch_file, edit_src
    if task_displayed:
        # Terminal and task display are being displayed, hide them
        terminal_text.pack_forget()
        try:
            task_display.pack_forget()
        except:
            terminal_text.pack_forget()
        try:
            open_file.pack_forget()
            touch_file.pack_forget()
            edit_src.pack_forget()
        except:
            terminal_text.pack_forget()
        task_displayed = False
    else:
        # Terminal and task display are not being displayed, show them
        terminal_text.pack(side=LEFT)
        task_display.pack(side=RIGHT)
        task_displayed = True
        
# return keyboard combination
def return_combination(event=None):
    global task_displayed
    root.update()
    if terminalVar == False:
        root.bind('<Control-m>', terminal)
        root.bind('<Control-m>', tasks_display)
        task_displayed = False
    if terminalVar:
        root.unbind('<Control-m>')
    root.after(1, return_combination)

# main terminal
def terminal(event=None):
    global terminal_text, shell, root, terminalVar
    terminalVar = True
    terminal_text = Text(root, cursor='xterm', insertbackground='yellow', insertwidth=15, bg='white', fg='blue', height=screen_height-850, width=100, selectbackground='light blue', highlightcolor='red', highlightthickness=3, highlightbackground='red')
    terminal_text.pack(side=LEFT)
    shell = True
    if shell:
        root.bind('<Return>', execute_command)

# skyos loading progressbar
def load_skyos():
    global root, label, progress_bar
    # Increment the value of the progress bar by 10
    bg = '#52f7f7'
    root.config(bg=bg)
    label.config(bg=bg)
    for i in range(10):
        progress_bar["value"] += 10
        root.update_idletasks()
        time.sleep(1)
        if progress_bar['value'] == 100:
            root.after(1000, start_skyos)

# opening tranistion
def transition2():
    global root
    bg = '#010169'
    root.config(bg=bg)
    root.update()
    time.sleep(0.1)
    bg = '#020296'
    root.config(bg=bg)
    root.update()
    time.sleep(0.1)
    bg = '#0404c7'
    root.config(bg=bg)
    root.update()
    time.sleep(0.1)
    root.config(bg='blue')
    root.update()
    time.sleep(1)
    root.config(cursor='top_left_arrow')
    root.update()

# starting skyos
def start_skyos():
    global skyos_label, label, root, progress_bar
    root.after(1, transition2)
    skyos_label = Label(root, bg='light blue', fg='white', text='SkyOS', width=20)
    label.destroy()
    progress_bar.destroy()
    root.config(bg='blue')
    skyos_label.pack(side=TOP)
    root.after(600, show_skylog)
    root.after(600, skylog)
    root.after(600, return_combination)
    root.after(1, terminal)
    root.after(500, tasks_display)
    root.after(500, task_update)

# loading transition
def transition():
  global root, label
  bg = '#035454'
  root.config(bg=bg)
  label.config(bg=bg)
  root.update()
  time.sleep(0.1)
  bg = '#27a3a3'
  root.config(bg=bg)
  label.config(bg=bg)
  root.update()
  time.sleep(0.1)
  bg = '#52f7f7'
  root.config(bg=bg)
  label.config(bg=bg)
  root.update()

# Function to boot the SkyOS
def boot_skyos():
    global root, boot_text, label, progress_bar
    root.after(1, transition)
    root.config(bg='#52f7f7')
    boot_text.destroy()
    root.config(bg='#52f7f7')
    label = tk.Label(root, bg='#52f7f7', fg='black', font=('Small Fonts', 80), text='SkyOS')
    label.place(x=690, y=240)
    progress_bar.place(x=690, y=350)
    root.after(100, load_skyos)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
# start functions
root.after(2000, load_boot)
root.after(4000, display_cpu_info)
root.after(6000, display_cpu_name)
root.after(8000, display_machine_name_and_prompt_install)
root.after(500, task_update)
root.update()
root.update_idletasks()

# start the mainloop
root.mainloop()
