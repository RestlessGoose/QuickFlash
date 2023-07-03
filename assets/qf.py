import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import asksaveasfilename
import platform
import sys
import tkinter.messagebox as mbox
from PIL import ImageTk, Image
import os
import subprocess
import datetime
import atexit
import shutil
import threading
import math
import webbrowser
import re

def exit_handler():
    print("Exiting QuickFlash...\nDeleting any temporary files...")
    os.system("find /tmp/ -type d -name 'qf-*' -exec rm -r {} +")
    subprocess.call(['rm', '/tmp/homebrew_install.sh'])
    print("done")

atexit.register(exit_handler)

file_length = 0
global length
length = 320
global start_offset
start_offset = 0x0
global file_path
file_path = ''

version = "0.4.2"
identifier = "Beta"

def alert(sound):
    if mBool.get()==False:
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

def hexjump():
    if file_path=='':
        alert("Hero")
        mbox.showwarning("Warning", "No file opened on the hex viewer yet.")
    else:
        hexjump_window()
        
def hexjump_window():
    def cancel():
        window.destroy()
    def ok():
        def floor_to_nearest_16(number):
            return math.floor(number / 16) * 16
        if mode_var.get()=="Decimal":
            pattern = textbox.get()
            if pattern.isdigit():
                update_start_offset(floor_to_nearest_16(int(textbox.get())))
                window.destroy()
            else:
                alert("Sosumi")
        elif mode_var.get()=="Hexadecimal":
            pattern = re.compile(r'^[0-9A-Fa-f]+$')
            if pattern.match(textbox.get()):
                update_start_offset(floor_to_nearest_16(int(textbox.get(), 16)))
                window.destroy()
            else:
                alert("Sosumi")
    global window
    window = tk.Toplevel()
    window.title("Offset")
    wwidth = 400
    wheight = 102
    wscreen_width = root.winfo_screenwidth()
    wscreen_height = root.winfo_screenheight()
    wx = round((wscreen_width/2) - (wwidth/2))
    wy = round((wscreen_height/2) - (wheight/2))
    window.geometry(str(wwidth) + "x" + str(wheight) + "+" + str(wx) + "+" + str(wy))
    window.protocol("WM_DELETE_WINDOW", lambda: None)
    window.resizable(False, False)
    mode_var = tk.StringVar()
    mode_var.set("Hexadecimal")
    decimal_radio = tk.Radiobutton(window, text="Decimal", variable=mode_var, value="Decimal")
    hex_radio = tk.Radiobutton(window, text="Hexadecimal", variable=mode_var, value="Hexadecimal")
    textbox = tk.Entry(window)
    ok_button = ttk.Button(window, text="OK", command=ok)
    cancel_button = ttk.Button(window, text="Cancel", command=cancel)
    decimal_radio.grid(row=0, column=0, sticky="w", padx=(110,0), pady=(7,0))
    hex_radio.grid(row=0, column=1, sticky="w", pady=(7,0), padx=(14,0))
    textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=(2,0), sticky="we")
    ok_button.grid(row=2, column=1, padx=(10,13), pady=(2,10), sticky="e")
    cancel_button.grid(row=2, column=1, padx=(0,118), pady=(2,10), sticky="e")
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.grab_set()
    window.focus_set()
    window.wait_window()


def enable_main_buttons():
    button_erase.config(state="normal", style="Style2.TButton")
    button_flash.config(state="normal", style="Style2.TButton")
    button_read.config(state="normal", style="Style2.TButton")
    button_initialize.config(state="normal", style="Style2.TButton")
    button_verify.config(state="normal", style="Style2.TButton")
    autoverify.configure(state="normal")
    verbose.configure(state="normal")

