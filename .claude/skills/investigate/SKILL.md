---
name: investigate
description: アイデアを調査し、出典付きの調査ノートを 20_Investigation に作成する。テーマのリサーチ・下調べ・最新動向の調査・「〜について調べて」と頼まれたときに使う。
when_to_use: ユーザーがテーマの調査・リサーチ・下調べを求めたとき。10_Ideas のアイデアを掘り下げるとき。
argument-hint: [調査テーマ]
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# 調査スキル

「$ARGUMENTS」について調査し、`20_Investigation/` に出典付きの調査ノートを作成する。

## 手順
1. まず `10_Ideas/` を Grep し、このテーマの元アイデアノートがあるか確認する。
2. WebSearch / WebFetch で一次情報・最新動向を確認する。**出典URLは必須**。
3. `${CLAUDE_SKILL_DIR}/template.md` の構造に従ってノートを作成する。
   - ファイル名: `20_Investigation/YYYY-MM-DD_テーマ.md`（日付は本日、テーマは簡潔に）
4. 事実と推測を明確に分ける。不確実な点は「要確認」と明記する。
5. frontmatter の `related` に、元になった 10_Ideas ノートへの `[[ウィキリンク]]` を張る。
6. タグは `#status/investigating` と `#topic/分野` を付与する。

## 厳守事項
- 出典のない主張を断定で書かない。
- 一次情報（公式・論文・公的機関）を優先し、アグリゲータは補助に留める。
- テンプレの見出し構成は崩さない（後で Dataview / 横断検索が効くため）。

テンプレ: [template.md](template.md)
