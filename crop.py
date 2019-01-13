# _*_ coding:utf-8 _*_ 

import json,os
from PIL import Image

__doc__=\
'''
用于图片的裁剪，合并
'''

def crop(x=15,y=25,path=u'c:/users/sunzhiming/desktop/result-p(3).png',folder=None):
    ##将一张图片切割成多张

    if folder is None:
        folder=path.rsplit('.',1)[0]
        os.mkdir(folder)
        print u'makedir:%s'%(folder)

    img=Image.open(path)
    width,height=img.size
    print width,height

    for i in range(0,y):
        for j in range(0,x):

            ltx=(j % x) * (width  / x)
            lty=i  *(height / y)

            rlx=ltx + (width / x)
            rly=lty + (height / y)
            print (ltx,lty,rlx,rly)

            box1=(ltx,lty,rlx,rly)
            img1=img.crop(box1)
            imgpath=u'%s/crop-(%d,%d).png'%(folder,ltx,lty)
            print u'save :%s'%(imgpath)
            img1.save(imgpath)



def combine(x=15,y=25,inputfolder='c:/users/sunzhiming/desktop/crop',outputfolder=u'..'):
    ##将切割的小图片还原为原图片

    if outputfolder is None:

        outputfolder=u'..'

    os.chdir(inputfolder)
    imgs=os.listdir(u'.')
    temp=Image.open(imgs[0])
    width,height=temp.size
    mode=temp.mode
    ouput=Image.new(mode,(width*x,height*y))

    for img in imgs:

        print u'execute:%s'%(img)
        xy=img.rsplit(')',1)[0].rsplit('(',1)[1].split(',')
        x=int(xy[0])
        y=int(xy[1])
        image=Image.open(img)
        ouput.paste(image,box=(x,y))


    outputpath=u'%s/%s(combine).png'%(outputfolder,inputfolder.rsplit('/',1)[-1])
    ouput.save(outputpath)

    print u'save %s'%(outputpath)


if __name__ =='__main__':
    

    # combine()

    # crop(x=6,y=10,path=u'../6.jpg')
    combine(x=6,y=10,inputfolder=u'../6',)



