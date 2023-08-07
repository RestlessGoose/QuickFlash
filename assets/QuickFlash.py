import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import asksaveasfilename
import platform
import sys
import tkinter.messagebox as mbox
import os
import subprocess
import datetime
import atexit
import shutil
import threading
import math
import re
import time
sys.path.append('.')
import usb

def exit_handler():
    print("Exiting QuickFlash...\nDeleting any temporary files...")
    os.system("find /tmp/ -type d -name 'qf-*' -exec rm -r {} +")
    subprocess.call(['rm', '/tmp/homebrew_install.sh'])
    print("done\nStopping threads...")
    global exit_flag
    exit_flag = True
    time.sleep(0.4)
    print("done")

atexit.register(exit_handler)

file_length = 0
global length
length = 304
global start_offset
start_offset = 0x0
global file_path
file_path = ''
global exit_flag
exit_flag = False

version = "0.6.0"
identifier = "Beta"
# Run the shell command and capture its output
command = "whereis flashrom"
fpoutput = subprocess.check_output(command, shell=True, text=True)

# Extract the path from the output
global flashrompath
flashrompath = "./flashrom"

# Print the path
print("Flashrom path:", flashrompath)

def updatelabel(arg):
    label_var.set(arg)

def handle_usb_events():
    while not exit_flag:
        # Wait for a USB event (device connection or disconnection)
        usb.core.find(find_all=True)
        # Find USB device with the specified vendor and product IDs
        device = usb.core.find(idVendor=0x1a86, idProduct=0x5512)
        if device is not None:
            # Device is connected
            usblabel.config(text="Device state: Connected", fg="green")
        else:
            # Device is disconnected
            usblabel.config(text="Device state: Not Connected", fg="red")
        time.sleep(0.1)

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
        root.focus_set()
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
    root.bind_all("<Command-i>",menuinitialize)
    root.bind_all("<Command-f>",menuflash)
    root.bind_all("<Command-r>",menuread)
    root.bind_all("<Command-w>",menuerase)
    root.bind_all("<Command-v>",menuverify)
    file_menu.entryconfig(3, state="normal")
    file_menu.entryconfig(4, state="normal")
    file_menu.entryconfig(5, state="normal")
    file_menu.entryconfig(6, state="normal")
    file_menu.entryconfig(7, state="normal")

def disable_main_buttons():
    button_erase.config(state="disabled", style="Custom.TButton")
    button_flash.config(state="disabled", style="Custom.TButton")
    button_read.config(state="disabled", style="Custom.TButton")
    button_initialize.config(state="disabled", style="Custom.TButton")
    button_verify.config(state="disabled", style="Custom.TButton")
    autoverify.configure(state="disabled")
    verbose.configure(state="disabled")
    root.unbind_all("<Command-i>")
    root.unbind_all("<Command-f>")
    root.unbind_all("<Command-r>")
    root.unbind_all("<Command-w>")
    root.unbind_all("<Command-v>")
    file_menu.entryconfig(3, state="normal")
    file_menu.entryconfig(4, state="disabled")
    file_menu.entryconfig(5, state="disabled")
    file_menu.entryconfig(6, state="disabled")
    file_menu.entryconfig(7, state="disabled")


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
        root.focus_set()
    else:
        save_file = asksaveasfilename()
        if save_file:
            shutil.copy(file_path, save_file)
            root.title("QuickFlash " + identifier + " - " + save_file)

def detect_usb_device(vendor_id, product_id):
    devices = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if devices:
        return True
    else:
        return False

def select_option(arg1):
    opt.set(arg1)
    global selected_option
    selected_option = arg1
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Initialization complete!\n    Selected chip model: " + arg1), arg2="tag2")
    alert("Blow")
    popupdropdown["menu"].delete(0, "end")
    enable_main_buttons()
    updatelabel("Status: READY")
    button_initialize.configure(state="normal", style="Style2.TButton")

def flashrom_exists2():
    is_device_present = detect_usb_device(0x1a86, 0x5512)
    if is_device_present:
        command = flashrompath + " --programmer ch341a_spi | grep Found"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        for line in iter(process.stdout.readline, b''):
            terminalappend(arg1=line, arg2="tag1")
            root.update_idletasks()
        #output, error = process.communicate()
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
            root.focus_set()
            button_initialize.configure(state="normal", style="Style2.TButton")
            label.after(0, updatelabel("Status: READY"))
        else:
            alert("Tink")
            popupdropdown["menu"].delete(0)
            for line in results_list:
                popupdropdown["menu"].add_command(label=str(line), command=lambda: select_option(arg1=(line)))
            opt.set(str(results_list[0]))
    else:
        alert("Hero")
        mbox.showerror("Error", "CH341A programmer is not detected to be plugged in.")
        disable_main_buttons()
        root.focus_set()
        button_initialize.configure(state="normal", style="Style2.TButton")
        label.after(0, updatelabel("Status: READY"))
        
