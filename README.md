# m3u8maker
引数で渡されたディレクトリをベースにm3u8を生成するプログラム。
必要に応じて、引数でオプションを指定したり、設定ファイルを書き換えることで挙動が変化する。

## Install
Pythonとpipが使える環境であることを確認してください。
### Linux
ターミナルを開いて以下のコマンドを入力
```bash
git clone https://github.com/chekke1999/m3u8maker
cd m3u8maker
pip3 install .
```
### Windows
PowerShellやコマンドプロンプトを開いて以下のコマンドを入力
```powershell
git clone https://github.com/chekke1999/m3u8maker
cd m3u8maker
pip3 install .
```
## Uninstall
### Linux
```bash
pip3 uninstall m3u8maker
```
### Windows
```powershell
pip3 uninstall m3u8maker
```
## How to use

## Options
|Option|omit|Ex.|description|
|:-|:-|:-|:-|
|--input|-i||Plylistにしたいフォルダを渡す。必須引数。|