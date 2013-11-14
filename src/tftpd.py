import socket,binascii,os
from math import ceil
from sys import exit
import Queue

q = Queue.Queue()

host = ''
port = 69
pxe_basedir = "./"

def group(self, s, n): return [s[i:i+n] for i in xrange(0, len(s), n)]

power = "on"

def start(pxe_dir='/etc/cluster.conf'):
  print "[tfptd] Initializing tftp server"
  print "[tfptd] Directory of pxe files: " + pxe_dir
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(( host, port))
  last=()
  os.chdir(pxe_dir)
  print "[tfptd] Working in: " + os.getcwd()
  while power == "on":
      message, address = s.recvfrom(8192)
      if last == address: continue
      print "hola"
      if message.startswith('\x00\x01'): #WRQ
        message=message.split('\x00')
        filename=message[1][1:]
        print address,"wants",repr(filename)
        # Se concatena el directorio donde se encuentran pxe files
        filename = filename
        if not os.path.exists(filename):
          print "[tfptd] no such file exists: " + filename
          s.sendto('\x00\x05\x00\x01no such file exists',address)
          continue
        print "[tfptd] file " + os.path.basename(filename) + " ok" 
        fsize=os.path.getsize(filename)
        s.sendto('\x00\x06blksize\x00512\x00tsize\x00%s\x00' % fsize,address)
      elif message.startswith('\x00\x04'): #OptACK
        last=address
        f=open(filename,'r')
        data=f.read()
        dataset=self.group(data,512)
        if len(dataset) > 65534: print "Won't work, too large... >64MB"
        for index,chunk in enumerate(dataset):
          try:
            s.sendto('\x00\x03'+binascii.unhexlify(hex(index+1)[2:].rjust(4,'0'))+chunk,address)
          except TypeError:
            break
          s.recvfrom(128)
        s.sendto('\x00\x03'+binascii.unhexlify(hex(index+2)[2:].rjust(4,'0')),address)
        if os.path.basename(filename) == "initrd.img":
          q.put(address)
          break
        f.close() 
  print "[tfptd] Terminating server..."
  s.close()
  return True

#Para pruebas unitarias
if __name__ == '__main__':
   t = tftp('/var/www/html/pycia/paquetes/PyPXE')
   t.start()
