#!/usr/bin/python
# -*- coding: utf-8 -*-   
import datetime,time
import threading
import subprocess
import os, base64
import sys
import Queue
import platform

queue = Queue.Queue()

#需要手动配置的参数

#启动序号
SLEEP_TIME = 0

#需要手动配置的参数
#播放url
HTTP_ADDR = ''
#线程数量
THREAD_NUM = 100
#启动间隔
INTERVAL_TIME = 5

class Video_To_Bench(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        liveAddr = self.queue.get()
        #print liveAddr
        try:
            print liveAddr
            sysstr = platform.system()
            if(sysstr =="Windows"):
                subprocess.call('ffmpeg.exe -re -stream_loop -1 -i \"%s\" -c:v copy -c:a copy -bsf:a aac_adtstoasc -y -f flv -timeout 4000 NUL 2>NUL' %liveAddr,stdout=subprocess.PIPE,shell=True)
            elif(sysstr == "Linux"):
                subprocess.call('./ffmpeg -re -stream_loop -1 -i \"%s\" -c:v copy -c:a copy -bsf:a aac_adtstoasc -y -f flv -timeout 4000 /dev/null 2>/dev/null' %liveAddr,stdout=subprocess.PIPE,shell=True)
        except Exception as e:
            WriteLog('ERROR',str(e))
        self.queue.task_done()


if __name__ == "__main__":
    time.sleep(SLEEP_TIME)

    print "%d 个 %s 进程开始运行........" %(THREAD_NUM, Video_To_Bench)
    for i in xrange(THREAD_NUM):
        videotobench = Video_To_Bench(queue)
        videotobench.setDaemon(True)
        videotobench.start()

    for i in xrange(THREAD_NUM):
        liveaddr = HTTP_ADDR
        queue.put(liveaddr)
        time.sleep(INTERVAL_TIME)
    queue.join()
    print "进程退出"
