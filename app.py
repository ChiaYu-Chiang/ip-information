import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from ip_tool import (
    get_hostname,
    get_cache_from_local_dns,
    get_ipaddr_list,
    get_ipinfo_detail,
)
from forms import URLForm

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# > $set access_token="access_token from https://ipinfo.io/account/token"
app.config["access_token"] = os.environ.get("access_token")
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def home():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data

        local_catch = get_cache_from_local_dns(url)
        name = local_catch[0]
        aliases = local_catch[1]
        ips = get_ipaddr_list(url)

        ipdetail_list = []
        for ipnum in range(0, len(ips)):
            ip = ips[ipnum]
            hostname = get_hostname(ip)
            ipinfo = get_ipinfo_detail(ip, ipinfo_api_token=app.config["access_token"])
            ipdetail_list.append([ip, hostname, ipinfo])

        return render_template(
            "beauti_home.html",
            iplist=ipdetail_list,
            name=name,
            aliases=aliases,
            url=url,
            form=form,
        )
    form.url.data = ""
    return render_template("beauti_home.html", form=form)
