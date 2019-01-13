# _*_ coding:utf-8 _*_ 

from functools import wraps
from time import time

def timer(func):
    ##计时装饰函数

    @wraps(func)
    def inner(cls,*args,**kw):

        t1=time()
        func(cls,*args,**kw)
        t2=time()

        print u'cost time :%s'%(t2-t1)
        return t2-t1

    return inner



def putty_size(size=1233333):

        ksize=size*1.0/1024
        if ksize<1024:

            if ksize<1:
                extend='B'
                size=size

            else:
                extend='K'
                size=ksize

        else:

            msize=ksize/1024
            extend='M'
            size=msize

            if msize>=1024:

                gsize=msize/1024
                extend='G'
                size=gsize

        return u'%.2f%s'%(size,extend)


big=[(1920,1080),(1280,720),(1024,576),(848,480),(768,432),(640,360),(424,240)]
speed=[('libx264','faster'),('libx264','fast'),('libx264','medium'),('copy','medium')]