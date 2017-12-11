# -*- coding: utf-8 -*-
#!/usr/bin/env python

import requests
from lxml import etree
import time
import os

kuaidaili1 = "http://www.kuaidaili.com/free/inha/"
kuaidaili2 = "http://www.kuaidaili.com/free/intr/"
xici = "http://www.xicidaili.com/"


headers = {
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive"

}


class GetProxies:
    def __init__(self, url):
        self.url = url

    def kuaidailiIPs(self):  # 爬取kuaidaili IP方式
        for i in range(1, 11):
            req = requests.get(self.url + '/' + str(i))
            tree = etree.HTML(req.text)
            treelist = tree.xpath("//tbody/tr")
            for tr in treelist:
                proxies = {}
                ip = tr.xpath("td[@data-title='IP']/text()")[0]
                pt = tr.xpath("td[@data-title='PORT']/text()")[0]
                ty = tr.xpath("td[@data-title='类型']/text()")[0]
                proxies[ty] = ip + ':' + pt
                yield proxies

    def xiciIPs(self):  # 爬取xici IP方式
        req = requests.get(self.url, headers=headers)
        tree = etree.HTML(req.text)
        treelist = tree.xpath("//table//tr")
        for tr in treelist:
            try:
                ip = tr.xpath("td[2]/text()")[0]
                pt = tr.xpath("td[3]/text()")[0]
                ty = tr.xpath("td[6]/text()")[0]
            except IndexError:
                continue
            else:
                proxies = {}
                proxies[ty] = ip + ':' + pt
                yield proxies


def test(liter):
    for d in liter:
        starttime = time.time()
        for i in range(5):  # 五次访问测试
            try:
                # s = requests.session()
                # s.keep_alive = False
                code = requests.get(testurl, proxies=d, headers=headers).status_code
                i += 1
            except requests.exceptions.ProxyError:
                continue
            else:
                break
        endtime = time.time()
        if code == requests.codes.ok:
            with open("AvailIP.txt", "a") as file:
                for key in d:
                    if key.upper() == 'HTTP' or key.upper() == 'HTTPS':
                        print("Success", d, "Spend: %.2f" % (endtime - starttime))
                        if endtime - starttime < 0.5:
                            file.write(key + '\t' + d[key] + '\n')
        else:
            print("Fail", d, code)


def renameLastFile(file):  # 将之前的AvailIP.txt加上时间
    creattime = time.ctime(os.path.getctime(file))[4:-14].replace(' ', '')
    os.rename(file, file[:-4] + creattime + '.txt')


if __name__ == '__main__':
    try:
        renameLastFile("AvailIP.txt")
    except Exception as e:
        print(e)
        pass

    testurl = input("Input test url: ")
    if testurl[:4] != 'http':
        testurl = 'http://' + testurl
    now = str(int(time.time()))
    khttp = GetProxies(kuaidaili1).kuaidailiIPs()
    khttps = GetProxies(kuaidaili2).kuaidailiIPs()
    xicihttp = GetProxies(xici).xiciIPs()
    test(khttp)
    test(khttps)
    test(xicihttp)
