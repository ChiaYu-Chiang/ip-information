import pytest
import os
from flask import current_app
from models import db
import ip_tool
import app


class TestIPTool:
    def test_get_ipaddr_list(self):
        fqdn = "www.google.com"
        assert ip_tool.get_ipaddr_list(fqdn) == ['142.251.42.228']

    def test_get_cache_from_local_dns(self):
        fqdn = "www.youtube.com"
        assert ip_tool.get_cache_from_local_dns(fqdn) == (
            'youtube-ui.l.google.com', ['www.youtube.com'])

    def test_get_hostname(self):
        ipaddr = "13.213.231.25"
        assert ip_tool.get_hostname(
            ipaddr) == "ec2-13-213-231-25.ap-southeast-1.compute.amazonaws.com"

    def test_get_ipinfo_detail(self):
        ipaddr = "13.213.231.25"
        ipinfo_api_token = os.environ.get("access_token")
        assert ip_tool.get_ipinfo_detail(
            ipaddr, ipinfo_api_token) == ('AS16509 Amazon.com, Inc.', 'Singapore', 'Singapore')
