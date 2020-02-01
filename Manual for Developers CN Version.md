# 安装（已完成）

1. 安装ANACONDA（注：最新版的ANACONDA与artiq不兼容）
2. 用CONDA新建artiq-main环境
3. 将电脑切换至artiq-main环境
4. 联网时，在`artiq-main`环境下从ANACONDA官网的`m-labs/packages `里选择artiq 包，用`conda install XXX`的方式下载   （注：不要用`pip install XXX`下载！因为artiq有一部分是用C++写的，用pip安装会导致安装中断）
5. 同理，下载`artiq-kc705-nist_clock ，artiq-kc705-nist_qc2 ，artiq-kasli-tester ，artiq-kasli-wipm `



# 运行前的准备（已完成）

1. 从artiq官网提供的github地址中下载包至本地
2. 从`example/master `文件夹中拷贝出`device_db.py`文件
3. 在与`device_db.py`同一文件夹下新建`repository`文件夹



# 操作

### dashboard的启动

点击桌面右上角的`dashboard.bat `脚本文件

脚本内容详情见桌面上的`artiq_dashboard`文件夹中的`artiq-dashboard.md`文件

### dashboard右侧的任务栏（Explorer）

1. 任务栏中现实的任务的设置：

需要我们在 repository 文件夹中新建一个.py 文件，之后在文件中用python代码定义一个类，类的内部第一行用三个双引号括起一个我们设置的名字，这个名字就是显示在dashboard中Explorer中的任务名称。额外，我们可以在一个.py文件中定义多个类，这些类对应的任务都可以被Explorer发现到。

2. 任务的提交机制：

点击任务之后会弹出一个对话框。（对话框的GUI页面可以通过类中的`.build`函数来定义）

点击任务对话框中的submit按钮后，系统会自动检索类中的`prepare() `函数，`run()`函数，`analyse()` 函数，并且依次运行。其中`prepare() `函数和` analyse() `函数可以省略。

此外，引用不同文件里的类和函数的无效。但是同一个文件内部的类和函数可以引用。

### dashboard的实时监控GUI界面（Applets）

1.  实时监控界面可以右键点击以新建显示界面，这个监控界面关联的数据是我们的dataset中的数据，在我们GUI 界面的任务名称里重命名即可更改我们想显示的数据  

2.  此外，假如你想自己写面板，你可以参考artiq的applets下的源代码仿写，（此时应当用到python的pyqt包），并将写好的面板代码放到artiq的applets源代码的同一文件夹下。  


## dashboard左侧的datasets

datasets 中包含着实验中涉及到的参数。在我们提交任务的代码中，我们可以利用`self.set_dataset()`函数来将我们的程序内部的参数传递到我们的datasets中，例如：

```python
self.set_dataset("NUM1", 5, broadcast=True)
```

即是将5这个数赋予给了NUM1这个datasets中的参数。

此外，在命名的时候，我们可以将参数命名为NUM1.NUM2，这样一来，NUM1将会被命名为一个类似于文件夹的元素，在NUM1中我们可以找到NUM2这个参数。



# 代码的书写规则

### 代码的框架

1. 每一个在dashboard中提交的任务对应了一个类，每一个类包含了如下模块：`build()`函数，`prepare() `函数，`run() `函数，`analyse() `函数

2. build()函数定义了在dashboard中点击任务后出现的GUI界面，以及负责将这些输入的数据传递给类中的对应元素。（注：此时，数据不会显示在dashboard中的dataset中，想将其显示在dataset中，需要额外的函数。）关于详情见Artiq官网中的`build()`函数的详细讲解。

3. `run()`函数的前面可以定义这个函数在哪一个装置下运行，如果`run()`前没有`@kernel`，则系统不会调用artiq硬件，代码可以在PC端上运行，此时如果你在`run()`函数下定义了需要调用ttl和dds的代码，系统就会报错。而在`run()`前加入了@kernel的话，系统则会先在PC端编译代码，再按照时序在FPGA上运行编译后的代码。但由于Artiq的编译原理相当简陋，所以在@kernel下进行复杂运算、调用除了`numpy`之外的包都可能会报错。

