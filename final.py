#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
  	s1 = self.addSwitch('s1')    ## Adds a Switch
  	s2 = self.addSwitch('s2')    ## Adds a Switch
  	s3 = self.addSwitch('s3')    ## Adds a Switch
  	s4 = self.addSwitch('s4')    ## Adds a Switch
  	s5 = self.addSwitch('s5')    ## Adds a Switch

        h1 = self.addHost('h1',mac='00:00:00:00:00:01',
		ip='10.0.1.1/24', defaultRoute="h1-eth0")       ## Adds a Host
        h2 = self.addHost('h2',mac='00:00:00:00:00:02',
		ip='10.0.1.2/24', defaultRoute="h2-eth0") 	 ## 6 more
        h3 = self.addHost('h3',mac='00:00:00:00:00:03',
		ip='10.0.2.1/24', defaultRoute="h3-eth0") 
        h4 = self.addHost('h4',mac='00:00:00:00:00:04',
		ip='10.0.2.2/24', defaultRoute="h4-eth0") 
        h5 = self.addHost('h5',mac='00:00:00:00:00:05',
		ip='10.0.3.1/24', defaultRoute="h5-eth0") 
        h6 = self.addHost('h6',mac='00:00:00:00:00:06',
		ip='10.0.3.2/24', defaultRoute="h6-eth0") 
        h7 = self.addHost('h7',mac='00:00:00:00:00:07',
		ip='10.0.4.1/24', defaultRoute="h7-eth0")

	self.addLink(s2,h1, port1=8, port2=0)
	self.addLink(s2,h2, port1=9, port2=0)
	self.addLink(s3,h3, port1=8, port2=0)
	self.addLink(s3,h4, port1=9, port2=0)
	self.addLink(s4,h5, port1=8, port2=0)
	self.addLink(s4,h6, port1=9, port2=0)
	self.addLink(s5,h7, port1=8, port2=0)

	self.addLink(s1,s2, port1=8, port2=10)
	self.addLink(s1,s3, port1=9, port2=10)
	self.addLink(s1,s4, port1=10, port2=10)
	self.addLink(s1,s5, port1=11, port2=9)	

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
