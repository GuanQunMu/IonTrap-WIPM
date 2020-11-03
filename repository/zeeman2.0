from artiq.experiment import *
import numpy as np
import os 
import time 

class Run2(EnvExperiment):
    """test zeeman2.3"""
    def build(self):
    
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl4")
        self.setattr_device("ttl6")
        self.setattr_device("ttl8")
        self.setattr_device("ttl10")
        self.setattr_device("ttl12")
        self.setattr_device("ttl14")
        self.setattr_device("ttl16")
        self.setattr_device("ttl18")
        self.setattr_device("ttl20")
        self.setattr_device("ttl22")
        self.setattr_device("ttl24")
        self.setattr_device("ttl26")
        self.setattr_device("ttl28")
        self.setattr_device("ttl30")
        self.setattr_device("ttl32")
        self.setattr_device("urukul2_ch1")
        self.setattr_device("urukul2_ch2")
        self.setattr_device("urukul2_cpld")#定义设备
        
    def prepare(self):
    
        self.parameter=self.get_dataset("para")
        #self.Rabi_Start=self.get_dataset("Run_Uint.Rabi.Start")
        #self.Rabi_End=self.get_datase================================================m'm'm'm'm'm'm'm'm'm'm'm'm'm'm'm'm'm'mt("Run_Uint.Rabi.End")
        #.Rabi_Step=self.get_dataset("Run_Uint.Rabi.Step")
        self.Zeeman_Frequency=self.get_dataset("Run_Uint.Zeeman.Start")
        self.Zeeman_Frequency_End=self.get_dataset("Run_Uint.Zeeman.End")
        self.Zeeman_Frequency_Step=self.get_dataset("Run_Uint.Zeeman.Step")
        #self.Zeeman_Repeat=self.get_dataset("Run_Uint.Zeeman.Repeat")
        #self.Zeeman_Threshould=self.get_dataset("Run_Uint.Zeeman.Threshould")
        #self.Rabi_Threshould=self.get_dataset("Run_Uint.Rabi.Threshould")

        #self.Preparation_Frequency=self.get_dataset("Run_Uint.Preparation.Frequency")
        #self.Preparation_Attenuation=self.get_dataset("Run_Uint.Preparation.Attenuation")
        #self.Zeeman_Attenuation=self.get_dataset("Run_Uint.Zeeman.Attenuation")

        self.length=int((self.Zeeman_Frequency_End-self.Zeeman_Frequency)/(self.Zeeman_Frequency_Step/1000))+1
        
        
    @kernel
    def run(self):
        print(66)
        self.core.reset()

        #刷新时间轴防止报错
        delay(2*ms)
        self.urukul2_cpld.init()
        self.urukul2_ch2.init()
        self.urukul2_ch1.init()
        self.urukul2_ch2.sw.on()#控制729的三种光频率与三种功率
        self.urukul2_ch1.sw.on()
        self.ttl2.input()
        self.ttl1.input()
        self.ttl0.input()
        self.ttl4.output()
        self.ttl6.output()
        self.ttl8.output()
        self.ttl10.output()
        self.ttl18.output()
        self.ttl12.output()
        self.ttl14.output()
        self.ttl16.output()
        self.ttl20.output()
        self.ttl22.output()
        delay(50*ms)

        print("ok1")



        #self.urukul0_ch0.set(self.Preparation_Frequency*MHz)             #设置729态制备频率
        #self.urukul0_ch0.set_att(self.Preparation_Attenuation)              #设置729态制备功率
        #self.urukul0_ch1.set_att(self.Zeeman_Attenuation)                   #设置729扫Zeeman功率

        #delay(50*ms)

        if self.parameter==2:
            self.length=int((self.Zeeman_Frequency_End-self.Zeeman_Frequency)/(self.Zeeman_Frequency_Step/1000))
            
            self.set_dataset("FrequncyList", np.full(self.length, np.nan), broadcast=True)
            self.set_dataset("D_List", np.full(self.length, np.nan), broadcast=True)
            
            self.set_dataset("Data", np.full(self.length, np.nan), broadcast=True)
            
            delay(15*ms)
            
            print(self.Zeeman_Frequency)
            print(self.Zeeman_Frequency_End)
            print(self.Zeeman_Frequency_Step/1000)
            
            

            t=0
            
            while self.Zeeman_Frequency<self.Zeeman_Frequency_End:
                
                #print(self.Zeeman_Frequency)
                
                delay(200*ms)
                self.urukul2_ch1.set(self.Zeeman_Frequency*MHz)
                self.urukul2_ch1.set_att(4.0)
                delay(5*ms)
                a=0
                delay(5*ms)
                
                #print(1)
                for i in range(1000):
                    #try:
                        
                    print('ok')
                    t_end=self.ttl1.gate_rising(20*ms)#从当前时刻开始记录上升沿，直到括号内的时间为止。
                    t_edge=self.ttl1.timestamp_mu(t_end) 
                    
                    
                        #rtio = self.core.get_rtio_counter_mu()
                        #now = now_mu()
                        #print(rtio-now)
                    if t_edge>0:#如果探测到触发信号的上
                    
                        at_mu(t_edge)
                        delay(7*ms)
                        print(t_edge)
                        
                        self.ttl20.off()#打开397Double pass                            
                        self.ttl4.off()#打开大功率AOM
                        self.ttl8.on()#打开397-Z-小功率-Doppler cooling
                        self.ttl10.on()#关闭397-x&y-Doppler cooling
                        delay(2*ms)
                        self.ttl20.on()#关闭397Double pass 
                        self.ttl8.off()#打开397-z-大功率-态探测
                        self.ttl6.on()#关闭854Double pass
                        self.ttl22.on()#关闭854小功率
                        self.ttl18.off()#打开729Double Pass的AOM
                        delay(2*ms)
                        self.ttl18.on()#关闭729Double Pass的AOM
                        self.ttl20.off()#打开397Double Pass的AOM
                        self.ttl10.off()#打开397--x&y的AOM 
                        
                                               
                        gate_end_mu = self.ttl0.gate_rising(5700*us)
                            #记录探测时长内的上升沿并计数
                        delay(3.5*ms)
                        num_rising_edges=self.ttl0.count(gate_end_mu)
                        
                        self.set_dataset("Photon_Count",num_rising_edges, broadcast=True)
                        
                        self.ttl6.off()#打开854-Double pass
                        self.ttl22.off()#打开854大功率

                     
                        if num_rising_edges>0:
                            a+=1
                       
                        #self.core.reset()
                        #self.core.wait_until_mu(now_mu())
                        
                        delay(1*ms)


                    #except RTIOUnderflow:
            #时间溢出报错时会打印"Error for time"
                        #print("Error for time")
                        
                self.ttl20.off()#打开397Double pass 
                self.ttl10.off()#打开397--x&y的AOM         
                self.ttl6.off()#打开854-Double pass
                self.ttl22.off()#打开854大功率        
                
                
                D=1-a/100
                
                self.mutate_dataset("FrequncyList", t, self.Zeeman_Frequency)
                self.mutate_dataset("D_List", t, D)
                
                t+=1
                
                self.Zeeman_Frequency+=self.Zeeman_Frequency_Step/1000
                    
                    
                    
                    

            
            
            
    def analyze(self):

        try:
            name=time.strftime("%F")
            filename="E:/data/"+str(name) 
            os.mkdir(filename)
        except:
            pass
            
        D_List=self.get_dataset("D_List")
        FrequncyList=self.get_dataset("FrequncyList")
        
        
        name1=time.strftime("%H-%M-%S")+"-Zeeman"
        filename1=filename+"/"+str(name1)
        
        file=open(filename1+".txt","a")
        str4="Fre"
        str5="Jump"
        str6=str4+"     "+str5+"\n"
        file.write(str6)
        for i in range(self.length):
            str1=str(D_List[i])
            str2=str(FrequncyList[i])
            str3=str2+"     "+str1+"\n"
            file.write(str3)
        
        file.close()
    