4. 在一个`.py`文件的`.build()`函数中，我们要列举出在本文件中所有要涉及的接口，假如我们在本实验中涉及到ttl0，ttl1，我们要在`build()`函数中这样写：

   ```python
   self.setattr_device("core")
   self.setattr_device("ttl0")
   self.setattr_device("ttl1")
   ```

5. 在`run()`函数中，我们通常要加上一句刷新时间轴的代码以防止出现时间溢出类型的报错，如下：

   ```python
   self.core.reset()
   ```

### TTL 输出

1. TTL 的控制代码只能在@kernel下运行。在控制TTL的输出的时候，ttl的开可以`self.ttl.on()`来控制，ttl的关闭可以用`self.ttl.off()`来控制，中间的时长可以用delay(time*ms)来控制。

   例如我们想让ttl0开5ms，可以这样写：

   ```python
   self.ttl0.on()
   delay(5*ms)
   self.ttl0.off()
   
   或者这样写:
   ```

   ```python
   self.ttl0.pulse(5*ms)
   ```

   假如我们想控制多个ttl信号的时候，例如ttl0和ttl1同时打开5ms，我们可以这样做：

   ```python
   self.ttl0.on()
   self.ttl1.on()
   delay(5*ms)
   self.ttl0.off()
   self.ttl1.off()
   ```

   或者这样做：

   ```python
   with parallel:
   	self.ttl0.pulse(5*ms)
       self.ttl1.pulse(5*ms)
   ```

   额外的示例可以见` 三种完美示例\ttl_test.py` 文件。经测试这个文件可以完美运行。其他示例也可以见artiq官网的示例。

2. 需要格外注意的是，在控制TTL的时候，一定要格外注意我们控制的TTL接口究竟是输出接口还是输入接口。假如是输入接口，我们就不能通过代码控制这个TTL接口的输出，转而只能做TTL输入信号的分析。

3. 此外，还要说明的是，TTL的名称我们可以随意更改，若想更改TTL的名称，我们可以在`device_db.py`中更改，并且在执行代码中，我们也要相应地更改TTL的名称，例如：我们在`device_db.py`中将TTL的名称改为了729，则在执行代码的时候，我们需要将代码改成类似`self.729.on()`的形式。（理论上可行，但我没有尝试过）


### TTL 输入

1. ttl输入只能在@kernel下运行。ttl输入的模块我们一般用于光子探测，在光子探测的过程中，我们将光子探测器输出的ttl的信号接到ARTIQ的ttl输入信号接口上，我们在PC端就可以数出ttl信号的上升沿有多少个，由此我们就可以读出有多少个光子被探测到。在PC端，我们要设置我们将要处理的ttl信号侦测的时间，以及数出有多少个ttl信号的上升沿。假如我们想看出5ms内有多少个上升沿，我们可以这样写：

   ```python
   self.ttl4.gate_rising(5*ms)
   count = self.ttl4.count()
   ```

   这样在5ms内输入ttl信号的上升沿的个数就可以赋值给count这个数。

2. 值得注意的是，像我们上面这样写的时候，这意味着，在我们ttl输入信号侦测的5ms内，我们其他什么操作都做不了，假如我们希望在ttl输入信号侦测的同时，做一些其他操作的时候，我们通常可以这样写：

   ```python
   with parallel:
   	self.ttl4.gate_rising(self.DETECTION_time*ms)
   	
       with sequential:
           (the code you want to do at the same time...)
   
   count = self.ttl4.count()
   ```

   额外的示例可以见 `三种完美示例\photon_detection_text_new.py` 文件，经测试这个文件可以完美运行。

### DDS 输出

