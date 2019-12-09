#!/usr/bin/python2
# -*- coding: utf-8 -*-

import yaml
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
verifyssl = False # server's certificate
timeout = 10 # http timeout
file = '01.yml'

data = yaml.load(open(file).read())['urls']

print "Status\tMethod\tCode\tPlan\tURL"
for line in data:
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'deflate','Connection': 'keep-alive','Cache-Control': 'max-age=0','Referer': line['url'] }
    resp = requests.request(line['method'], line['url'], headers=headers, verify=verifyssl, timeout=timeout)
    if str(resp.status_code) != str(line['planned_code']):
        print "FAIL\t%s\t%s\t%s\t%s" % (line['method'], resp.status_code, line['planned_code'], line['url']) # error
    else:
        print "OK\t%s\t%s\t%s\t%s" % (line['method'], resp.status_code, line['planned_code'], line['url']) # ok

        