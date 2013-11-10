import info
import tools
import dhcpd

def writeconf_ipmi():
  tools.header_msg("Generating dhdcp.conf file for IPMI nodes...")
  
  f = "ddns-update-style none; \n"
  f = f + "shared-network cluster{\n"

  for iface in info.net:
    subnet = info.net[iface]['net']
    netmask = info.net[iface]['netmask']
    f = f + "\tsubnet " + subnet + " netmask " + netmask + " {\n"
    f = f + "\t\tdefault-lease-time 3600;\n"
    f = f + "\t\tmax-lease-time 4800;\n"
    f = f + "\t\toption subnet-mask " + netmask + ";\n"
    for grupo in info.net[iface]['grupos']:
      if info.macs[grupo]['type'] == 'ipmi':
        nodes_grupo = info.macs[grupo]['nodes'] 
        nodes = info.macs[grupo]['num_nodes']
        for i in range(1, nodes + 1):
          mac, ip, machine = nodes_grupo[i]
          f = f + "\t\thost " + machine + " {\n"
          f = f + "\t\t\thardware ethernet " + mac + ";\n"
          f = f + "\t\t\toption host-name \"" + machine + "\";\n" 
          f = f + "\t\t\tfixed-address " + ip + ";\n"
          f = f + "\t\t\tfilename \"pxelinux/pxelinux.0\";\n"
          f = f + "\t\t}\n"
    f = f + "\t}\n"
  f = f + "}\n"
  #print f
  tools.writefile("dhcpd.conf",f,type="conf")
  tools.footer_msg()

def dhcpd_ipmi():
  tools.header_msg("Setting IPMI devices with dhcp...")
  dhcpd.start("/etc/cluster.conf/dhcpd.conf")
    

  tools.footer_msg()
