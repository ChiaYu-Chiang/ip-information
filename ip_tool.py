import re
import socket
import ipinfo


# nslookup: domain name to ip address
def get_ipaddr_list(qfdn):
    ip_list = []
    qfdn = re.sub(r"^https?://|/$", "", qfdn)
    ais = socket.getaddrinfo(qfdn, 0, 0, 0, 0)
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    return ip_list


# nslookup: domain name to aliases
def get_cache_from_local_dns(qfdn):
    qfdn = re.sub(r"^https?://|/$", "", qfdn)
    host_ex = socket.gethostbyname_ex(qfdn)
    name = host_ex[0]
    alias_list = list(host_ex[1])
    return (name, alias_list)


# ping –a: ip address to hostname
def get_hostname(ip_addr):
    hostname = socket.getfqdn(ip_addr)
    return hostname


# ipinfo:
def get_ipinfo_detail(ip_addr, ipinfo_api_token):
    access_token = ipinfo_api_token
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_addr)
    return (details.org, details.country_name, details.city)


# simple test region
if __name__ == "__main__":
    ipinfo_api_token = input("Please enter your ipinfo_api_token: ")
    url = "www.sugar.com.tw"
    ipaddr = "13.213.231.25"

    iplist = get_ipaddr_list(url)
    print(iplist)

    local_catch = get_cache_from_local_dns(url)
    name = local_catch[0]
    alias = local_catch[1]
    print(name)
    print(alias)

    hostname = get_hostname(ipaddr)
    print(hostname)

    ASN, Country, City = get_ipinfo_detail(ipaddr, ipinfo_api_token)
    print(ASN, Country, City)
