import os
from flask import Flask, render_template, request
from ip_tool import get_hostname, get_ipaddr_list, get_ipinfo_detail

app = Flask(__name__)

# > $set access_token="access_token from https://ipinfo.io/account/token"
app.config["access_token"] = os.environ.get("access_token")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.values['send']=='送出':
            url = request.values['url']
            ips = get_ipaddr_list(url)

            ipdetail_list = []
            for ipnum in range(0, len(ips)):
                ip = ips[ipnum]
                hostname = get_hostname(ip)
                ipinfo = get_ipinfo_detail(ip, ipinfo_api_token=app.config["access_token"])
                ipdetail_list.append([ip, hostname, ipinfo])

            return render_template("home.html", iplist = ipdetail_list)

    return render_template("home.html")