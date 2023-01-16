import re
import socket
import ipinfo

# nslookup: domain name to ip address


def get_ipaddr_list(fqdn):
    ip_list = []
    fqdn = re.sub(r"^https?://|/$", "", fqdn)
    ais = socket.getaddrinfo(fqdn, 0, 0, 0, 0)
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    return ip_list


# nslookup: domain name to aliases
def get_cache_from_local_dns(fqdn):
    try:
        fqdn = re.sub(r"^https?://|/$", "", fqdn)
        host_ex = socket.gethostbyname_ex(fqdn)
        name = host_ex[0]
        alias_list = list(host_ex[1])
        return (name, alias_list)
    except socket.gaierror as e:
        return None

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
