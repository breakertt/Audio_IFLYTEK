#-*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json
import os
import wave
from pyaudio import PyAudio,paInt16
import cv2

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=10
URL = "http://openapi.xfyun.cn/v2/aiui"
APPID = ""
API_KEY = ""
AUE = "raw"
AUTH_ID = ""
DATA_TYPE = "audio"
SAMPLE_RATE = "16000"
SCENE = "main"
RESULT_LEVEL = "complete"
LAT = "39.938838"
LNG = "116.368624"
#个性化参数，注意需进行两层转义
PERS_PARAM = "{\\\\\\\"auth_id\\\\\\\":\\\\\\\"AUTH-ID\\\\\\\"}"
FILE_PATH = "C:/Users/break/Desktop/audio/temp.wav"

def my_record(filename):
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    print("开始录音 按crtl+C终止")
    try:
        while 1:
            string_audio_data = stream.read(NUM_SAMPLES)
            my_buf.append(string_audio_data)
            count+=1
            print('.')
    except KeyboardInterrupt:
        pass
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)#声道
    wf.setsampwidth(sampwidth)#采样字节 1 or 2
    wf.setframerate(framerate)#采样频率 8000 or 16000
    wf.writeframes(b"".join(my_buf))#https://stackoverflow.com/questions/32071536/typeerror-sequence-item-0-expected-str-instance-bytes-found
    wf.close()
    stream.close()

def buildHeader():
    curTime = str(int(time.time()))
    param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
    #使用个性化参数时参数格式如下：
    #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
    param = param.encode()
    paramBase64 = base64.b64encode(param)
    m2 = hashlib.md5()
    hash_data = (API_KEY + curTime + paramBase64.decode()).encode()
    m2.update(hash_data)
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header

def readFile(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    data = data
    return data


while True:
    text = input("若要说话请按回车")
    my_record(FILE_PATH)
    print("Record finish")
    r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
    json_dict = json.loads(r.content)
    print(json_dict)
    flag = False
    for element in json_dict['data']:
        #print(element) 
        #print(type(element))
        if 'intent' in element:
            for element2 in element['intent']:
                if 'answer' in element2:
                    os.system('python tts.py %s' % element['intent']['answer']['text'])
                    flag = True
    if not flag:
        os.system('python tts.py %s' % "我没有听懂，可以再说一遍吗")
        #if json_dict['code'] == '0' and 'answer' in json_dict['data'][0]['intent']:
        #    print(json_dict['data'][0]['intent']['answer']['text'])
        #if text == "quit":
        #    break