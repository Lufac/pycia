import config_python
from subprocess import Popen, PIPE
import os
import Queue 
import tools
import info
import time
import tftp

def start_ipmi(f_conf="/etc/dhcpd.conf"):
  f_lease = "/tmp/lease.file"
  if not os.path.exists(f_lease): 
    tools.warning_msg("Creating lease file: " + f_lease) 
    open(f_lease, 'a').close()
  if not os.path.exists(f_conf):
    error_msg("dhcpd.conf dosen't exist")
  total_ipmi_macs = info.get_ipmi_nodes() 
  cmd = "dhcpd -4 -d -cf " + f_conf + " -lf " + f_lease
  print cmd
  print "Sleeping 5 seconds ..."
  time.sleep(5)
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True)
  while True: 
    s = p.stderr.readline()
    s = s.split()
    #print "linea dhcpd: ", s
    if s: #checa que la slida no este vacia
      if s[0] == 'DHCPOFFER':
        print "Finding DHCPOFFER... " + str(s)
        set_ip = s[2]
        set_mac = s[5] 
        print "Setting MAC " +  set_mac + " with ip: " + set_ip
        total_ipmi_macs = total_ipmi_macs - 1
        print "Missing " + str(total_ipmi_macs) + " MAC's"
    if total_ipmi_macs == 0:
      print "Completed all MAC's"
      print "killing in 10 seconds"
      time.sleep(10)
      p.kill()
      break

def start_install(f_conf):
  tftp_server = tftp.tftp('/etc/cluster.conf/pxe')
  f_lease = "/tmp/lease.file"
  if not os.path.exists(f_lease):
    tools.warning_msg("Creating lease file: " + f_lease)
    open(f_lease, 'a').close()
  if not os.path.exists(f_conf):
    error_msg("dhcpd.conf dosen't exist")
  total_install_nodes = info.get_install_nodes()
  cmd = "dhcpd -4 -d -cf " + f_conf + " -lf " + f_lease
  print cmd
  print "Sleeping 5 seconds ..."
  print "Installling " + str(total_install_nodes) + " nodes"
  time.sleep(5)
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True) 
  while power == "on":
    s = p.stderr.readline()
    s = s.split()
    print "linea dhcpd: ", s
    if s: #checa que la slida no este vacia
      if s[0] == 'DHCPOFFER':
        print "Finding DHCPOFFER... " + str(s)
        tftp_server.start()
        ip = s[2]
        mac = s[4]
        q.put(mac)

power = "on"
q_dhcp = Queue.Queue()
q_tftp = Queue.Queue()
def start_server(f_conf):
  tftp_server = tftp.tftp('/etc/cluster.conf/pxe')
  f_lease = "/tmp/lease.file"
  if not os.path.exists(f_lease):
    tools.warning_msg("Creating lease file: " + f_lease)
    open(f_lease, 'a').close()
  if not os.path.exists(f_conf):
    error_msg("dhcpd.conf dosen't exist")
  cmd = "dhcpd -4 -d -cf " + f_conf + " -lf " + f_lease
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True)
  while power == "on":
    s = p.stderr.readline()
    s = s.split()
    #print "linea dhcpd: ", s
    if s: #checa que la slida no este vacia
      if s[0] == 'DHCPOFFER':
        #print "[DHCPD] Finding DHCPOFFER... " + str(s)
        ip = s[2]
        mac = s[4]
        q_dhcp.put(mac)
        addr = tftp_server.start()
        q_tftp.put(mac)
        time.sleep(5)
  print "[DHCPD] terminating"
  p.kill()  
