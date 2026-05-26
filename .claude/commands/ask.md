---
description: 既存ノートに追加質問して本文末の Q&A に追記
argument-hint: <ファイル名> <質問>
allowed-tools: Read, Edit, Glob, Grep, Bash, WebFetch, WebSearch
---

既存ノートへの追加質問・深掘り。`$ARGUMENTS` の最初のトークンを対象ファイル名、残りを質問として扱う。

## 手順

1. ファイル名はパスでもファイル名のみでも可。`Glob` で `**/<name>*` を探し、複数一致なら候補をユーザーに確認。
2. ノートを読み、質問に答えるのに必要なら `WebSearch` / `WebFetch` で調査。
3. 新規に参照したソースは `99_sources/<YYYY-MM-DD>-<slug>.md` に保存。
4. ノート末尾(なければ作る)の `## Q&A` セクションに以下の形で追記:

   ```markdown
   ### YYYY-MM-DD: <質問本文>

   <回答本文。参考にしたソースは [[YYYY-MM-DD-slug]] で内部リンク>
   ```

5. frontmatter の `updated` を今日に更新。`status` は変えない(`inbox` / `researching` / `draft` / `published` どれでも実行可)。

## ルール

- ノート全体を勝手に書き換えない。追記のみ。
- 出典が見つからない場合は「未確認」と明記する。憶測で書かない。
