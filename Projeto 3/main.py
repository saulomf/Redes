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

        #h1 = self.addHost( 'h1', ip='192.168.1.0/28' )
        #h2 = self.addHost( 'h2', ip='192.168.1.16/28' )
        #h3 = self.addHost( 'h3', ip='192.168.1.32/28' )
        #h4 = self.addHost( 'h4', ip='192.168.1.48/28' )
        hosts = []
        ips = '/28'
        i = 0
        j = 0
        k = 1
        ipi = 1
        while i < 4:
            while j < 10:
                host = 'h'
                ip='192.168.1.'
                ip = ip + str(ipi) + ips
                hosts.append(self.addHost(host + str(k), ip=ip))
                ipi = ipi+1
                k = k+1
                j = j+1
            j = 0
            i = i+1
            if i == 1:
                ipi = 17
            if i == 2:
                ipi = 33
            if i == 3:
                ipi = 49

        #h5 = self.addHost( 'h5', ip='192.168.1.64/29' )
        #h6= self.addHost( 'h6', ip='192.168.1.72/29' )
        #h7 = self.addHost( 'h7', ip='192.168.1.80/29' )
        #h8 = self.addHost( 'h8', ip='192.168.1.88/29' )
        ips = '/29'
        i = 0
        j = 0
        ipi = 65
        while i < 4:
            while j < 6:
                host = 'h'
                ip='192.168.1.'
                ip = ip + str(ipi) + ips
                hosts.append(self.addHost(host + str(k), ip=ip))
                ipi = ipi+1
                k = k+1
                j = j+1
            j = 0
            i = i+1
            if i == 1:
                ipi = 73
            if i == 2:
                ipi = 81
            if i == 3:
                ipi = 89


        Switch_1 = self.addSwitch( 's1', ip='192.168.1.100/30')
        Switch_2 = self.addSwitch( 's2', ip='192.168.1.112/30')
        Switch_3 = self.addSwitch( 's3', ip='192.168.1.128/30')
        Switch_4 = self.addSwitch( 's4', ip='192.168.1.140/30')
        Switch_5 = self.addSwitch( 's5', ip='192.168.1.96/30')
        Switch_6 = self.addSwitch( 's6', ip='192.168.1.124/30')
        Switch_7 = self.addSwitch( 's7' )

		# Add links
        #self.addLink( h1, Switch_1 )
        #self.addLink( h2, Switch_1 )
        #self.addLink( h3, Switch_2 )
        #self.addLink( h4, Switch_2 )
        #self.addLink( h5, Switch_3 )
        #self.addLink( h6, Switch_3 )
        #self.addLink( h7, Switch_4 )
        #self.addLink( h8, Switch_4 )
        i = 0
        while i <= len(hosts):
            if i < 20:
                self.addLink( hosts[i], Switch_1 )
            if i > 19 and i <40:
                self.addLink( hosts[i], Switch_2 )
            if i > 39 and i <53:
                self.addLink( hosts[i], Switch_3 )
            if i > 52 and i <len(hosts):
                self.addLink( hosts[i], Switch_4 )
            i=i+1

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
