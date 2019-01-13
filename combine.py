# _*_ coding:utf-8 _*_ 

import json,os
from PIL import Image


__doc__=\
'''
将一个文件夹所有的图片合并成一张图片
'''


def combine(p=2,path=u'c:/users/sunzhiming/desktop/02',outputfolder=None):
    ##p代表一行几张图片

    if outputfolder is None:
        outputfolder=path

    os.chdir(path)
    imgs=[Image.open(img) for img in os.listdir(u'.')]

    width,height=imgs[0].size

    nums=len(imgs)

    if nums % p==0:
        rheight=nums / p * height / p
    else:
        rheight=(nums / p + 1) * height / p

    result=Image.new(imgs[0].mode,(width,rheight))

    for i,img in enumerate(imgs):

        im=img.resize((width/p,height/p))
       
        x=(i % p) * (width / p)
        y=(i / p) * (height / p)

        print (x,y)
        result.paste(im,box=(x,y))


    result.save(u'%s/result-p(%s).png'%(outputfolder,p))


if __name__ == '__main__':
    
    combine(p=3,outputfolder=u'..')