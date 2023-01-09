# ip-information

This repository is a web application for users to query the corresponding IP and detailed information of FQDN
<br>Use waitress as web server

## How to install

1. Clone this repository.
* clone with SSH
```cmd
git clone git@github.com:ChiaYu-Chiang/ip-information.git
```
* clone with HTTPS
```cmd
git clone https://github.com/ChiaYu-Chiang/ip-information.git
```
2. Enable virtual environment.
```cmd
cd ip-information\
python -m venv .venv
.venv\Scripts\activate
```
3. Install required packages.
```cmd
pip install -r requirements.txt
```

## How to use

1. Provide access token for ipinfo api.
* Register an account and get a token 
  * <https://ipinfo.io/account/token>
2. execute program.
```cmd
set access_token='access_token from ipinfo api'
python run_waitress
```
3. visit website.
* <http://127.0.0.1:5000>

## Nginx provides regional network access as a reverse proxy

1. install Nginx.
* <http://nginx.org/en/download.html>
2. start Nginx.
```cmd
cd C:\yourpath\nginx-version\
start nginx 
```
3. set Nginx.cof.
```nginx
http {
    server {
        # IP Information project with waitress
        listen 8000;
        server_name localhost;
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
```cmd
nginx -s reload
```
5. visit website.
* <http://localhost:8000/> or <http://yourip:8000>
