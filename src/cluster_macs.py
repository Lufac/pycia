import info
import tools
import catchMAC
from colours import *

def make():
  tools.header_msg("Initializing macs data ...")
  grupos = info.cluster['grupos']
  for grupo in grupos:
    if 'ipmi' in grupos[grupo]:
      grupo_name = grupo + '-ipmi'
      tools.insert_dict(info.macs, [grupo_name,'iface'], grupos[grupo]['ipmi']['iface'])
      tools.insert_dict(info.macs, [grupo_name,'type'], "ipmi")
      tools.insert_dict(info.macs, [grupo_name,'num_nodes'], grupos[grupo]['nodes'])
      tools.insert_dict(info.macs, [grupo_name,'group_ref'], grupo)
      total_macs_ipmi = int()
    tools.insert_dict(info.macs, [grupo,'iface'], grupos[grupo]['iface_install'])
    tools.insert_dict(info.macs, [grupo,'type'], "nodes")
    tools.insert_dict(info.macs, [grupo,'num_nodes'], grupos[grupo]['nodes'])
  tools.footer_msg()

def get_ipmi_groups():
  tools.header_msg("Gettting IPMI mac's data ...")
  #info.print_macs()

  #Primero se obtienen los ipmis
  for grupo in info.macs:
    iface = info.macs[grupo]['iface']
    type = info.macs[grupo]['type']
    nodes = info.macs[grupo]['num_nodes']
    ip = info.net[iface]['contador']
    if type == "ipmi":
      for i in range( 1, nodes + 1):
        printout("Getting MAC of node " + str(i) + " of group " + grupo, WHITE)
        mac = catchMAC.get_interactive(iface)
        #mac = "11:11:11:11:11:11"
        tools.insert_dict(info.macs, [grupo,'nodes',i], ( mac, str(ip), grupo + str(i) ) ) 
        ip = ip + 1
    info.net[iface]['contador'] = ip
  info.print_macs()

def get_admin_macs_by_ipmi():
  tools.header_msg("Gettting IPMI mac's data ...")
  info.print_macs()

  #Primero se obtienen los ipmis
  for grupo in info.macs:
    if type == "ipmi":
    
