#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import redis
import urllib2
import time
from datetime import datetime as dt
from netifaces import interfaces, ifaddresses, AF_INET

class CsClient:
    def __init__(self):
        self._namespace = os.getenv("NAMESPACE")
        self._service_name = os.getenv("TAIR_CS_SERVICE_NAME")
        self._raft_port = os.getenv("CS_RAFT_PORT")
        self._rest_port = os.getenv("CS_REST_PORT")
        self.rest_timeout = os.getenv("CS_REST_TIMEOUT")
        self.podHost = os.getenv("HOSTNAME")
        self.podIp = os.getenv("PODIP")
        self.node_IP = os.getenv("NODEIP")
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
            print("==>%s\t%s\tget cs clustr status error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), self.node_IP, str(e)))
        return ""

def check_ready_by_cs():
    myself = os.getenv("HOSTNAME")
    try:
        client = CsClient()
        print("==>%s\t%s\tmasterURL=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.node_IP, str(client.master_url)))
        if client.master_url == "":
            return 0
        req = urllib2.Request(client.master_url + "/v2/corrupt_db")
        resp = urllib2.urlopen(req, timeout = client.rest_timeout)
        r = resp.read()
        if r.find(client.podHost) != -1:
            print("==>%s\t%s\tcorrupt_db contain myself%s" & (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.node_IP, str(r)))
            return -1
        return 0
    except Exception as e:
        print("==>%s\t%s\thealth check error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), client.node_IP,str(e)))
        return 0

def check_ready():
    try:
        podIp = os.getenv("PODIP")
        port = os.getenv("HA_PORT")
        adminpass = os.getenv("ADMIN_PASSWORD")
        nodeIp = os.getenv("NODEIP")
        
        r = redis.Redis(host=podIp, port=int(port), password=adminpass, socket_connect_timeout=2, socket_timeout=2)
        ret = r.ping()
        print("==>%s\t%s\tping loading..." % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), nodeIp, str(ret)))

        if ret == False:
            print("==>%s\t%s\tping False..." % (dt.now().strftime("%d/%m/%Y %H:%M:%S"),nodeIp))
            return -1

        return check_ready_by_cs()
    except Exception as e:
        if str(e).find("loading the dataset") >= 0:
            print("==>%s\t%s\tloading the dataset exception...%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), nodeIp,str(e)))
            return 0
        print("==>%s\t%s\thealth check error: err=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), nodeIp,str(e)))
        return -1
if __name__ == "__main__":
    from netifaces import interfaces, ifaddresses, AF_INET
    for ifaceName in interfaces():
        if ifaceName == "eth0":
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            os.environ["NODEIP"] = addresses
    
    nodeIP = os.getenv("NODEIP")
    while True:
        ret_code=check_ready()
        print("%s\t%s\tReturn Code=%s" % (dt.now().strftime("%d/%m/%Y %H:%M:%S"), nodeIp,str(ret_code)))
        time.sleep(3)

