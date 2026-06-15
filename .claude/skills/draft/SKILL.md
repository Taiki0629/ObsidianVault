---
name: draft
description: 30_Summary のまとめを素材に、読者向けのブログ記事ドラフトを 40_Output に作成する。「記事にして」「ブログ書いて」「アウトプットして」と頼まれたときに使う。
when_to_use: まとめを公開用の記事に仕上げたいとき。
argument-hint: [対象テーマ または まとめノート名]
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 記事ドラフトスキル

`30_Summary/` の「$ARGUMENTS」を素材に、読者向けブログ記事のドラフトを `40_Output/` に作成する。

## 手順
1. `30_Summary/` を Grep / Glob し、対象まとめを読む。関連まとめがあれば併せて読む。
2. `${CLAUDE_SKILL_DIR}/template.md` の構成で記事を作成する。
   - ファイル名: `40_Output/YYYY-MM-DD_記事タイトル.md`
3. 構成は 導入（フック）→ 本論 → 結論。専門用語は初出で補足する。
4. まとめの「使いどころ」を記事の具体例・読者メリットに変換する。
5. frontmatter の `status` を `published`（公開前なら `draft`）にする。
6. `related` に素材の `[[まとめ]]` へのリンクを張る。

## 厳守事項
- まとめにない事実・数字を創作しない。
- 「まとめの貼り直し」にしない。読者の関心に沿って再構成する。
- 一次情報の出典は記事末尾にも残す。

テンプレ: [template.md](template.md)
