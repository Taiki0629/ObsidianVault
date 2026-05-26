---
description: 01_inbox/ のノートを調査して 03_drafts/ までフローを進める
argument-hint: [--file <name>] [--tag <tag>] [--limit <n>]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
---

`01_inbox/` のノートを「調査 → ドラフト化」まで進める。`$ARGUMENTS` でフィルタする。

## 引数

- `--file <name>` : 特定ファイル 1 件
- `--tag <tag>` : 指定タグを持つノートのみ
- `--limit <n>` : 古い順に N 件

複数指定可。引数なしなら `status: inbox` 全件。

## 手順(各ノートに対して)

1. **researching 化**
   - `git mv 01_inbox/<file> 02_research/<file>` でフォルダ移動。
   - frontmatter `status` を `researching` に、`updated` を今日に。
2. **調査**
   - ノートの「何を知りたいか」を読み、必要に応じて `WebSearch` / `WebFetch` で調査。
   - 1 次ソース(公式ドキュメント・GitHub README・公式ブログ)を優先。Qiita/Zenn 等の二次情報は補助に留める。
3. **ソース保存**
   - 重要な参照 URL ごとに `99_sources/<YYYY-MM-DD>-<slug>.md` を作成。
   - 各ファイルは frontmatter `type: source`, `url:`, `fetched:`, `related:` を含む。
   - 本文に URL・要約(3〜5 行)・引用したい箇所をメモ。
4. **本文追記**
   - 調査結果をノート本文の「## 調査結果」セクションに追記。
   - 参考にしたソースは `[[YYYY-MM-DD-slug]]` で内部リンク。
5. **draft 化**
   - 内容が「自分が説明できる」レベルまで固まったら `git mv 02_research/<file> 03_drafts/<file>`。
   - `status: draft`、`updated` を今日に。
   - 固まらない場合は `researching` のまま残し、不足情報をノート末尾に「## TODO」として書く。

## 出力

処理したファイルごとに「inbox → researching → draft」のどこまで進めたかを 1 行で報告。
