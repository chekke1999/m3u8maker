# m3u8playlistMaker
引数で渡されたディレクトリをベースにm3u8を生成するプログラム。
必要に応じて、引数でオプションを指定したり、設定ファイルを書き換えることで挙動が変化する。

## 使い方
保存先を指定しない場合
```bash
python3 m3u8playlistMaker fullpathdir
```

保存先を指定する場合
```bash
python3 m3u8playlistMaker -d savedir fullpathdir
```
