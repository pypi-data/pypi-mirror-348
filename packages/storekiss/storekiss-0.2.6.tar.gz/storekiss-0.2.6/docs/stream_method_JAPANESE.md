# storekissライブラリのstream()メソッド

## 概要

`stream()`メソッドは、コレクションやクエリの結果をバッチ単位で効率的に取得するためのメソッドです。Firestoreの同名メソッドと互換性があり、大量のデータを扱う際のメモリ使用量とパフォーマンスを最適化します。

## 特徴

- バッチ単位でドキュメントを取得し、イテレータとして返す
- メモリ使用量を抑えながら大量のデータを処理できる
- SQLiteとPostgreSQLの両方に対応（将来的な拡張性）
- Firestoreと互換性のあるAPI

## 使用方法

### 基本的な使用方法

```python
db = litestore.Client("my_database.db")
collection_ref = db.collection("users")

# stream()メソッドを使用してドキュメントを順次取得
for doc in collection_ref.stream():
    print(f"ドキュメントID: {doc.id}, データ: {doc.to_dict()}")
```

### バッチサイズの指定

```python
# バッチサイズを指定して効率的に取得（デフォルトは20）
for doc in collection_ref.stream(batch_size=10):
    print(f"ドキュメントID: {doc.id}, データ: {doc.to_dict()}")
```

### クエリとの組み合わせ

```python
# whereクエリとの組み合わせ
query = collection_ref.where("age", ">=", 30)
for doc in query.stream():
    print(f"ドキュメントID: {doc.id}, 年齢: {doc.to_dict().get('age')}")

# 複数の条件を組み合わせたクエリ
query = collection_ref.where("age", ">=", 30).where("city", "==", "Tokyo")
for doc in query.stream(batch_size=5):
    print(f"ドキュメントID: {doc.id}, データ: {doc.to_dict()}")

# order_byとの組み合わせ
query = collection_ref.order_by("created_at", direction="DESC").limit(10)
for doc in query.stream():
    print(f"ドキュメントID: {doc.id}, 作成日時: {doc.to_dict().get('created_at')}")
```

### ドキュメントの更新

```python
# stream()を使用して大量のドキュメントを効率的に更新
for doc in collection_ref.stream(batch_size=50):
    doc_id = doc.id
    doc_ref = collection_ref.document(doc_id)
    doc_ref.update({"processed": True})
```

## 技術的な詳細

### 実装の概要

`stream()`メソッドは内部的に`limit()`と`offset()`を使用してバッチ処理を実現しています。各バッチでは指定されたサイズ分のドキュメントを取得し、イテレータとして順次返します。

```python
def stream(self, batch_size: int = 20):
    # バッチ処理のための初期化
    offset = 0
    
    while True:
        # バッチサイズ分のドキュメントを取得
        query = self._collection.limit(batch_size)
        if offset > 0:
            query = query.offset(offset)
            
        # クエリを実行
        batch = query.get()
        
        # 結果が空の場合は終了
        if not batch:
            break
            
        # 各ドキュメントを順番に返す
        for doc in batch:
            yield doc
            
        # 取得したドキュメント数がバッチサイズより少ない場合は終了
        if len(batch) < batch_size:
            break
            
        # 次のバッチのためにオフセットを更新
        offset += batch_size
```

### SQLクエリの最適化

内部的には、以下のようなSQLクエリが生成されます：

1. 最初のバッチ：
   ```sql
   SELECT id, data FROM "collection_name" LIMIT ?
   ```

2. 2番目以降のバッチ：
   ```sql
   SELECT id, data FROM "collection_name" LIMIT ? OFFSET ?
   ```

3. 条件付きクエリの場合：
   ```sql
   SELECT id, data FROM "collection_name" WHERE json_extract(data, '$.field') >= ? LIMIT ? OFFSET ?
   ```

## パフォーマンスの考慮事項

- バッチサイズが大きすぎると、メモリ使用量が増加します
- バッチサイズが小さすぎると、データベースへのクエリ回数が増加します
- 一般的には、処理内容に応じて10〜100の範囲でバッチサイズを調整することをお勧めします
- 大量のデータを処理する場合は、適切なインデックスを作成することでパフォーマンスが向上します

## 将来の拡張性

この実装は、将来的にPostgreSQLをサポートするための拡張性を考慮しています。SQLiteとPostgreSQLの両方で同様のバッチ処理機能を提供できるよう設計されています。
