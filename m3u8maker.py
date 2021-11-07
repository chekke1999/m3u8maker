#!/usr/bin/env python3
import argparse,re,toml,shutil
from os import path,sep
from sys import stderr
from pathlib import Path
from mutagen import File
from subprocess import call

class Playlist:
    def __init__(self, input_directory:list, sub_directory:bool, absolute_path:bool, save:str, remote:bool):
        self.input = input_directory
        self.sub_directory = sub_directory
        self.absolute_path = absolute_path
        self.save = save
        self.remote = remote
        config_path = f"{path.expanduser('~')}{sep}.config{sep}m3u8maker{sep}config.toml"
        self.conf = toml.load(config_path)
        # ライブラリの上書き防止
        # シンボリックリンクを解決した絶対パスを比較
        if Path(self.conf["main_lib"]).resolve() == Path(self.conf["sub_lib"]).resolve():
            print(f"設定ファイル: {config_path}", file=stderr)
            print("以下のmain_libとsub_libの記述が同じです。ライブラリ破壊防止のため終了します。", file=stderr)
            print(f"main_lib{self.conf['main_lib']}, moble_path: {self.conf['sub_lib']}", file=stderr)
            exit()

    def path_resolve(self,path:str):
        # シンボリックリンクや相対パスを絶対パスに
        return str(Path(path).resolve())
    def AudioFileSearch(self,dirlib):
        for files in (i for i in sorted(dirlib.glob("**/*")) if i.is_file()):
            if File(str(files)) != None:
                yield files 
    # パス変換処理本体
    def PathConv(self, after:str, from_behind:str, source:str):
        # from_behind = self.path_resolve(from_behind)
        # source = self.path_resolve(source)
        print("from: " + from_behind)
        print("source: " + str(Path(source).resolve()))
        print("after: " + after)
        return Path(after + re.search(f"(?<={from_behind})(.*)",source).group())
    # リモート時のパス変換処理ラップ
    def RemoteDir(self,path):
        server_path = Path(self.conf["main_lib"])
        client_path = path.replace("\\","/")
        return self.PathConv(str(server_path),server_path.name,client_path)

    def Convinfo(self,dirlib):
        def CoverSerch(dirlib):
            reg_str = "(cover|folder).(png|jpg|jpeg)"
            for coverf in (i for i in sorted(dirlib.glob("**/*")) if re.search(reg_str,str(i),flags=re.IGNORECASE)):
                yield coverf
        print(dirlib)
        return {"cover":CoverSerch(dirlib),
            "audio":self.AudioFileSearch(dirlib)
        }


    def M3u8info(self,dirlib):
            # 保存先確定処理
        def SaveDir(dirlib):
            if self.save != None and not self.remote:
                return f"{self.save}{sep}{dirlib.name}.m3u8"
            elif self.save != None and self.remote:
                return f"{self.RemoteDir(self.save)}{sep}{dirlib.name}.m3u8"
            else:
                return f"{dirlib.resolve()}.m3u8"

        # プレイリストに記述する為に必要なファイルの情報を返すジェネレータ
        def FileInfo(dirlib):
            for afile in self.AudioFileSearch(dirlib):
                ap_path = afile.resolve()
                audio_length = re.match("(.*)(?=\.)",str(File(ap_path).info.length)).group()
                # デフォトは相対パス
                if self.absolute_path:
                    yield {"title":afile.stem,"file":ap_path,"length":audio_length}
                else:
                    yield {
                        "title":afile.stem,
                        "file":path.relpath(ap_path,path.dirname(Path(self.save_path).resolve())), 
                        "length":audio_length
                        }
        self.save_path = SaveDir(dirlib)
        return FileInfo(dirlib),self.save_path

    # チェック結果に応じて、関数の結果を返す
    def __Main(self,func):
        # if self.remote:
        #     self.save = self.RemoteDir(self.save)
        for dpath in self.input:
            # リモートの有無をチェックして基点ファイルを作成
            if self.remote:
                print("リモート接続として処理します")
                dirlib = self.RemoteDir(dpath)
            else:
                dirlib = Path(dpath)
            # 入力されたディレクトリ存在チェック
            if not dirlib.is_dir():
                print(f"inputに指定したディレクトリ: {dpath}は存在しません。", file=stderr)
                continue
            # サブディレクトリ有効チェック
            if self.sub_directory:
                for dirlib_in in (i for i in dirlib.glob("*") if i.is_dir()):
                    yield func(dirlib_in)
            else:
                # サブディレクトリ無効時
                yield func(dirlib)

    def MobileConv(self):
        # ファイルコピー。コピーの途中のディレクトリなければ作成
        def copy(from_p,to_p):
            print(f"{from_p} > {to_p}\n")
            to_p.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy(from_p,to_p)
        cnt = 0
        for data_info in self.__Main(self.Convinfo):
            # カバー画像をsub_lib で設定したディレクトリにコピー
            for i in data_info["cover"]:
                from_path = Path(i)
                to_path = self.PathConv(self.conf["sub_lib"],self.conf["main_lib"],str(i))
                print("カバー画像をコピーします")
                copy(from_path,to_path)
            # オーディオファイルを変換
            for i in data_info["audio"]:
                from_path = Path(i)
                to_path = self.PathConv(self.conf['sub_lib'],self.conf['main_lib'],str(i))
                to_path_conv = f"{to_path.parent}/{to_path.stem}{self.conf['to_conv_ext']}"
                if from_path.suffix.lower() in self.conf["not_conv_ext"]:
                    print(f"{from_path} > {to_path}\n")
                    copy(from_path,to_path)
                    continue
                print(f"{from_path} > {to_path_conv}\n")
                cmd = ["ffmpeg","-i",from_path,to_path_conv,"-y"] + self.conf["ffmpeg_op"]
                call(cmd)
        self.input = [str(self.PathConv(self.conf["sub_lib"],self.conf["main_lib"],i)) for i in self.input]
        self.remote = False 
        self.save = self.PathConv(self.conf["sub_lib"],self.conf["main_lib"],str(Path(self.save_path).parent))
        self.Write()

    def Write(self):
        for result in self.__Main(self.M3u8info):
            save_path = result[1]
            Path(save_path).parent.mkdir(parents=True,exist_ok=True)
            with open(save_path,mode="w",encoding='utf-8') as f:
                f.write('#EXTM3U\n')
                for finfo in result[0]:
                    print(finfo["title"])
                    f.write(f"#EXTINF:{finfo['length']},{finfo['title']}\n{finfo['file']}\n")
            print("-"*80)
            print(f"{self.save_path}が出力されました")
def main():
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
        "-a","--absolute-path", action="store_true",
        help="m3u8プレイリストのファイル参照方法が絶対パスになる。デフォルトは相対パス。"
        )
    parser.add_argument(
        "-m","--mobile-library", action="store_true",
        help="モバイル版として、音楽ファイルを圧縮したバージョンのライブラリ作成を行う"
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
    if args.mobile_library:
        p.MobileConv()
if __name__ == "__main__":
    main()