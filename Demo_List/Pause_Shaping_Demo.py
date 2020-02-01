from artiq.experiment import *
import numpy as np

class Test_dds(EnvExperiment):
    
    """paulse_shaping"""
    
    #脉冲塑性的功率变化存于这个数组中
    def prepare(self):
        self.P=[120,12,9,6,4,3,3,3,3,3,4,6,9,12,120]
        
    def build(self):
        
        self.setattr_argument("dt", NumberValue(3, scale=1,unit="us",step=10))
        self.setattr_argument("times", NumberValue(100, scale=1,unit="次",step=10))
        
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul1_ch1")
        
    @kernel
    def run(self):
        self.core.reset()
        delay(10*ms)
        # self.ttl4.output()
        self.urukul1_ch0.sw.on()
        self.urukul1_ch0.set_att(5.0)
        delay(100*ms)
        self.urukul1_ch1.sw.on()
        self.urukul1_ch1.set_att(5.0)
        delay(100*ms)
        
        self.urukul1_ch0.set(10*MHz)
        self.urukul1_ch1.set(10*MHz)
        delay(100*ms)
        try:
            p=0
            while p<self.times:
                t=0
                while t<len(self.P):
                    
                    self.urukul1_ch0.set_att(float(self.P[t]))
                    delay(self.dt*us)
                    
                    t+=1
                p+=1
            
            self.urukul1_ch0.sw.off()
            self.urukul1_ch1.sw.off()

        except RTIOUnderflow:
            print("Error for time")
            
            
