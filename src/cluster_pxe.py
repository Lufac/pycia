import config_python
from colours import *
from netaddr import *
import tools 
import info
import os

def writepxe():
  tools.header_msg("Writing PXE files... ")
  pxe_dir = '/etc/cluster.conf/pxe/pxelinux/pxelinux.cfg'
  for grupo in info.macs:
    printout("Processing group: " + grupo,GREEN)
    type = info.macs[grupo]['type']
    ######## Solo los nodes tienen pxe
    if type == 'nodes':
      iface = info.macs[grupo]['iface']
      ip_webserver = str(info.net[iface]['ip']).split('/')[0]
      printout("\tip webserver: " + ip_webserver,GREEN)
      for i in info.macs[grupo]['nodes']:
        printout("\t\tProcessing node: " + str(i) + " of group " + grupo,GREEN)
        mac, ip, nname = info.macs[grupo]['nodes'][i] 
        s = "default install\n"
        s = s + "prompt 1\n"
        s = s + "timeout 10\n"
        s = s + "display display.msg\n"
        s = s + "\n"
        s = s + "label localboot\n"
        s = s + "\t\tLOCALBOOT 0\n"
        s = s + "\n"
        s = s + "label install\n"
        s = s + "\tKERNEL " + info.cluster['grupos'][grupo]['kernel'] +"\n"

        initrd = "\tAPPEND initrd=" + info.cluster['grupos'][grupo]['initrd'] + " "
        initrd = initrd + info.cluster['grupos'][grupo]['kernel_params'] + " " 
        initrd = initrd + "ksdevice=" + mac + " " 
        ks_path = "ks=http://" + ip_webserver + "/kickstart/getks.php?"
        ks_path = ks_path + "ks_type=" + info.cluster['grupos'][grupo]['ks_type'] + "&"
        ks_path = ks_path + "gw=" + info.cluster['grupos'][grupo]['gw'] + "&"
        ks_path = ks_path + "hostname=" + nname + '&'
        ks_path = ks_path + "storage=" + info.cluster['grupos'][grupo]['ks_storage'] + '&'
        if not info.cluster['grupos'][grupo]['ks_bench']:
          ks_path = ks_path + "bench=" + info.cluster['grupos'][grupo]['ks_bench'] + '&'
        ks_path = ks_path + "distro=" + info.cluster['grupos'][grupo]['ks_distro']

        s = s + initrd + ks_path
#      #s = s + "\tAPPEND initrd=../boot/x86_64/initrd.img ip=dhcp nicdelay=60 linksleep=60 noipv6 ksdevice=eth0 noselinux selinux=0 headless xdriver=vesa nomodeset sshd  ks=http://192.168.1.253/kickstart/getks.php?ks_type=base&gw=192.168.1.1&hostname=node3&storage=normal&bench=bonnie,hoomd_openmp&distro=centos6/x86_64  \n"
        s = s + "\tIPAPPEND 2\n"
        s = s + "EOF\n"
        pxe_fname = "01-" + "-".join(mac.split(':'))
        tools.writefile( pxe_fname, s, pxe_dir, type="pxe")
  tools.footer_msg()




#Para pruebas unitarias
if __name__ == '__main__':
  print "Pruebas unitarias"
  info.macs = {u'blade-ipmi': {'group_ref': u'blade', 'iface': u'eth1', 'type': 'ipmi', 'nodes': {1: ('00:25:90:45:45:86', '172.16.0.1', u'blade-ipmi1'), 2: ('00:25:90:45:45:58', '172.16.0.2', u'blade-ipmi2')}, 'num_nodes': 2}, u'blade': {'nodes': {1: ('00:25:90:44:04:b4', '172.16.0.3', u'blade1'), 2: ('00:25:90:44:04:58', '172.16.0.4', u'blade2')}, 'iface': u'eth1', 'type': 'nodes', 'num_nodes': 2}}
  info.cluster = {u'grupos': {u'blade': {u'kernel': u'../boot/x86_64/vmlinuz', u'ks_bench': u'bonnie,hoomd_openmp', u'iface_install': u'eth1', u'ipmi': {u'iface': u'eth1'}, u'ks_type': u'base', u'ks_distro': u'centos6/x86_64', u'kernel_params': u'ip=dhcp nicdelay=60 linksleep=60 noipv6 noselinux selinux=0 headless xdriver=vesa nomodeset sshd', u'initrd': u'../boot/x86_64/initrd.img', u'ks_storage': u'normal', u'gw': u'172.16.253.253', u'nodes': 2}}, u'master': {"tftp_dir" : "/var/lib/tftpboot/pxelinux/pxelinux.cfg"}}
  info.net = {u'eth1': {'grupos': {u'blade-ipmi': 0, u'blade': 0}, 'ip': IPNetwork('172.16.253.253/16'), 'net': '172.16.0.0', 'contador': IPAddress('172.16.0.1'), 'netmask': '255.255.0.0'}}
  info.print_macs()
  info.print_cluster()
  info.print_net()
  writepxe() 
