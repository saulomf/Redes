#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class MyFirstTopo( Topo ):
    "Simple topology example."
    def __init__(self):
        "Create custom topo."
		# Initialize topology
        Topo.__init__(self)
		# Add hosts and switches
        h1 = self.addHost( 'h1', ip='192.168.1.0/28' )
        h2 = self.addHost( 'h2', ip='192.168.1.16/28' )
        h3 = self.addHost( 'h3', ip='192.168.1.32/28' )
        h4 = self.addHost( 'h4', ip='192.168.1.48/28' )

        h5 = self.addHost( 'h5', ip='192.168.1.64/29' )
        h6= self.addHost( 'h6', ip='192.168.1.72/29' )
        h7 = self.addHost( 'h7', ip='192.168.1.80/29' )
        h8 = self.addHost( 'h8', ip='192.168.1.88/29' )

        Switch_1 = self.addSwitch( 's1', ip='192.168.1.100/30')
        Switch_2 = self.addSwitch( 's2', ip='192.168.1.112/30')
        Switch_3 = self.addSwitch( 's3', ip='192.168.1.128/30')
        Switch_4 = self.addSwitch( 's4', ip='192.168.1.140/30')
        Switch_5 = self.addSwitch( 's5', ip='192.168.1.96/30')
        Switch_6 = self.addSwitch( 's6', ip='192.168.1.124/30')
        Switch_7 = self.addSwitch( 's7' )
		# Add links
        self.addLink( h1, Switch_1 )
        self.addLink( h2, Switch_1 )
        self.addLink( h3, Switch_2 )
        self.addLink( h4, Switch_2 )
        self.addLink( h5, Switch_3 )
        self.addLink( h6, Switch_3 )
        self.addLink( h7, Switch_4 )
        self.addLink( h8, Switch_4 )

        self.addLink( Switch_1, Switch_5 )
        self.addLink( Switch_2, Switch_5 )
        self.addLink( Switch_3, Switch_6 )
        self.addLink( Switch_4, Switch_6 )
        self.addLink( Switch_5, Switch_7 )
        self.addLink( Switch_6, Switch_7 )

topos = { 'myfirsttopo': ( lambda: MyFirstTopo() ) }

def runExperiment():
    "Create and test a simple experiment"
    topo = MyFirstTopo()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
	setLogLevel('info')
	runExperiment()
