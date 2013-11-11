import config_python
import info
import cluster_read
import cluster_macs
import cluster_network
import cluster_dhcp
import cluster_pxe
import dhcpd

cluster_read.config("../conf_examples/cluster.conf")
cluster_macs.make()
cluster_network.make()
#Se configuran los ipmis
cluster_macs.get_ipmi_groups()
cluster_dhcp.writeconf_ipmi()
cluster_dhcp.dhcpd_ipmi()
#Se obtienen las macs apartir de los ipmis
cluster_macs.get_admin_macs_by_ipmi()
#Se escribe el dhcp de instalacion
cluster_dhcp.writeconf_allnodes()
cluster_pxe.writepxe()
cluster_dhcp.dhcpd_install()




#from cluster_properties import cluster_config
#import cluster_read
#import cluster_macaddres
#import cluster_dhcpd
#import cluster_pxe
#from colours import *
#import simplejson as json
#import sys
#
#c = cluster_config()
#c.cluster_info = cluster_read.config("../cluster.conf")
##Hasta este punto se da por sentado que existen todas las interfaces
##c.print_cluster_config()
#cluster_macaddres.conf = c.cluster_info
#macs = cluster_macaddres.getmacs()
#cluster_dhcpd.macs_json = macs
#cluster_dhcpd.conf = c.cluster_info
#cluster_dhcpd.writeconf()
#sys.exit()
#
#cluster_pxe.macs = macs['macs']
#cluster_pxe.conf = c.cluster_info
#cluster_pxe.writepxe()
