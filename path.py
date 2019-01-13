# _*_ coding:utf-8 _*_ 

import os,json

class Path(object):

    root=u'F:/迅雷下载/abc'
    attrs=['mp4','avi','mkv',]

    @classmethod
    def videos(cls,):
        w=os.walk(cls.root)
        for root,folder,filenames in w:
            for filename in filenames:
                if filename.rsplit('.',1)[-1] in cls.attrs:
                    filepath=u'%s/%s'%(root,filename)
                    filepath=filepath.replace('\\','/')
                    print filepath
                    yield filepath

    @classmethod
    def write_path_to_json(cls,):

        
        l=[]
        paths=cls.videos()
        for path in paths:
            l.append(path)

        j=json.dumps(obj=l,ensure_ascii=False,indent=4)

        with open('videopath.json','w',) as f:

            f.write(j.encode('utf-8','ignore'))




            
                


paths=Path.videos()


if __name__ == '__main__':


    Path.write_path_to_json()

        