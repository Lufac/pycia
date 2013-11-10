import json
from colours import *

cluster = {}
macs = {}
net = {}

def get_ipmi_nodes():
  total_nodes_ipmi = 0
  for grupo in cluster['grupos']:
    if 'ipmi' in cluster['grupos'][grupo]:
      total_nodes_ipmi = total_nodes_ipmi + int(cluster['grupos'][grupo]['nodes'])
  return total_nodes_ipmi

def print_net():
  printout("++++++++++++++++++++ net data info+++++++++++",RED)
  print net
  #printout(json.dumps(net, sort_keys=True, indent=2),RED)

def print_macs():
  printout("++++++++++++++++++++ macs data info+++++++++++",RED)
  printout(json.dumps(macs, sort_keys=True, indent=2),RED)

def print_cluster():
  printout("++++++++++++++++++++ clsuter data info+++++++++++",RED)
  printout(json.dumps(cluster, sort_keys=True, indent=2),RED)

def print_all_data():
  print_ifaces()
  print_macs()
  print_cluster() 