def disable_main_buttons():
    button_erase.config(state="disabled", style="Custom.TButton")
    button_flash.config(state="disabled", style="Custom.TButton")
    button_read.config(state="disabled", style="Custom.TButton")
    button_initialize.config(state="disabled", style="Custom.TButton")
    button_verify.config(state="disabled", style="Custom.TButton")
    autoverify.configure(state="disabled")
    verbose.configure(state="disabled")

def read_hex_data(file_path, start_offset, length):
    with open(file_path, 'rb') as file:
        file.seek(start_offset)
        formatted_data = ''
        offset = start_offset
        while length > 0:
            chunk_data = file.read(16)
            if not chunk_data:
                break
            hex_data = ' '.join(format(byte, '02X') for byte in chunk_data)
            ascii_data = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk_data)
            formatted_line = f"0x{offset:08X}  {hex_data}{' ' * (3 * (16 - len(chunk_data)))}     {ascii_data}\n"
            formatted_data += formatted_line
            length -= len(chunk_data)
            offset += len(chunk_data)
    return "            ⁰⁰ ⁰¹ ⁰² ⁰³ ⁰⁴ ⁰⁵ ⁰⁶ ⁰⁷ ⁰⁸ ⁰⁹ ⁰ᴬ ⁰ᴮ ⁰ᶜ ⁰ᴰ ⁰ᴱ ⁰ᶠ     ⁰¹²³⁴⁵⁶⁷⁸⁹ᴬᴮᶜᴰᴱᶠ\n" + formatted_data[:-1]

global update_start_offset
def update_start_offset(new_offset):
    text.configure(state="normal")
    global start_offset
    start_offset = new_offset
    length = 304
    text.delete('1.0', tk.END)
    hex_data = read_hex_data(file_path, start_offset, length)
    text.insert('1.0', hex_data)
    text.configure(state="disabled")
    slider.set(start_offset)

def slider_update_start_offset(arg1):
    text.configure(state="normal")
    global start_offset
    sliderval = math.floor(float(slider.get()))
    rounded_sliderval = (sliderval + 8) // 16 * 16
    start_offset = rounded_sliderval
    length = 304
    text.delete('1.0', tk.END)
    hex_data = read_hex_data(file_path, start_offset, length)
    text.insert('1.0', hex_data)
    text.configure(state="disabled")

def decrease_offset():
    update_start_offset(max(start_offset - 16, 0))

def increase_offset():
    update_start_offset(start_offset + 16)

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    text.config(state="normal")
    text.delete('1.0', tk.END)
    if file_path:
        # Read the file length
        with open(file_path, 'rb') as file:
            file.seek(0, 2)
            global file_length
            file_length = file.tell()
        increase_button.configure(state="normal")
        decrease_button.configure(state="normal")
        slider.configure(state="normal")
        slider.configure(to=(file_length - 16))
        start_offset = 0x0
        length = 304
        hex_data = read_hex_data(file_path, start_offset, length)
        text.insert('1.0', hex_data)
        root.title("QuickFlash " + identifier + " - " + file_path)
    else:
        increase_button.config(state="disabled")
        decrease_button.configure(state="disabled")
        slider.configure(state="disabled")
    text.config(state="disabled")

def save_file():
    content = text.get("1.0", "end-1c")
    if not content:
        alert("Hero")
        mbox.showwarning("Warning", "No file is opened that you can save.")
    else:
        save_file = asksaveasfilename()
        if save_file:
            shutil.copy(file_path, save_file)
            root.title("QuickFlash " + identifier + " - " + save_file)

def select_option(arg1):
    opt.set(arg1)
    global selected_option
    selected_option = arg1
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Initialization complete!\n    Selected chip model: " + arg1), arg2="tag2")
    alert("Blow")
    popupdropdown["menu"].delete(0, "end")
    enable_main_buttons()
    label.configure(text="Status: READY")
    button_initialize.configure(state="normal", style="Style2.TButton")

