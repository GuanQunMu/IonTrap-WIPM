from artiq.experiment import *


class LED(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl4")

    @kernel
    def run(self):
        try:    
            self.core.reset()
            self.ttl4.output()
            self.ttl4.on()
            delay(3*ms)
            self.ttl4.off()
            delay(3*ms)
        
        except RTIOUnderflow:
            print("Error for time")
