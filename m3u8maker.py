#!/usr/bin/env python3
import glob,os,sys,argparse,inspect
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from lib.mutagen import File
from lib.pathlib import Path
from lib.pathlib import PurePath

class PathOperation:
    # Namespace(input=['/hoge/hoge1'], sub_directory=False, absolute_path=False, save=None)
    def __init__(self, args):
        # ディレクトリ存在チェック
        for dpath in args.input:
            check_dir = Path(dpath)
            if not check_dir.is_dir():
                print(f"inputに指定したディレクトリ: {dpath}は存在しません。\n処理を中断します。")
                exit()
        self.args = args


    def m3u8SavePath(self):
        if self.args.save == None:
            save_path = []
            for path in self.args.input:
                
                p = Path(path)
                if self.args.sub_directory:
                    save_path.append(p)
                else:
                    save_path.append(p.parent)
        else:
            save_path = Path(self.args.save)
        return save_path


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

    print(po.m3u8SavePath())
