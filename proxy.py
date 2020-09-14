# encoding:utf-8
"""
配置代理
get_ip_xiongmao :熊猫代理
get_ip_suwei：借速威代理ip
back_ip_suwei：还速威代理ip
"""
import json
import requests
import time

def get_ip_xiongmao():
    url = "http://www.xiongmaodaili.com/xiongmao-web/api/glip?secret=f30a329545d379f7b3feadf7761ffb55&orderNo=GL20190611161733AsEdHDHg&count=1&isTxt=0&proxyType=1"
    text = requests.get(url).text
    ip_dict = json.loads(text)
    ip = ip_dict["obj"][0]["ip"]
    port = ip_dict["obj"][0]["port"]
    proxy = ip + ":" + port
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    print(proxies)
    return proxies


def get_ip_suwei():
    url = "http://39.104.68.122:8000/GetAdsl?TC_String=bgnCompany&TIB_ID=22"
    Guid = ''
    proxies = {}
    try:
        text = requests.get(url).text
        ip_dict = json.loads(text)
        ip = ip_dict["IpAddress"]
        Guid = ip_dict["Guid"]
        proxies = {
            'http': 'http://' + ip,
            'https': 'https://' + ip
        }
        print(proxies)
    except Exception as e:
        print(f'get proxy error:{e}')
    return proxies, Guid


def back_ip_suwei(Guid):
    url_c = "http://39.104.68.122:8000/GetAdslBack?TC_String=bgnCompany&ENTITY_ID=142&TIB_ID=22&GUID={}"
    url = url_c.format(Guid)
    text = requests.get(url).text
    message = json.loads(text)
    if message["IsSucess"]:
        print("ip归还成功")


if __name__=="__main__":
    proxies, Guid = get_ip_suwei()
    back_ip_suwei(Guid)