def flashrom_exists():
    terminalwipe()
    terminalappend(arg1=('  MacOS Version: ' + mac_version + "\n"), arg2="tag2")
    command = [flashrompath, "--version"]
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
    if usblabel.cget("text") == "Device state: Not Connected":
        return
    if label.cget("text") == "Status: READY":
        updatelabel("Status: INITIALIZING")
        button_initialize.config(state="disabled", style="Custom.TButton")
        try:
            subprocess.check_output(['which', flashrompath])
            flashrom_exists()
        except subprocess.CalledProcessError:
            # flashrom is not installed
            alert("Hero")
            mbox.showwarning("Fatal error", "Flashrom is not installed.\nCheck the Readme for troubleshooting.")
            root.focus_set()
            root.destroy()
    
def flash():
    if usblabel.cget("text") == "Device state: Not Connected":
        return
    content = text.get("1.0", "end-1c")
    if not content:
        alert("Hero")
        mbox.showwarning("Warning", "No file is opened that you can flash.")
        root.focus_set()
    else:
        disable_main_buttons()
        updatelabel("Status: BUSY")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting flash procedure.\n"), arg2="tag2")
        if avfBool.get()==True and vBool.get()==True:
            command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path), "--noverify", "--verbose"]
        elif avfBool.get()==False and vBool.get()==True:
            command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path), "--verbose"]
        elif avfBool.get()==True and vBool.get()==False:
            command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path), "--noverify"]
        elif avfBool.get()==False and vBool.get()==False:
            command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "-w", str(file_path)]            
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
            updatelabel("Status: READY")
            terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Flash complete.\n"), arg2="tag2")
            alert("Blow")
        output_thread = threading.Thread(target=read_output)
        output_thread.start()

def read():
    if usblabel.cget("text") == "Device state: Not Connected":
        return
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    global file_path
    file_path = "/tmp/qf-" + formatted_datetime + "/" + formatted_datetime + ".rom"
    os.system("mkdir " + "/tmp/qf-" + formatted_datetime)
    os.system("touch " + file_path)
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting read procedure.\n"), arg2="tag2")
    disable_main_buttons()
    updatelabel("Status: BUSY")
    left_frame.update_idletasks()
    if vBool.get()==True:
        command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "-r", str(file_path), "--verbose"]
    elif vBool.get()==False:
        command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "-r", str(file_path)]
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
        length = 304
        hex_data = read_hex_data(file_path, start_offset, length)
        text.insert('1.0', hex_data)
        text.config(state="disabled")
        enable_main_buttons()
        updatelabel("Status: READY")
    output_thread = threading.Thread(target=read_output)
    output_thread.start()

def erase():
    if usblabel.cget("text") == "Device state: Not Connected":
        return
    disable_main_buttons()
    updatelabel("Status: BUSY")
    terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting erase procedure.\n"), arg2="tag2")
    if vBool.get()==True:
        command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "--erase", "--verbose"]
    elif vBool.get()==False:
        command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "--erase"]
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
        updatelabel("Status: READY")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Erase complete.\n"), arg2="tag2")
        alert("Blow")
    output_thread = threading.Thread(target=read_output)
    output_thread.start()

def verify():
    if usblabel.cget("text") == "Device state: Not Connected":
        return
    content = text.get("1.0", "end-1c")
    if not content:
        alert("Hero")
        mbox.showwarning("Warning", "No file is opened that you can verify against.")
        root.focus_set()
    else:
        disable_main_buttons()
        updatelabel("Status: BUSY")
        terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Starting verify procedure.\n"), arg2="tag2")
        if vBool.get()==True:
            command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "--verify", file_path, "--verbose"]
        elif vBool.get()==False:
            command = [flashrompath, "--programmer", "ch341a_spi", "--chip", selected_option, "--verify", file_path]
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
            updatelabel("Status: READY")
            terminalappend(arg1=("\n  [QUICKFLASH v" + str(version) + "] Verify complete.\n"), arg2="tag2")
            alert("Blow")
        output_thread = threading.Thread(target=read_output)   
        output_thread.start()

#def install_driver():
#    webbrowser.open('https://github.com/WCHSoftGroup/ch34xser_macos')

def install_flashrom():
    try:
        subprocess.check_output(['which', '/usr/local/bin/brew'])
        try:
            subprocess.check_output(['which', flashrompath])
            alert("Hero")
            mbox.showinfo("Info", "Homebrew and flashrom are already installed on your Mac.")
            root.focus_set()
        except subprocess.CalledProcessError:
            alert("Hero")
            mbox.showwarning("Warning", "Homebrew is already installed on your Mac, but flashrom is not. QuickFlash will open a Terminal window and install it for you.")
            root.focus_set()
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
        root.focus_set()
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

