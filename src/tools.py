from colours import *
import simplejson as json
import os, shutil

def writefile(fname,data,confdir="/etc/cluster.conf",type="json"):
  #Escribir archivos de configuracion en el directorio /etc/cluster.conf
  #Validar que exista si no crearlo
  if not os.path.exists(confdir):
    warning_msg("Creating conf directory: " + confdir)
    os.makedirs(confdir)
  pathfile = confdir + "/" + fname
  if os.path.exists(pathfile):
    warning_msg("Making backup of: " + pathfile)
    shutil.move(pathfile,pathfile + '.old')
  file_conf = open(pathfile,'w')
  printout("Writing " +  type + " file: " + pathfile, GREEN)
  if type == "json":
    file_conf.write(json.dumps(data, sort_keys=True, indent=2))
  if type == "conf":
    file_conf.write(data)
  if type == "pxe":
    file_conf.write(data)
  file_conf.close()

def header_msg(msg):
  printout("++++++++++++++++++++++++++++++++++++++++++++",CYAN)
  printout(msg,BLUE)
  printout("++++++++++++++++++++++++++++++++++++++++++++",CYAN)

def footer_msg():
  #printout("--------------------------------------------\n",CYAN)
  print

def warning_msg(msg=""):
  printout("WARNNING: " + msg,WHITE)

def error_msg(msg=""):
  printout(msg,RED)
  sys.exit()

def critical_data_check(d, msg):
  if not d:
    printout(msg,RED)
    sys.exit()

def insert_dict(cur, list, value):
    if len(list) == 1:
        cur[list[0]] = value
        return
    if not cur.has_key(list[0]):
        cur[list[0]] = {}
    insert_dict(cur[list[0]], list[1:], value)
