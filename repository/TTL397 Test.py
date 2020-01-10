
from artiq.experiment import *

import numpy as np

class TTL_397(EnvExperiment):
    "397 TTL Test"
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl4")#397
        self.setattr_device("ttl6")
        self.setattr_device("ttl8")
        self.setattr_device("ttl10")

        self.parameter1=1
        # 目前2&3 Switch 反向，接的为RF OUT 2
        # 注：Switch 接RF OUT1 为反向，接RF OUT2 为正向
        # Switch 2&3 RF OUT1 正常，RF OUT2 可能是坏了 
        self.parameter2=0
        self.parameter3=0

        self.parameter4=1

    @kernel
    def run(self):
        self.core.reset()
        
        try:
            if self.parameter1==1:
                self.ttl4.on()
                if self.parameter2==1:
                    self.ttl6.on()
                elif self.parameter2==0:
                    self.ttl6.off()
                if self.parameter3==1:
                    self.ttl8.on()
                elif self.parameter3==0:
                    self.ttl8.off()
                if self.parameter4==1:
                    self.ttl10.on()
                elif self.parameter4==0:
                    self.ttl10.off()

            elif self.parameter1==0:
                self.ttl4.off()
        
        except RTIOUnderflow:
            #时间溢出报错时会打印"Error for time"
            print("Error for time")