def save_terminal_text():
    text_content = terminal_output.get("1.0", "end-1c")  # Get the contents of the text widget
    file_path = filedialog.asksaveasfilename(defaultextension=".log")  # Open the file dialog for saving
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_content)
        print("File saved successfully.")

def menuhexjump(arg):
    hexjump()

def menuopenfile(arg):
    open_file()

def menusavefile(arg):
    save_file()

def menusaveterminal(arg):
    save_terminal_text()

def menuinitialize(arg):
    if label.cget("text") == "Status: READY":
        initialize()

global menuflash
def menuflash(arg):
    if label.cget("text") == "Status: READY":
        flash()

global menuread
def menuread(arg):
    if label.cget("text") == "Status: READY":
        read()

global menuerase
def menuerase(arg):
    if label.cget("text") == "Status: READY":
        erase()

global menuverify
def menuverify(arg):
    if label.cget("text") == "Status: READY":
        verify()

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
    try:
        from Cocoa import NSApplication, NSImage
    except ImportError:
        print('Unable to import pyobjc modules')
    else:
        ns_application = NSApplication.sharedApplication()
        logo_ns_image = NSImage.alloc().initByReferencingFile_('ApplicationStub.icns')
        ns_application.setApplicationIconImage_(logo_ns_image)
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
image = tk.PhotoImage(file="1.png")
#photo = ImageTk.PhotoImage(image)
photo1 = ttk.Label(bottomleft_frame, image=image, style='Transparent.TLabel')
photo1.image = image
photo1.pack(padx=48)
label_var = tk.StringVar()
label_var.set("Status: READY")
label = tk.Label(bottomleft_frame, textvariable=label_var, background="SystemTransparent")
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
terminal_output = tk.Text(right_frame, width=80, bg='black', fg='white', state="disabled", font=("Menlo", 11), height=19)
terminal_output.pack(fill=tk.BOTH, expand=True)
terminal_output.tag_configure("tag1", foreground="white")
terminal_output.tag_configure("tag2", foreground="#89CFF0")
bottomright_frame = tk.Frame(right_frame, background="SystemTransparent")
bottomright_frame.pack(padx=0, pady=0, fill='x', expand=False, side=tk.BOTTOM, anchor='s')
border = tk.Canvas(bottomright_frame, width=1, height=20, bg="#7F7F7F")
border.pack(side=tk.LEFT)
#global infolabel
#infolabel = tk.Label(bottomright_frame, font=("TkDefaultFont", 12, "bold"), text="", background="SystemTransparent")
global usblabel
usblabel = tk.Label(bottomright_frame, font=("TkDefaultFont", 12, "bold"), text="Device status daemon not started. Is the libusb backend installed?", background="SystemTransparent", foreground='red')
usblabel.pack(anchor='e', pady=(0,4), padx=4)
usb_thread = threading.Thread(target=handle_usb_events)
usb_thread.daemon = True
usb_thread.start()

# Menubar management
menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file, accelerator="Command+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Command+S")
file_menu.add_separator()
entryinitialize = file_menu.add_command(label="Initialize", command=initialize, accelerator="Command+I")
entryflash = file_menu.add_command(label="Flash", command=flash, accelerator="Command+F", state="disabled")
entryread = file_menu.add_command(label="Read", command=read, accelerator="Command+R", state="disabled")
entryerase = file_menu.add_command(label="Erase", command=erase, accelerator="Command+W", state="disabled")
entryverify = file_menu.add_command(label="Verify", command=verify, accelerator="Command+V", state="disabled")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy, accelerator="Command+Q")

tools_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Tools", menu=tools_menu)
#tools_menu.add_command(label="Install Driver", command=install_driver)
tools_menu.add_command(label="Install Flashrom", command=install_flashrom)

term_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Terminal", menu=term_menu)
term_menu.add_command(label="Clear contents", command=terminalwipe)
term_menu.add_command(label="Save contents to file", command=save_terminal_text, accelerator="Command+T")

hex_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Hex Viewer", menu=hex_menu)
hex_menu.add_command(label="Jump to offset", command=hexjump, accelerator="Command+E")

root.bind_all("<Command-o>",menuopenfile)
root.bind_all("<Command-s>",menusavefile)
root.bind_all("<Command-e>",menuhexjump)
root.bind_all("<Command-t>",menusaveterminal)
root.bind_all("<Command-i>",menuinitialize)

#terminalappend(arg1=flashrompath, arg2="")

root.mainloop()
