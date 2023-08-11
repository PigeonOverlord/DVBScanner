# DVB Scanner

Scans, Records and Analyzes Terrestrial and Satellite streams

## Prerequisites

Requires [TSduck](https://tsduck.io) installation

Satellite/Terrestrial Tuner with up to date drivers

## Dependancies

tkinter
customtkinter

## Usage

```
1. Run script.py
3. Satellite scan to scan transmission feed and create XML scan file. Satellite scan requires transponder transmission parameters.
4. Select 'Record Frequency' tab to record single frequency
5. Select scan file from drop down
6. Select Frequency to download & analyze
7. Channel names are displayed in text window 
5. Select 'Record All' tab to record all frequencies
```
+ If scan is successful, results are written to scan.xml and x2j.json
+ recordings can be found in sat_streams/recordings or terr_streams/recordings
+ please check console for errors
+ terrestrial scan requires no input as it uses standard uhf-bands
+ satellite scan requires valid frequency, symbol rate & polarity for the scan to initially lock.

#### Useful TSduck console commands

+ tslsdvb - list connected tuner devices' driver and DVB compatibility
+ tsp - records channels on frequency ```e.g tsp -I dvb -a 0 --delivery-system DVB-S2 --frequency 10744000000 --polarity horizontal -s 22000000  -O file sat_test.ts```
+ tsscan - scans transponder network | use --nit-scan for DVB-S2 & --uhf-band for DVB-T ```e.g tsscan --uhf-band --service-list```

#### Console script - pScanner
Initial console script for building of functions - was expanded to utilise pi display, now obsolete
```
1. run pScanner.py to run console script 
2. follow user input (1-2) to scan or record
```
### Useful libraries for scanning and troubleshooting

+ w_scan_cpp - uses satellite and region parameters to scan frequencies ```e.g w_scan_cpp -fs -s S19E2 -c DE```
+ dvbv5_scan - requires initial scan file and the LNB to be specified ```e.g dvbv5_scan Astra-1N-19.2E --lnbf=EXTENDED --output=FILENAME```


