# Manual for Developers(English Version)

## Dashboard Fuction

### Dashboard Explorer

1. How does Explorer work:

We need to create a new .py file in the repository folder, and then use the python code to define a class in the file. The first line inside the class encloses a name we set with three double quotes. This name is displayed in Explorer. In addition, we can define multiple classes in a .py file, and the tasks corresponding to these classes can be found by Explorer.

2. Task submission mechanism:

After clicking the task, a dialog box will pop up. (The GUI page of the dialog box can be defined by the `.build` function in the class)

After clicking the submit button in the task dialog box, the system will automatically retrieve the `prepare ()` function, `run ()` function, `analyse ()` function in the class, and run them in order. The `prepare ()` function and the `analyze ()` function can be omitted.

In addition, references to classes and functions in different files are invalid. But classes and functions inside the same file can be referenced.

### Dashboard Applets

1. You can right-click Applets to create a new display interface. The data associated with it is the data in our dataset. Rename the prompt line after Applet task to change the data corresponded.

2. In addition, if you want to designe the Applet by yourself, you can refer to the source code under artiq's applets for copying (at this time, you should use python's pyqt package), and put the written panel code into the applet's applets source code. Under the same folder.

## Dashboard Datasets

The datasets contain the parameters involved in the experiment. In the code we submit the task, we can use the `self.set_dataset ()` function to pass the parameters inside our program to our datasets, for example:

```python
self.set_dataset ("NUM1", 5, broadcast = True)
```

That is, the number 5 is assigned to the parameters in the dataset NUM1.

In addition, when naming, we can name the parameter NUM1.NUM2. In this way, NUM1 will be named an element similar to a folder. In NUM1 we can find the parameter NUM2.

## Code writing rules

### Framework of code

1. Each task submitted in the dashboard corresponds to a class, and each class contains the following modules: `build ()` function, `prepare ()` function, `run ()` function, `analyse ()` function

2. The build () function defines the GUI interface that appears after clicking the task in the dashboard, and is responsible for passing these input data to the corresponding elements in the class. (Note: At this time, the data will not be displayed in the dataset in the dashboard. To display it in the dataset, additional functions are required.) For details, see the detailed explanation of the `build ()` function in the Artiq official website.

3. The front of the `run ()` function can define which device this function runs under. If there is no `@ kernel` before` run () `, the system will not call the artiq hardware, and the code can run on the PC side. At this point, if you define the code that needs to call ttl and dds under the `run ()` function, the system will report an error. If @kernel is added before `run ()`, the system will compile the code on the PC first, and then run the compiled code on the FPGA according to the timing. However, because the compilation principle of Artiq is quite simple, complex calculations under @kernel and calls to packages other than `numpy` may report errors.

4. In the `.build ()` function of a `.py` file, we need to enumerate all the interfaces to be involved in this file. If we involve ttl0 and ttl1 in this experiment, we will use the` build () `Function is written like this:

   ```python
   self.setattr_device("core")
   self.setattr_device("ttl0")
   self.setattr_device("ttl1")
   ```

5. In the `run ()` function, we usually add a line of code to refresh the timeline to prevent errors of time overflow type, as follows:

   ```python
   self.core.reset()
   ```
   
   ### TTL output

1. TTL control code can only run under @kernel. When controlling the output of TTL, the opening of ttl can be controlled by `self.ttl.on ()`, the closing of ttl can be controlled by `self.ttl.off ()`, and the intermediate time can be delayed (time * ms) to control.

   For example, if we want ttl0 to be on for 5ms, we can write:

   ```python
   self.ttl0.on()
   delay(5*ms)
   self.ttl0.off()
   ```
   
   Or:
   

   ```python
   self.ttl0.pulse(5*ms)
   ```
   
   If we want to control multiple ttl signals, for example ttl0 and ttl1 are turned on for 5ms at the same time, we can do this:

   ```python
   self.ttl0.on ()
   self.ttl1.on ()
   delay (5 * ms)
   self.ttl0.off ()
   self.ttl1.off ()
   ```

   Or do this:

   ```python
   with parallel:
   self.ttl0.pulse (5 * ms)
       self.ttl1.pulse (5 * ms)
   ```

   There is a Demo in `GuanQunMu/IonTrap-WIPM/Demo_List/TTL_Output_Demo.py` file. This file has been tested to work perfectly. For other examples, see the examples on the artiq website.

