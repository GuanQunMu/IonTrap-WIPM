from artiq.experiment import *
import sys
import numpy as np
import os

class AWG(EnvExperiment):
    """AWG"""

    def build(self):
        pass
    
    def prepare(self):
        pass
        
    def run(self):
        os.system('C:\\Users\Administrator\Desktop\IonTrap-WIPM-master\AWG4100-Python64\AWG.bat')