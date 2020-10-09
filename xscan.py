#! /usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #This is supress scapy warnings
from scapy.all import *

def check(dst_ip,dst_port,dst_timeout,mode,filename,proxy):

    if proxy != 'null':
        import socket
        import socks
        ip = (proxy.split(':'))[0]
        port = (proxy.split(':'))[1]
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
    else:
        pass

    src_port = RandShort()

    if mode == 'tcp_scan':
        res = tcp_scan(dst_ip,dst_port,src_port,dst_timeout)
    elif mode == 'syn_scan':
        res = syn_scan(dst_ip,dst_port,src_port,dst_timeout)
    elif mode == 'xmas_scan':
        res = xmas_scan(dst_ip,dst_port,dst_timeout)
    elif mode == 'fin_scan':
        res = fin_scan(dst_ip,dst_port,dst_timeout)
    elif mode == 'null_scan':
        res = null_scan(dst_ip,dst_port,dst_timeout)
    elif mode == 'window_scan':
        res = window_scan(dst_ip,dst_port,dst_timeout)
    elif mode == 'udp_scan':
        res = udp_scan(dst_ip,dst_port,dst_timeout)
    else:
        print 'mode wrong'

    if "Open" in res:
        with open(filename,"a+") as f:
            f.write(dst_ip + " "+ str(dst_port) + "\n")
        f.close()
    else:
        pass

def tcp_scan(dst_ip,dst_port,src_port,dst_timeout):
    tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
    if(str(type(tcp_connect_scan_resp))==""):
        print "Closed"
    elif(tcp_connect_scan_resp.haslayer(TCP)):
        if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
            send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
            print "Open"
    elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
        print "Closed"

def syn_scan(dst_ip,dst_port,src_port,dst_timeout):
    stealth_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
    if(str(type(stealth_scan_resp))==""):
        print "Filtered"
    elif(stealth_scan_resp.haslayer(TCP)):
        if(stealth_scan_resp.getlayer(TCP).flags == 0x12):
            send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="R"),timeout=10)
            print "Open"
        elif (stealth_scan_resp.getlayer(TCP).flags == 0x14):
            print "Closed"
    elif(stealth_scan_resp.haslayer(ICMP)):
        if(int(stealth_scan_resp.getlayer(ICMP).type)==3 and int(stealth_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            print "Filtered"

def xmas_scan(dst_ip,dst_port,dst_timeout):
    xmas_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="FPU"),timeout=dst_timeout)
    if (str(type(xmas_scan_resp))=="<type 'NoneType'>"):
        return "Open|Filtered"
    elif(xmas_scan_resp.haslayer(TCP)):
        if(xmas_scan_resp.getlayer(TCP).flags == 0x14):
            return "Closed"
    elif(xmas_scan_resp.haslayer(ICMP)):
        if(int(xmas_scan_resp.getlayer(ICMP).type)==3 and int(xmas_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            return "Filtered"
    else:
        return "CHECK"


def fin_scan(dst_ip,dst_port,dst_timeout):
    fin_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="F"),timeout=dst_timeout)
    if (str(type(fin_scan_resp))=="<type 'NoneType'>"):
        return "Open|Filtered"
    elif(fin_scan_resp.haslayer(TCP)):
        if(fin_scan_resp.getlayer(TCP).flags == 0x14):
            return "Closed"
    elif(fin_scan_resp.haslayer(ICMP)):
        if(int(fin_scan_resp.getlayer(ICMP).type)==3 and int(fin_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            return "Filtered"
    else:
        return "CHECK"

def null_scan(dst_ip,dst_port,dst_timeout):
    null_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags=""),timeout=dst_timeout)
    if (str(type(null_scan_resp))=="<type 'NoneType'>"):
        return "Open|Filtered"
    elif(null_scan_resp.haslayer(TCP)):
        if(null_scan_resp.getlayer(TCP).flags == 0x14):
            return "Closed"
    elif(null_scan_resp.haslayer(ICMP)):
        if(int(null_scan_resp.getlayer(ICMP).type)==3 and int(null_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            return "Filtered"
    else:
        return "CHECK"


def window_scan(dst_ip,dst_port,dst_timeout):
    window_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="A"),timeout=dst_timeout)
    if (str(type(window_scan_resp))=="<type 'NoneType'>"):
        return "No response"
    elif(window_scan_resp.haslayer(TCP)):
        if(window_scan_resp.getlayer(TCP).window == 0):
            return "Closed"
        elif(window_scan_resp.getlayer(TCP).window > 0):
            return "Open"
    else:
        return "CHECK"

def udp_scan(dst_ip,dst_port,dst_timeout):
    udp_scan_resp = sr1(IP(dst=dst_ip)/UDP(dport=dst_port),timeout=dst_timeout)
    if (str(type(udp_scan_resp))=="<type 'NoneType'>"):
        retrans = []
        for count in range(0,3):
            retrans.append(sr1(IP(dst=dst_ip)/UDP(dport=dst_port),timeout=dst_timeout))
        for item in retrans:
            if (str(type(item))!="<type 'NoneType'>"):
                udp_scan(dst_ip,dst_port,dst_timeout)
        return "Open|Filtered"
    elif (udp_scan_resp.haslayer(UDP)):
        return "Open"
    elif(udp_scan_resp.haslayer(ICMP)):
        if(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code)==3):
            return "Closed"
        elif(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code) in [1,2,9,10,13]):
            return "Filtered"
    else:
        return "CHECK"
