#!/usr/bin/env python



import tkinter
import tkinter.messagebox
import customtkinter
import scanFuncs
import os
import asyncio
import threading

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

satFolder = 'sat_streams/sat_tuning_data/'
satScanFile = [fname for fname in os.listdir(satFolder) if fname.endswith('.xml')]

terrFolder = 'terr_streams/terr_tuning_data/'
terrScanFile = [fname for fname in os.listdir(terrFolder) if fname.endswith('.xml')]
transmission = 'DVBT'



# pop out window for satellite scan
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Satellite Scan')
        self.geometry("400x300")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=0)

        self.satNamelabel = customtkinter.CTkLabel(self, text="File name:")
        self.satNamelabel.grid(row=0, column=0, padx=(0 ,10), pady=(40 , 10), sticky='e')

        self.satNameInput = customtkinter.CTkEntry(self, placeholder_text="File name")
        self.satNameInput.grid(row=0, column=1, padx=(0 ,0), pady=(40 , 10), sticky='w')

        self.freqInputlabel = customtkinter.CTkLabel(self, text="Frequency:")
        self.freqInputlabel.grid(row=1, column=0, padx=(0, 10), pady=(10 , 10), sticky='e')

        self.freqInput = customtkinter.CTkEntry(self, placeholder_text="Frequency")
        self.freqInput.grid(row=1, column=1, padx=(0, 0), pady=(10 , 10), sticky='w')

        self.symbInputLabel = customtkinter.CTkLabel(self, text="Symbol rate:")
        self.symbInputLabel.grid(row=2, column=0, padx=(0, 10), pady=(10 , 10), sticky='e')

        self.symbInput = customtkinter.CTkEntry(self, placeholder_text="Symbol rate")
        self.symbInput.grid(row=2, column=1, padx=(0, 0), pady=(10 , 10), sticky='w')

        self.polarityLabel = customtkinter.CTkLabel(self, text="Polarity:")
        self.polarityLabel.grid(row=3, column=0, padx=(0, 10), pady=(10 , 10), sticky='e')

        self.polarity = customtkinter.CTkOptionMenu(self, values=["horizontal", "vertical", "auto"])
        self.polarity.grid(row=3, column=1, padx=(0, 0), pady=(10 , 10), sticky='w')

        self.satScan_button = customtkinter.CTkButton(self, text="Satellite scan")
        self.satScan_button.configure(command=self.satScan)
        self.satScan_button.grid(row=5, columnspan=2, padx=0, pady=(20, 0))

    def satScan(self):
        threading.Thread(target=self.run_async_scan).start()

    def run_async_scan(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(scanFuncs.satScan(self.satNameInput.get(), self.freqInput.get(), self.symbInput.get(), self.polarity.get()))
        loop.close()


# Main window
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Stream Recorder")
        self.geometry(f"{800}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Transmission", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.DVBT_button_event, text='DVB-T')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.DVBS_button_event, text='DVB-S')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text='DVB-C',state="disabled")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Welcome\n\n" + " Please select a transmission.\n\n")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Scan")
        self.tabview.add("Record frequency")
        self.tabview.add("Record ALL")
        self.tabview.tab("Scan").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Record frequency").grid_columnconfigure(0, weight=1)

        # scan tab
        self.scan_button = customtkinter.CTkButton(self.tabview.tab("Scan"), command=self.scan, text='Scan')
        self.scan_button.grid(row=3, column=0, padx=20, pady=10)
    
        self.toplevel_window = None
        
        # record frequency tab
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Record frequency"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.fileMenu = customtkinter.CTkComboBox(self.tabview.tab("Record frequency"),
                                                        values='', command=lambda:[self.fileMenuSet, self.freqMenuFill], height=10)
        self.fileMenu.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.servicesTitle = customtkinter.CTkLabel(self.tabview.tab("Record frequency"), text="Service list", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.servicesTitle.grid(row=2, column=0, padx=10, pady=(10, 1))

        self.servicesTextbox = customtkinter.CTkTextbox(self.tabview.tab("Record frequency"), width=250)
        self.servicesTextbox.grid(row=3, column=0, padx=(10, 10), pady=(1, 5), sticky="nsew")

        self.recordFreq_button = customtkinter.CTkButton(self.tabview.tab("Record frequency"), command= self.recordFreq, text='Record Frequency')
        self.recordFreq_button.grid(row=4, column=0, padx=20, pady=10)

        # record ALL tab
        
        self.recordAllFreq_button = customtkinter.CTkButton(self.tabview.tab("Record ALL"), command= self.recordAllFreq, text='Record ALL Channels')
        self.recordAllFreq_button.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    # DVBT button
    def DVBT_button_event(self):
        global transmission
        transmission = 'DVBT'
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", 'DVBT')
        self.fileMenuSet()
        self.freqMenu = customtkinter.CTkComboBox(self.tabview.tab("Record frequency"),
                                                        values='',command= self.servicesFill)                                                       
        self.freqMenu.grid(row=1, column=0, padx=20, pady=(10, 10))

    # DVBS button
    def DVBS_button_event(self):
        global transmission
        transmission = 'DVBS'
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", 'DVBS')
        self.fileMenuSet()
        self.freqMenu = customtkinter.CTkComboBox(self.tabview.tab("Record frequency"),
                                                        values='',command= self.servicesFill)
                                                        
        self.freqMenu.grid(row=1, column=0, padx=20, pady=(10, 10))

    # configures fileMenu dropdown with scan files
    def fileMenuSet(self):
        global transmission
        if transmission == 'DVBS':
            scanFile = satScanFile
        if transmission == 'DVBT':
            scanFile = terrScanFile
        self.fileMenu = customtkinter.CTkOptionMenu(self.tabview.tab("Record frequency"), dynamic_resizing=False,
                                                        values=scanFile, command= self.freqMenuFill)
        self.fileMenu.grid(row=0, column=0, padx=20, pady=(20, 10))

    # configures freqMenu dropdown with frequencies from scan file selected in fileMenu
    def freqMenuFill(self, event):
        global tranmission
        if transmission == 'DVBS':
            freq_list = scanFuncs.satNetworkInfo(self.fileMenu.get())
        if transmission == 'DVBT':
            freq_list = scanFuncs.terrNetworkInfo(self.fileMenu.get())
        else:
            print('error')
        
        self.freqMenu.set('Please select')

        frequencies = []
        for freq in freq_list:
            frequencies.append(freq['frequency'])
        print(len(frequencies))
        if len(frequencies) < 1:
            self.freqMenu.configure(values=['No frequencies on scan file'])
        else:
            self.freqMenu.configure(values=frequencies)

    # inserts services from selected scan file into textbox
    def servicesFill(self, event):
        global transmission
        self.servicesTextbox.delete('0.0','end')
        if transmission == 'DVBS':
            service_list = scanFuncs.satServicesInfo(self.fileMenu.get())
        if transmission == 'DVBT':
            service_list = scanFuncs.terrServicesInfo(self.fileMenu.get())
        service = (self.freqMenu.get())
        print(service)
        field = service_list[service]
        for x in field:
            self.servicesTextbox.insert('0.0', str(x) + '\n')
        print(field)

    def satelliteScan(self):
        scanFuncs.satScan(self.satNameInput.get(), self.freqInput.get(), self.symbInput.get(), self.polarity.get())

    def scan(self):
        global tranmission
        def run_async_terrScan():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(scanFuncs.terrScan('test2'))
                loop.close()

        if transmission == 'DVBS':
            self.open_toplevel()
        if transmission == 'DVBT':
            threading.Thread(target=run_async_terrScan).start()

            
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def recordFreq(self):
        global tranmission
        if transmission == 'DVBS':
            scanFuncs.satFreqRecord(self.fileMenu.get(), self.freqMenu.get())
        if transmission == 'DVBT':
            scanFuncs.terrFreqRecord(self.fileMenu.get(), self.freqMenu.get())
        else:
            print()

    def recordAllFreq(self):
        global transmission
        if transmission == 'DVBS':
            print('Attempting to record all satellite channels')
            scanFuncs.satNetworkRecord(self.fileMenu.get())
        if transmission == 'DVBT':
            print('Attempting to record all terrestrial channels')
            scanFuncs.terrNetworkRecord('terr_scan')
        else:
            print('error')

if __name__ == "__main__":
    app = App()
    app.mainloop()
