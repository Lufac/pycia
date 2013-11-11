import subprocess as sp

class pyipmi():

  user = "ADMIN"
  passw = "ADMIN"

  def __init__(self):
    child = sp.Popen("extras/ipmitool", stdout=sp.PIPE, stderr=sp.PIPE, shell=True)  
    retcode = child.wait()
    if retcode != 1:
      raise Exception("ipmitool command dosen't exist")

  def ipmitool( self, ip):
    return "ipmitool -U " + self.user +  " -P " + self.passw + " -H " + ip + " " 

  def execute_ipmi(self, ip, cmd, err_msg):
    error_msg = "Erro: " + err_msg + " in machine: " + ip
    cmd = self.ipmitool(ip) +  cmd
#    print cmd
    child = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    retcode = child.wait()
    if retcode != 0:
      raise Exception( err_msg + '\n' + child.stderr.read() )
    return child.stdout.read()


  def get_adminMAC( self, ip):
    mac = self.execute_ipmi(ip, "raw 0x30 0x21","Error getting admin mac")
    return ":".join( mac.split('\n')[0].split(' ')[5:11])

  def get_PowerStatus( self, ip):
    status = self.execute_ipmi(ip, "power status","Error getting Power Satus")
    return status.split('\n')[0].split(' ')[3]

  def set_IPstatic( self, ip):
    cmd = "lan set 1 ipsrc static"
    self.execute_ipmi(ip, cmd, "setting ip static")
  
  def set_IPdhcp( self, ip):
    cmd = "lan set 1 ipsrc dhcp"
    self.execute_ipmi(ip, cmd, "setting ip dhcp")

  def set_BootPxe( self, ip):
    cmd = "chassis bootdev pxe"
    self.execute_ipmi(ip, cmd, "setting PXE boot")

  def set_BootBios( self, ip):
    cmd = 'chassis bootdev bios'
    self.execute_ipmi(ip, cmd, "setting BIOS boot")

  def set_PowerOn( self, ip):
    cmd = 'chassis power on'
    self.execute_ipmi(ip, cmd, "Power ON")

  def set_PowerOFF( self, ip):
    cmd = 'chassis power off'
    self.execute_ipmi(ip, cmd, "Power OFF")
  
  def set_PowerRESET( self, ip):
    cmd = 'chassis power reset'
    self.execute_ipmi(ip, cmd, "Power RESET")

  def set_identify( self, ip, sec=180):
    cmd = 'chassis identify ' + str(sec)
    self.execute_ipmi(ip, cmd, "chassis identify")


# Para pruebas unitarias
if __name__ == '__main__':
    import re, time
    py = pyipmi()
   
    ip = "172.16.0.1"
    set = re.compile(r'^set_*')
    get = re.compile(r'^get_*')
    for i in dir(py):
      if get.match(i):
        print "Testing [ " + i + " ]..."
        func = getattr(py,i)
        print  func(ip)
    for i in dir(py):
      if i == "set_IPdhcp":
        print "Probar individualmente [ " + i + " ]..."
      if set.match(i):
        if i == "set_IPdhcp":
          print "Probar individualmente [ " + i + " ]..."
          continue
        print "Testing [ " + i + " ]..."
        #func = getattr(py,i)
        print "Pause to verify ... "
        time.sleep(120)
    