def flashrom_exists2():       
    command = "/opt/local/bin/flashrom --programmer ch341a_spi | grep Found"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        terminalappend(arg1=line, arg2="tag1")
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
    terminalappend(arg1=("\n  !!Please choose chip model on the bottom-left corner!!\n    Chip model(s) found: " + str(results_list)) + "\n", arg2="tag2")
    if len(results_list) == 0:
        alert("Hero")
        mbox.showwarning("Fatal error", "Flashrom did not find any chips.\nCH341A programmer is not plugged in or working properly.")
        button_initialize.configure(state="normal", style="Style2.TButton")
    else:
        alert("Tink")
        popupdropdown["menu"].delete(0)
        for line in results_list:
            popupdropdown["menu"].add_command(label=str(line), command=lambda: select_option(arg1=(line)))
        opt.set(str(results_list[0]))
        
def flashrom_exists():
    terminalwipe()
    terminalappend(arg1=('MacOS Version: ' + mac_version + "\n"), arg2="tag2")
    command = ["/opt/local/bin/flashrom", "--version"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    def read_output():
        while True:
            output = process.stdout.readline()
            if not output:
                break
            terminal_output.configure(state="normal")
            terminal_output.insert(tk.END, output)
            terminal_output.see(tk.END)
            terminal_output.configure(state="disabled")
        flashrom_exists2()
    output_thread = threading.Thread(target=read_output)
    output_thread.start() 
    
def initialize():
    label.config(text="Status: INITIALIZING")
    button_initialize.configure(state="disabled", style="Custom.TButton")
    try:
        subprocess.check_output(['which', '/opt/local/bin/flashrom'])
        flashrom_exists()
    except subprocess.CalledProcessError:
        # flashrom is not installed
        alert("Hero")
        mbox.showwarning("Fatal error", "Flashrom is not installed.\nCheck the Readme for troubleshooting.")
        root.destroy()
    
def flash():
    content = text.get("1.0", "end-1c")
    if not content:
        alert("Hero")
        mbox.showwarning("Warning", "No file is opened that you can flash.")
    else:
        disable_main_buttons()
        label.configure(text="Status: BUSY")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting flash procedure.\n"), arg2="tag2")
        if avfBool.get()==True and vBool.get()==True:
            command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path), "--noverify", "--verbose"]
        elif avfBool.get()==False and vBool.get()==True:
            command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path), "--verbose"]
        elif avfBool.get()==True and vBool.get()==False:
            command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path), "--noverify"]
        elif avfBool.get()==False and vBool.get()==False:
            command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path)]            
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        def read_output():
            while True:
                output = process.stdout.readline()
                if not output:
                    break
                terminal_output.configure(state="normal")
                terminal_output.insert(tk.END, output)
                terminal_output.see(tk.END)
                terminal_output.configure(state="disabled")
            enable_main_buttons()
            label.configure(text="Status: READY")
            terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Flash complete.\n"), arg2="tag2")
            alert("Blow")
        output_thread = threading.Thread(target=read_output)
        output_thread.start()

def read():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    global file_path
    file_path = "/tmp/qf-" + formatted_datetime + "/" + formatted_datetime + ".rom"
    os.system("mkdir " + "/tmp/qf-" + formatted_datetime)
    os.system("touch " + file_path)
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting read procedure.\n"), arg2="tag2")
    disable_main_buttons()
    label.configure(text="Status: BUSY")
    left_frame.update_idletasks()
    if vBool.get()==True:
        command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "-r", str(file_path), "--verbose"]
    elif vBool.get()==False:
        command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "-r", str(file_path)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    def read_output():
        while True:
            output = process.stdout.readline()
            if not output:
                break
            terminal_output.configure(state="normal")
            terminal_output.insert(tk.END, output)
            terminal_output.see(tk.END)
            terminal_output.configure(state="disabled")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Read complete.\n"), arg2="tag2")
        alert("Blow")
        text.config(state="normal")
        text.delete('1.0', tk.END)
        # Read the file length
        with open(file_path, 'rb') as file:
            file.seek(0, 2)
            global file_length
            file_length = file.tell()
        increase_button.configure(state="normal")
        decrease_button.configure(state="normal")
        slider.configure(state="normal")
        slider.configure(to=(file_length - 16))
        root.title("QuickFlash " + identifier + " - " + file_path)
        start_offset = 0x0
        length = 320
        hex_data = read_hex_data(file_path, start_offset, length)
        text.insert('1.0', hex_data)
        text.config(state="disabled")
        enable_main_buttons()
        label.configure(text="Status: READY")
    output_thread = threading.Thread(target=read_output)
    output_thread.start()

