#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import ttk
import re

win = tk.Tk()
win.title("Mac Daddy")

cmd = "ls /sys/class/net/"
out = subprocess.check_output(["ls", "/sys/class/net/"]).decode('utf-8').split()
out.remove("lo")
aLabel = ttk.Label(win, text="Select an interface:").grid(column=0, row=0)
interface = tk.StringVar()
interfaceEntered = ttk.Combobox(win, textvariable=interface, state='readonly')
interfaceEntered['values'] = out
interfaceEntered.grid(column=0, row=1)
interfaceEntered.current(0)

aLabel = ttk.Label(win, text="Enter a new Mac Address:").grid(column=1, row=0)
mac_address = tk.StringVar()
mac_addressEntered = ttk.Entry(win, textvariable=mac_address)
mac_addressEntered.grid(column=1, row=1)


def changeAddress():
	mac = mac_address.get()
	banner = ttk.Label(win, text="                          	").grid(column=0, row=2, columnspan=2)
	if len(mac)==17 and mac[:2].isalnum() and mac[3:5].isalnum() and mac[6:8].isalnum() and mac[9:11].isalnum() and mac[12:14].isalnum() and mac[15:17].isalnum() and (len(re.findall(":", mac)) == 5):
    	subprocess.run(["ifconfig", interface.get(), "down"])
    	x = subprocess.run(["ifconfig", interface.get(), "hw", "ether",  mac])
    	subprocess.run(["ifconfig", interface.get(), "up"])
    	if (x.returncode == 0):
        	banner = ttk.Label(win, text="[+] Changing Mac Address for " + interface.get() + " to " + mac_address.get() + "").grid(column=0, row=2, columnspan=2)
   	 
    	else:
        	banner = ttk.Label(win, text="The Mac Address entered was not acceptable").grid(column=0, row=2, columnspan=2)
	else:
    	banner = ttk.Label(win, text="The Mac Address entered was not acceptable").grid(column=0, row=2, columnspan=2)
	
def onselect(evt):
	result = subprocess.run(["ifconfig", interface.get()], capture_output=True)
	current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(result.stdout))
	banner = ttk.Label(win, text="[-] " + interface.get() + " Address: " + str(current_mac[0])).grid(column=0, row=2, columnspan=2)
    

interfaceEntered.bind('<<ComboboxSelected>>', onselect)    
action = ttk.Button(win, text="Confirm", command=changeAddress)
action.grid(column=2, row=1)

win.mainloop()
