from artiq.experiment import *
import numpy as np

class Test_dds(EnvExperiment):
    """test DDS"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul1_cpld")
        
    @kernel
    def run(self):
  
        self.core.reset()
        delay(10*ms)
        # self.ttl4.output()
        self.urukul1_cpld.init()
        self.urukul1_ch0.init()
        self.urukul1_ch0.sw.on()
        self.urukul1_ch0.set_att(4.0)
        delay(100*ms)
        try:
            self.urukul1_ch0.set(200*MHz)
            delay(30000*ms)
            self.urukul1_ch0.set(300*MHz)
            delay(30000*ms)
            self.urukul1_ch0.set(100*MHz)
            delay(30000*ms)

            self.urukul1_ch0.sw.off()
            
        except RTIOUnderflow:
            print("Error for time")
