---
name: scenario
description: 30_Summary のまとめを素材に、動画台本を 50_Scenario に作成する。「台本にして」「動画用にして」「スクリプト書いて」と頼まれたときに使う。
when_to_use: まとめを動画の台本に仕上げたいとき。
argument-hint: [対象テーマ または まとめノート名]
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 動画台本スキル

`30_Summary/` の「$ARGUMENTS」を素材に、動画台本を `50_Scenario/` に作成する。

## 手順
1. `30_Summary/` を Grep / Glob し、対象まとめを読む。
2. `${CLAUDE_SKILL_DIR}/template.md` の構成で台本を作成する。
   - ファイル名: `50_Scenario/YYYY-MM-DD_動画タイトル.md`
3. 構成は フック → 本編 → まとめ → CTA。
4. **ナレーション（話し言葉）とテロップ/画面指示を分けて記載**する。
5. frontmatter の `related` に素材の `[[まとめ]]` へのリンクを張る。

## 厳守事項
- 書き言葉ではなく、声に出して自然な話し言葉にする。
- 冒頭5秒で視聴者を掴むフックを必ず置く。
- まとめにない事実を創作しない。

テンプレ: [template.md](template.md)
