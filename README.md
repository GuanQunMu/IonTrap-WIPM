# The Control System for Quantum Information Processing in Ion Traps

>Updated on Spt 03, 2020  
The spin-echo opreation has been added, in particular the CPMG and the UDD modes.


Experimental operations of a single qubit in an ion trap can be realized by this project, including a designed GUI and functions of rabi scan, zeeman scan, and pulse shaping for the DDS (generated by AWG).


###  Research group:

MangFeng Ion Trap Group, WIPM, CAS, P. R China

Homepage link: http://english.wipm.cas.cn/rh/rd/yzfzsys/bsqip/bsqipr/

###  Contributors:

1. Guanqun Mu     -Research Assistant (was an undergraduate at Wuhan University)
3. GeYi Ding     -PhD Student at WIPM, CAS
2. Kamran Rehan   -PhD at WIPM, CAS

If you have any question using it or have any suggestion, please contact Guanqun Mu: **guanqun_mu@whu.edu.cn**

## 1. Introduction

<img src="/Pictures/GUI2.1.png" width="100%">

ARTIQ was initiated by the Ion Storage Group at NIST. Based on this, we developed the control system for quantum information process in ion traps. It can support rabi scan, zeeman scan and paulse shaping for DDS. Furthermore, We developed a GUI and attached AWG (Arbitrary waveform generator) and the data from wave length meter with this control system.

<img src="/Pictures/structure.png" width="70%">

## 2. Usage

### 1. Installing Artiq5 for Windows Users

This part has been updated by M-Labs, to see the latest procedue, please follow: https://m-labs.hk/artiq/manual/installing.html


### 2. Preparing

1. Download this project, Uncompress it.

2. Replace the initial 'device_db.py' with the latest 'device_db.py' in the folder. Then Change the IP data in the 'device_db.py' to the IP of the Artiq hardware. (If you have not bought the hardware from M-Labs, just skip it)

3. Command Prompt:

    `$ activate artiq  `

    `$ cd \Artiq_WIPM`

    `$ artiq_master`

4. Then turn on another Command Prompt:

    `$ activate artiq`

    `$ artiq_dashboard`

5. Now the dashboard of Artiq should appear. It is remarkable that if you skip the procedure2, you may not succeed to connect the hardware of Artiq, but you can still run codes without @kernel.



### 3. Getting Start

1. Find the ' Explorer ' part in the dashboard, double click the latest ' GUI ' operation, set the pipeline to 'GUI', then click ' Submit ' button.

2. After the GUI appears, change parameters (Rabi Scan/Zeeman Scan/...) and select a running mode, then click thhe 'Submit' botton on the GUI.

3. double click the latest ' Run ' operation in the ' Explorer ' part, set the pipeline to 'main', then click ' Submit ' button.


### 4. Advance Functions

#### 1. If you have HighFinesse wavelength meters and  want to display the frequency of lasers on your dashboard, please follow:

1. Uncompress the WLM.zip file, copy the file 'CallBackDemoTest.py' to the file of your wavelength meter software located.

2. Build an internet between the PC with wavelength meter software and the PC with Artiq. Make sure that your PC with Artiq is the same with the IP address showed in the  'CallBackDemoTest.py' file. If not, change it in the file.

3. Submit the 'TCPIP_LaserFrequency' in the 'Explorer' to build a server with the Artiq, then run the 'CallBackDemoTest.py' file to build a client with Python. Therefore, the connection between Artiq and wavelength meter will be build so the frequency of lasers will be displayed on the dashboard.

#### 2. If you want control the AWG from the CIQTEK (国仪量子) with this project, please follow:

1. Change the IP address in the '\AWG4100-Python64\example_AWG2.py' to the IP adress of your AWG.

2. Change the information of the location of your 'example_AWG2.py' in the '\AWG4100-Python64\AWG.bat' and change the information in the '\repository\AWG_ON.py'

3. Modify the wavefunction in the file of '\AWG4100-Python64\wave.txt' (Don't change the first line of setting repeat parameter in the file.)

3. Submit the 'AWG_ON' in the 'Explorer'.
 
