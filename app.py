import os
import re
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from models import db, Search
from forms import URLForm
from werkzeug.exceptions import HTTPException
from ip_tool import (
    get_hostname,
    get_cache_from_local_dns,
    get_ipaddr_list,
    get_ipinfo_detail,
)


app = Flask(__name__)
bootstrap = Bootstrap5(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# > $set access_token='access_token from https://ipinfo.io/account/token'
app.config["access_token"] = os.environ.get("access_token")
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# configure the log handler
log_handler = TimedRotatingFileHandler(
    "logs/app.log", when='D', interval=1)
log_handler.suffix = "%Y_%m_%d"

# logging file format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)-15s - %(levelname)-8s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    # add the log handler to the app
    handlers=[log_handler],
)


# log status after every request


@app.after_request
def get_status_code(response):
    user_ip = request.headers["X-Forwarded-For"] or "127.0.0.1"
    status_code = response.status
    logging.info(
        "Request: method=%s, status=%s, path=%s, user_ip=%s",
        request.method,
        status_code,
        request.path,
        user_ip,
    )
    return response


# insert data after every request with form submitted
@app.after_request
def save_to_database(response):
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        fqdn = re.sub(r"^https?://|/$", "", url)
        ip = request.headers["X-Forwarded-For"] or "127.0.0.1"

        result = get_cache_from_local_dns(fqdn)
        if result is None:
            return response
        search = Search(fqdn=fqdn, ip=ip)
        db.session.add(search)
        db.session.commit()

    return response


# auto import objects when using flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Search=Search)


# main page
@app.route("/", methods=["GET", "POST"])
def home():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        url = re.sub(r"^https?://|/$", "", url)
        local_catch = get_cache_from_local_dns(url)
        if local_catch is None:
            error_message = "找不到FQDN"
            return render_template("beauti_home.html", error_message=error_message, form=form), 500

        name = local_catch[0]
        aliases = local_catch[1]
        ips = get_ipaddr_list(url)

        ipdetail_list = []
        for ipnum in range(0, len(ips)):
            ip = ips[ipnum]
            hostname = get_hostname(ip)
            ipinfo = get_ipinfo_detail(
                ip, ipinfo_api_token=app.config["access_token"])
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


@app.errorhandler(403)
def forbidden(error):
    message = "Access denied"
    return render_template("403.html", message=message), 403


@app.errorhandler(404)
def page_not_found(error):
    message = "This page dose not exist"
    return render_template("404.html", message=message), 404


@app.errorhandler(Exception)
def app_errorhandler(e):
    if isinstance(e, HTTPException):
        return e
    message = "Oops! Something went wrong. Please come back in a while."
    return render_template("500.html", message=message), 500


if __name__ == "__main__":
    app.run()
