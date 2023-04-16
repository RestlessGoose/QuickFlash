import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import sys
import time
from tkinter import filedialog

version = "0.2.3"
identifier = "Alpha"

def quit():
    a == "exit"
    event.set(True)

def resetonpopup():
    a == "reset"
    event.set(True)

def loadstart():
    progress_bar.start()
def loadstop():
    progress_bar.stop()

def alert(sound):
    if sys.platform == 'win32':
        import winsound
        # Play system default sound
        winsound.PlaySound("*", winsound.SND_ALIAS)
    elif sys.platform == 'darwin':
        # os.system("afplay /System/Library/Sounds/Purr.aiff")
        subprocess.Popen(["afplay", "/System/Library/Sounds/" + sound + ".aiff"])
    else:
        # os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")
        subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])

def disablemainbuttons():
    autoflash_button.configure(state="disabled")
    read_save_button.configure(state="disabled")
    erase_button.configure(state="disabled")
    exit_button.configure(state="disabled")
    clear_button.configure(state="disabled")

def enablemainbuttons():
    autoflash_button.configure(state="normal")
    read_save_button.configure(state="normal")
    erase_button.configure(state="normal")
    exit_button.configure(state="normal")
    clear_button.configure(state="normal")


def flashrom_exists():
    output = subprocess.Popen(["flashrom", "-R"], stdout=subprocess.PIPE)
    line = output.stdout.readlines()
    for l in line:
        l = l.decode("utf-8").strip()
        if "flashrom v" in l:
            aversion = l.split("\n")[-1]
            break
    terminalappend(arg1=("DISCLAIMER: I am not responsible for bricked devices, data loss, dead chips, thermonuclear war, or the current economic crisis caused by you using this piece of software. Please use with caution while keeping in mind that this is alpha stage software and is not guaranteed to have 100% stability. And also as of right now, it's been tested only on MacOS.\n\n"))
    terminalappend(arg1=("  [QUICKFLASH v" + version + "] Flashrom detected successfully.\n    " + aversion + "\n"))

def check_flashrom():
    try:
        subprocess.check_output(['which', 'flashrom'])
        flashrom_exists()
    except subprocess.CalledProcessError:
        # flashrom is not installed
        terminalappend(arg1=("E:[QUICKFLASH v" + str(version) + "] Flashrom not detected!\n"))
        alert(sound="Sosumi")
        error1Window = tk.Toplevel(root)
        error1Window.title("Fatal Error - QuickFlash")
        ewidth = 400
        eheight = 80
        escreen_width = root.winfo_screenwidth()
        escreen_height = root.winfo_screenheight()
        ex = round((escreen_width/2) - (ewidth/2))
        ey = round((escreen_height/2) - (eheight/2))
        error1Window.geometry(str(ewidth) + "x" + str(eheight) + "+" + str(ex) + "+" + str(ey))
        error1Window.resizable(False, False)
        error1Window.protocol("WM_DELETE_WINDOW", lambda: None)
        errorlabel = tk.Label(error1Window, text="Flashrom is not installed on your system.\nPlease read the ReadMe for troubleshooting issues.", anchor='center')
        errorlabel.pack()
        global event
        event = tk.BooleanVar(value=False)
        global a
        a = "exit"
        errorbutton = tk.Button(error1Window, text="Exit", command=lambda:quit())
        errorbutton.pack(side='right')
        root.wait_variable(event)
        root.destroy()
    #try:
    #    subprocess.run(["flashrom", "-R"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    #    # flashrom is installed
        
    #except subprocess.CalledProcessError:
        

def terminalwipe():
    terminal_output.config(state="normal")
    terminal_output.delete(1.0, tk.END)
    terminal_output.config(state="disabled")
    init_button.config(state="normal")
    disablemainbuttons()
    alert(sound="Frog")

global terminalappend
def terminalappend(arg1):
    terminal_output.config(state="normal")
    terminal_output.insert('end', arg1)
    terminal_output.see('end')
    terminal_output.config(state="disabled")
    
def initok():
    popupWindow.destroy()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Initialization complete!\n    Selected chip model: " + selected_option.get()))
    enablemainbuttons()
    init_button.config(state="disabled")
    alert(sound="Purr")

