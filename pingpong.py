#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import redis
import urllib2
import time
from datetime import datetime as dt

class CsClient:
    def __init__(self):
        self._namespace = os.getenv("NAMESPACE")
        self._service_name = os.getenv("TAIR_CS_SERVICE_NAME")
        self._raft_port = os.getenv("CS_RAFT_PORT")
        self._rest_port = os.getenv("CS_REST_PORT")
        self.rest_timeout = 3
        self.podHost = os.getenv("HOSTNAME")
        self.podName = os.getenv("PODNAME")
        # self.node_IP = os.getenv("NODEIP")
        self._cs_status_url = "http://%s.%s.svc.cluster.local:%s/v2/cs_cluster_status" % (self._service_name, self._namespace, self._rest_port)
        self.master_url = self.get_master_url()
            

    def get_master_url(self):
        """
        Get master cs url
        """
        try:
            req = urllib2.Request(self._cs_status_url)
            result = urllib2.urlopen(req, timeout = self.rest_timeout)
            clustr_status = json.loads(result.read())
            if clustr_status["ret_code"] != 0:
                raise Exception(clustr_status["err_msg"])
            for item in clustr_status["cs_cluster"]:
                if item["raft_role"] == "master":
                    return "http://%s.%s.%s.svc.cluster.local:%s" % (item["cs_id"], self._service_name, self._namespace, self._rest_port)
        except Exception as e:
            print("==>%s\t%s\tget cs clustr status error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], self.podName, str(e)))
        return ""

def check_ready_by_cs():
    myself = os.getenv("HOSTNAME")
    try:
        client = CsClient()
        print("==>%s\t%s\tmasterURL=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName, str(client.master_url)))
        if client.master_url == "":
            print("==>%s\t%s\treturn Line48" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
            return 0
        req = urllib2.Request(client.master_url + "/v2/corrupt_db")
        resp = urllib2.urlopen(req, timeout = client.rest_timeout)
        r = resp.read()
        if r.find(client.podHost) != -1:
            print("==>%s\t%s\tcorrupt_db contain myself%s" & (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName, str(r)))
            print("==>%s\t%s\treturn Line55" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
            return -1
        print("==>%s\t%s\treturn Line57" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
        return 0
    except Exception as e:
        print("==>%s\t%s\thealth check error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName,str(e)))
        print("==>%s\t%s\treturn Line61" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
        return 0

def check_ready():
    try:
        podName = os.getenv("podName")
        port = os.getenv("HA_PORT")
        adminpass = os.getenv("ADMIN_PASSWORD")
        # nodeIp = os.getenv("NODEIP")

        r = redis.Redis(host=podName, port=int(port), password=adminpass, socket_connect_timeout=2, socket_timeout=2)
        ret = r.ping()
        print("==>%s\t%s\tping loading...\t%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], podName, str(ret)))

        if ret == False:
            print("==>%s\t%s\tping False..." % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3],podName))
            print("==>%s\t%s\treturn Line77" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
            return -1

        return check_ready_by_cs()
    except Exception as e:
        if str(e).find("loading the dataset") >= 0:
            print("==>%s\t%s\tloading the dataset exception...%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], podName,str(e)))
            print("==>%s\t%s\treturn Line84" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
            return 0
        print("==>%s\t%s\thealth check error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], podName,str(e)))
        print("==>%s\t%s\treturn Line87" % (dt.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3], client.podName))
        return -1
if __name__ == "__main__":
    ###改这个变量
    podName = os.getenv("PODNAME")
    
    while True:
        startTime=dt.now()
        print("Start time: %s\t%s\t" % (startTime.strftime("%d/%m/%Y %H:%M:%S"), podName))
        ret_code=check_ready()
        endTime=dt.now()
        print("End Time:%s\t%s, Return Code=%s, Delta time: %s ms" % (endTime.strftime("%d/%m/%Y %H:%M:%S"), podName,ret_code,(endTime-startTime).microseconds / 1000))
        time.sleep(3)