def erase():
    disable_main_buttons()
    label.configure(text="Status: BUSY")
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting erase procedure.\n"), arg2="tag2")
    if vBool.get()==True:
        command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "--erase", "--verbose"]
    elif vBool.get()==False:
        command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "--erase"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    def read_output():
        while True:
            output = process.stdout.readline()
            if not output:
                break
            terminal_output.configure(state="normal")
            terminal_output.insert(tk.END, output)
            terminal_output.see(tk.END)
            terminal_output.configure(state="disabled")
        enable_main_buttons()
        label.configure(text="Status: READY")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Erase complete.\n"), arg2="tag2")
        alert("Blow")
    output_thread = threading.Thread(target=read_output)
    output_thread.start()

def verify():
    content = text.get("1.0", "end-1c")
    if not content:
        alert("Hero")
        mbox.showwarning("Warning", "No file is opened that you can verify against.")
    else:
        disable_main_buttons()
        label.configure(text="Status: BUSY")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting verify procedure.\n"), arg2="tag2")
        if vBool.get()==True:
            command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "--verify", file_path, "--verbose"]
        elif vBool.get()==False:
            command = ["/opt/local/bin/flashrom", "--programmer", "ch341a_spi", "--chip", selected_option, "--verify", file_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        def read_output():
            while True:
                output = process.stdout.readline()
                if not output:
                    break
                terminal_output.configure(state="normal")
                terminal_output.insert(tk.END, output)
                terminal_output.see(tk.END)
                terminal_output.configure(state="disabled")
            enable_main_buttons()
            label.configure(text="Status: READY")
            terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Verify complete.\n"), arg2="tag2")
            alert("Blow")
        output_thread = threading.Thread(target=read_output)   
        output_thread.start()

def install_driver():
    webbrowser.open('https://github.com/WCHSoftGroup/ch34xser_macos')

def install_flashrom():
    try:
        subprocess.check_output(['which', '/usr/local/bin/brew'])
        try:
            subprocess.check_output(['which', '/opt/local/bin/flashrom'])
            mbox.showinfo("Info", "Homebrew and flashrom are already installed on your Mac.")
        except subprocess.CalledProcessError:
            alert("Hero")
            mbox.showwarning("Warning", "Homebrew is already installed on your Mac, but flashrom is not. QuickFlash will open a Terminal window and install it for you.")
            shell_script = '#!/bin/bash\n/usr/local/bin/brew install flashrom'
            # Save the shell script to a temporary file
            with open('/tmp/homebrew_install.sh', 'w') as file:
                file.write(shell_script)
            # Make the temporary shell script executable
            subprocess.call(['chmod', '+x', '/tmp/homebrew_install.sh'])
            # Open the macOS Terminal app and execute the shell script
            subprocess.call(['open', '-a', 'Terminal', '/tmp/homebrew_install.sh'])

    except subprocess.CalledProcessError:
        alert("Hero")
        mbox.showwarning("Warning", "Homebrew is not installed on your Mac. QuickFlash will open a Terminal window and install it for you, along with flashrom.")
        # Command to execute
        shell_script = '#!/bin/bash\n/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"\n/usr/local/bin/brew install flashrom'
        # Save the shell script to a temporary file
        with open('/tmp/homebrew_install.sh', 'w') as file:
            file.write(shell_script)
        # Make the temporary shell script executable
        subprocess.call(['chmod', '+x', '/tmp/homebrew_install.sh'])
        # Open the macOS Terminal app and execute the shell script
        subprocess.call(['open', '-a', 'Terminal', '/tmp/homebrew_install.sh'])

def hex_jump():
    pass

global textwipe
def textwipe():
    text.config(state="normal")
    text.delete(1.0, tk.END)
    text.config(state="disabled")
    button_initialize.config(state="normal")

global terminalwipe
def terminalwipe():
    terminal_output.config(state="normal")
    terminal_output.delete(1.0, tk.END)
    terminal_output.config(state="disabled")
    button_initialize.config(state="normal")

global terminalappend
def terminalappend(arg1, arg2):
    terminal_output.config(state="normal")
    terminal_output.insert('end', arg1, arg2)
    terminal_output.see('end')
    terminal_output.config(state="disabled")

root = tk.Tk()
root.title("QuickFlash " + identifier)
width = 865
height = 620
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = round((screen_width/2) - (width/2))
y = round((screen_height/2) - (height/2))
root.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))
root.resizable(False, True)
root.minsize(865,600)

