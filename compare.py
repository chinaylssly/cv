# _*_ coding:utf-8 _*_ 

from ffmpeg import FFmpeg
import json
from tools import big

'''
比较不同preset的转码时间

'''
class Compare(object):
    pass

def compare(path=u'../02-cut-00.mp4',width=1280,height=720,vcodec='libx264',preset='faster',crf=23):

    
    ffmpeg=FFmpeg(path=path)
    output='%s/%s.%s'%(ffmpeg.root,preset,ffmpeg.attr)
    cmd='ffmpeg.exe -i "%s" -s %dx%d  -vcodec %s -preset %s -crf %d "%s"'%(ffmpeg.path,width,height,vcodec,preset,crf,output)
    cost=ffmpeg.execute(cmd)
    return cost


def result(path=u'../02-cut-00.mp4'):

    results=[]

    params=[('libx264','faster'),('libx264','fast'),('libx264','medium'),('copy','medium')]

    for p in params:

        vcodec=p[0]
        preset=p[1]

        cost=compare(path=path,vcodec=vcodec,preset=preset)
        results.append(dict(vcodec=vcodec,preset=preset,cost=cost))


    print results


cp=result

if __name__ =='__main__':

    result()