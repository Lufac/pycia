import config_python
import threading  
import dhcpd
#import tftpd
import time 
import getch
import Queue

killd_queue = Queue.Queue()
killed_power = "on"

def dhcpd_t(num):  
    print "dhcp start", num  
    dhcpd.start_server("/etc/cluster.conf/dhcpd.conf")

#def tftpd_t(num):
#    print "tftp start", num  
#    tftpd.start('/etc/cluster.conf/pxe')
  
def ciad_t(num):
    print "cia start", num

def httpd_t(num):
    print "httpd start", num

def killd_t(num):
  while killed_power == "on":
    c = getch.getch()
    if c == "k":
      killd_queue.put('k')
      break
       

t_dhcp = threading.Thread(target=dhcpd_t, args=(3, ))  
t_dhcp.start()  
#t_ftpd = threading.Thread(target=tftpd_t, args=(6, ))
#t_ftpd.start()
#t_httpd = threading.Thread(target=httpd_t, args=(8, ))
#t_httpd.start()
#t_ciad = threading.Thread(target=ciad_t, args=(9, ))
#t_ciad.start()
t_killd = threading.Thread(target=killd_t, args=(9, ))
t_killd.start()

time.sleep(2)
while True:
  if not dhcpd.q_dhcp.empty():
    print "[DHCP] ofrecido",  dhcpd.q_dhcp.get()
  if not dhcpd.q_tftp.empty():
    print "[TFTP] initrd mandado a:",  str(dhcpd.q_tftp.get())
#  if not tftpd.q.empty():
#    print "[TFTPD] ofrecido",  dhcpd.q.get()
  if not killd_queue.empty():
    print "Matando esta cosa"
    break
dhcpd.power = "off" 
#tftpd.power = "off"
killed_power = "off"

