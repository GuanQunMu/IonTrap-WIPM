# Control System for Quantum Information Process in Ion Traps

Updated on February 1, 2020.

This project can be used to realize experimental operations of a single qubit in the ion trap, including rabi scan, zeeman scan, and pulse shaping for rabi scan. Otherwise, for the convenience of experiment, we also Designed a convenient GUI.

## 1. Introduction

###  Copyright:

Belongs to WIPM MangFeng Ion Trap Group.

Homepage link: http://english.wipm.cas.cn/rh/rd/yzfzsys/bsqip/bsqipr/

###  Developers:

1. Guanqun Mu     -Undergraduate at Wuhan University, P. R China
2. Kamran Rehan   -PhD at WIPM, CAS
3. GeYi Ding     -Master at WIPM, CAS

If you want to be a developer, please contact Guanqun Mu: **guanqun_mu@whu.edu.cn**

And go to ' Manual for Developers.md ' for more details.




## 2. Manual for Users

### 1. Installing Artiq5 for Windows Users

1. Come to the link of script: <https://raw.githubusercontent.com/m-labs/artiq/release-5/install-with-conda.py> , copy all the script.
2. Create a new python file on your desktop, copy the script into the file.  Name it with `artiq_script.py`
3. Command Prompt:  `$ python artiq_script.py `
4. After minutes, packages Artiq5 will be installed in your PC.



### 2. Preparing

1. Creating a new folder, name it with `Artiq_WIPM`.

2. Create a new folder called `repository` inside `Artiq_WIPM`.

3. Copy the file `device_db.py` into the `Artiq_WIPM`. This file is always given by M-Labs guys.

4. Click the button ' Clone or download ' of this project.

5. Click ' Download ZIP '.

6. Uncompress the .zip file, copy the folder `repository` to recover the same name folder in `Artiq_WIPM`.

7. Command Prompt:

    `$ activate artiq  `

    `$ cd \Artiq_WIPM`

    `$ artiq_main`

    Now artiq_master is done.

8. Turn on another Command Prompt:

    `$ activate artiq`

    `$ artiq_dashboard`

    Now the dashboard is done.




### 3. Getting Start

1. Go to the ' Explorer ' part in dashboard, select the ' GUIFinal ' operation, then click ' Submit ' button.

2. GUI will come out, change parameters (Rabi Scan/Zeeman Scan/...) , select one choice in ' Selection ' part, then Click ' Submit '.

3. To be continued...



