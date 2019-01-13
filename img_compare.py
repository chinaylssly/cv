# _*_ coding:utf-8 _*_ 


from skimage.measure import compare_ssim
#~ import skimage  as ssim
import argparse
import imutils
import cv2


__doc__=\
'''
该程序用来比较两张图片是否相似
第三方库依赖：
pip install scikit-image
pip install imutils
'''

def img_diff(Apath=u"test.png",Bpath=u"011.png",is_show=True,wait=0):
    ##两张图片需要有相同的尺寸


    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-f", "--first", required=True,
    #     help="first input image")
    # ap.add_argument("-s", "--second", required=True,
    #     help="second")
    # args = vars(ap.parse_args())
    # # load the two input images
    # imageA = cv2.imread(args["first"])
    # imageB = cv2.imread(args["second"])

    Apath=Apath.encode('utf-8','ignore')
    Bpath=Bpath.encode('utf-8','ignore')
    ##文件名改为utf-8编码

    imageA = cv2.imread(Apath)
    imageB = cv2.imread(Bpath)


    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)



    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    #​structural similarity index measurement (SSIM) system一种衡量两幅图像结构相似度的新指标，其值越大越好，最大为1。

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if is_show is True:

        imshow(grayA,grayB,imageA,imageB,diff,thresh,wait)

    aname=Apath.rsplit('/',1)[-1]
    bname=Bpath.rsplit('/',1)[-1]

    print aname,bname,score

    return dict(Apath=Apath,Bpath=Bpath,score=score,)

def imshow(grayA,grayB,imageA,imageB,diff,thresh,wait=0):

    # show the output images
    # cv2.imshow('grayA',grayA)
    # cv2.imshow('grayB',grayB)
    # cv2.imshow("Original", imageA)
    # cv2.imshow("Modified", imageB)
    # cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(wait)


def generate_args(root=u'c:/users/sunzhiming/desktop/02'):

    import os
    from copy import deepcopy


    imgs=os.listdir(root)

    imgs1=[]
    imgattrs=['png','jpg']
    for img in imgs:
        if img.rsplit('.',1)[-1] in imgattrs :
            imgpath=u'%s/%s'%(root,img)
            imgs1.append(imgpath)

        else:
            pass

    args=[]
    for i in range(0,len(imgs1)-1):
        
        a=imgs1[i]
        b=imgs1[i+1]
        args.append((a,b))


    return args


def generate_args(root=u'c:/users/sunzhiming/desktop/02'):

    import os
    from copy import deepcopy

    os.chdir(root)
    imgs=os.listdir(u'.')

    imgs1=[]
    imgattrs=['png','jpg']
    for img in imgs:
        if img.rsplit('.',1)[-1] in imgattrs :
            imgs1.append(img)

        else:
            pass

    args=[]
    for i in range(0,len(imgs1)-1):
        
        a=imgs1[i]
        b=imgs1[i+1]
        args.append((a,b))


    return args



def test():

    args=generate_args(root=u'')
    for arg in args:
        try:
            img_diff(*arg,is_show=True,wait=300)
        except Exception,e:
            print e
            pass


if __name__ =='__main__':

    test()

    # img_diff('../6.jpg','../6(combine).png')
    pass
