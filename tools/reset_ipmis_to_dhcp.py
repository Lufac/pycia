import sys, os
sys.path.append(sys.path[0] + '/../src')
import ipmi

p = ipmi.pyipmi()
ips = ['172.16.0.1','172.16.0.2']

for ip in ips:
  print "Reseting", ip
  p.set_IPdhcp(ip)
