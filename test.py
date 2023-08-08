#!/usr/bin/env python

import tkinter as tk
from tkinter import *
import subprocess
import scanFuncs
import os
from tkinter import ttk, messagebox

root = tk.Tk()
root.geometry('600x500')
root.title('test')

## DVB HOME PAGES

def home_page():
    home_frame = tk.Frame(main_frame)

    lb = tk.Label(home_frame, text=' Welcome\n\n TO JURASSIC PARK',font=('Bold' ,30))
    lb.pack()

    home_frame.pack(pady=20)

def DVBT_page():
    DVBT_frame = tk.Frame(main_frame)

    lb = tk.Label(DVBT_frame, text=' DVB-T\n',font=('Bold' ,25))
    lb.pack()
    dvbt_scan = tk.Button(DVBT_frame, text='DVB-T SCAN',font=('Bold' ,10),
                          command=lambda: [indicate(DVBT_indicate, terr_scan_page), scanFuncs.terrScan()])
    dvbt_scan.pack()

    dvbt_record = tk.Button(DVBT_frame, text='DVB-T RECORD',font=('Bold' ,10),
                          command=lambda: [indicate(DVBT_indicate, terr_record_page)])
    dvbt_record.pack()

    DVBT_frame.pack(pady=20)

def DVBS_page():
    DVBS_frame = tk.Frame(main_frame)

    # text
    lb = tk.Label(DVBS_frame, text=' DVB-S \n',font=('Bold' ,25))
    lb.pack()

    # scan button
    dvbs_scan = tk.Button(DVBS_frame, text='DVB-S SCAN',font=('Bold' ,10),
                          command=lambda: [indicate(DVBS_indicate, sat_scan_page)])
    dvbs_scan.pack()

    # record button
    dvbs_record = tk.Button(DVBS_frame, text='DVB-S RECORD',font=('Bold' ,10),
                          command=lambda: [indicate(DVBS_indicate, sat_record_page)])
    dvbs_record.pack()

    DVBS_frame.pack(pady=20)

def DVBC_page():
    DVBC_frame = tk.Frame(main_frame)

    lb = tk.Label(DVBC_frame, text=' DVB-C\n\n TO BE DONE',font=('Bold' ,25))
    entry1 = tk.Entry(DVBC_frame)
    lb.pack()
    entry1.pack()

    DVBC_frame.pack(pady=20)



## SCAN PAGES ##

#DVBT scan page
def terr_scan_page():
    scan_frame = tk.Frame(main_frame)

    lb = tk.Label(scan_frame, text=' asdasd Page\n\nPage: 1',font=('Bold' ,10))
    freq = tk.Entry(scan_frame)
    lb.pack()
    freq.pack()
    scan_frame.pack(pady=20)

#DVBS scan page
def sat_scan_page():
    scan_frame = tk.Frame(main_frame)
    
    lb = tk.Label(scan_frame, text=' Scan Page\n\nPage: 1',font=('Bold' ,10))
  
    lb.pack()

    #satName Entry
    satName_frame = tk.Frame(scan_frame)
    satName = tk.Entry(satName_frame, bd=2)
    Label(satName_frame, text='Satellite name').pack(side='left', padx=5)
    satName_frame.pack()
    satName.pack(side='right')

    #frequency Entry
    freq_frame = tk.Frame(scan_frame)
    freq = tk.Entry(freq_frame, bd=2)
    Label(freq_frame, text='Frequency').pack(side='left', padx=5)
    freq_frame.pack()
    freq.pack(side='right')

    # symbol rate entry
    symb_frame = tk.Frame(scan_frame)
    symb = tk.Entry(symb_frame, bd=2)
    Label(symb_frame, text='Symbol').pack(side='left', padx=14)
    symb_frame.pack()
    symb.pack(side='right')

    #polarity Entry
    pol_frame = tk.Frame(scan_frame)
    pol = tk.Entry(pol_frame, bd=2)
    Label(pol_frame, text='polarity').pack(side='left', padx=5)
    pol_frame.pack()
    pol.pack(side='right')

    scan_button = Button(scan_frame, text="GO!", command=lambda: scanFuncs.satScan(satName.get(), freq.get(), symb.get(), pol.get()), bg="#333e48", width=15)
    scan_button.pack(pady=5)

    
    
    scan_frame.pack(pady=20)

