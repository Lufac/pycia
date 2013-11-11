import config_python
import info
import tools
import dhcpd
import ipmi

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
  tools.writefile("dhcpd.conf.ipmi",f,type="conf")
  tools.footer_msg()


def dhcpd_ipmi():
  tools.header_msg("Setting IPMI devices with dhcp...")
  dhcpd.start_ipmi("/etc/cluster.conf/dhcpd.conf.ipmi")
  tools.footer_msg()


def writeconf_allnodes():
  tools.header_msg("Generating dhdcp.conf file for ALL nodes...")

  f = "ddns-update-style none; \n"
  f = f + "shared-network cluster{\n"

  for iface in info.net:
    subnet = info.net[iface]['net']
    netmask = info.net[iface]['netmask']
    f = f + "\tsubnet " + subnet + " netmask " + netmask + " {\n"
    f = f + "\t\tdefault-lease-time 3600;\n"
    f = f + "\t\tmax-lease-time 4800;\n"
    f = f + "\t\toption subnet-mask " + netmask + ";\n"
    print "Processing subnet " + subnet + "..." 
    for grupo in info.net[iface]['grupos']:
        nodes_grupo = info.macs[grupo]['nodes']
        nodes = info.macs[grupo]['num_nodes']
        type = info.macs[grupo]['type']
        print "Processing grupo " + grupo + " con " + str(nodes) + " nodos..." 
        for i in range(1, nodes + 1):
          print "Processing node " + str(i) + " del grupo " + grupo + "..." 
          mac, ip, machine = nodes_grupo[i]
          f = f + "\t\thost " + machine + " {\n"
          f = f + "\t\t\thardware ethernet " + mac + ";\n"
          f = f + "\t\t\toption host-name \"" + machine + "\";\n"
          f = f + "\t\t\tfixed-address " + ip + ";\n"
          if type == 'nodes': 
            f = f + "\t\t\tfilename \"pxelinux/pxelinux.0\";\n"
          f = f + "\t\t}\n"
        #print f
    f = f + "\t}\n"
  f = f + "}\n"
  print f
  tools.writefile("dhcpd.conf",f,type="conf")
  tools.footer_msg()

def dhcpd_install():
  tools.header_msg("Sarting dhcpd...")
  dhcpd.start_install("/etc/cluster.conf/dhcpd.conf")
  tools.footer_msg()


#Para pruebas unitarias
if __name__ == '__main__':
  print "Pruebas unitarias"
  info.macs = {u'blade-ipmi': {'group_ref': u'blade', 'iface': u'eth1', 'type': 'ipmi', 'nodes': {1: ('00:25:90:45:45:86', '172.16.0.1', u'blade-ipmi1'), 2: ('00:25:90:45:45:58', '172.16.0.2', u'blade-ipmi2')}, 'num_nodes': 2}, u'blade': {'nodes': {1: ('00:25:90:44:04:b4', '172.16.0.3', u'blade1'), 2: ('00:25:90:44:04:58', '172.16.0.4', u'blade2')}, 'iface': u'eth1', 'type': 'nodes', 'num_nodes': 2}}
  info.cluster = {u'grupos': {u'blade': {u'kernel': u'../boot/x86_64/vmlinuz', u'ks_bench': u'bonnie,hoomd_openmp', u'iface_install': u'eth1', u'ipmi': {u'iface': u'eth1'}, u'ks_type': u'base', u'ks_distro': u'centos6/x86_64', u'kernel_params': u'ip=dhcp nicdelay=60 linksleep=60 noipv6 noselinux selinux=0 headless xdriver=vesa nomodeset sshd', u'initrd': u'../boot/x86_64/initrd.img', u'ks_storage': u'normal', u'gw': u'172.16.253.253', u'nodes': 2}}, u'master': {"tftp_dir" : "/var/lib/tftpboot/pxelinux/pxelinux.cfg"}}
#  info.net = {u'eth1': {'grupos': {u'blade-ipmi': 0, u'blade': 0}, 'ip': IPNetwork('172.16.253.253/16'), 'net': '172.16.0.0', 'contador': IPAddress('172.16.0.1'), 'netmask': '255.255.0.0'}}
  info.print_macs()
  info.print_cluster()
  info.print_net()
  dhcpd_install()