if sys.platform == 'darwin':
    #PyQt code just to change dock icon
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon
    app = QApplication([])
    app.setWindowIcon(QIcon('ApplicationStub.icns'))
    global mac_version
    mac_version = platform.mac_ver()[0]
else:
    mbox.showwarning("Warning", "Unsupported platform.")

# Side panel frame
left_frame = tk.Frame(root, bg="systemTransparent")
left_frame.pack(side=tk.LEFT, fill=tk.Y)
header = tk.Label(left_frame, text="QuickFlash " + identifier + " v" + version, font=("TkDefaultFont", 15), background="SystemTransparent")
header.pack(pady=(10,0))
subheader = tk.Label(left_frame, text="CH341A_SPI", background="SystemTransparent")
subheader.pack()
style1 = ttk.Style()
style1.configure("Custom.TButton", background=left_frame['bg'], foreground="black")
style2 = ttk.Style()
style2.configure("Style2.TButton", background=left_frame['bg'])
button_initialize = ttk.Button(left_frame, text="Initialize", command=initialize, width=7)
button_initialize.pack(pady=(10,3), padx=10)
button_flash = ttk.Button(left_frame, text="Flash", command=flash, width=7, state="disabled", style="Custom.TButton")
button_flash.pack(pady=3)
button_read = ttk.Button(left_frame, text="Read", command=read, width=7, state="disabled", style="Custom.TButton")
button_read.pack(pady=3)
button_erase = ttk.Button(left_frame, text="Erase", command=erase, width=7, state="disabled", style="Custom.TButton")
button_erase.pack(pady=3)
button_verify = ttk.Button(left_frame, text="Verify", command=verify, width=7, state="disabled", style="Custom.TButton")
button_verify.pack(pady=3)
button_exit = ttk.Button(left_frame, text="Exit", command=root.quit, width=7)
button_exit.pack(pady=3)
optionslabel = tk.Label(left_frame, text="OPTIONS", background="SystemTransparent", foreground="#7F7F7F", font=("TkDefaultFont", 12, "bold"))
optionslabel.pack(pady=(10,0))
avfBool = tk.BooleanVar()
autoverify = tk.Checkbutton(left_frame, text="Disable flash auto-verify", variable=avfBool, background="SystemTransparent", state="disabled")
autoverify.pack(anchor='w', padx=(8,0))
vBool = tk.BooleanVar()
verbose = tk.Checkbutton(left_frame, text="Enable more verbose", variable=vBool, background="SystemTransparent", state="disabled")
verbose.pack(anchor='w', padx=(8,0))
mBool = tk.BooleanVar()
mute = tk.Checkbutton(left_frame, text="Mute sound effects", variable=mBool, background="SystemTransparent", state="normal")
mute.pack(anchor='w', padx=(8,0))
bottomleft_frame = tk.Frame(left_frame, background="SystemTransparent")
bottomleft_frame.pack(side=tk.BOTTOM, expand=False)
image = Image.open("1.png")
photo = ImageTk.PhotoImage(image)
photo1 = ttk.Label(bottomleft_frame, image=photo, style='Transparent.TLabel')
photo1.pack(padx=48)
photo1.configure()
label = tk.Label(bottomleft_frame, text="Status: READY", background="SystemTransparent")
label.pack()
global opt
results_list=['']
opt = tk.StringVar(bottomleft_frame)
opt.set(str(results_list[0]))
popupdropdown = tk.OptionMenu(bottomleft_frame, opt, *results_list)
popupdropdown.configure(width=10)
popupdropdown.pack(pady=(8, 10), expand=False, fill='x', padx= 10, anchor='s')
popupdropdown["menu"].delete(0)

