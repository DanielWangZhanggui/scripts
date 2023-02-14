#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import redis
import urllib2
import time
from datetime import datetime as dt

def check_ready():
    try:
        #改这些变量
        podIp = ""
        port = "6879"
        adminpass = ""
        # nodeIp = os.getenv("NODEIP")

        r = redis.Redis(host=podIp, port=int(port), password=adminpass, socket_connect_timeout=2, socket_timeout=2)
        ret = r.ping()
        print("==>%s\t%s\tping loading...\t%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), podIp, str(ret)))

        if ret == False:
            print("==>%s\t%s\tping False..." % (dt.now().strftime("%d/%m/%Y %H:%M:%S"),podIp))
            print("==>%s\t%s\treturn Line25" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.podIp))
            return -1

        print("==>%s\t%s\treturn Line28" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.podIp))
        return 0
    except Exception as e:
        if str(e).find("loading the dataset") >= 0:
            print("==>%s\t%s\tloading the dataset exception...%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), podIp,str(e)))
            print("==>%s\t%s\treturn Line33" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.podIp))
            return 0
        print("==>%s\t%s\thealth check error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), podIp,str(e)))
        print("==>%s\t%s\treturn Line36" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.podIp))
        return -1
        
if __name__ == "__main__":
    ret_code=check_ready()
    print("%s\t%s\tReturn Code=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), podIp,str(ret_code)))
    # while True:
    #     ret_code=check_ready()
    #     print("%s\t%s\tReturn Code=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), nodeIp,str(ret_code)))
    #     time.sleep(3)
