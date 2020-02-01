# Manual for Developers(CN Version)

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