# Hex viewer frame
outoutmiddle_frame = tk.Frame(root)
outoutmiddle_frame.pack(padx=0, pady=0, fill=tk.BOTH, side=tk.TOP)
hexlabel = tk.Label(outoutmiddle_frame, text="HEX VIEWER", foreground="#7F7F7F", font=("TkDefaultFont", 12, "bold"))
hexlabel.pack()
outmiddle_frame = tk.Frame(outoutmiddle_frame)
outmiddle_frame.pack()
middle_frame = tk.Frame(outmiddle_frame)
middle_frame.grid()
text = tk.Text(middle_frame, height=20, width=80, state="disabled", font="Courier")
text.grid(row=0, column=0, sticky='nsw',rowspan=3, ipadx=1)
style1.configure("Narrow.TButton", width=1)
decrease_button = ttk.Button(middle_frame, text='▲', command=decrease_offset, state="disabled", style="Narrow.TButton")
decrease_button.grid(row=0, column=0, sticky='n',padx=(636,0))
slider = ttk.Scale(middle_frame, from_=0, to=(file_length - 16), orient=tk.VERTICAL, command=slider_update_start_offset, state="disabled")
slider.grid(row=1, column=0, sticky='ns',rowspan=1, ipady=55, padx=(638,0))
increase_button = ttk.Button(middle_frame, text='▼', command=increase_offset, state="disabled", style="Narrow.TButton")
increase_button.grid(row=2, column=0, sticky='s',padx=(636,0))
buttoncover = tk.Frame(middle_frame, width=10)
buttoncover.grid(row=0, column=0, rowspan=3, sticky='ns', padx=(669,0))
text.lift()
slider.set(start_offset)

# Terminal output frame
right_frame = tk.Frame(root)
right_frame.pack(padx=0, pady=0, fill='both', expand=True, side=tk.BOTTOM, anchor='n')
termlabel = tk.Label(right_frame, text="TERMINAL OUTPUT", foreground="#7F7F7F", font=("TkDefaultFont", 12, "bold"))
termlabel.pack()
terminal_output = tk.Text(right_frame, width=80, bg='black', fg='white', state="disabled", font=("Menlo", 11))
terminal_output.pack(fill=tk.BOTH, expand=True)
terminal_output.tag_configure("tag1", foreground="white")
terminal_output.tag_configure("tag2", foreground="#89CFF0")

# Menubar management
menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

tools_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Tools", menu=tools_menu)
tools_menu.add_command(label="Install Driver", command=install_driver)
tools_menu.add_command(label="Install Flashrom", command=install_flashrom)

term_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Terminal", menu=term_menu)
term_menu.add_command(label="Clear contents", command=terminalwipe)

hex_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Hex Viewer", menu=hex_menu)
hex_menu.add_command(label="Jump to offset", command=hexjump)

root.mainloop()
