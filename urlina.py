#!/usr/bin/python2
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------
def main():
    read_param()
    reqs = test_params()
    test_url(reqs)
    exit(0)
#--------------------------------------------------------------------------------
def usage():
    print """Использование:
	%s -h|--help	Вывод этой справки.

	%s <file> [-s] [-c] [-r] [-d] [-txx]
        <file>      YAML файл со списком адресов.
        -s          Продолжать при несовпадении ожидаемого и реального кода ответа сервера или ошибке запроса.
        -c          Проверять сертификат сервера при HTTPS запросе.
        -r          Добавлять в заголовок поле Referer, равный адресу запроса.
        -d          Вывод отладочной информации.
        -txx        Таймаут HTTP(S) запроса, по-умолчанию 10 секунд. 1 < t < 3600

Формат файла:
---
urls:
  - url: <полный адрес, например: https://yandex.ru/search?text=123456780&clid=2186621>
    code: <Необязательный. Ожидаемый код ответа сервера, по-умолчанию: 200>
    method: <Необязательный. Метод запроса, по-умолчанию: GET>
""" % (argv[0], argv[0])
    exit(0)
#--------------------------------------------------------------------------------
def read_param():
    global data
    global debug
    global verify
    global ignore
    global timeout
    global referer
    debug = True if '-d' in argv else False
    ignore = True if '-s' in argv else False
    verify = True if '-c' in argv else False
    referer = True if '-r' in argv else False
    if debug:
        print "Incoming params:"
        for arg in argv: print "\t%s" % arg
        print "----------------\n"
    if len(argv) < 2:
        print "Ошибка: Не заданы параметры.\nПопробуйте %s -h.\n" % argv[0]
        exit(1)
    if argv[1] in ['-h','--help']:
        usage()
    file = argv[1]
    if not isfile(file):
        print "Ошибка: Файл '%s' не найден.\nПопробуйте %s -h.\n" % (file, argv[0])
        exit(1)
    timeout = 10
    for arg in argv:
        if arg == argv[0]: continue
        if arg.startswith('-t'):
            timeout = arg.replace('-t', '')
    try:
        timeout = int(timeout)
    except Exception as exc:
        print "Ошибка: Неправильный параметр '-t'. ('%s')\nПопробуйте %s -h.\n" % (str(timeout), argv[0])
        if debug: print "[%s: %s]" % (type(exc).__name__, str(exc))
        exit(1)
    if timeout > 3600 or timeout < 1:
        print "Ошибка: Неправильный параметр '-t'. ('%s')\nПопробуйте %s -h.\n" % (str(timeout), argv[0])
        exit(1)
    try:
        data = load(open(file).read())
    except Exception as exc:
        print "Ошибка: Файл '%s' не существует или не является валидным YAML.\nПопробуйте %s -h.\n" % (file, argv[0])
        if debug: print "[%s: %s]" % (type(exc).__name__, str(exc))
        exit(1)
    if debug:
        print "Readed:"
        print "  - http timeout:         %i" % timeout
        print "  - cert check:           %s" % str(verify)
        print "  - ignore code mismatch: %s" % str(ignore)
        print "  - add referer:          %s" % str(referer)
        print "  - file:                 %s" % file
        print "data:\n%s\n" % str(data)
        print "---------"
    return
#--------------------------------------------------------------------------------
def test_params():
    if not 'urls' in data.keys() or type(data['urls']).__name__ != 'list':
        print "Ошибка: Неверный формат данных.\nПопробуйте %s -h.\n" % argv[0]
        exit(1)
    reqs = []
    for chk in data['urls']:
        if not 'code' in chk.keys(): chk['code'] = '200'
        else: chk['code'] = str(chk['code'])
        if not 'method' in chk.keys(): chk['method'] = 'GET'
        else: chk['method'] = str(chk['method'])
        if not 'url' in chk.keys():
            print "Ошибка: Адрес должен быть задан.\nПопробуйте %s -h.\n" % argv[0]
            exit(1)
        else: chk['url'] = str(chk['url'])
        if not chk['url'].lower().startswith('http://') and not chk['url'].lower().startswith('https://'):
            print "Ошибка: Адрес должен начинаться с 'http://' или 'https://'.\nПопробуйте %s -h.\n" % argv[0]
            exit(1)
        reqs.append(chk)
    return reqs
#--------------------------------------------------------------------------------
def test_url(reqs):
    print "Проверка..."
    print "Статус\tМетод\tКод\tОжидаемый Код\tАдрес"
    for req in reqs:
        if debug:
            print "Processing: %s" % str(req)
        if referer:
            headers['Referer'] = req['url']
        try:
            response = requests.request(req['method'], req['url'], headers=headers, verify=verify, timeout=timeout)
        except Exceptions as exc:
            if not ignore:
                print "Ошибка выполнения запроса. Выход."
                if debug: print "[%s: %s]" % (type(exc).__name__, str(exc))
                exit(1)
            else:
                print "ERROR\tОшибка выполнения запроса для '%s::%s'." % (req['method'], req['url'])
                if debug: print "[%s: %s]" % (type(exc).__name__, str(exc))
        if str(response.status_code) != str(req['code']):
            if not ignore:
                print "Ошибка: Несовпадение кода сервера с ожидаемым (%s != %s) для %s::%s\nПопробуйте '-s' ?\n" % (req['code'], str(response.status_code), req['method'], req['url'])
                exit(1)
            print "FAIL\t%s\t%s\t%s\t\t%s" % (req['method'], response.status_code, req['code'], req['url']) # error
        else:
            print "OK\t%s\t%s\t%s\t\t%s" % (req['method'], response.status_code, req['code'], req['url']) # ok
        if debug:
            print "\nRequest Headers:"
            for key in headers.keys(): print "\t%s:\t%s" % (key, headers[key])
            print "\nAnswer Headers:"
            for key in response.headers.keys(): print "\t%s:\t%s" % (key, response.headers[key])
    print "Готово."
    return
#--------------------------------------------------------------------------------
from os.path import isfile
from sys import argv, exit
from yaml import load
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#--------------------------------------------------------------------------------
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}
if __name__ == "__main__":
    main()
