---
name: monthly
description: 月次レビューを 83_Monthly に作成し、アウトプット成果とナレッジ全体を振り返る。
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find *), Bash(ls *)
---

# 月次レビュー

今月分のレビューを `83_Monthly/YYYY-MM.md` に作成する。

## 過去30日間で更新されたノート
```!
find . -type f -name '*.md' -mtime -30 -not -path './.claude/*' -not -path './8*_*/*' | sort
```

## 各フォルダの現在のノート数
```!
for d in 10_Ideas 20_Investigation 30_Summary 40_Output 50_Scenario; do printf '%s: ' "$d"; find "$d" -name '*.md' 2>/dev/null | wc -l; done
```

## 手順
1. 今月の `82_Weekly/` を読み、月の流れを把握する。
2. `83_Monthly/YYYY-MM.md` を作成し、以下を振り返る。
   - **アウトプット成果**: 公開した記事・台本の本数と反応
   - **ナレッジの蓄積**: まとめが増えたテーマ領域
   - **転換率**: Ideas のうち Output まで到達した割合の体感
   - **来月の重点テーマ**: 注力する分野
3. 死蔵されているアイデア・調査を棚卸しし、アーカイブ候補を挙げる。
