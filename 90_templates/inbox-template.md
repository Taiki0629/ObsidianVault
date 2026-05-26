<%*
// Templater テンプレ。新規ノートのファイル名は YYYY-MM-DD-<slug>.md を推奨。
const today = tp.date.now("YYYY-MM-DD");
-%>
---
status: inbox
tags: []
created: <% today %>
updated: <% today %>
qiita_url:
source:
---

# <% tp.file.title %>

## 何を知りたいか

-

## 想定読者・出力先

- 自分用メモ / Qiita 投稿(どちらか)

## 既知の参考リンク

-

## メモ
