import info
import tools
import catchMAC
import ipmi
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
  tools.header_msg("Gettting admin mac's data by IPMI...")
  #info.print_macs()
  ipmitool = ipmi.pyipmi()

  #Primero se obtienen los ipmis
  for grupo in info.macs:
    type = info.macs[grupo]['type']
    if type == "ipmi":
      grupo_admin = info.macs[grupo]['group_ref']
      iface_admin = info.macs[grupo_admin]['iface']
      nodes = info.macs[grupo]['num_nodes']
      ip_admin = info.net[iface_admin]['contador']
      print "Configuring admin group: " + grupo_admin
      print "Configuring iface admin group: " + iface_admin + " contador=" + str(ip_admin)
      for i in range( 1, nodes + 1):
        mac_ipmi, ip_ipmi, nname_ipmi = info.macs[grupo]['nodes'][i]
        mac_node = ipmitool.get_adminMAC(ip_ipmi)
        print "MAC " + mac_node + " of node " + str(i) + " of group " + grupo_admin
        tools.insert_dict(info.macs, [grupo_admin,'nodes',i], ( mac_node, str(ip_admin), grupo_admin + str(i) ) )
        ip_admin = ip_admin + 1
      info.net[iface_admin]['contador'] = ip_admin
  info.print_macs()






