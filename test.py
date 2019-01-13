# _*_ coding:utf-8 _*_ 

from ffmpeg import FFmpeg
import json
from cv import CV
from tools import big

path=u"test.mp4"
path=u'../02.mp4'

ffmpeg=FFmpeg(path)

ffmpeg.cut()

##处理有rorate的视频
cmd=u'ffmpeg.exe -y -i "test.mp4" -vf transpose=1 -vcodec libx264  -metadata:s:v:0 rotate=90" t1_r90.mp4"'
cmd=u'ffmpeg.exe -y -i "test.mp4" -vf transpose=2 -vcodec libx264  -metadata:s:v:0 rotate=270" t2_r270.mp4"'


##每300帧截一张图，并放入一个图片里
cmd=u'ffmpeg.exe -y -i "F:/迅雷下载/abc/bunnyjanjan.yummypura/JSQB9496.mp4"  -frames 1 -vf "transpose=1,select=not(mod(n\\,300)),scale=1280:720,tile=2x2" test.png'

##显示视频信息
cmd='ffprobe -v quiet -print_format json -show_format -show_streams t2.mp4 >t2.json'

##左右合并视频流
cmd=u'ffmpeg.exe -i "02.mp4" -vf "[in] scale=iw/2:ih/2, pad=2*iw:ih [left]; movie="xjp.mp4", scale=iw/2:ih/2 [right];[left][right] overlay=main_w/2:0 [out]" combine.mp4'

##上下播放视频流
cmd=u'ffplay.exe -i "02.mp4" -vf "[in] scale=iw/2:ih/2, pad=iw:2*ih [top]; movie="xjp.mp4", scale=iw/2:ih/2 [bottom];[top][bottom] overlay=0:main_h/2 [out]" '

##四个视频流放入同一个格子
cmd=u'ffplay.exe -i "raw.mp4" -vf "scale=iw/2:ih/2, pad=iw*2:2*ih [v1]; movie="faster.mp4", scale=iw/2:ih/2 [v2];[v1][v2] overlay=main_w/2:0[out1] ;movie="fast.mp4",scale=iw/2:ih/2 [v3];[out1][v3] overlay=0:main_h/2 [out2]; movie="medium.mp4",scale=iw/2:ih/2 [v4]; [out2][v4] overlay=main_w/2:main_h/2 [out]"'
# ffmpeg.execute(cmd)
