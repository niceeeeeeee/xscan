import time
import argparse
import xcheck
import xscan
from multiprocessing import Pool
import sys,os

def usage():
  parser = argparse.ArgumentParser(description="Servcie Discover Toolkit.")
  parser.add_argument("mode", choices=['tcp_scan','syn_scan','xmas_scan','fin_scan','null_scan','window_scan','udp_scan'], help="select scan mode")
  parser.add_argument("-host", help="target ip, example -host '1.1.1.1','1.1.1.1,2.2.2.2','1.1.1.1/24,2.2.2.2/24'" )
  parser.add_argument("-port", help="target port,example -port '80','80,8080','1-65535'")
  parser.add_argument("-pool", default=1 ,help="pool between 1 and 100")
  parser.add_argument("-outputfile", default="host_port_status.txt" ,help="output filename")
  parser.add_argument("-proxy", default="null" ,help="ip:port")
  parser.add_argument("-timeout", default=1 ,help="set timeout")
  return parser.parse_args()

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

if __name__ == '__main__':
    print time.asctime( time.localtime(time.time()) )
    result_list = []
    args = usage()
    check_list = xcheck.check_argvs(args)
    blockPrint()
    p = Pool(int(args.pool))
    for address,port in check_list:
        p.apply_async(xscan.check,args=(address,int(port),int(args.timeout),args.mode,args.outputfile,args.proxy,))
    p.close()
    p.join()
    enablePrint()
    print time.asctime( time.localtime(time.time()) )