1. dds的输出只能在@kernel下运行，dds的开启可以这样写：

   ```python
   self.urukul1_ch0.sw.on()
   ```

   关于`.sw.on()`这个操作，我在官网上没有找到过，这种执行方式在artiq开发版的硬件上可以运行，但是在我们实验室的新artiq上能否运行还需进一步测试。

2. 关于dds信号的振幅调整，加入我们想将将名称为`urukul1` 的 dds功率调整成 8 dBm,我们可以这样做：

   ```python
   self.urukul1_ch0.set_att(2)
   ```

   这表示，将功率调成`10-2=8 dBm`

3. 关于dds信号的频率调整，假如我们想将名称为`urukul1`的dds输出调成1000kHz,我们可以这样写：

   ```python
   self.urukul1_ch0.set(1000*kHz)
   ```
   额外示例可以见` 三种完美示例\dds_text_new.py` 文件，经测试这个文件可以完美运行。

### 脉冲塑性

1. 脉冲塑性是为了防止量子信息操作中的AC-Stark效应而做的。它在实验控制中本质上是DDS输出，只不过需要我们额外添加的是，我们将要在一个Rabi震荡的操作周期内实现DDS振幅随时间的变化，举例如下：

   ```python
   self.urukul1_ch0.sw.on()
   t=0
   	while t<10:
   	self.urukul1_ch0.set_att(float(t))
   	delay(300*us)
       
   	t+=1
       
   self.urukul1_ch0.sw.off()
   ```

   这是指，我们先将DDS的振幅调成`10-0 = 10 dBm `，持续300us后再将振幅调整成`10-1 = 9 dBm`，依次类推，直到将dBm调整成 1 dBm。

2. 在进行脉冲塑性的操作的时候，我们要尤其注意的可能有时间溢出类型的报错。因为调整dds功率的函数执行需要时间，所以我们脉冲塑性设置的步长不能太小。太小的话会报错。

3. 扩展示例见` repository 中的 paulse_shaping.py`




# 现已完工的项目

### Rabi Scan

与Rabi scan 有关的代码在 `initial_rabi.py` 和 `Run_rabi.py` 这两个文件中。这两个文件分别对应于 `initial for Rabi` 和 ` Run As Rabi` 这两个任务

在进行Rabi scan的时候，我们要如下执行：

1. 先点击 `initial for Rabi` 的任务，于是可以弹出这个人物的GUI页面，在这个任务的GUI页面中，我们可以定义我们在Rabi Scan的时候的一些参数，例如doppler cooling的时长，sideband cooling的时长，操作次数等等。

2. 提交 `initial for Rabi` 这个任务，这些你定义过的参数会保存在dashboard里的Dataset中。

3. 点击并提交 ` Run As Rabi` 这个任务，在这个任务中，系统会自动读取dataset中你定义过的参数，并根据这些参数自动在实验中执行。光子计数器收集到的光子数会实时赋予给 Dataset 中的 Count_Num这个参数。

（这个项目我没有经过硬件上的测试，预计会有一些小的bug，但不会有大的bug）

### Zeeman Scan

与Zeeman scan 有关的代码在 `initial_zeeman.py` 和 `Run_zeeman.py` 这两个文件中。这两个文件分别对应于 `initial for Zeeman` 和 ` Run As Zeeman` 这两个任务

在进行Rabi scan的时候，我们要如下执行：

1. 先点击 `initial for Zeeman` 的任务，于是可以弹出这个人物的GUI页面，在这个任务的GUI页面中，我们可以定义我们在Zeeman Scan的时候的一些参数，例如doppler cooling的时长，sideband cooling的时长，操作次数等等。

2. 提交 `initial for Zeeman` 这个任务，这些你定义过的参数会保存在dashboard里的Dataset中。

3. 点击并提交 ` Run As Zeeman` 这个任务，在这个任务中，系统会自动读取dataset中你定义过的参数，并根据这些参数自动在实验中执行。光子计数器收集到的光子数会实时赋予给 Dataset 中的 Count_Num这个参数。

