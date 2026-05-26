# Obsidian × Claude Code のナレッジリポジトリ

Obsidian の markdown vault を知識ベースとして使い、Claude Code が調査・整形・Qiita 投稿までを担う個人用ナレッジリポジトリ。

## 概要

- vault に放り込んだ「思いつき」「調査依頼」を Claude Code が自動で整理・調査
- ドラフトまで自動生成、Qiita への**下書き投稿**まで自動化
- 公開は人間が最終確認して手動で実行
- 全データは markdown + git で管理(将来のツール変更に強い)

## 全体構成

| 項目 | 内容 |
|---|---|
| OS | Windows 11 + WSL2 (Ubuntu-22.04) |
| エディタ | Obsidian (Windows 側) |
| AI / 自動化 | Claude Code (WSL 側) |
| vault の場所 | WSL 内 (`/home/taiki/...`)、Obsidian からは `\\wsl$\Ubuntu-22.04\...` 経由でアクセス |
| バージョン管理 | git + private GitHub リポジトリ |
| 連携先 | Qiita (API 経由で下書き投稿) |

## ディレクトリ構造

数字プレフィックスで Obsidian のサイドバーで並び順を固定する。`01〜04` が運用フローの本流、`90〜99` が支援用フォルダ。

```
Knowledge/
├── 01_inbox/        # 雑な思いつき・依頼の起点
├── 02_research/     # 調査中ノート
├── 03_drafts/       # Qiita 投稿前のドラフト
├── 04_published/    # 公開済み(qiita_url を保持)
├── 90_templates/    # Templater 用テンプレート
├── 99_sources/      # 調査の参照ログ(URL・要約)
├── .claude/
│   ├── commands/    # スラッシュコマンド定義
│   └── settings.local.json
├── CLAUDE.md        # 運用ルール
├── OBSIDIAN_USAGE.md  # Obsidian での検索・運用ガイド
├── .gitignore
└── .gitattributes
```

## Frontmatter スキーマ

各ノートの先頭に最小限の frontmatter を付与する。

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

### ステータス遷移

| status | 意味 |
|---|---|
| `inbox` | 起点ノート、未処理 |
| `researching` | Claude Code が調査中 |
| `draft` | ドラフト完成、Qiita 投稿待ち |
| `published` | Qiita 公開済み |

Dataview で `WHERE status = "draft"` のようなクエリで絞り込める。

## 必要なツール

### Obsidian プラグイン

| プラグイン | 用途 |
|---|---|
| Dataview | ステータス別ビュー、frontmatter クエリ |
| Templater | 新規ノート作成時に frontmatter 自動挿入 |
| Obsidian Git | コミット自動化 |

### Claude Code 側

- filesystem MCP(既存)
- web_search / web_fetch(調査用、組み込み)
- Qiita API 呼び出し用のローカルスクリプト(`/publish-qiita` 内で使用)

## Claude Code スラッシュコマンド

`.claude/commands/` 配下に以下を配置する。

### `/capture [初期アイディア]`

雑なアイディアから、Claude Code が質問しながらテンプレートを埋めて `01_inbox/` にノートを作成する。

**動作**

1. 初期アイディアを受け取る(引数になければ最初に聞く)
2. 以下を順に質問しながら埋めていく:
   - 何を知りたいか(調査の目的・問い)
   - 想定される読者・出力先(自分用メモか Qiita 投稿か)
   - 既知の参考リンク・きっかけ(あれば)
   - 関連タグの候補(複数提示して選ばせる)
3. 回答内容を `90_templates/inbox-template.md` をベースに埋める
4. `01_inbox/<YYYY-MM-DD>-<slug>.md` として保存(`status: inbox`)

「これ気になるんだけど何を聞けばいいか分からない」状態でも始められる、入口を整えるためのコマンド。

### `/process-inbox [オプション]`

`01_inbox/` 内のノートを処理する。引数なしの場合は `status: inbox` 全件が対象。

**オプション**

| オプション | 動作 |
|---|---|
| `--file <ファイル名>` | 特定のファイル 1 件だけ処理 |
| `--tag <タグ名>` | 指定タグを持つノートだけ処理 |
| `--limit <数>` | 古い順に N 件だけ処理 |

