import requests
import random
import time
import argparse
from multiprocessing import Pool
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

user_agent_list = [
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def usage():
    parser = argparse.ArgumentParser(description="Web Discover Toolkit.")
    parser.add_argument("-proxy", default="null" ,help="http:ip:port")
    parser.add_argument("-httpmode", default="null", help="select UA mode")
    parser.add_argument("-filepath", default="host_port_status.txt", help="file path" )
    parser.add_argument("-pool", default=1 ,help="pool between 1 and 100")
    parser.add_argument("-outputfile", default="web_status.txt" ,help="output filename")
    return parser.parse_args()

def check(address,proxy,httpmode,filename):

    if proxy != 'null':
        status = (proxy.split(':'))[0]
        address = ((proxy.split(':'))[1]) + ':' + ((proxy.split(':'))[2])
        proxy_ = {status:address}
    else:
        proxy_ = {}

    if httpmode == 'random':
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3'}

    http_url = "http://" + address
    https_url = "https://" + address
    try:
        response = requests.get(http_url, headers=headers,proxies=proxy_, timeout=1)
        if response.status_code:
            if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
	        pass
            else:
	        with open("web_status.txt","a+") as f:
		    f.write(http_url + "\n")
                f.close()
    except Exception as e:
        pass

    try:
        response = requests.get(https_url, headers=headers,proxies=proxy_,verify=False,timeout=1)
        if response.status_code:
            if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
                pass
            else:
                with open("web_status.txt","a+") as f:
                    f.write(https_url + "\n")
                f.close()
    except Exception as e:
        pass

if __name__ == '__main__':
    print time.asctime( time.localtime(time.time()) )
    args = usage()
    with open(args.filepath, "r") as f:
        data_list = f.readlines()
    p = Pool(int(args.pool))
    for info in data_list:
        address = (info.replace(' ',':')).strip()
        #check(address,args.proxy,args.httpmode,args.outputfile)
        p.apply_async(check,args=(address,args.proxy,args.httpmode,args.outputfile,))
    p.close()
    p.join()
    print time.asctime( time.localtime(time.time()) )
