#-*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64
import struct
import sys
import wave
from pyaudio import PyAudio,paInt16

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = ""
API_KEY = ""
chunk=2014

def play(filename):
    wf=wave.open(filename,'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if not data:break
        stream.write(data)
    stream.close()
    p.terminate()

def getHeader():
        curTime = str(int(time.time()))
        param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"  
        param = param.encode()
        paramBase64 = base64.b64encode(param)
        m2 = hashlib.md5()
        hash_data = (API_KEY + curTime + paramBase64.decode()).encode()
        m2.update(hash_data)
        checkSum = m2.hexdigest()
        header = {
                'X-CurTime':curTime,
                'X-Param':paramBase64,
                'X-Appid':APPID,
                'X-CheckSum':checkSum,
                'X-Real-Ip':'127.0.0.1',
                'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

def getBody(text):
        data = {'text':text}
        return data

def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()

r = requests.post(URL,headers=getHeader(),data=getBody(sys.argv[1]))
#print(r.content)
contentType = r.headers['Content-Type']
if contentType == "audio/mpeg":
    sid = r.headers['sid']
    if AUE == "raw":
        writeFile("audio/"+sid+".wav", r.content)
        play("audio/"+sid+".wav")
    else :
        writeFile("audio/"+sid+".mp3", r.content)
    print("success, sid = " + sid)
    
else :
    print(r.text) 