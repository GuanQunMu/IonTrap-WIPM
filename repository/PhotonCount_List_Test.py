import numpy as np
from artiq.experiment import *
class Photon_Detection22(EnvExperiment):
    """Photon_Detction"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")	

    #假设gate_rising语法和delay语法作用一样，则可以成功
    @kernel
    def run(self):
        self.core.reset()
        self.ttl0.input()
        delay(10*ms)
        try:
            while True:
                self.set_dataset("Time", np.full(1000, np.nan), broadcast=True)
                self.set_dataset("Photon_Counts", np.full(1000, np.nan), broadcast=True)
                delay(100*ms)
                for i in range(1000):
                    gate_end_mu = self.ttl0.gate_rising(200 * ms)
                    delay(1*ms)
                    Num_get_risings = self.ttl0.count(gate_end_mu)
                    self.set_dataset("gate_risings",Num_get_risings,broadcast=True)
                    self.mutate_dataset("Photon_Counts", i, Num_get_risings)
                    self.mutate_dataset("Time", i, i)
                    #self.analyse(i, Num_get_risings)
            
        except RTIOUnderflow:
            print("Error for time")
            
    
    #def analyse(self, time, count):
    #    self.array1.append(time)
    #    self.array2.append(count)
    #    self.set_dataset("gate_risings",count,broadcast=True)
    #    self.set_dataset("Photon_Counts",self.array2,broadcast=True)
    #    self.set_dataset("Time",self.array1,broadcast=True)
        