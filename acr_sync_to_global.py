from flask import Flask,jsonify, request, abort
import json
import time
import docker
import asyncio

client = docker.from_env()
tgthost = 'testdanielaaa.azurecr.io'

app = Flask(__name__)

@app.route('/push', methods=['POST'])
def push():
    j_data = json.loads(request.data)
    target = json.loads(json.dumps(j_data['target']))
    req = json.loads(json.dumps(j_data['request']))
    print(target)
    image = target['repository']
    tag = target['tag']
    host= req['host']
    print(image)
    print(tag)
    srcimage = host+'/'+image+':'+tag
    print(srcimage)
    destimage = tgthost+'/'+image+':'+tag
    handler(srcimage,destimage)
    return 'succ'

def handler(srcimage, destimage):
    client.images.pull(srcimage)
    client.images.get(srcimage).tag(destimage)
    client.images.push(destimage)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
