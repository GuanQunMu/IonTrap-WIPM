from artiq.experiment import *
import numpy as np
import os 
import time 

class Run2(EnvExperiment):
    """test zeeman1.1"""
    def build(self):
    
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl4")
        self.setattr_device("ttl5")
        self.setattr_device("ttl8")
        self.setattr_device("ttl9")
        self.setattr_device("ttl11")
        self.setattr_device("ttl12")
        self.setattr_device("ttl30")
        self.setattr_device("ttl31")
        self.setattr_device("ttl32")
        self.setattr_device("urukul0_ch0")
        self.setattr_device("urukul0_ch1")
        self.setattr_device("urukul0_cpld")
        

    def prepare(self):
    
        self.parameter=self.get_dataset("para")
        #self.Rabi_Start=self.get_dataset("Run_Uint.Rabi.Start")
        #self.Rabi_End=self.get_datase================================================m'm'm'm'm'm'm'm'm'm'm'm'm'm'm'm'm'm'mt("Run_Uint.Rabi.End")
        #.Rabi_Step=self.get_dataset("Run_Uint.Rabi.Step")
        self.Zeeman_Frequency=self.get_dataset("Run_Uint.Zeeman.Start")
        self.Zeeman_Frequency_End=self.get_dataset("Run_Uint.Zeeman.End")
        self.Zeeman_Frequency_Step=self.get_dataset("Run_Uint.Zeeman.Step")
        self.Zeeman_Repeat=self.get_dataset("Run_Uint.Zeeman.Repeat")
        self.Zeeman_Threshould=self.get_dataset("Run_Uint.Zeeman.Threshould")
        #self.Rabi_Threshould=self.get_dataset("Run_Uint.Rabi.Threshould")

        self.Preparation_Frequency=self.get_dataset("Run_Uint.Preparation.Frequency")
        self.Preparation_Attenuation=self.get_dataset("Run_Uint.Preparation.Attenuation")
        self.Zeeman_Attenuation=self.get_dataset("Run_Uint.Zeeman.Attenuation")
        
        self.length=int((self.Zeeman_Frequency_End-self.Zeeman_Frequency)/(self.Zeeman_Frequency_Step/1000))+1
        
        
    @kernel
    def run(self):
       
        self.core.reset()

    #刷新时间轴防止报错
        delay(2*ms)
        self.urukul0_cpld.init()
        self.urukul0_ch0.init()
        self.urukul0_ch1.init()
        self.urukul0_ch0.sw.on()#控制729的三种光频率与三种功率
        self.urukul0_ch1.sw.on()
        self.ttl0.input()
        self.ttl1.input()
        self.ttl2.output()
        self.ttl4.output()
        self.ttl5.output()
        self.ttl8.output()
        self.ttl9.output()
        self.ttl11.output()
        self.ttl12.output()
        self.ttl30.output()
        self.ttl31.output()
        delay(2*ms)

        self.urukul0_ch0.set(self.Preparation_Frequency*MHz)#设置729态制备频率
        self.urukul0_ch0.set_att(self.Preparation_Attenuation)#设置729态制备功率
        self.urukul0_ch1.set_att(self.Zeeman_Attenuation)#设置729扫Zeeman功率
        
        delay(50*ms)
        
        if self.parameter==2:
            # self.length=int((self.Zeeman_Frequency_End-self.Zeeman_Frequency)/(self.Zeeman_Frequency_Step/1000))
            
            self.set_dataset("FrequncyList", np.full(self.length, np.nan), broadcast=True)
            self.set_dataset("D_List", np.full(self.length, np.nan), broadcast=True)
            
            self.set_dataset("Data", np.full(self.length, np.nan), broadcast=True)
            
            delay(1*ms)
            
            print(self.Zeeman_Frequency)
            print(self.Zeeman_Frequency_End)
            print(self.Zeeman_Frequency_Step/1000)
            
            delay(2*ms)
            
            t=0
            
            while self.Zeeman_Frequency<self.Zeeman_Frequency_End:
                
                a=0
                
                delay(1*ms)
                for i in range(100):
                    
                    t_end=self.ttl0.gate_rising(20*ms)#从当前时刻开始记录上升沿，直到括号内的时间为止。
                    t_edge=self.ttl0.timestamp_mu(t_end) 
                    
                
                    if t_edge>0:#如果探测到触发信号的上
                        at_mu(t_edge)
                        
                        delay(4*ms)
                        print(t_edge)
                        
                        self.urukul0_ch1.set(self.Zeeman_Frequency*MHz)
                        self.ttl30.on()
                        self.ttl4.on()#打开854Double Pass的AOM
                        delay(2000*us)
                        self.ttl30.off()
                        self.ttl4.off()
                        self.ttl8.on()#打开729
                        #态制备
                        delay(100*us)#持续态制备时长
                        self.ttl8.off()
                        self.ttl4.on()#将三维冷却的397光打开
                        self.ttl5.on()#将z方向的397光打开
                        self.ttl12.on()
                        delay(100*us)
                        self.ttl4.off()
                        self.ttl5.off()
                        self.ttl12.off()#关掉397Double Pass的光
                        
                        #扫描Zeeman
                        self.ttl2.on()#将三维冷却的397光打开
                        self.ttl4.on()#将z方向的397光打开
                        self.ttl5.on()
                        self.ttl11.on()
                        self.ttl12.on()
                        delay(2000*us)#持续Zeeman扫描时长
                        self.ttl2.off()
                        self.ttl4.off()
                        self.ttl5.off()
                        self.ttl11.off()
                        self.ttl12.off()
                        
                        #态探测
                        self.ttl2.on()#打开397Double Pass的AOM
                        self.ttl5.on()#打开397态探测的AOM
                        self.ttl9.on()
                        gate_end_mu=self.ttl1.gate_rising(5700*us)
                        self.ttl2.off()#打开397Double Pass的AOM
                        self.ttl5.off()#打开397态探测的AOM
                        self.ttl9.off()# 
                        num_rising_edges=self.ttl1.count(gate_end_mu)
             
                        self.set_dataset("Photon_Count",num_rising_edges, broadcast=True)
                        #计数上升沿
                        if num_rising_edges>self.Zeeman_Threshould:
                            a+=1
                        
                        self.core.reset()
                        
                
                
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
    
            
        