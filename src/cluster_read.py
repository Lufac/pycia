import info
import json, re
from colours import *
import tools 
import netifaces

#-> Validar que los values esten bien formados
#-> Validara que si alguna propiedad es una ruta exista el archivo
#-> Checar que la propiedad nodes de los grupos sea mayor que 1
#-> Cehcar que las interfaces existan

def config(fname = "cluster.conf"):
    tools.header_msg( __name__ + ": Reading conf file in json format ...")

    data = json.load(open(fname))
    grupos = data['grupos']
    if len(grupos) == 0:
      tools.error_msg("Not find groups in [" + fname + "]")

    for grupo in grupos:
      if 'ipmi' in grupos[grupo]:
        iface = grupos[grupo]['ipmi']['iface']
        check_iface(iface," in ipmi group" + grupo)
      iface = grupos[grupo]['iface_install']
      check_iface(iface," in group" + grupo)
    info.cluster = data
    tools.footer_msg()


def check_iface(iface,error_msg = "bad interface"):
  a = re.compile(r'\Aeth[0-9]\Z')
  if not a.match(iface):
    tools.error_msg(error_msg)
  try:
    netinfo = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
    tools.insert_dict( info.net, [iface], netinfo)
  except ValueError as e:
    print "\n\nSomething WRONG with iface (" + iface + "): " + error_msg