2. It is important to note that when controlling TTL, we must pay special attention to whether the TTL interface we control is an output interface or an input interface. If it is an input interface, we cannot control the output of this TTL interface by code, but can only do analysis of TTL input signals.

3. In addition, it should be noted that we can change the name of the TTL at will. If we want to change the name of the TTL, we can change it in `device_db.py`, and in the execution code, we also need to change the TTL accordingly. Name, for example: we changed the name of TTL in `device_db.py` to 729, then when executing the code, we need to change the code to a form similar to` self.729.on () `.

### TTL input

1. ttl input can only be run under @kernel. The ttl input module is generally used for photon detection. During the photon detection process, we connect the ttl signal output by the photon detector to the ttl input signal interface of ARTIQ. We can count the rise of the ttl signal on the PC. There are as many edges as we can read out how many photons are detected. On the PC side, we need to set the ttl signal detection time that we are going to process and count how many ttl signals are rising. If we want to see how many rising edges are within 5ms, we can write:

   ```python
   self.ttl4.gate_rising (5 * ms)
   count = self.ttl4.count ()
   ```

   In this way, the number of rising edges of the input ttl signal can be assigned to count in 5ms.

2. It is worth noting that when we write like this, it means that within 5ms of our ttl input signal detection, we can do nothing else. If we want to detect the ttl input signal, When doing some other operations, we can usually write:

   ```python
   with parallel:
   self.ttl4.gate_rising (self.DETECTION_time * ms)
   Ranch
       with sequential:
           (the code you want to do at the same time ...)
   
   count = self.ttl4.count ()
   ```

   Additional examples can be found in the `GuanQunMu / IonTrap-WIPM / Demo_List / TTL_Input_Demo.py` file, which has been tested to work perfectly.

### DDS output

1. The output of dds can only be run under @kernel. The opening of dds can be written as follows:

   ```python
   self.urukul1_ch0.sw.on ()
   ```

   Regarding the operation of `.sw.on ()`, I have not found it on the official website. This execution method can be run on the hardware of the development version of artiq, but whether it can run on the new artiq in our laboratory needs further testing .

2. Regarding the amplitude adjustment of the dds signal, add that we want to adjust the dds power named `urukul1` to 8 dBm, we can do this:

   ```python
   self.urukul1_ch0.set_att (2)
   ```

   This means that the power is adjusted to `10-2 = 8 dBm`

3. Regarding the frequency adjustment of the dds signal, if we want to adjust the dds output named `urukul1` to 1000kHz, we can write:

   ```python
   self.urukul1_ch0.set (1000 * kHz)
   ```
   Additional examples can be found in the `GuanQunMu / IonTrap-WIPM / Demo_List / DDS_Demo.py` file. This file has been tested to work perfectly.

### Pulse Shaping

1. Pulse shaping is done to prevent the AC-Stark effect in the operation of quantum information. It is essentially a DDS output in the experimental control, but what we need to add is that we will implement the DDS amplitude change over time during a Rabi oscillation operation cycle.

   ```python
   self.urukul1_ch0.sw.on ()
   t = 0
   while t <10:
   self.urukul1_ch0.set_att (float (t))
   delay (300 * us)
       
   t + = 1
       
   self.urukul1_ch0.sw.off ()
   ```

   This means that we adjust the amplitude of the DDS to `10-0 = 10 dBm` for 300us, and then adjust the amplitude to` 10-1 = 9 dBm`, and so on until the dBm is adjusted to 1 dBm.

2. When performing the operation of pulse shaping, we should pay special attention to the possible error of time overflow type. Because the function of adjusting the dds power takes time to execute, the step size of our pulse plasticity setting cannot be too small. If it is too small, an error will be reported.

3. For an extension example, see `GuanQunMu / IonTrap-WIPM / Demo_List / Pause_Shaping_Demo.py`

## How to design a GUI interface in Artiq