複数指定可(`--tag claude-code --limit 3` など)。

**処理内容**

1. 対象ノートを `02_research/` に移動し、status を `researching` に更新
2. 必要に応じて web 調査を実行
3. 参照 URL・要約を `99_sources/<日付>-<トピック>.md` に保存
4. 調査結果を本文に追記
5. 内容が固まったら `03_drafts/` に移動し、status を `draft` に更新

### `/ask <ファイル名> <質問>`

既存ノートに対する追加質問・深掘りを行う。

1. 指定ノートを読み込む
2. 質問内容に応じて web 調査を実行(必要なら)
3. ノート末尾の `## Q&A` セクションに **質問 + 回答** を追記
4. 追加で参照したソースは `99_sources/` に保存
5. frontmatter の `updated` を更新

ステータスに関わらず使える(`inbox` / `researching` / `draft` / `published` すべて対象)。
ドラフト確認中の「ここ詳しく」「ここの根拠は?」を貯めていける。

### `/draft-qiita <ファイル名>`

`03_drafts/` の指定ノートを Qiita 形式に整形する。

- `![[image.png]]` を標準 markdown 画像記法に変換
- コードブロックの言語タグを確認
- Qiita のタグ上限(5 個)に絞り込み
- 本文を Qiita のトーンに微調整

### `/publish-qiita <ファイル名>`

Qiita API で**下書き保存**まで実行する。

- API token は `~/.config/qiita/token` から読み込む
- 公開はせず、下書き状態で止める
- 返ってきた URL を frontmatter の `qiita_url` に書き込む
- 実際の公開は Qiita 上で手動で実施

## Qiita 連携

- Qiita API token を `~/.config/qiita/token` に保存(`chmod 600`)
- token は vault や git に**絶対に含めない**(`.gitignore` で念押し)
- 自動公開はしない。下書き保存までで止め、人間レビューを必ず挟む

## セットアップ手順

1. `Knowledge/` ディレクトリを作成し `git init`
2. private GitHub リポジトリを作成して remote 設定
3. Obsidian で `Knowledge/` を vault として開く
4. Dataview / Templater / Obsidian Git をインストール
5. `CLAUDE.md` と `90_templates/inbox-template.md` を作成
6. `.claude/commands/process-inbox.md` を作成
7. `01_inbox/` に試しに 1 件投げて `/process-inbox` を実行

`/capture` / `/ask` と Qiita 連携(`/draft-qiita` / `/publish-qiita`)は後から追加。
まずは「inbox に投げれば Claude Code が下書きまで作る」を動かすのを優先する。

## 運用フロー

1. `/capture` または手動で `01_inbox/` に md を作る
2. `/process-inbox` で調査・整形 → `02_research/` を経由して `03_drafts/` に自動移動
3. Obsidian でドラフトを目視確認、必要なら `/ask` で深掘り
4. `/draft-qiita` で Qiita 整形
5. `/publish-qiita` で Qiita 下書き投稿
6. Qiita 上で最終確認 → 公開
7. ノートを `04_published/` に移動、frontmatter を `published` に更新(自動化可)

ノートの探し方・Dataview クエリ例は `OBSIDIAN_USAGE.md` を参照。

## 注意事項

### WSL / Obsidian

- vault を WSL 側に置く場合、稀に Obsidian の file watcher が取りこぼす可能性がある
- 気になる場合は WSLg で Linux 版 Obsidian を動かす選択肢もある
- 改行コードは LF 統一(`.gitattributes` に `* text=auto eol=lf`)

### セキュリティ

- API token を git にコミットしない(`.gitignore` で `*token*`、`.env` などを除外)
- private な調査メモと公開予定のドラフトは物理的にフォルダを分ける
- vault のリポジトリは private を徹底

### 設計上の制約

- **自動公開はしない**。誤情報・著作権・タグミスを人間が止められるようにする
- 最初から完璧な frontmatter スキーマを決めない。`status` と `tags` のみで始めて、必要になったら足す
