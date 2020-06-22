from artiq.experiment import *
import numpy as np

class LED(EnvExperiment):
    """ttl test"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl4")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl4.output()
        delay(10*ms)
        try:
            while True:
                self.ttl4.on()
                delay(500*ns)
                self.ttl4.off()
                delay(500*ns)
              
            
        except RTIOUnderflow:
            #时间溢出报错时会打印"Error for time"
            print("Error for time")
    