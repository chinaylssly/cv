# _*_ coding:utf-8 _*_ 

import subprocess,os,json
from tools import timer,putty_size
from traceback import format_exc


__doc__=\
'''
ffmpeg的python封装
'''

class FFmpeg(object):

    def __init__(self,path=u'c:/users/sunzhiming/desktop/02.mp4'):

        self.path=path
        self.split_path=self.path.rsplit('/',1)
        if len(self.split_path)==1:
            self.root=u'.'
        else:
            self.root=self.split_path[0]

        self.filename=self.split_path[-1]
        self.name=self.filename.rsplit('.',1)[0]
        self.attr=self.filename.rsplit('.',1)[1]
        self.cutno=0
        self.info_file=u'%s/%s.json'%(self.root,self.name)

        self.read_info_from_json()
        self.show_video_info()

    def write_json_info(self,):
        '''写入信息文件'''

        cmd=u'ffprobe -v quiet -print_format json -show_format -show_streams "%s" >"%s"'%(self.path,self.info_file)
        self.execute(cmd,output=self.info_file)

    
    def read_info_from_json(self,):
        '''读入视频信息'''

        self.write_json_info()
        with open(self.info_file,'r')as f:
            self.info=json.load(f)


    def show_video_info(self,):
        '''显示视频信息'''

        streams=self.info.get('streams')
        for stream in streams:
            if stream.get('codec_type') == 'video':

                self.stream=stream
                self.width=stream.get('width')
                self.height=stream.get('height')
                self.codec_name=stream.get('codec_name') #流的编码格式
                self.r_frame_rate =stream.get('r_frame_rate') #实际帧率
                self.bit_rate =stream.get('bit_rate') #视频的比特率
                self.nb_frames =stream.get('nb_frames') ##视频帧数
                self.tags =stream.get('tags') ##流中的附加信息，其中的字段可能为空
                self.rotate=self.tags.get('rotate')
                
                break

        _format=self.info.get('format')

        self.size=int(_format.get('size'))
        self.duration=float(_format.get('duration'))
        self.bps=int(_format.get('bit_rate'))
        self.fps=int(eval(self.r_frame_rate))
        self.frames=int(self.nb_frames)
        self.psize=putty_size(self.size)


        print 
        print u'width:%d'%(self.width)
        print u'height:%d'%(self.height)
        print u'fps:%d'%(self.fps)
        print u'frames:%d'%(self.frames)
        print u'bps:%d'%(self.bps)
        print u'size:%s'%(self.psize)
        print u'duration:%.2fs'%(self.duration)
        print u'rotate:%s'%(self.rotate)
        print 


    @classmethod
    def time(cls,m=0,s=0,ms=0,h=0):
        '''时间格式转换'''
        return u'%d:%02d:%02d.%d'%(h,m,s,ms)

    @classmethod
    @timer
    def execute(cls,cmd,output=None):
        '''执行函数'''

        if output is not None and os.path.exists(output):
            print u'filepath:%s exists'%(output)

            # os.remove(output)
            # ##测试用

        else:

            print u'runing cmd: %s'%(cmd)
            cmd=cmd.encode('gbk','ignore')
            sub=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)

            ##阻塞一下
            sub.wait()

    def make_img_path(self,):
        '''创建截图文件夹'''

        img_root=u'%s/%s'%(self.root,self.name)
        if not os.path.exists(img_root):
            os.mkdir(img_root)
            print u'mkdir %s'%(img_root)
        self.img_root=img_root


    def cut_img(self,time=30):
        '''依照时间间隔对视频进行截图'''

        self.make_img_path()
        print u'ready cut img from %s'%(self.path)
        output=u'%s/frames_%%03d.png'%(self.img_root)
        r=1.0/time
        cmd=u'ffmpeg.exe -i %s  -y -r %.2f %s'%(self.path,r,output)
        self.execute(cmd,output)

    def cut_img_long(self,width=1280,height=720,step=1000,x=2,y=3):
        '''长截图，x为行的图片数，y为列图片数,step表示帧数（每1000帧截图一张）'''

        output=u'%s/%s-long(%sx%s).png'%(self.root,self.name,x,y)
        print u'ready cut long img from %s'%(self.path)

        cmd=u'ffmpeg.exe  -i  %s -frames 1  -vf "select=not(mod(n\\,%d)),scale=%d:%d,tile=%dx%d" %s'\
            %(self.path,step,width,height,x,y,output)

        self.execute(cmd,output)


    def cut(self,start='00:00:00.0',end='00:01:30.0'):
        '''剪裁视频，次函数不建议使用，除非start不大'''

        output=u'%s/%s-cut-%02d.%s'%(self.root,self.name,self.cutno,self.attr)
        print u'cut filepath at: %s'%(output)
        cmd=u'ffmpeg.exe -i "%s" -ss %s -codec copy -to %s "%s"'%(self.path,start,end,output)
        self.execute(cmd,output)
        self.cutno+=1

        return output

    @classmethod
    def compute_time(cls,start=(0,0,0,0),end=(0,1,0,0)):

        def convert_timetuple(timetuple):

            if len(timetuple)==3:
                h,m,s = timetuple
                ms=0
            elif len(timetuple)==4:
                h,m,s,ms = timetuple
            else:
                raise IndexError(u'lenght of timetuple must be 3 or 4 ')

            return h,m,s,ms

        start = convert_timetuple(start)
        end =convert_timetuple(end)

        def timetuple_to_second(timetuple):
            h,m,s,ms=timetuple
            return h * 3600 + m * 60 + s + ms / 1000.0 

        duration=timetuple_to_second(end) - timetuple_to_second(start)

        startdict=dict(zip(('m','h','s','ms'),start))
        startstring=cls.time(**startdict)

        return startstring,duration


    def cut_video(self,start=(0,0,0,0),end=(0,1,0,0)):
        '''
        裁剪视频，针对start很大的时，更快的裁剪速度
        params: srart,end 开始和结束时间，接收至少三个元素的可迭代对象，分别代表hour，minute，second，如果有第四个元素，则代表millisecond
        '''

        startstring,duration = self.compute_time(start,end)

        output=u'%s/%s-cut-%02d.%s'%(self.root,self.name,self.cutno,self.attr)
        print u'cut filepath at: %s'%(output)
        cmd=u'ffmpeg.exe -ss %s -i "%s"  -codec copy -t %s "%s"'%(startstring,self.path,duration,output)
        self.execute(cmd,output)
        self.cutno+=1
        return output



    def cut_video_advance(self,width=1280,height=720,vcodec='libx264',preset='faster',crf=23,durationtuple=None):
        '''
        可剪辑视频切可转码
        params: durationtuple=((0,0,1),(0,0,8))接收开始时间和结束时间
        '''

        if durationtuple:
            start,end=durationtuple
            startstring,duration = self.compute_time(start,end)
            durationstring=u'-ss %s -t %s'%(self.compute_time(start,end))

        else:

            durationstring=u''

        output='%s/%s(%dx%d)-(%s-%s-%s).%s'%(self.root,self.name,width,height,vcodec,preset,crf,self.attr)
        cmd='ffmpeg.exe %s -i "%s" -s %dx%d  -vcodec %s -preset %s -crf %d "%s"'%(durationstring,self.path,width,height,vcodec,preset,crf,output)
        cost=self.execute(cmd=cmd,output=output)
        return cost

      
    def convert(self,width=1280,height=720,vcodec='libx264',b=None):
        '''
        vcodec='copy'时，分辨率就失效了
        b最好设置为默认
        '''

        if b is None:
            fb=0
            cb=''
        else:
            fb=b
            cb='-b %d'%(b)

        # self.attr='avi'

        output='%s/%s(%dx%d)-(%db).%s'%(self.root,self.name,width,height,fb,self.attr)
        print u'convert filepath at:%s'%(output)
        cmd='ffmpeg.exe -i "%s" -s %dx%d  -vcodec %s %s "%s"'%(self.path,width,height,vcodec,cb,output)

        self.execute(cmd,output)
        return output

    def convert_more(self,width=1280,height=720,vcodec='libx264',preset='faster',crf=23):
        '''
        更快速的转码方法
        '''

        output='%s/%s(%dx%d)-(%s-%s-%s).%s'%(self.root,self.name,width,height,vcodec,preset,crf,self.attr)
        cmd='ffmpeg.exe -i "%s" -s %dx%d  -vcodec %s -preset %s -crf %d "%s"'%(self.path,width,height,vcodec,preset,crf,output)
        cost=self.execute(cmd=cmd,output=output)
        return cost

 

    def convert_sp(self,):
        '''
        处理带有ratate的视频

        '''

        output=u'%s/%s_t2.%s'%(self.root,self.name,self.attr)
        cmd=u'ffmpeg.exe -y -i "%s" -vf transpose=2 -vcodec libx264 "%s"'\
            %(self.path,output)

        self.execute(cmd,output=output)

        output1=u'%s/%s_t2r270.%s'%(self.root,self.name,self.attr)
        cmd=u'ffmpeg.exe -i "%s" -c copy -metadata:s:v:0 rotate=270 "%s"'%(output,output1)
        self.execute(cmd=cmd,output=output1)


    def play(self,start=u'0:00:30.0',):
        '''
        播放视频,最好在命令行直接执行

        '''

        ##set SDL_AUDIODRIVER=directsound && ffplay.exe
        cmd=u'ffplay.exe -ss %s %s'%(start,self.path,)
        self.execute(cmd,output=None)



    @classmethod
    def combine_lr(cls,left=u'02.mp4',right=u'xjp.mp4',output=u'combine_lr.mp4'):
        '''
        两个文件左右合并（无敌了)
        '''

        cmd=u'ffmpeg.exe -i "%s" -vf "[in] scale=iw/2:ih/2, pad=2*iw:ih [left]; movie="%s", scale=iw/2:ih/2 [right];[left][right] overlay=main_w/2:0 [out]" %s'\
            %(left,right,output)

        cls.execute(cmd=cmd,output=output)

    @classmethod
    def combine_four(cls,v1,v2,v3,v4,output=u'combine_four.mp4'):
        '''
        四路视频合并为1路
        '''
        
        cmd=u'ffmpeg.exe -i %s -i %s -i %s -i %s -filter_complex "[0:v]pad=iw*2:ih*2[a];[a][1:v]overlay=w[b];[b][2:v]overlay=0:h[c];[c][3:v]overlay=w:h" %s'\
            %(v1,v2,v3,v4,output)

        cls.execute(cmd=cmd,output=output)


    @classmethod
    def play_four(cls,v1=u'02.mp4',v2=u'02.mp4',v3=u'02.mp4',v4=u'02.mp4',):
        '''
        同时播放四路视频
        '''

        cmd=u'ffplay.exe -i "%s" -vf "scale=iw/2:ih/2, pad=iw*2:2*ih [v1]; movie="%s", scale=iw/2:ih/2 [v2];[v1][v2] overlay=main_w/2:0[out1] ;movie="%s",scale=iw/2:ih/2 [v3];[out1][v3] overlay=0:main_h/2 [out2]; movie="%s",scale=iw/2:ih/2 [v4]; [out2][v4] overlay=main_w/2:main_h/2 [out]"'\
                %(v1,v2,v3,v4)

        cls.execute(cmd)

    @classmethod
    def play_tb(cls,top=u'02.mp4',buttom=u'xjp.mp4'):
        '''
          两个文件上下合并（无敌了）
        '''

        cmd=u'ffplay.exe -i "%s" -vf "[in] scale=iw/2:ih/2, pad=iw:2*ih [top]; movie="%s", scale=iw/2:ih/2 [bottom];[top][bottom] overlay=0:main_h/2 [out]"'\
            %(top,buttom)
        cls.execute(cmd)


    @classmethod
    def play_in(cls,big=u'02.mp4',small=u'xjp.mp4'):
        '''
          文件重叠合并，把第二个文件的视频缩小为四分之一后，放到第一个视频的宽高八分之一画面处（更无敌）
        '''


        cmd='ffplay.exe -i "%s" -vf "[in] scale=iw:ih, pad=iw:ih [top];movie="%s", scale=iw/4:ih/4 [bottom];[top][bottom] overlay=main_w*5/8:main_h/8 [out]"'\
            %(big,small,)
        cls.execute(cmd)


    def test(self,width,height,vcodec='libx264',b=None,t=30):
          

        start=self.time(m=1,s=0)
        end=self.time(m=1,s=t)

        output=self.cut(start,end)

        ffmpeg=FFmpeg(output)

        try:
            ffmpeg.convert(width=width,height=height,vcodec=vcodec,b=b)

        except:
            print u'catch exception when convert file:%s'%(self.path)
            print format_exc()
            raise



