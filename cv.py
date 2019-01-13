# _*_ coding:utf-8 _*_ 
import cv2
import os
import time
from tools import timer,putty_size

__doc__=\
'''
opencv相关操作的封装
'''

class CV(object):

    def __init__(self,path=u'c:/users/sunzhiming/desktop/02.mp4'):

        self.path=path
        self.split_path=self.path.rsplit('/',1)
        self.filename=self.split_path[-1]
        self.name=self.filename.rsplit('.',1)[0]
        self.attr=self.filename.rsplit('.',1)[1]
        self.root=self.split_path[0]
        
        if len(self.split_path)==1:
            self.root=u'.'

        self.init_cap()
        self.show_video_info()


    def init_cap(self,):
        ##初始化capture

        if os.path.exists(self.path):
            self.cv2=cv2
            self.cap=self.cv2.VideoCapture(self.path.encode('utf-8'))
        else:
            raise

    def get_frame_by_num(self,num,):
        ##获取对应帧数的帧内容

        self.cap.set(cv2.CAP_PROP_POS_FRAMES,num)  #设置要获取的帧号
        ret,frame=self.cap.read()  #read方法返回一个布尔值和一个视频帧。若帧读取成功，则返回True
        return frame


    def show_frame(self,frame,wait=1000,title='frame'):
        ##显示帧画面

        cv2.imshow(title, frame)
        cv2.waitKey(wait)

    def show_multi_frame(self,width=1280,height=720,t=30,wait=60,title='frame'):
        ##相当于快进播放frame

        cv2.namedWindow(title,0)
        cv2.resizeWindow(title, width, height)
        step=int(self.fps * t)
        for num in range(0,int(self.framenums),step):
            self.show_frame_by_num(num=num,wait=wait)
            

    def show_frame_by_num(self,num=50,wait=1500):
        ##显示指定帧

        frame=self.get_frame_by_num(num=num)
        self.show_frame(frame=frame,wait=wait)
        

    def get_frame_num_by_timepoint(self,timepoint=1):
        ##timepoint单位为秒

        framenum=self.framerawrate * timepoint
        return int(framenum)


    def get_timepoint_by_frame_num(self,framenum):
        ##根据帧所在的时间点

        timepoint=framenum / self.framerawrate
        return timepoint



    def show_video_info(self,):
        ##显示视频信息

        self.width=self.cap.get(3)
        self.height=self.cap.get(4)
        self.framerawrate=self.cap.get(5)
        self.framenums=self.cap.get(7)
        self.totaltime=int(self.framenums / self.framerawrate)
        self.wait=int(1000/self.framerawrate)
        self.fsize=os.path.getsize(self.path)
        self.pfsize=putty_size(self.fsize)
        self.bps=self.fsize * 8 * self.framerawrate / self.framenums /1000
        self.fps=self.framerawrate

        print u'width:%s\nheight:%s\nframerawrate:%.1f\nframenums:%d\ntotaltime:%s\npfsize:%s\nbps:%d'\
        %(self.width,self.height,self.framerawrate,self.framenums,self.totaltime,self.pfsize,self.bps)


    def is_open(self,):
        return self.cap.isOpened()


    def make_img_path(self,):
        ##创建截图文件夹

        self.imgno=0
        img_root=u'%s/%s'%(self.root,self.name)
        if not os.path.exists(img_root):
            os.mkdir(img_root)
            print u'mkdir %s'%(img_root)
        self.img_root=img_root


    def is_done(self,):
        ##判断视频是否已截过图

        done_file=u'%s/done'%(self.img_root)

        if os.path.exists(done_file):
            return True
        else:
            return False


    def wrtie_frame_to_img(self,frame):
        ##将指定帧写入图片

        img_path=u'%s/%03d.jpg'%(self.img_root,self.imgno)
        cv2.imencode('.jpg',frame)[1].tofile(img_path)
        # cv2.imwrite(img_path.encode('utf-8'),frame)
        print u'save %s'%(img_path)
        self.imgno+=1


    def remove_imgs(self,):
        ##删除截图文件

        imgs=os.listdir(self.img_root)

        if u'0.jpg' in imgs:

            for img in imgs:
                imgpath=u'%s/%s'%(self.img_root,img)
                os.remove(imgpath)
                print u'delete img:%s'%(imgpath)


        else:

            print u'with no need to remove_imgs from:%s'%(self.img_root)


        self.remove_empty_folder()


    def remove_empty_folder(self,):
        ##删除空的截图文件夹

        imgs=os.listdir(self.img_root)

        if not imgs:
            os.rmdir(self.img_root)
            print u'rmdir :%s'%(self.img_root)




    def get_full_screen_cut(self,step=20):
        ##按时间间隔给视频截图

        self.make_img_path()

        if self.is_done():
            print u'video:%s screen cut done!'%(self.path)

        else:
            print u'ready to screen cut video:%s'%(self.path)

            # point=0
            point=60 * self.framerawrate
            ##前60秒视为片头，不做截取

            while point < self.framenums:

                self.cap.set(cv2.CAP_PROP_POS_FRAMES,point)
                ret,frame=self.cap.read()

                if ret:
                    self.wrtie_frame_to_img(frame)

                point += int(self.framerawrate * step)

            done_file=u'%s/done'%(self.img_root)
            with open(done_file,'wb')as f:
                print u'video:%s screen cut done! create flagfile:%s'%(self.path,done_file)



    def get_range_by_time(self,start_time=0,end_time=-1,):
        ##根据时间获取截取视频的开始以及结束帧数
       
        if end_time >= self.totaltime or end_time ==-1:
            end_time=self.totaltime

        if start_time > end_time:

            start_time = end_time - 10

        start_time=max(0,start_time)

        point=self.get_frame_num_by_timepoint(start_time)
        end=self.get_frame_num_by_timepoint(end_time)

        return point,end


    def jump_play_by_time(self,start_time=0,end_time=-1,wait=None):
        ##按照时间播放视频
       
        point,end = self.get_range_by_time(start_time=start_time,end_time=end_time)
        print u'play %s by timeline,start at %s second,end at %s second!!'%(self.filename,start_time,end_time)
        self.jump_play_by_frame(point=point,end=end,wait=wait)


    @timer
    def jump_play_by_frame(self,point=0,end=-1,wait=None):
        ##按照帧数播放视频

        if wait is None:
            wait=self.wait


        if end ==-1:
            end = self.framenums

        point = max(0,point)
        end=min(end,self.framenums)

        self.cap.set(cv2.CAP_PROP_POS_FRAMES,point)  #设置要获取的帧号

        print u'play video:%s by frame,start at: %s frame,end at %s frame'%(self.filename,point,end)
        while point < end:

            point+=1
            ret, frame = self.cap.read()

            if ret:
                time=point / self.framerawrate
                # print time
                cv2.imshow(self.filename,frame)
                if cv2.waitKey(wait) & 0xFF == ord('q'):
                    break

    
    @timer
    def show_all_frame(self,wait=25):
        ##播放视频

        while(self.cap.isOpened()):
          # Capture frame-by-frame

          ret, frame = self.cap.read()
          if ret == True:

            # Display the resulting frame
            cv2.imshow(self.filename,frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(wait) & 0xFF == ord('q'):
              break

          # Break the loop
          else: 
            break

    def convert_video(self,fps=None,width=None,height=None,start_time=0,end_time=-1,name=None,attr=None):

        if fps is None:
            fps=int(self.framerawrate)

        if width is None or height is None:
            width=int(self.width)
            height=int(self.height)

        if attr is None:
            attr=self.attr

        if name is None:
            name=self.name

        size=(width,height)

        attr='avi'
        
        filename=u'%s/%s-(%d*%d)-(%dfps).%s'%(self.root,name,width,height,fps,attr)
        print u'ready convert video:%s to %s'%(self.path,filename)
        # videoWriter =cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('X','V','I','D'),fps,size)
        fourcc = cv2.VideoWriter_fourcc(*'X264')
        videoWriter = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))


        point,end =self.get_range_by_time(start_time=start_time,end_time=end_time)
        print point,end
        point = max(0,point)
        end=min(end,self.framenums)

        self.cap.set(cv2.CAP_PROP_POS_FRAMES,point)  #设置要获取的帧号

        print point,end
        print u'start convert video................'
        while point < end:

            point+=1
            ret, frame = self.cap.read()

            if ret:
                cv2.imshow(self.filename,frame)
                print u'write frame point at:%s'%(point)
                videoWriter.write(frame)

                if cv2.waitKey(fps) & 0xFF == ord('q'):
                    break

        videoWriter.release()
        print u'convert Video:%s successfully!'%(self.path)






    def close(self,):

        # When everything done, release the video capture object
        self.cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

        print u'release the video capture object'

    @classmethod
    def show_lunkuo(cls,path=u'../result-p(2).png'):
        ##显示图片轮廓

        frame=cv2.imread(path)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=cv2.blur(frame, (7,7))
        frame=cv2.Canny(frame,0,30,3)
        cv2.imshow("Pick Picture:",frame)
        a=cv2.waitKey(0)


    def test_play(self,):

        self.show_frame_by_num(num=1000)
        self.jump_play_by_frame(point=5000,end=5100,wait=self.wait)
        self.jump_play_by_time(start_time=100,end_time=105,wait=1)


    def test_img(self,):

        self.make_img_path()
        self.remove_imgs()
        self.get_full_screen_cut()





        

if __name__ == '__main__':

    path='c:/users/sunzhiming/desktop/02.mp4'
    cv=CV(path)
    # cv.test_img()
    # cv.test_play()   
    cv.convert_video(start_time=10,end_time=30)
    cv.close()

  


