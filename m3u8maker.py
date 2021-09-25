#!/usr/bin/env python3
import glob,os,sys,argparse,inspect
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from lib.mutagen import File
from lib.pathlib import Path
from lib.pathlib import PurePath

class PathOperation:
    # Namespace(input=['/hoge/hoge1'], sub_directory=False, absolute_path=False, save=None)
    def __init__(self, args):
        # 入力されたディレクトリ存在チェック
        for dpath in args.input:
            check_dir = Path(dpath)
            if not check_dir.is_dir():
                print(f"inputに指定したディレクトリ: {dpath}は存在しません。\n処理を中断します。")
                exit()
        # プレイリスト辞書定義
        self.PlaylistProperty = {
            "savedir": args.save,
            "playlistName": {
                "subject_dir": None,
                "savedir": None
            }
        }
        # inputされたパスはpathlib
        for path in args.input:
            p = Path(path)
            if args.sub_directory:
                self.playlistName = 
            else:
        # m3u8保存先確定処理
        if args.save == None:
            self.__m3u8SavePath = []
            for path in input_path:
                if args.sub_directory:
                    self.__m3u8SavePath.append(path)
                else:
                    self.__m3u8SavePath.append(path.parent)
        else:
            self.__m3u8SavePath = Path(args.save)
        # m3u8に記述する音声ファイルパス

        
    @property
    def m3u8SavePath(self):
        return self.__m3u8SavePath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ディレクトリをベースにm3u8形式のプレイリストを生成します。")
    # 必須引数
    parser.add_argument("-i", "--input", required=True, nargs='*', help="\
    指定したディレクトリの中の音声ファイル群を参照したm3u8プレイリストを生成。ファイル名は指定したディレクトリ名になる。")
    # オプション引数
    parser.add_argument("-sd","--sub-directory", action="store_true", help="\
    [-i]で指定したディレクトリのサブディレクトリをプレイリスト化する")
    parser.add_argument("-ap","--absolute-path", action="store_true", help="\
    m3u8プレイリストのファイル参照方法が絶対パスになる。デフォルトは相対パス。")
    parser.add_argument("-s","--save", help="\
    プレイリストの保存先を指定する。")
    args = parser.parse_args()
    po = PathOperation(args)

    print(po.m3u8SavePath)
