# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリについて

これは **Obsidian の markdown vault** であり、コードプロジェクトではない。ビルド・テスト・lint は存在しない。Claude Code の役割は「ノートを調査・整形し、Qiita 下書き投稿まで自動化する」こと。詳細な背景は `README.md` と `Obsidianusage.md` を参照。

## ワークフロー上の不変条件(厳守)

ノートは status と物理フォルダが**常に一致**している必要がある。片方だけ更新するのは禁止。

| status | 配置フォルダ |
|---|---|
| `inbox` | `01_inbox/` |
| `researching` | `02_research/` |
| `draft` | `03_drafts/` |
| `published` | `04_published/` |

ノートを編集したら frontmatter の `updated` を必ず今日の日付に更新する(Dataview クエリが日付で絞り込むため)。

ファイル名は `YYYY-MM-DD-<slug>.md` 形式で統一する。

## Frontmatter スキーマ

すべてのノートは以下の frontmatter を持つ。`status` と `tags` 以外は空でも可。

```yaml
---
status: inbox          # inbox → researching → draft → published
tags: [claude-code, mcp]
created: 2026-05-15
updated: 2026-05-15
qiita_url:             # 公開後に埋まる
source:                # 調査の起点(URL や人)
---
```

frontmatter が崩れると Dataview が拾えなくなる。コロン後のスペース・`[a, b]` 形式・`YYYY-MM-DD` を守る。

## スラッシュコマンド

`.claude/commands/` に `/capture` `/process-inbox` `/ask` `/draft-qiita` `/publish-qiita` を定義する想定(現状フォルダは空)。各コマンドの仕様は `README.md` 「Claude Code スラッシュコマンド」節が一次ソース。実装・修正時はその仕様と齟齬を出さないこと。

調査の参照ログ(URL・要約)は `99_sources/<日付>-<トピック>.md` に保存する。テンプレートは `90_templates/` に置く。

## Qiita 連携(重要)

- **自動公開は絶対にしない**。`/publish-qiita` は API で**下書き保存までで停止**し、最終公開は人間が Qiita 上で行う。誤情報・著作権・タグミスを人間が止められる設計を崩さない。
- API token は `~/.config/qiita/token`(`chmod 600`)から読む。vault や git に**絶対に含めない**。
- Qiita のタグ上限は 5 個。`/draft-qiita` で `![[image.png]]` を標準 markdown 画像記法に変換する。

## 判断に迷ったら勝手に決めない

ノートの内容・調査方針・タグ選択・整形ルールなどで「どちらでも進められるが選択肢が複数ある」状況になったら、自分で決めずに **候補を 2〜4 個提示してユーザーに質問する**。具体的には:

- 調査の方向性が複数ありえる(深さ・スコープ・対象読者など)
- frontmatter のタグや slug の候補が複数ある
- ノートを `researching` のまま残すか `draft` に進めるかの判断
- Qiita 整形で表現を変える際に複数の言い回しがありえる
- 既存ファイル名と衝突した時のリネーム方針

「とりあえず妥当そうな方で進める」を避ける。後で巻き戻すコストの方が高い。なお、frontmatter スキーマ・フォルダ ↔ status 対応・Qiita 自動公開禁止のような **本ファイルで明示されたルール** は質問せず守る。

## 環境メモ

- Windows 11 + WSL2 (Ubuntu-22.04)。vault は WSL 側、Obsidian は Windows 側から `\\wsl$\...` 経由でアクセス。
- 改行は LF 統一。
- Obsidian の file watcher が稀に取りこぼすため、自動化スクリプトはファイル内容の確認をしてから次工程に進めること。
