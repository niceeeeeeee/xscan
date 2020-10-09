# xscan  

xscan是一款简单高效的端口扫描及web服务探测工具，在某些场景对开源扫描工具检测较为严格，极有可能导致IP封禁，对后续工作造成不便。

## 端口扫描  main.py 

**端口扫描Demo**

```python
python main.py xmas_scan -host "xx.xx.xx.xx/24" -port "xx,xx" -pool 100  
```

**参数说明**  

-mode       端口嗅探模式 tcp_scan,syn_scan,xmas_scan，fin_scan，null_scan，window_scan，udp_scan

-proxy      指定代理 "ip:port",不使用代理：默认不使用代理

-host       目标地址 单个ip：'1.1.1.1'，多个ip：'1.1.1.1,2.2.2.2'，ip段：'1.1.1.1/24,2.2.2.2/24'

-port       目标端口 单个端口：'80'，多个端口：'80,8080'，全端口：'1-65535'，任意端口：'1-20'

-pool       并发数量 并发1：1，并发100: 100

-outputfile 输出文件 指定：xxx.txt，默认：host_port_status.txt

-timeout    超时时间 指定：'10'，默认：1s

## web服务检测  xhttp.py

**web服务检测Demo**

```python
python xhttp.py -pool 100  
```

**参数说明**

-proxy      http代理 指定代理："http:ip:port" or "https:ip:port"，不使用代理：默认不使用代理

-httpmode   http UA头 随机UA头：random，不使用随机UA头：默认不使用随机UA头

-filepath   ip端口信息 指定txt文件读取："/xxx/xxx/xx/xx.txt" ，文件格式 ip port \n，默认读取端口扫描结果 host_port_status.txt

-pool       并发数量 并发1：1，并发100: 100

-outputfile 输出文件 指定：xxx.txt，默认：web_status.txt

