import random

def check_argvs(args):
    result_list = []

    if ',' and '/24' in args.host:
        host_list = (args.host).split(',')
        host_list = clearup(host_list)
    elif ',' in args.host and '/24' not in args.host:
        host_list = (args.host).split(',')
    else:
        host_list = []
        host_list.append(args.host)
    
    if '-' in args.port:
        start_num = int(((args.port).split('-'))[0])
        finish_num = int(((args.port).split('-'))[1]) + 1
        port_list = list(range(start_num,finish_num))
    elif ',' in args.port:
        port_list = (args.port).split(',')
    else:
        port_list = []
        port_list.append(args.port)

    for host_ip in host_list:
        for port in port_list:
            result_list.append([host_ip,port])

    random.shuffle(result_list)
    return result_list

def clearup(host_list):
    result_list = []

    for ip_c in host_list:
        l = ip_c.split('.')
        i = l[0]+'.'+l[1]+'.'+l[2]+'.'
        for q in range(1,256):
            ip = i+str(q)
            result_list.append(ip)
    return result_list

if __name__=='__main__':
    host_list = ['1.1.1.1/24','2.2.2.2/24']
    check_ip(host_list)
    
