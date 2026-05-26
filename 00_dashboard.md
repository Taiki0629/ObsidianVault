---
status: meta
tags: [dashboard]
---

# Dashboard

vault の俯瞰用ノート。Dataview プラグインが有効になっていれば下のクエリが自動でテーブルに展開される。詳細は `Obsidianusage.md` を参照。

## Inbox(未処理)

```dataview
TABLE WITHOUT ID file.link AS "ノート", tags, updated
FROM "01_inbox"
WHERE status = "inbox"
SORT updated DESC
```

## Researching(調査中)

```dataview
TABLE WITHOUT ID file.link AS "ノート", tags, updated
FROM "02_research"
WHERE status = "researching"
SORT updated DESC
```

## Draft(投稿待ち)

```dataview
TABLE WITHOUT ID file.link AS "ノート", tags, updated
FROM "03_drafts"
WHERE status = "draft"
SORT updated DESC
```

## Qiita 未公開のドラフト

```dataview
TABLE updated, tags
FROM "03_drafts"
WHERE !qiita_url
SORT updated DESC
```

## 直近 7 日に更新

```dataview
TABLE status, updated
FROM "01_inbox" OR "02_research" OR "03_drafts"
WHERE updated >= date(today) - dur(7 days)
SORT updated DESC
```

## Published(参考)

```dataview
TABLE WITHOUT ID file.link AS "ノート", qiita_url, updated
FROM "04_published"
WHERE status = "published"
SORT updated DESC
LIMIT 20
```