The solution we take is: The custom GUI only has the function of changing the data in the dataset in the Dashboard. Other than that, it does not assume any function.

Making a GUI requires the following steps:

Making a .ui file in QTdesigner, translating the .ui file into a .py file, adding features to the .py file and changing the .py file to fit the Artiq compiler

### Making .ui files in QTdesigner

Install PyQt5 and enter in the command line:

`$ pip install PyQt5`

`$ pip install PyQt5-tools`

Go to the QTdesigner installation address: \ Anaconda3 \ Scripts \ pyqt5designer.exe and open pyqt5designer.exe

Save as XXX.ui file after making GUI

### Translating .ui files into .py files

`$ python -m PyQt5.uic.pyuic -o XXX.py XXX.ui` or` $ pyuic5 -o XXX.py XXX.ui`

### Adding functionality to .py files

Find the newly generated XXX.py file and open it with Notepad

Add functions after the setupUi function in the class, such as the effect of a button click, etc.

### Changing .py file to fit Artiq compiler

Copy all functions in the class and overwrite all functions with the same name in the Demo file. (Demo file link: `GuanQunMu / IonTrap-WIPM / Demo_List / GUI_Demo`)

Put the changed files in the repository folder and submit the operation in the dashboard

# Questions and Answers

### What's the matter of compiling and running under @kernel? What exactly is the error of the time overflow type?

The dialogue is as follows:

** Q: **

As shown below, if we submit such a piece of code, the calculation of this line of code takes time for `a = 1 + 1`. And because the code is executed in order from top to bottom, then due to the existence of this line of code, will the actual output TTL last longer than our set 10ms?

```python
self.ttl0.on ()
delay (5 * ms)
a = 1 + 1
self.ttl0.off ()
```

** A: **

No more than 10 ms. ARTIQ's kernel is real-time. There are two mechanisms to ensure real-time characteristics:

1. The code in @kernel is compiled and then run instead of interpreted and executed like python, so as in your case, you can know exactly the result of this code during the compilation phase. , Then `a` will be set to 2 at compile time, and then run. Similar code is very common, for example:

```python
self.ttl1.pulse (self.cool_time + self.pump_time)
```

Then it will calculate `self.cool_time + self.pump_time` at compile time and substitute it.

2. The delay (t) function does not simply wait for t. Mechanically, ARTIQ has a timestamp variable assigned to each operation (such as `ttl.on ()`). During the compilation process, `delay ( The) `function is responsible for making the interval between the timestamps before and after the event t, rather than letting the system idle t.

Subsequently, when the code is actually running, the FPGA internal timer (an accessible variable `time_now`) is gradually accumulated. When` time_now` is equal to the time stamp of a certain time, this event is executed.

Therefore, consider the following examples to understand two issues:

```python
do_something_before ()
self.ttl1.on ()
delay (1 * ms)
do_something_inside ()
self.ttl.off ()
```

First of all, since the start time of `time_now` is not clear, then it is entirely possible that after` do_something_before () `,` time_now` has exceeded the timestamp of `self.ttl1.on ()`. If so, ARTIQ runs (and Not compiling) After this line, it reports an `underflow` error and then exits.

So in order to avoid this, the timing code usually starts with `core.reset ()` or `core.break_realtime ()` with the initial value of the given timestamp offset.

Secondly, if `do_something_inside ()` takes less than 1 ms, the subsequent code will have no effect, because `time_now ()` has not reached the time of `self.ttl.off ()`, so the system continues to wait. Yes, but if `do_something_inside ()` takes more than 1 ms, then you also get a time overflow error and stop when running to `self.ttl.off ()`. At this time, you can only try to reduce `do_something_inside ( ) `Or increase the delay () time.

In short, the code running on the FPGA in ARTIQ is either strictly according to the timing, or it stops by directly reporting an error.



### Why the tasks corresponding to the code I wrote are not displayed in the dashboard?

If you write a code with grammatical errors in the Python language, then even if you put this file in the repository folder, the dashboard will not recognize the file when you open the dashboard. At this time, you should see to check your Is there a syntax type error in your python code.

In addition, tab type carry spaces are prohibited in python code, otherwise they will not be recognized. We should replace one tab with four spaces.
