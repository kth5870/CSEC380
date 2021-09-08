import sys
from multiprocessing.pool import ThreadPool
import ipaddress
import requests

HTTP_PORTS = [80, 443, 8080]

def scan_for_proxy(ip):
    ip_range = str(ipaddress.ip_address(ip))
    print("ips:", ip_range)
    returned_proxy = set()

    for port in HTTP_PORTS:
        proxy = "http://%s:%s" % (ip_range, port)
        # print(proxy)
        request = requests.get("https://csec.rit.edu", proxies={"http":proxy})
        if request.status_code == 200:
            returned_proxy.add(ip_range)  
    return returned_proxy

def main():
    if len(sys.argv) != 3: 
        print("Usage: python3 act4step2.py [start-ip] [end-ip]")
        sys.exit(0)

    start_ip = ipaddress.ip_address(sys.argv[1])
    end_ip = ipaddress.ip_address(sys.argv[2])
    ip = range(int(start_ip), int(end_ip) + 1)

    thread = ThreadPool(600)
    results = thread.map(scan_for_proxy, ip)
  
    thread.close()
    thread.join()

    if len(results) > 0:
        print("Found Proxy Servers:")
        for i in results:
            for ip in i:
                print("  -", ip)

if __name__ == "__main__":
    main()