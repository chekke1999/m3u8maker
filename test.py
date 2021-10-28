#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser(
    description="ディレクトリをベースにm3u8形式のプレイリストを生成。",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    "-i", "--input", required=True, nargs='*',
    help="指定したディレクトリの中の音声ファイル群を参照したm3u8プレイリストを生成。ファイル名は指定したディレクトリ名になる。"
)
args = parser.parse_args()
print(args.input)