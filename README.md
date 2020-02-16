# m3u8playlistMaker
m3u8形式のプレイリストを引数に与えられたディレクトリごとに相対パスで生成します。最初の引数に-dでオプションをつけその次の引数に保存先を指定すると保存先基準の相対パスでm3u8を生成し、指定したディレクトリにm3u8を保存します。

## 使い方
保存先を指定しない場合
```bash
python3 m3u8playlistMaker fullpathdir
```

保存先を指定する場合
```bash
python3 m3u8playlistMaker -d savedir fullpathdir
```
