from subprocess import Popen, PIPE
from colours import *
import getch


mac_selected = {}

def getcmd(m_iface):
  printout("Listening tcpdump in " + m_iface + "...",GREEN)
  cmd = "tcpdump -lenx -s 1500 -c 1 -i " + m_iface + " port bootps or port bootpc 2>/dev/null | dhcpdump"
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True)
  p.wait()
  out = p.stdout.read()
  if not out:  #catch if error in Popen
    error_msg("TCPdump Error in out check if exist interface") 
  mac = out.split()[32].split(':')
  mac = mac[0] + ":" + mac[1] + ":" + mac[2] + ":" + mac[3] + ":" + mac[4] + ":" + mac[5]
  vendor = out.split()[59]
  return mac,vendor

def get_interactive(m_iface):
  bad_macs = {}
  while True:
    mac,vendor = getcmd(m_iface)
    if mac in bad_macs:
      printout("MAC addres " + mac + " already deny", RED)
      continue
    if mac in mac_selected:
      printout("MAC addres " + mac + " already selected", GREEN)
      continue
    printout("Continue with (" + vendor + ")(" + mac + ")? y/n >>>",GREEN)
    c = getch.getch()
    if c == "y":
      printout("Working with MAC: " +  mac,GREEN)
      mac_selected[mac] = vendor
  #####print "Bad macs" +  str(bad_macs)
      return mac
    else:
      printout("Add MAC " + mac + " to deny", RED)
      bad_macs[mac] = vendor
      continue
