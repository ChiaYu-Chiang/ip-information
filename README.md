# ip-information

This repository is a web application for users to query the corresponding IP and detailed information of FQDN
<br>Use waitress as web server

## How to install

1. Clone this repository.
* clone with SSH
```shell
git clone git@github.com:ChiaYu-Chiang/ip-information.git
```
* clone with HTTPS
```shell
git clone https://github.com/ChiaYu-Chiang/ip-information.git
```
2. Enable virtual environment.
```shell
cd ip-information\
```
* windows
```shell
python -m venv .venv
.venv\Scripts\activate
```
* linux
```shell
python3 -m venv .venv
source .venv/bin/activate
```
3. Install required packages.
```shell
pip install -r requirements.txt
```

## How to use

1. Provide access token for ipinfo api.
* Register an account and get a token 
  * <https://ipinfo.io/account/token>
2. execute program.
```shell
set access_token='access_token from ipinfo api'
python run_waitress
```
3. visit website.
* <http://127.0.0.1:5000>

## Nginx provides regional network access as a reverse proxy

1. install Nginx.
* <http://nginx.org/en/download.html>
2. start Nginx.
```shell
cd C:\yourpath\nginx-version\
start nginx 
```
3. set nginx.conf.
```nginx
http {
    server{
        listen 80;
        server_name localhost;
        # Redirect http to https
        return 301 https://$server_name$request_uri;
    }

    server {
        # IP Information project with waitress
        listen 443 ssl http2;
        server_name localhost;

        ssl_certificate yourpath/filename.crt;
        ssl_certificate_key yourpath/filename.key;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

        error_page 502 503 /custom_50x.html;
        location = /custom_50x.html {
            internal;
        }

        location / {
            proxy_pass http://127.0.0.1:5000;
 
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $host:$server_port;
            proxy_set_header X-Forwarded-Port $server_port;
        }
    }
}
```
4. restart Nginx.
```shell
nginx -s reload
```
5. visit website.
* <http://localhost:8000/> or <http://yourip:8000>
