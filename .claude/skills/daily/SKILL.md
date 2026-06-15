---
name: daily
description: 本日の Daily ノートを 81_Daily に作成し、進捗と次アクションを整理する。
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find *), Bash(ls *)
---

# 日次ノート

本日分のノートを `81_Daily/YYYY-MM-DD.md` に作成する。

## 直近24時間で更新されたノート
```!
find . -type f -name '*.md' -mtime -1 -not -path './.claude/*' -not -path './81_Daily/*' -not -path './82_Weekly/*' -not -path './83_Monthly/*' | sort
```

## 手順
1. 上記の更新ノートを読み、今日の進捗を把握する。
2. `81_Daily/YYYY-MM-DD.md` を作成し、以下を記入する。
   - 今日やったこと（更新ノートへの `[[リンク]]` 付き）
   - 気づき・アイデアの種（必要なら 10_Ideas にも切り出す）
   - 明日の次アクション（`- [ ]` チェックボックスで）
3. 滞留しているもの（idea のまま放置されたノート）があれば軽く触れる。

簡潔に。日報は3〜5分で書ける分量に収める。
