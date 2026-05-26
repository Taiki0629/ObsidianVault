---
description: 雑なアイディアを質問で深掘りして 01_inbox/ にノートを作成
argument-hint: [初期アイディア]
allowed-tools: Read, Write, Glob, Bash
---

ユーザーの「気になること」を整理して `01_inbox/` にノートを作成する。

## 手順

1. 引数 `$ARGUMENTS` を初期アイディアとして受け取る。空なら最初に「今気になっていることは?」と聞く。
2. 以下を **1 つずつ** 順番に質問して埋める(まとめて聞かない)。
   - 何を知りたいか(調査の目的・問い)
   - 想定読者・出力先(自分用メモ / Qiita 投稿 のどちらか)
   - 既知の参考リンク・きっかけ(あれば。なくても可)
   - 関連タグ候補。既存タグを `grep -rh '^tags:' 01_inbox 02_research 03_drafts 04_published 2>/dev/null` で拾い、候補 + 新規提案を 3〜5 個提示してユーザーに選ばせる。
3. `90_templates/inbox-template.md` の本文構造に沿って回答を埋める。frontmatter は以下:
   - `status: inbox`
   - `created` / `updated`: 今日の日付(`YYYY-MM-DD`)
   - `tags`: 選ばれたタグの配列
   - `source`: 参考リンクがあれば
4. slug を ASCII の kebab-case で生成(例: `mcp-skills-overview`)。日本語タイトルでも slug は ASCII に。
5. ファイルパス: `01_inbox/<YYYY-MM-DD>-<slug>.md`。同名があれば末尾に `-2` 等。
6. 作成したファイルパスを最後に表示。

## ルール

- frontmatter のコロン後に半角スペース、リストは `[a, b]` 形式、日付は `YYYY-MM-DD`。崩すと Dataview が拾えない。
- inbox 段階では web 調査はしない。あくまで「問いを整える」段階。
- ノートを `01_inbox/` 以外に作らない。