（这个项目我没有经过硬件上的测试，预计会有一些小的bug，但不会有大的bug）

### 脉冲塑性

脉冲塑性的代码在 `paulse_shaping.py`  文件中。

在代码的注解中，正如所示，在 `self.P` 数组中更改元素可以改变脉冲塑性的形状，并可以通过GUI页面来设置我们塑性的取点间隔和取点个数。

将脉冲塑性的文件代码更改好之后，就可以将脉冲塑性的代码粘贴到Rabi Scan的对应组件中。

这个项目我在硬件上测试过，这可以完美运行。



# 问题与解答

### 在@kernel下先编译再运行究竟是怎么一回事？时间溢出类型的报错究竟是怎么一回事?

对话如下：

**Q：**

如下所示，假如我们提交了这样一段代码，那么对于`a=1+1`这行代码，这行代码的运算需要时间。又由于代码是从上至下依次执行的，那么由于这行代码的存在，我们实际输出的TTL持续的时间会大于我们所设定的10ms吗？

```python
self.ttl0.on()
delay(5*ms)
a=1+1
self.ttl0.off()
```

**A:**

不会大于 10 ms, ARTIQ 的 kernel 是 real-time 的，有两种机制保证 real-time 特性： 	

1，@kernel 内的代码是先编译再运行的，而不是像 python 一样解释执行，因此像你图中这种情况，在编译阶段就可以确切知道 `a=1+1`这段代码的结果，那么就会在编译时直接将 `a`赋值为 2 ，然后再运行。类似的代码非常常用，例如:

```python
self.ttl1.pulse(self.cool_time + self.pump_time) 
```

那么就会在编译的时候算好` self.cool_time + self.pump_time `然后代进去。

2，delay(t) 函数并不是简单的等待 t 的时间，机制上，ARTIQ 内有给每一个操作（例如` ttl.on()` ）分配有 时间戳 变量，在编译过程中，`delay()` 函数负责让前后两个事件之间的时间戳的间隔为 t，而不是让系统空转 t 的时间。 

随后，当代码真正运行的时候，FPGA 内部计时器（一个可获取的变量 `time_now`）逐渐累加，当 `time_now` 和某个时间的时间戳相等的时候，就执行这个事件。

因此，考虑如下例子就能理解两个问题： 

```python
do_something_before() 
self.ttl1.on() 
delay(1*ms) 
do_something_inside() 
self.ttl.off()
```

首先，由于并不清楚`time_now`开始时间，那么完全可能，在 `do_something_before()` 后，`time_now`已经超过了`self.ttl1.on()` 的时间戳，如果这样， ARTIQ 运行（而不是编译）到这一行后就报 `underflow` 错误，然后退出运行。

所以为了避免这种情况，时序代码开始前通常有 `core.reset()`或者`core.break_realtime()`以给定时间戳偏移量的初始值。

其次，如果`do_something_inside()`花费的时间小于 1 ms, 那么后续代码不会有任何影响，因为`time_now()`还没到 `self.ttl.off()`的时间，所以系统继续等待即可，但倘若`do_something_inside()`花费的时间超过 1 ms, 那么同样在运行到 `self.ttl.off()`时得到时间溢出类报错并且停止，这时你只能想办法降低 `do_something_inside()` 的耗时或者增加 `delay()` 的时间。

总之，ARTIQ 中在 FPGA 上运行的代码，要么是严格按照定时的，要么就直接报错停止。



### 为什么我写过的代码对应的任务在dashboard中没有显示？

假如你写了一段python语言下有语法错误的代码，那么，即使你将这个文件放在了 repository 文件夹中，但是打开dashboard时，dashboard并不会识别这个文件，此时，你应该见检查你的python代码中是否有语法类型的错误。

此外，python代码中禁止出现tab类型的进位空格，否则会不识别。我们应该用四个空格来代替一个tab。
