---
name: weekly
description: 週次レビューを 82_Weekly に作成し、進捗と滞留を棚卸しする。
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find *), Bash(ls *)
---

# 週次レビュー

今週分のレビューを `82_Weekly/YYYY-Www.md` に作成する。

## 過去7日間で更新されたノート
```!
find . -type f -name '*.md' -mtime -7 -not -path './.claude/*' -not -path './81_Daily/*' -not -path './82_Weekly/*' -not -path './83_Monthly/*' | sort
```

## status: idea のまま停滞しているノート
```!
grep -rl 'status: idea' 10_Ideas 2>/dev/null | sort
```

## 手順
1. 今週の `81_Daily/` を読み、流れを把握する。
2. `82_Weekly/YYYY-Www.md` を作成し、以下を整理する。
   - **進んだもの**: 10→40 のどこまで進んだか
   - **滞留中**: idea のまま放置されているもの。続けるか捨てるか判断
   - **アウトプット実績**: 40_Output / 50_Scenario の成果
   - **来週やること**: `- [ ]` で
3. パイプライン（Ideas→Output）の詰まりどころを一言で診断する。
