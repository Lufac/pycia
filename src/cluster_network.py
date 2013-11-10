import info
import tools
from netaddr import *

def make():
  tools.header_msg("Creating network data ...")
  #info.print_net()
  #info.print_macs()

  data ={}
  for grupo in info.macs:
    iface = info.macs[grupo]['iface']
    tools.insert_dict(data, [iface,'grupos',grupo], 0)

  for iface in data:
    ip = info.net[iface]['addr']
    netmask = info.net[iface]['netmask']
    ip = IPNetwork(ip + "/" + netmask)
    tools.insert_dict( data, [iface,'net'], str(ip.network))
    tools.insert_dict( data, [iface,'ip'], ip)
    tools.insert_dict( data, [iface,'netmask'], netmask)
    tools.insert_dict( data, [ iface, 'contador'], ip.network + 1)
  
  info.net = data
  info.print_net()
  tools.footer_msg()
