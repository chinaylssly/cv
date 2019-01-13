
1、python环境 python2.7

2、库依赖： 

    a, cv.py --> pip install opencv-python

    b, img_compare.py -->pip install scikit-image
                      -->pip install imutils

    c, ffmpeg.py -->ffmpeg安装包

3、功能：
    
    a，ffmpeg.py基于对ffmpeg.exe封装，可以实现视频的连续截图，长截图，多路视频合并为一路，视频剪裁，格式转换等功能
    b，cv.py基于对cv2库的封装，也可以实现类似ffmpeg的功能
    c, img_compare.py用来比较两张图片是否相似
    d, crop.py用于将一张图片切割成多张小图片，以及将这些小图片还原成之前的图片
    e, combine.py用于将一个文件夹中的图片合并成一张长图片
    f, compare.py用来测试不同preset对视频转码速度的影响
    g, tools.py封装了一下简单的小工具

