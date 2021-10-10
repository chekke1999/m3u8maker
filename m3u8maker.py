#!/usr/bin/env python3
import os,argparse,re,toml
from pprint import pprint
from pathlib import Path
from mutagen import File

class Playlist:
    def __init__(self, input_directory:list, sub_directory:bool, absolute_path:bool, save:str, remote:bool):
        self.input = input_directory
        self.sub_directory = sub_directory
        self.absolute_path = absolute_path
        self.save = save

    # プレイリストに記述する為に必要なファイルの情報を返すジェネレータ
    def __FileInfo(self,dirlib):
        for afile in (j for j in (i for i in sorted(dirlib.glob("**/*")) if i.is_file()) if File(str(j)) != None):
            afile_str = str(afile)
            audio_length = re.match("(.*)(?=\.)",str(File(afile_str).info.length)).group()
            # デフォトは相対パス
            if self.absolute_path:
                yield {"title":afile.stem,"file":afile_str,"length":audio_length}
            else:
                yield {
                    "title":afile.stem,
                    "file":os.path.relpath(afile_str,os.path.dirname(self.save_path)), 
                    "length":audio_length
                    }
    # チェック結果に応じて、__FileInfoジェネレーターと保存先情報を返すジェネレーター
    def __InputChecker(self):
        for dpath in self.input:
            dirlib = Path(dpath)
            sep = os.sep
            # 保存先
            self.save_path = f"{self.save}{sep}{dirlib.name}.m3u8" if self.save != None else f"{dirlib.resolve()}.m3u8"
            # 入力されたディレクトリ存在チェック
            if not dirlib.is_dir():
                print(f"inputに指定したディレクトリ: {dpath}は存在しません。")
                continue
            if self.sub_directory:
                # サブディレクトリ有効時 and ディレクトリか否かのチェック
                for dirlib_in in (i for i in dirlib.glob("*") if i.is_dir()):
                    yield self.__FileInfo(dirlib_in),self.save_path
            else:
                # サブディレクトリ無効時
                yield self.__FileInfo(dirlib),self.save_path
    def Write(self):
        for result in self.__InputChecker():
            save_path = result[1]
            for finfo in result[0]:
                with open(save_path,mode="w",encoding='utf-8') as f:
                    f.write('#EXTM3U\n')
                    pprint(finfo["title"])
                    f.write(f"#EXTINF:{finfo['length']},{finfo['title']}\n{finfo['file']}\n")
            print("-"*80)
            print(f"{self.save_path}が出力されました")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ディレクトリをベースにm3u8形式のプレイリストを生成。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # 必須引数
    parser.add_argument(
        "-i", "--input", required=True, nargs='*',
        help="指定したディレクトリの中の音声ファイル群を参照したm3u8プレイリストを生成。ファイル名は指定したディレクトリ名になる。"
    )
    # オプション引数
    parser.add_argument(
        "-sd","--sub-directory", action="store_true",
        help="[-i]で指定したディレクトリのサブディレクトリをプレイリスト化する"
    )
    parser.add_argument(
        "-ap","--absolute-path", action="store_true",
        help="m3u8プレイリストのファイル参照方法が絶対パスになる。デフォルトは相対パス。"
        )
    parser.add_argument("-s","--save", help="プレイリストの保存先を指定する。")
    parser.add_argument(
        "-r","--remote", action="store_true",
        help="本プログラムが動いてるコンピュータ(以後サーバと呼ぶ)でファイル共有を行ってる状態で本コンピュータのファイル共有している\
        ディレクトリをマウントしたコンピュータ(以後クライアントと呼ぶ)がsshの引数越しにコマンドを実行した場合サーバ側から見たとき存在\
        しないパスが渡される可能性があるので、事前にlibrary.iniに起点となるディレクトリを設定し、本オプションにて外部のクライアンから\
        のコマンドであることを明示的に示すことで、サーバのディレクトリパスに変換する"
        )
    # Namespace(input=['/hoge/hoge1'], sub_directory=False, absolute_path=False, save=None) 
    args = parser.parse_args()
    p = Playlist(args.input,args.sub_directory,args.absolute_path,args.save,args.remote)
    p.Write()