def test_cut_img():

    ffmpeg=FFmpeg()
    ffmpeg.cut_img_long()
    # ffmpeg.cut_img()


def test_play():

    ffmpeg=FFmpeg()
    start=ffmpeg.time(m=3,s=8)
    ffmpeg.play()



def test_cut():
    path=u'../小卡片.mp4'
    ffmpeg=FFmpeg(path)
    start=ffmpeg.time(m=2,s=0)
    end=ffmpeg.time(m=2,s=10)
    ffmpeg.cut(start,end)


def test_cut_video():

    path=u'02.mp4'
    ffmpeg=FFmpeg(path)
    ffmpeg.cut_video(start=(0,0,1),end=(0,0,8))


def test_cut_video_advance():

    path=u'02.mp4'
    ffmpeg=FFmpeg(path)
    from tools import PPI,speed
    width,height =PPI[-2]
    ffmpeg.cut_video_advance(width=width,height=height,durationtuple=((0,0,1),(0,0,8)))
    ffmpeg.cut_video_advance(width=width,height=height,preset=speed[1][1])


def test_convert():

    print FFmpeg.time()
    ffmpeg=FFmpeg(path=u'test.mp4')
    ffmpeg.convert(width=1280,height=720,vcodec='h264')


def test_info():
    ffmpeg=FFmpeg()
    print ffmpeg.info




if __name__ =='__main__':

    # test_cut()
    # test_convert()
    # test_cut_img()
    # test_play()
    # FFmpeg()
    # FFmpeg().cut_img()
    # test_cut_video()
    # test_cut_video_advance()
    pass
