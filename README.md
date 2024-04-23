# AtCoder Tools

AtCoder 関連の自作 CLI ツールを集めたリポジトリ。

## Problem Downloader

AtCoder の問題文（英語）をダウンロードしてマークダウンとして保存するツール。

### 実行方法

例えば ABC200 から ABC300 までの問題をダウンロードしたい場合、以下のコマンドを実行する。

```
poetry run python cmd/problem-downloader.py --contest-type abc --range-start 200 --range-end 301
```
