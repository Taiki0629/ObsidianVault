---
name: summarize
description: 20_Investigation の調査ノートを構造化し、再利用可能なまとめを 30_Summary に作成する。「まとめて」「整理して」「要約して」調査結果を知識化するときに使う。
when_to_use: 調査が終わり、結果を再利用可能なナレッジとして構造化したいとき。
argument-hint: [対象テーマ または 調査ノート名]
allowed-tools: Read, Write, Edit, Glob, Grep
---

# まとめスキル

`20_Investigation/` の「$ARGUMENTS」に該当する調査ノートを読み、`30_Summary/` に構造化したまとめを作成する。

## 手順
1. `20_Investigation/` を Grep / Glob し、対象の調査ノートを特定して読む。
   複数該当する場合は関連するものをすべて読み、統合する。
2. `${CLAUDE_SKILL_DIR}/template.md` の構造でまとめを作成する。
   - ファイル名: `30_Summary/YYYY-MM-DD_テーマ.md`
3. 「結論 / 根拠 / 使いどころ / 落とし穴」を第三者が再利用できる粒度で書く。
4. frontmatter の `status` を `summarized` にする。
5. `related` に元の調査ノートへの `[[ウィキリンク]]` を張る。
6. 元調査ノートにも、このまとめへの逆リンクを追記する。

## 厳守事項
- 調査ノートにない事実を新たに足さない（足す必要があれば investigate に戻す）。
- 「使いどころ」を必ず書く（後でアウトプットの素材になるため）。

テンプレ: [template.md](template.md)