## RECORD PAGES ##

def terr_record_page():

    #frames
    record_frame = tk.Frame(main_frame)
    freq_frame = tk.Frame(main_frame)
    services_frame = tk.Frame(main_frame)
    buttons_frame = tk.Frame(main_frame)

    lb = tk.Label(record_frame, text='\n Record Page \n',font=('Bold' ,10))
    lb.pack()


    # data file variable
    folder = 'terr_streams/terr_tuning_data/'
    filelist = [fname for fname in os.listdir(folder) if fname.endswith('.xml')]
    print(filelist)

    # populates drop down menus with data from XML file
    def dvbtmaincombo():
        global dvbtcombo, dvbtcombo2

        dvbtcombo = ttk.Combobox(record_frame, values=filelist, state='readonly')
        Label(record_frame, text='saved scan file').pack(side='left', padx=5)
        dvbtcombo.pack(side='right', pady=5)
        dvbtcombo.bind('<<ComboboxSelected>>', combofill)

        dvbtcombo2 = ttk.Combobox(freq_frame, state='readonly')
        Label(freq_frame, text='Frequency').pack(side='left', padx=5)
        dvbtcombo2.pack(side='right', pady=5)
        dvbtcombo2.bind('<<ComboboxSelected>>', serviceFill)



        # combo3 = ttk.Combobox(services_frame, state='readonly')
        # Label(services_frame, text='services').pack(side='left', padx=5)
        # combo3.pack(side='right', pady=5)
        
    # populates frequency drop down with frequencies
    def combofill(event):
        freq_list = scanFuncs.terrNetworkInfo()

        frequencies = []
        for freq in freq_list:
            frequencies.append(freq['frequency'])
            dvbtcombo2.config(values=frequencies)
        dvbtcombo2.current(0)
        
    # populates textbox with services  
    def serviceFill(event):
        dvbtServicesBox.delete(1.0,END)
        service_list = scanFuncs.terrServicesInfo()
        service = (dvbtcombo2.get())
        print(service)
        field = service_list[service]
        for x in field:
            dvbtServicesBox.insert(tk.END, str(x) + '\n')
        print(field)
           


    # record freq button
    recordFreq_button = Button(buttons_frame, text="Record Frequency", command=lambda: scanFuncs.terrFreqRecord(dvbtcombo2.get()), bg="#6FAFE7", width=15)
    recordFreq_button.pack(pady=5)

    # record ALL freq button
    recordNetwork_button = Button(buttons_frame, text="Record ALL frequencies", command=lambda: scanFuncs.terrNetworkRecord(), bg="#6FAFE7", width=18)
    recordNetwork_button.pack(pady=5)

    dvbtServicesBox = tk.Text(services_frame, height=6, width=30)
    dvbtscroll_bar = tk.Scrollbar(services_frame)
    dvbtscroll_bar.config(command=dvbtServicesBox.yview)
    dvbtServicesBox.configure(yscrollcommand=dvbtscroll_bar.set)
    dvbtscroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    dvbtServicesBox.pack(side=tk.LEFT)


    dvbtmaincombo()
    record_frame.pack(pady=5)
    freq_frame.pack(pady=5)
    services_frame.pack(pady=5)
    buttons_frame.pack(pady=5)

