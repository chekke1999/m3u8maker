#!/usr/bin/env python3
import glob,os,sys,argparse,inspect,re
from re import A
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from pprint import pprint
from lib.mutagen import File
from lib.pathlib import Path
from lib.pathlib import PurePath

def Playlist(args):
    # プレイリストの保存先&ファイル名ジェネレータを返すジェネレータ
    playlist_dict = {}
    sep = os.sep
    def set_palylist(dirlib):
        # 保存先
        playlist_dict["s_path"] = f"{args.save}{sep}{dirlib.name}.m3u8" if args.save != None else f"{dirlib.resolve()}.m3u8"
        # ファイルリストジェネレーター
        def flie_list_gen(): 
            for k in (str(j) for j in (i for i in dirlib.glob("**/*") if i.is_file()) if File(str(j)) != None):
                # デフォトは相対パス
                if args.absolute_path:
                    yield k
                else:
                    yield os.path.relpath(k,os.path.dirname(playlist_dict["s_path"]))
        playlist_dict["f_list"] = flie_list_gen()
        return playlist_dict
    for dpath in args.input:
        # Namespace(input=['/hoge/hoge1'], sub_directory=False, absolute_path=False, save=None) 
        dirlib = Path(dpath)
        # 入力されたディレクトリ存在チェック
        if not dirlib.is_dir():
            print(f"inputに指定したディレクトリ: {dpath}は存在しません。")
            continue
        if args.sub_directory:
            # サブディレクトリ有効時 and ディレクトリか否かのチェック
            for dirlib_in in (i for i in dirlib.glob("*") if i.is_dir()):
                yield set_palylist(dirlib_in)
        else:
            # サブディレクトリ無効時
            yield set_palylist(dirlib)

def PlaylistWrite(playlist_dict):
    # with opne(playlist_dict["s_path"]):
    #     for file_path in playlist_dict["f_gen"]:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ディレクトリをベースにm3u8形式のプレイリストを生成します。",formatter_class=argparse.RawTextHelpFormatter)
    # 必須引数
    parser.add_argument("-i", "--input", required=True, nargs='*',
    help="指定したディレクトリの中の音声ファイル群を参照したm3u8プレイリストを生成。ファイル名は指定したディレクトリ名になる。")
    # オプション引数
    parser.add_argument("-sd","--sub-directory", action="store_true",
    help="    [-i]で指定したディレクトリのサブディレクトリをプレイリスト化する")
    parser.add_argument("-ap","--absolute-path", action="store_true",
    help="m3u8プレイリストのファイル参照方法が絶対パスになる。デフォルトは相対パス。")
    parser.add_argument("-s","--save", help="プレイリストの保存先を指定する。")
    parser.add_argument("-r","--remote", action="store_true",
    help="本プログラムが動いてるコンピュータ(以後サーバと呼ぶ)でファイル共有を行ってる状態で本コンピュータのファイル共有している\
    ディレクトリをマウントしたコンピュータ(以後クライアントと呼ぶ)がsshの引数越しにコマンドを実行した場合サーバ側から見たとき存在\
    しないパスが渡される可能性があるので、事前にlibrary.iniに起点となるディレクトリを設定し、本オプションにて外部のクライアンから\
    のコマンドであることを明示的に示すことで、サーバのディレクトリパスに変換する")
    args = parser.parse_args()
    for i in Playlist(args):
        PlaylistWrite(i)

