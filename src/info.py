import config_python
import json
import tools
import pickle
from colours import *

cluster = {}
macs = {}
net = {}

def read_from_files(folder = "/etc/cluster.conf"):
  global cluster
  global macs
  global net
#  cluster = json.load(open(folder + "/cluster.json"))
#  macs = json.load(open(folder + "/macs.json"))
  net = pickle.load(open(folder + "/net.json", 'rb'))
  macs = pickle.load(open(folder + "/macs.json", 'rb'))
  cluster = pickle.load(open(folder + "/cluster.json", 'rb'))

def write_to_files():
#  tools.writefile("cluster.json",cluster,"/etc/cluster.conf",type="json")
#  tools.writefile("macs.json",macs,"/etc/cluster.conf",type="json")
  pickle.dump(cluster, open('/etc/cluster.conf/cluster.json', 'wb'))
  pickle.dump(macs, open('/etc/cluster.conf/macs.json', 'wb'))
  pickle.dump(net, open('/etc/cluster.conf/net.json', 'wb'))

def get_ipmi_nodes():
  total_nodes_ipmi = 0
  for grupo in cluster['grupos']:
    if 'ipmi' in cluster['grupos'][grupo]:
      total_nodes_ipmi = total_nodes_ipmi + int(cluster['grupos'][grupo]['nodes'])
  return total_nodes_ipmi

def get_install_nodes():
  total_nodes = 0
  for grupo in cluster['grupos']:
      total_nodes = total_nodes + int(cluster['grupos'][grupo]['nodes'])
  return total_nodes

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
  print_net()
  print_macs()
  print_cluster() 

if __name__ == '__main__':
  write_to_files()