def sat_record_page():

    #frames
    record_frame = tk.Frame(main_frame)
    freq_frame = tk.Frame(main_frame)
    services_frame = tk.Frame(main_frame)
    buttons_frame = tk.Frame(main_frame)

    lb = tk.Label(record_frame, text='\n Record Page \n',font=('Bold' ,10))
    lb.pack()


    # data file variable
    folder = 'sat_streams/sat_tuning_data/'
    filelist = [fname for fname in os.listdir(folder) if fname.endswith('.xml')]
    print(filelist)

    # populates drop down menus with data from XML file
    def maincombo():
        global combo1, combo2
        combo1 = ttk.Combobox(record_frame, values=filelist, state='readonly')
        Label(record_frame, text='Saved scan file').pack(side='left', padx=5)
        combo1.pack(side='right',pady=5)       
        combo1.bind('<<ComboboxSelected>>', combofill)

        combo2 = ttk.Combobox(freq_frame, state='readonly')
        Label(freq_frame, text='Frequency').pack(side='left', padx=5)
        combo2.pack(side='right', pady=5)
        combo2.bind('<<ComboboxSelected>>', serviceFill)

        # combo3 = ttk.Combobox(services_frame, state='readonly')
        # Label(services_frame, text='services').pack(side='left', padx=5)
        # combo3.pack(side='right', pady=5)
        
    # populates frequency drop down with frequencyes
    def combofill(event):
        freq_list = scanFuncs.satNetworkInfo(combo1.get())

        frequencies = []
        services = []
        for freq in freq_list:
            frequencies.append(freq['frequency'])
            services.append(freq['polarity'])
            combo2.config(values=frequencies)
        combo2.current(0)
        
    # populates textbox with services  
    def serviceFill(event):
        T.delete(1.0,END)
        service_list = scanFuncs.satServicesInfo(combo1.get())
        service = (combo2.get())
        print(service)
        field = service_list[service]
        for x in field:
            T.insert(tk.END, str(x) + '\n')
        print(field)
           
    # services text box and scroll bar
    T = tk.Text(services_frame, height=6, width=30)
    scroll_bar = tk.Scrollbar(services_frame)
    scroll_bar.config(command=T.yview)
    T.configure(yscrollcommand=scroll_bar.set)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT)

    # record freq button
    recordFreq_button = Button(buttons_frame, text="Record Frequency", command=lambda: scanFuncs.satFreqRecord(combo1.get(), combo2.get()), bg="#6FAFE7", width=15)
    recordFreq_button.pack(pady=5)

    # record ALL freq button
    recordNetwork_button = Button(buttons_frame, text="Record ALL frequencies", command=lambda: scanFuncs.satNetworkRecord(combo1.get()), bg="#6FAFE7", width=18)
    recordNetwork_button.pack(pady=5)

    maincombo()
    record_frame.pack(pady=5)
    freq_frame.pack(pady=5)
    services_frame.pack(pady=5)
    buttons_frame.pack(pady=5)


## HIDE BLUE SELECTION INDICATOR ON NAVIGATION TABS ##
def hide_indicators():
    home_indicate.config(bg='#c3c3c3')
    DVBT_indicate.config(bg='#c3c3c3')
    DVBS_indicate.config(bg='#c3c3c3')
    DVBC_indicate.config(bg='#c3c3c3')

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

## BLUE SELECTION INDICATOR FOR NAVIGATION TABS

def indicate(lb, page):
    hide_indicators()
    lb.config(bg='#158aff')
    delete_pages()
    page()


options_frame = tk.Frame(root, bg='#c3c3c3')

home_btn = tk.Button(options_frame, text='Home', font =('Bold',15),
                     fg='#158aff', bd=0, bg='#c3c3c3', width= 5, height= 1,
                     command=lambda: indicate(home_indicate, home_page))

home_btn.place(x=10, y=50)

home_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
home_indicate.place(x=3, y=50, width=5, height=37)

DVBT = tk.Button(options_frame, text='DVB-T', font =('Bold',15),
                     fg='#158aff', bd=0, bg='#c3c3c3', width= 5, height= 1,
                     command=lambda: indicate(DVBT_indicate, DVBT_page))

DVBT.place(x=10, y=100)

DVBT_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
DVBT_indicate.place(x=3, y=100, width=5, height=37)

DVBS = tk.Button(options_frame, text='DVB-S', font =('Bold',15),
                     fg='#158aff', bd=0, bg='#c3c3c3', width= 5, height= 1,
                     command=lambda: indicate(DVBS_indicate, DVBS_page))

DVBS.place(x=10, y=150)

DVBS_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
DVBS_indicate.place(x=3, y=150, width=5, height=37)

DVBC = tk.Button(options_frame, text='DVB-C', font =('Bold',15),
                     fg='#158aff', bd=0, bg='#c3c3c3', width= 5, height= 1,
                     command=lambda: indicate(DVBC_indicate, DVBC_page))

DVBC.place(x=10, y=200)

DVBC_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
DVBC_indicate.place(x=3, y=200, width=5, height=37)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=110, height=500)

main_frame = tk.Frame(root, highlightbackground='black',
                     highlightthickness=1)

main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height=500, width=500)

root.mainloop()