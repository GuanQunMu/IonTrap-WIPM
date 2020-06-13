from artiq.experiment import *                  #imports everything from artiq experiment library

#This code demonstrates how to use a TTL pulse(channel0) to trigger another event.
#In this code the event being triggered is another ttl pulse 
#however the same principle can be used to trigger an experimental sequence.
#pulses occur 5.158us appart with about 1ns jitter

class TTL_Trigger(EnvExperiment):
	"""Trigger"""
	def build(self):
		self.setattr_device("core")             #sets drivers of core device as attributes
		self.setattr_device("ttl1")
		self.setattr_device("ttl5")             #sets drivers of TTL4 as attributes
		self.setattr_device("ttl6")             #sets drivers of TTL6 as attributes
        
	@kernel #this code runs on the FPGA
	def run(self):
		self.core.reset()                       #resets core device
		self.ttl1.input()
		self.ttl5.output()                       #sets TTL0 as an input
		self.ttl6.output()                       #sets TTL0 as an input                   #sets TTL6 as an output
		delay(1*us) 
		for i in range(1000000):                            #1us delay, necessary for using trigger, no error given if removed
			gate_end_mu=self.ttl1.gate_rising(20*ms)    #opens gate for rising edges to be detected on TTL0 for 10ms
													#sets variable t_end as time(in MUs) at which detection stops                                        
			t_edge=self.ttl1.timestamp_mu(gate_end_mu)  #sets variable t_edge as time(in MUs) at which first edge is detected
													#if no edge is detected, sets t_edge to -1
			if t_edge>0:                          #runs if an edge has been detected
				at_mu(t_edge)
				delay(5*us)                       #set time cursor to position of edge
				self.ttl5.on()
				self.ttl6.on()
				delay(3*ms)
				self.ttl5.off()
				delay(3*ms)
				self.ttl6.off()
			self.ttl1.count(gate_end_mu)                       #5us delay, to prevent underflow               #outputs 5ms pulse on TTL6
			self.core.reset()
