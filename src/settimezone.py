#! /usr/bin/python
#SetTimeZone Application
#Application to change the timezone in Arch Linux.
#
#Copyright 2013 Nitin Mathew <nitn_mathew2000@hotmail.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import messagebox, simpledialog
from subprocess import check_output, PIPE, Popen
import sys
import logging
from os import path
class ApplicationSetTimeZone(tk.Frame):
    
    #Declare paths
    ZONEINFO_PATH="/usr/share/zoneinfo/"
    LOCALTIME_PATH="/etc/localtime"
    #List of zones
    zonelist=None
    #list index for searching
    search_list_index=None
    #Declare widgets
    statusbar_label=None
    info_label=None
    zoneinfo_list=None
    y_scrollbar_zoneinfo_list=None
    quit_butt=None
    change_zone_butt=None
    search_entry=None
    
    def __init__(self, master=None):
        logging.debug("Inside init")
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.populate_list()
        self.update_statusbar()
    
    #Create widgets     
    def create_widgets(self):
        logging.debug("Inside create_widgets")
        
        #Info Label
        self.info_label=tk.Label(self, text="Choose TimeZone:", takefocus=0)
        self.info_label.grid(row=0,column=0, columnspan=2, sticky="ew")
        
        #Timezone list
        self.zoneinfo_list = tk.Listbox(self, selectmode="single", height=15, width=30)
        self.zoneinfo_list.grid(row=1, column=0, padx=5)
        self.zoneinfo_list.bind('<<ListboxSelect>>',self.list_item_selected)
        
        #Scrollbar for timezone list 
        self.y_scrollbar_zoneinfo_list = tk.Scrollbar(self,command=self.zoneinfo_list.yview, orient="vertical", takefocus=0)
        self.y_scrollbar_zoneinfo_list.grid(row=1, column=1, sticky="ns")
        self.zoneinfo_list.config(yscrollcommand = self.y_scrollbar_zoneinfo_list.set)
        
        #Search label
        self.search_label=tk.Label(self,text="Search:", anchor="w", width=7,takefocus=0)
        self.search_label.grid(row=2, column=0, sticky="w",pady=1)
        
        #Search text box
        self.search_entry=tk.Entry(self, text="search", bg="white", width=24)
        self.search_entry.grid(row=2, column=0,sticky='e',pady=1)
        self.search_entry.bind('<Return>', self.search_zone)
            
        #Button which will enable the change zone
        self.change_zone_butt = tk.Button(self, text="Change\nZone", command=self.change_timezone, width=5, height=2)
        self.change_zone_butt.grid(row=3, column=0, sticky="w", padx=5,pady=2)
        
        #Button to perform ntp sync
        self.quit_butt = tk.Button(self, text="NTP\nSync", command=self.ntp_sync, width=5, height=2)
        self.quit_butt.grid(row=3, column=0,  padx=5,pady=2)
        
        #Button which will enable exit
        self.quit_butt = tk.Button(self, text="Exit", command=self.exit_app, width=5, height=2)
        self.quit_butt.grid(row=3, column=0, sticky="e", padx=5,pady=2)
        
        #Stausbar Label
        self.statusbar_label=tk.Label(self, text="", bd=2, relief="ridge", anchor="w", takefocus=0)
        self.statusbar_label.grid(row=4,column=0, columnspan=3, sticky="ew",padx=5,pady=2 )
        
        #Exit application using Escape
        root.bind('<Escape>',self.exit_app)
        
        logging.debug("Widget creation is complete")
        
    #Populate the list of available timezones dynamically. Is called only once, at startup
    def populate_list(self):
        logging.debug("Inside populate_list")
        #Command to extract the list of time zones available in /usr/share/zoneinfo
        zonelist_cmd="(cd /usr/share/zoneinfo && find . | sort | sed 's/\.\///g' | grep -Ev 'right|posix' | grep 'Africa\|America\|Antarctica\|Arctic\|Asia\|Atlantic\|Australia\|Brazil\|Canada\|Chile\|Europe\|Indian\|Mexico\|Mideast\|Pacific\|US' | grep '\/')"
        try:
            self.zonelist=check_output(zonelist_cmd, shell=True).decode('ascii').strip().split()
            #Populate the list with timezones
            logging.debug("Zone Lists: %s", self.zonelist)
            for zone in self.zonelist:
                self.zoneinfo_list.insert("end", zone)
            self.zoneinfo_list.selection_set(first=0)
            self.zoneinfo_list.event_generate('<<ListboxSelect>>')
        except:    
             self.general_exception_handler()
    
    #Update index used by search tool when selection is changed
    def list_item_selected(self, event):
        self.search_list_index=self.zoneinfo_list.curselection()[0]
        
    #Contains the logic to change the timezone based on what user has selected
    def change_timezone(self):
        logging.debug("Inside change_timezone")
        if not self.zoneinfo_list.curselection():
            messagebox.showinfo("Error","Please select a timezone")
            return
        
        selected_zone=self.zoneinfo_list.get(self.zoneinfo_list.curselection())
        logging.debug("Selected Zone: %s", selected_zone)
        #If selected timezone does not exist then dont do anything further
        if not path.isfile(self.ZONEINFO_PATH+selected_zone):
            logging.error(self.ZONEINFO_PATH+selected_zone+" does not exist")
            messagebox.showinfo("Error",self.ZONEINFO_PATH+selected_zone+" does not exist")
            return
        #Request for password for running with sudo
        passwd=simpledialog.askstring("Password","Enter root password",show="*")
        if passwd==None or passwd=="":
            return
        #Remove current symbolic link and create new with the selected timezone. Clear sudo cached credentials at the end.
        changezone_cmd1=["sudo", "-S", "rm", self.LOCALTIME_PATH]
        changezone_cmd2=["sudo", "-S", "ln", "-s", self.ZONEINFO_PATH+selected_zone, self.LOCALTIME_PATH]
        changezone_cmd3=["sudo", "-k"]
        readlink_cmd="readlink "+self.LOCALTIME_PATH
        try:
            if path.isfile(self.LOCALTIME_PATH) or path.islink(self.LOCALTIME_PATH):
                stz_process = Popen(changezone_cmd1, universal_newlines=True, stdin=PIPE)
                stz_process.communicate(input=passwd+"\n")
                stz_process.stdin.close()
                if stz_process.wait() != 0:
                    messagebox.showinfo("Error", "COMMAND FAILED: "+' '.join(changezone_cmd1))
                    logging.error("COMMAND FAILED: "+' '.join(changezone_cmd1))
                    self.update_statusbar()
                    return
            stz_process = Popen(changezone_cmd2,  universal_newlines=True, stdin=PIPE)
            #Sending password into stdin in case changezone_cmd1 was not run due to missing localtime file
            stz_process.communicate(input=passwd+"\n")
            if stz_process.wait() != 0:
                messagebox.showinfo("Error", "COMMAND FAILED: "+' '.join(changezone_cmd2))
                logging.error("COMMAND FAILED: "+' '.join(changezone_cmd2))                
                self.update_statusbar()
                return      
            stz_process = Popen(changezone_cmd3,  universal_newlines=True)
            if stz_process.wait() != 0:
                messagebox.showinfo("Error", "COMMAND FAILED: "+' '.join(changezone_cmd3))
                logging.error("COMMAND FAILED: "+' '.join(changezone_cmd3))
                self.update_statusbar()
                return            
            
            cmd_output=check_output(readlink_cmd, shell=True)
            logging.debug("Changed timezone to %s",cmd_output)
            self.update_statusbar()
            messagebox.showinfo("Executed", self.LOCALTIME_PATH+" -> "+cmd_output.decode("ascii").strip())
        except:
            self.general_exception_handler()
            
    #Update the status bar with latest timezone
    def update_statusbar(self):
        try:
            if path.islink(self.LOCALTIME_PATH):
                cmd_output=check_output("readlink "+self.LOCALTIME_PATH, shell=True)
                self.statusbar_label.config(text=cmd_output.decode("ascii").strip())
            else:
                self.statusbar_label.config(text="n/a")
        except:
            self.general_exception_handler()
    
    #Search for timezones. Current searched position is kept track using an index.
    #This is incremented when a successful search happens.
    #If nothing is found then start from 0 and do one more run if search started from a non-zero position
    def search_zone(self, event):
        search_str=self.search_entry.get()
        if search_str=="":
            return
        for item in self.zonelist[self.search_list_index:]:
            if search_str.upper() in item.upper():
                self.zoneinfo_list.selection_clear(0,"end")
                self.zoneinfo_list.selection_set(first=self.zonelist.index(item))
                self.zoneinfo_list.see(self.zonelist.index(item))
                self.zoneinfo_list.event_generate('<<ListboxSelect>>')
                self.search_list_index=self.search_list_index+1
                logging.debug("Search term '%s' found", search_str)
                return
        self.search_list_index=0
        for item in self.zonelist[self.search_list_index:]:
            if search_str.upper() in item.upper():
                self.zoneinfo_list.selection_clear(0,self.zoneinfo_list.size())
                self.zoneinfo_list.selection_set(first=self.zonelist.index(item))
                self.zoneinfo_list.see(self.zonelist.index(item))
                self.zoneinfo_list.event_generate('<<ListboxSelect>>')
                self.search_list_index=self.search_list_index+1
                logging.debug("Search term '%s' found(restart section)", search_str)
                return
        logging.debug("Search term '%s' not found", search_str)
        messagebox.showinfo("Error", "'"+search_str+"' not found")
        self.search_entry.selection_range(0, "end")
    
    #Perform NTP sync
    def ntp_sync(self):
        logging.debug("Inside ntp_sync")
        #check if ntpd service is running, if running inform user and do nothing further
        service_chk_cmd="systemctl is-active ntpd.service"
        try:
            cmd_output=check_output(service_chk_cmd, shell=True)
            if cmd_output.decode("ascii").strip() == "active":
                    messagebox.showinfo("Info", "ntpd service is running, please stop it and then try again.")
                    logging.error("ntpd service is running, will not perform one time sync")
                    self.update_statusbar()
                    return
        except:
            #Assume the command failed due service not running/disabled/not available and proceed with one time sync
            pass
        #Request for password for running with sudo
        passwd=simpledialog.askstring("Password","Enter root password",show="*")
        if passwd==None or passwd=="":
            return
        #Sycn with ntp time, set the hwclock to the system time and clear the sudo cached credentials
        ntpsync_cmd1=["sudo", "-S","ntpd", "-q"]
        ntpsync_cmd2=["sudo", "-S","hwclock", "-w"]
        ntpsync_cmd3=["sudo", "-k"]
        try:
            stz_process = Popen(ntpsync_cmd1, universal_newlines=True, stdin=PIPE)
            stz_process.communicate(input=passwd+"\n")
            if stz_process.wait() != 0:
                messagebox.showinfo("Error", "COMMAND FAILED: "+' '.join(ntpsync_cmd1))
                logging.error("COMMAND FAILED: "+' '.join(ntpsync_cmd1))
                self.update_statusbar()
                return
            stz_process = Popen(ntpsync_cmd2,  universal_newlines=True, stdin=PIPE)
            if stz_process.wait() != 0:
                messagebox.showinfo("Error", "COMMAND FAILED: "+' '.join(ntpsync_cmd2))
                logging.error("COMMAND FAILED: "+' '.join(ntpsync_cmd2))
                self.update_statusbar()
                return
            stz_process = Popen(ntpsync_cmd3,  universal_newlines=True)
            if stz_process.wait() != 0:
                messagebox.showinfo("Error", "COMMAND FAILED: "+' '.join(ntpsync_cmd3))
                logging.error("COMMAND FAILED: "+' '.join(ntpsync_cmd3))
                self.update_statusbar()
                return
            messagebox.showinfo("Executed", "NTP Date sync complete")
        except:
            self.general_exception_handler()
            
    #Exit application
    def exit_app(self, event=None):
        logging.info("Exiting Application SetTimeZone")
        root.destroy()
    
    #Handle exceptions    
    def general_exception_handler(self):
        logging.error('Caught Exception:', exc_info=True)
        messagebox.showinfo("Error", sys.exc_info()[1])
        
#Check if logging is requested on startup and enable
if len(sys.argv) == 2 and sys.argv[1]=="--log":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(lineno)s: %(message)s')
    
logging.info("Application SetTimeZone has started")
root = tk.Tk()
root.title("Set Time Zone")
root.geometry('245x400+300+180')
root.resizable(0,0)
app = ApplicationSetTimeZone(master=root)
app.mainloop()
