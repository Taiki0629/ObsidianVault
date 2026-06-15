# 📊 Dashboard

> Dataview プラグインを有効にすると、以下が自動で一覧表示されます。

## 調査待ちのアイデア
```dataview
TABLE created, tags
FROM "10_Ideas"
WHERE status = "idea"
SORT created DESC
```

## 進行中（全パイプライン）
```dataview
TABLE status, source, updated
FROM "10_Ideas" OR "20_Investigation" OR "30_Summary"
WHERE status != "published"
SORT updated DESC
```

## アウトプット候補（まとめ済み・未公開）
```dataview
LIST
FROM "30_Summary"
WHERE status = "summarized"
```

## 公開済みアウトプット
```dataview
TABLE created, tags
FROM "40_Output" OR "50_Scenario"
WHERE status = "published"
SORT created DESC
```

## 滞留アラート（30日以上更新なし）
```dataview
TABLE status, updated
FROM "10_Ideas" OR "20_Investigation" OR "30_Summary"
WHERE updated <= date(today) - dur(30 days)
SORT updated ASC
```