def init():
    loadstart()
    disablemainbuttons()
    init_button.config(state="disabled")
    check_flashrom()
    terminalappend(arg1=("  [QUICKFLASH v" + str(version) + "] Starting utility initialization\n"))
    command = "flashrom --programmer ch341a_spi | grep Found"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        terminalappend(arg1=line)
        root.update_idletasks()
    output, error = process.communicate()
    output_text = terminal_output.get("1.0", "end-1c") 
    lines = output_text.split("\n") 
    results_list = [] 
    for line in lines:
        start_index = line.find('"')
        end_index = line.find('"', start_index + 1) 
        if start_index != -1 and end_index != -1: 
            result = line[start_index + 1:end_index] 
            results_list.append(result)
    terminalappend(arg1=("\n    Chip model(s) found: " + str(results_list)))
    loadstop()
    if len(results_list) == 0:
        alert(sound="Sosumi")
        error2Window = tk.Toplevel(root)
        error2Window.title("Fatal Error - QuickFlash")
        ewidth = 400
        eheight = 83
        escreen_width = root.winfo_screenwidth()
        escreen_height = root.winfo_screenheight()
        ex = round((escreen_width/2) - (ewidth/2))
        ey = round((escreen_height/2) - (eheight/2))
        error2Window.geometry(str(ewidth) + "x" + str(eheight) + "+" + str(ex) + "+" + str(ey))
        error2Window.resizable(False, False)
        error2Window.protocol("WM_DELETE_WINDOW", lambda: None)
        errorlabel = tk.Label(error2Window, text="Flashrom did not find any chips.\nCH341A programmer is not plugged in or working properly.\nMake sure you have installed drivers correctly.", anchor='center')
        errorlabel.pack()
        global event
        event = tk.BooleanVar(value=False)
        global a
        a = "reset"
        errorbutton = tk.Button(error2Window, text="Close", command=lambda:quit())
        errorbutton.pack(side='right')
        #eresetbutton = tk.Button(error2Window, text="Reset", command=lambda:resetonpopup())
        #eresetbutton.pack(side='right')
        root.wait_variable(event)
        #if a == "reset":
        #    error2Window.destroy()
        #elif a == "exit":
        error2Window.destroy()
        terminalwipe()
    else:
        global popupWindow
        popupWindow = tk.Toplevel(root)
        popupWindow.title("Specify chip model - QuickFlash")
        pwidth = 400
        pheight = 80
        pscreen_width = root.winfo_screenwidth()
        pscreen_height = root.winfo_screenheight()
        px = round((pscreen_width/2) - (pwidth/2))
        py = round((pscreen_height/2) - (pheight/2))
        popupWindow.geometry(str(pwidth) + "x" + str(pheight) + "+" + str(px) + "+" + str(py))
        popupWindow.protocol("WM_DELETE_WINDOW", lambda: None)
        popupWindow.resizable(False, False)
        global selected_option
        selected_option = tk.StringVar(popupWindow)
        selected_option.set(results_list[0])
        popupdropdown = tk.OptionMenu(popupWindow, selected_option, *results_list)
        popupdropdown.pack(pady=(8, 0))
        popupok = tk.Button(popupWindow, text="Close", width=10, command=initok)
        popupok.pack(side='right', padx=6, pady=(0,2))

def autoflash():
    disablemainbuttons()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Autoflash! Please specify your target file to flash.\n"))
    time.sleep(0.2)
    filepath = filedialog.askopenfilename()
    terminalappend(arg1=("\n    File path: " + filepath + "\n"))
    terminalappend(arg1=("\n                Please wait as flashrom wipes chip and flashes target file onto chip...\n\n"))
    loadstart()
    command = "flashrom --programmer ch341a_spi -c " + selected_option.get() + " -w " + str(filepath)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        terminalappend(arg1=line)
        root.update_idletasks()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Autoflash complete."))
    loadstop()
    alert(sound="Funk")
    enablemainbuttons()

def readsave():
    disablemainbuttons()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Read & Save! Please specify savefile."))
    global save_path
    save_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("All files", "*.*")])
    terminalappend(arg1=("\n    Specified savefile path: " + save_path))
    terminalappend(arg1=("\n\n                          Please wait as flashrom dumps chip contents to file...\n\n"))
    loadstart()
    command = "flashrom --programmer ch341a_spi -c " + selected_option.get() + " -r " + str(save_path)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        terminalappend(arg1=line)
        root.update_idletasks()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Read & Save complete."))
    loadstop()
    alert(sound="Funk")
    enablemainbuttons()

def erase():
    disablemainbuttons()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Erase & Blank check!\n\n                                   Please wait as flashrom erases chip...\n\n"))
    loadstart()
    command = "flashrom --programmer ch341a_spi -c " + selected_option.get() + " -E"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        terminalappend(arg1=line)
        root.update_idletasks()
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Erase complete."))
    loadstop()
    alert(sound="Funk")
    enablemainbuttons()
    

root = tk.Tk()
root.title("QuickFlash " + identifier)
width = 900
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = round((screen_width/2) - (width/2))
y = round((screen_height/2) - (height/2))
root.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))
root.resizable(False, False)

top_frame = tk.Frame(root, height=100)
top_frame.pack(fill="x")

button_frame = tk.Frame(root, height=1)
button_frame.pack(side='bottom', anchor='center')

bottom_frame = tk.Frame(root, height=410)
bottom_frame.pack(fill="both", expand=True)

header = tk.Label(top_frame, text="QuickFlash " + identifier + " v" + version + " - CH341A_SPI", font=("Arial", 16))
header.pack(fill='x', anchor="center")

init_button = tk.Button(button_frame, text="Initialize", command=lambda: init())
init_button.pack(side="left", padx=0, pady=(0, 8))

autoflash_button = tk.Button(button_frame, text="Autoflash", command=lambda: autoflash(), state="disabled")
autoflash_button.pack(side="left", padx=0, pady=(0, 8))

read_save_button = tk.Button(button_frame, text="Read & Save", command=lambda: readsave(), state="disabled")
read_save_button.pack(side="left", padx=0, pady=(0, 8))

erase_button = tk.Button(button_frame, text="Erase & Blank check", command=lambda: erase(), state="disabled")
erase_button.pack(side="left", padx=0, pady=(0, 8))

clear_button = tk.Button(button_frame, text="Reset", command=lambda: terminalwipe(), state="disabled")
clear_button.pack(side="left", padx=0, pady=(0, 8))

exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)
exit_button.pack(side="left", padx=0, pady=(0, 8))

terminal_header = tk.Label(bottom_frame, text="↓ Terminal output ↓")
terminal_header.pack(anchor='center', pady=2)
global terminal_output
terminal_output = tk.Text(bottom_frame, font=("Courier New", 14))
terminal_output.pack(fill="both", expand=True)
terminal_output.config(state="disabled")
progress_bar = ttk.Progressbar(root, mode='indeterminate')
#progress_bar.pack(fill="x")

root.mainloop()
