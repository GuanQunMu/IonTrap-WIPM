# The Control System for Quantum Information Process in Ion Traps

>Updated on July 02, 2020  
The frequency reading of lasers has been added  
The communication between Artiq and another PC with HighFinesse WLM has been added


Experimental operations of a single qubit in an ion trap can be realized by this project, including a designed GUI and functions of rabi scan, zeeman scan, and pulse shaping for the DDS (generated by AWG).


###  Research group:

MangFeng Ion Trap Group, WIPM, CAS, P. R China

Homepage link: http://english.wipm.cas.cn/rh/rd/yzfzsys/bsqip/bsqipr/

###  Contributors:

1. Guanqun Mu     -Undergraduate at Wuhan University, P. R China
3. GeYi Ding     -Master at WIPM, CAS
2. Kamran Rehan   -PhD at WIPM, CAS

If you have any question or you want to be a developer, please contact Guanqun Mu: **guanqun_mu@whu.edu.cn**

## 1. Introduction
<table border="0">
  <tr>
    <td width="70%">
      <img src="/Pictures/GUI2.1.png" width="100%">
    </td>
    <td width="30%">
      <img src="/Pictures/structure.png" width="100%">
      
    </td>
  </tr>
</table>


<img src="/Pictures/GUI2.1.png" width="100%">

ARTIQ was initiated by the Ion Storage Group at NIST. Based on this, we developed the control system for quantum information process in ion traps. It can support rabi scan, zeeman scan and paulse shaping for DDS. Furthermore, We developed a GUI and attached AWG (Arbitrary waveform generator) and the data from wave length meter with this control system.


## 2. Usage

### 1. Installing Artiq5 for Windows Users

1. Come to the link of script: <https://raw.githubusercontent.com/m-labs/artiq/release-5/install-with-conda.py> , copy all the script.
2. Create a new python file on your desktop, copy the script into the file.  Name it with `artiq_script.py`
3. Command Prompt:  `$ python artiq_script.py `
4. After minutes, packages Artiq5 will be installed in your PC.



### 2. Preparing

1. Creating a new folder, name it with `Artiq_WIPM`.
2. Create a new folder called `repository` inside `Artiq_WIPM`.
3. Copy the file `device_db.py` into the `Artiq_WIPM`. This file should be given by M-Labs guys.
4. Click the button ' Clone or download ' of this project.
5. Click ' Download ZIP '.
6. Uncompress the .zip file, copy the folder `repository` to recover the same name folder in `Artiq_WIPM`.
7. Command Prompt:

    `$ activate artiq  `

    `$ cd \Artiq_WIPM`

    `$ artiq_main`

8. Turn on another Command Prompt:

    `$ activate artiq`

    `$ artiq_dashboard`





### 3. Getting Start

1. Go to the ' Explorer ' part in dashboard, click the ' GUIFinal ' operation, set the pipeline to 'GUI', then click ' Submit ' button.

2. GUI will come out, change parameters (Rabi Scan/Zeeman Scan/...) , select one choice in ' Selection ' part, then Click ' Submit '.

<img src="https://github.com/GuanQunMu/IonTrap-WIPM/blob/master/Pictures/GUI1.0.png" width="400"/>

3. Go to the ' Explorer ' part in dashboard, select the ' Run ' operation, then click ' Submit ' button.

4. After opreation done, photon count picture will appear at Applet.


