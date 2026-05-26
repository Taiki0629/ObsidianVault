# OBSIDIAN_USAGE

`Knowledge/` vault で「特定のノートを見つける」「ステータス別に俯瞰する」ための使い方ガイド。

Obsidian は markdown ファイルの集合体に過ぎないが、Dataview プラグインを入れることで frontmatter を**簡易 DB のように扱える**。このファイルを vault ルートに置いておけば、Obsidian 内から直接参照できる。

## 0. 前提

- Dataview / Templater / Obsidian Git の 3 プラグインが入っていること
- 各ノートに README.md の **Frontmatter スキーマ**通りの frontmatter が付いていること

## 1. Dataview の基本

Dataview には 2 つの書き方がある。

### コードブロッククエリ

ノート内に以下のように書くと、その場でテーブルやリストとして展開される。

````markdown
```dataview
TABLE status, tags, updated
FROM "01_inbox" OR "02_research" OR "03_drafts"
WHERE status != "published"
SORT updated DESC
```
````

### インラインクエリ

文中に埋め込めるショート版。

```markdown
未処理ノート: `= length(filter(this.file.inlinks, (i) => i.status = "inbox"))`
```

普段は **コードブロッククエリ** だけ覚えていれば十分。

## 2. よく使うクエリ例

「ダッシュボード」用のノートを 1 つ作って、以下のクエリを並べておくと毎日の起点になる。
例: `00_dashboard.md` を vault ルートに作る。

### ステータス別の一覧

```dataview
TABLE WITHOUT ID file.link AS "ノート", tags, updated
FROM "01_inbox" OR "02_research" OR "03_drafts" OR "04_published"
WHERE status = "draft"
SORT updated DESC
```

`status = "draft"` の部分を `"inbox"` / `"researching"` / `"published"` に変えれば各ステータス用になる。

### タグで絞り込み

```dataview
LIST
FROM #claude-code
WHERE status != "published"
SORT file.mtime DESC
```

`#claude-code` の部分を実際のタグに変える。複数タグは `FROM #a AND #b` / `FROM #a OR #b`。

### 最近更新されたもの(直近 7 日)

```dataview
TABLE updated, status
FROM "01_inbox" OR "02_research" OR "03_drafts"
WHERE updated >= date(today) - dur(7 days)
SORT updated DESC
```

### Qiita 未公開のドラフト

```dataview
TABLE updated, tags
FROM "03_drafts"
WHERE !qiita_url
SORT updated DESC
```

`qiita_url` が空のドラフトだけ拾える。投稿候補リストとして使える。

### 特定のソース由来のノート

```dataview
LIST
FROM "01_inbox" OR "02_research" OR "03_drafts" OR "04_published"
WHERE contains(source, "claude.ai/code")
```

`source` フィールドに URL や人名が入っているので、出典別の俯瞰ができる。

### 進行中タスクの俯瞰(横断ビュー)

```dataview
TABLE status, length(file.tasks) AS "残タスク"
FROM "01_inbox" OR "02_research" OR "03_drafts"
WHERE status != "published"
SORT status ASC, updated DESC
```

ノート内に `- [ ] xxx` を書いておけば、未完了タスクが多い順に並べることもできる。

## 3. Obsidian 標準の検索機能

Dataview を使わなくてもできる範囲。

### クイックスイッチャー

`Ctrl + O`(Win)/ `Cmd + O`(Mac)でファイル名検索。
ファイル名に日付・slug を入れておけば(`2026-05-17-mcp-skills.md` など)、日付や単語の断片で一発で開ける。

### 全文検索

`Ctrl + Shift + F` でファイル横断検索。以下の演算子が使える。

| 構文 | 意味 |
|---|---|
| `tag:#claude-code` | タグで絞り込み |
| `path:03_drafts` | パスで絞り込み |
| `file:(.md)` | ファイル名で絞り込み |
| `line:(エラー)` | 同一行内に「エラー」を含む |
| `"完全一致 phrase"` | フレーズ検索 |

組み合わせ可: `tag:#mcp path:03_drafts エラー`

### タグペイン

左サイドバーの「タグ」ペインで、vault 内の全タグを一覧できる。
クリックすればそのタグを持つノート一覧に飛べる。

### グラフビュー

`Ctrl + G`(Win)/ `Cmd + G`(Mac)でノート同士のリンク関係を可視化。
内部リンク `[[xxx]]` を使っていないと意味が薄いが、関連ノートをたどるのに便利。

## 4. Templater の活用

`90_templates/` 配下のテンプレを新規ノート作成時に適用する。

### 設定

1. Templater の設定で **Template folder location** を `90_templates` に
2. 必要なら **Trigger Templater on new file creation** を有効化

### 使い方

- コマンドパレット → `Templater: Insert template` でテンプレを挿入
- ホットキー(例: `Alt + E`)を割り当てると即適用できる

`/capture` コマンドが書き込むテンプレも、ここで管理する `inbox-template.md` と同じ構造にしておくと、手動作成と Claude Code 作成のノートが揃う。

## 5. 推奨ワークフロー(検索目線)

毎日の使い方の目安:

1. **朝**: `00_dashboard.md` を開く → 未処理 inbox / draft の数を確認
2. **思いつき**: `/capture` か、Obsidian でテンプレ呼び出して `01_inbox/` に放り込む
3. **作業前**: ダッシュボードの「最近更新されたもの」で前回作業を思い出す
4. **記事化前**: 「Qiita 未公開のドラフト」クエリで投稿候補をピック
5. **振り返り**: タグペイン or グラフビューで「最近何を書いてるか」俯瞰

## 6. つまづきやすいポイント

- **frontmatter が崩れると Dataview が拾えない**: コロンの後にスペース、リストは `[a, b]` 形式、日付は `YYYY-MM-DD`
- **タグは `tags:` フィールドと本文中 `#tag` のどちらも有効**: 統一しておく(おすすめは frontmatter 側)
- **Dataview のキャッシュ**: たまに古い結果が出る。コマンドパレットの `Dataview: Rebuild current view` で再構築できる
- **Obsidian Git の自動 push**: 失敗していても通知が出にくい。たまに手動で git status を見る
