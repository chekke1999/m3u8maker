#! /usr/bin/env python
# -*- coding: utf-8 -*-
#保存先を基準に相対パスでプレイリスト生成。指定が無ければ対象のフォルダと同じディレクトにm3u8を生成。
#tstee
import glob,os,sys
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.aac import AAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.oggopus import OggOpus
sp = os.sep#セパレータ
class Gplaylist:
    def __init__(self,arg):
        if arg[1] == "-d":
            self.start = 2
        else:
            self.start = 1
        self.args = arg
    def Gm3u8(self):
        for i in range(self.start,len(self.args)):
            dirpath = self.args[i]
            filelist = glob.glob(dirpath + sp + '**', recursive=True)
            print('--------------------------------------------')
            listnameen = dirpath.rfind(sp)
            print("listnameen",listnameen)
            playlistname = dirpath[listnameen+1:]
            savepath = dirpath[:dirpath.rfind(sp)]
            f = open(savepath + sp + playlistname + '.m3u8', 'wt', encoding='utf-8-sig')
            f.write('#EXTM3U\n')
            yyy = 0
            for name in filelist:
                if os.path.isdir(name) == False:
                    fileformat = os.path.splitext(name)
                    print(name)
                    if fileformat[1] == '.mp3' :
                        audio = MP3(name)
                    elif fileformat[1] == '.flac':
                        audio = FLAC(name)
                    elif fileformat[1] == '.aac' :
                        audio = AAC(name)
                    elif fileformat[1] == '.m4a' :
                        audio = MP4(name)
                    elif fileformat[1] == '.ogg' :
                        audio = OggVorbis(name)
                    elif fileformat[1] == '.opus' :
                            audio = OggOpus(name)
                    else:
                        continue
                    filelength = int(audio.info.length)
                    filenameen = name.rfind(sp)
                    filenamedot = name.rfind('.')
                    filename = name[filenameen+1:filenamedot]
                    filepath = name[len(dirpath)+1:]
                    print("dirpath == "+dirpath)
                    print("dirpath2 == "+dirpath[dirpath.rfind(sp):])
                    f.write('#EXTINF:' + str(filelength) + ',' + filename + '\n' + dirpath[dirpath.rfind(sp)+1:] + sp + filepath + '\n')
                    yyy += 1
                else:
                    pass

            f.close()
            print("--------------------------------------------\n" + savepath + sp + playlistname + '.m3u8\nが出力されました。')
            print("ファイル数：" + str(yyy))


Glist = Gplaylist(sys.argv)
Glist.Gm3u8()