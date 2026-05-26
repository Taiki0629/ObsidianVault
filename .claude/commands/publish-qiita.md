---
description: Qiita API で下書き保存して qiita_url を frontmatter に書き込む
argument-hint: <ファイル名>
allowed-tools: Read, Edit, Glob, Bash
---

`$ARGUMENTS` のノートを Qiita に **下書き(private 投稿)** として保存する。**公開は絶対にしない**。

## 手順

1. 対象ファイルを `Glob` で `03_drafts/**/<name>*` から探す。1 件に絞れなければユーザーに確認。
2. `scripts/publish-qiita.py <ファイルパス>` を実行する。スクリプトが:
   - `~/.config/qiita/token` から token 読み込み(無ければエラー)
   - frontmatter / 本文をパース
   - Qiita API `POST /api/v2/items` に `private: true` で送信
   - 返ってきた `url` を標準出力に出す
3. 標準出力の URL を取得し、ノートの frontmatter `qiita_url` に書き込む。`updated` を今日に。
4. ユーザーに以下を伝える:
   - 「Qiita 上で内容を確認 → 公開設定を変更してください(自動公開はしない設計)」
   - 返ってきた URL

## エラー時

- token が無い: `~/.config/qiita/token` を作って `chmod 600` を促す。コミットしない注意も。
- API エラー: ステータスコードと本文をそのまま表示。ノートには何も書き込まない。
- 既に `qiita_url` がある: 上書きはせず、ユーザーに確認(再投稿か中止か)。

## ルール

- `private: false`(公開)では絶対に投稿しない。スクリプト側で固定。
- token を echo したり log に出したりしない。
