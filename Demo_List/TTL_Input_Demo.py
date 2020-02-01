import numpy as np
from artiq.experiment import *
class Photon_Detection22(EnvExperiment):
	#"""Photon_Detction"""
	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl1")	
		self.array1 = []
		self.array2 = []

	@kernel
	def run(self):
		self.core.reset()
		try:
			for i in range(10000000):
				self.core.break_realtime()
				gate_end_mu = self.ttl1.gate_rising(200 * ms)
				Num_get_risings = self.ttl1.count(gate_end_mu)
				#print(Num_get_risings)
				self.analyse(200*i, Num_get_risings)
		except RTIOUnderflow:
			print("Error for time")
			
	def analyse(self, time, count):
		self.array1.append(time)
		self.array2.append(count)
		self.set_dataset("Photon_Counts",self.array2,broadcast=True)
		self.set_dataset("Time",self.array1,broadcast=True)
