# バッチ処理の改善

## 概要

`WriteBatch` クラスの実装を改善し、より堅牢なバッチ処理を実現しました。以下の問題点を修正しています：

1. テーブル存在確認の欠如
2. 例外処理の不十分さ
3. エラーログの不足
4. リトライメカニズムの欠如
5. トランザクション管理の不完全さ

## 改善内容

### 1. テーブル存在確認の追加

バッチ処理前に、操作対象のすべてのテーブルの存在を確認し、存在しない場合は自動的に作成するようになりました。

```python
def _ensure_tables_exist(self):
    """
    バッチ操作で使用されるすべてのテーブルの存在を確認し、
    存在しない場合は作成します。
    """
    # 操作対象のテーブルを収集
    collections = set()
    for op in self._operations:
        if op[0] in ["set", "update", "delete"]:
            doc_ref = op[1]
            collections.add(doc_ref._document.collection)
    
    # 各テーブルの存在を確認
    for collection in collections:
        try:
            self._store._ensure_table_exists(collection)
            logger.debug(f"バッチ操作のためのテーブル確認: {collection} は存在します")
        except Exception as e:
            logger.error(f"テーブル {collection} の確認中にエラーが発生しました: {str(e)}")
            raise DatabaseError(f"Failed to ensure table exists: {collection}. Error: {str(e)}")
```

### 2. リトライメカニズムの実装

操作が失敗した場合に再試行する機能を追加しました。特に「no such table」エラーの場合はテーブルを作成して再試行し、`NotFoundError` の場合は `update` を `set` に変更して再試行します。

```python
def _execute_operation_with_retry(self, op, max_retries=3):
    """
    単一のバッチ操作を実行し、必要に応じて再試行します。

    Args:
        op: 実行する操作のタプル
        max_retries: 最大再試行回数

    Returns:
        操作の結果
    """
    retries = 0
    last_error = None

    while retries < max_retries:
        try:
            # 操作の実行
            # ...
        except sqlite3.OperationalError as e:
            if "no such table" in str(e) and retries < max_retries - 1:
                # テーブルが存在しない場合、作成して再試行
                # ...
            else:
                # その他のSQLiteエラー
                # ...
        except NotFoundError as e:
            if op[0] == "update" and retries < max_retries - 1:
                # updateがNotFoundErrorの場合、setに変更して再試行
                # ...
            else:
                # その他のNotFoundError
                # ...
        # その他の例外処理
        # ...
```

### 3. 詳細なログ出力

バッチ処理の開始、各操作の実行、完了、エラー発生時など、重要なポイントでログを出力するようになりました。これにより、問題の診断と追跡が容易になります。

### 4. 適切な例外処理

例外の種類に応じた適切なエラーハンドリングを実装しました。単に `raise e` するのではなく、より具体的なエラー情報を提供します。

```python
# 例外の種類に応じた適切なエラーを発生させる
if isinstance(e, (DatabaseError, ValidationError, NotFoundError)):
    raise
elif isinstance(e, sqlite3.Error):
    raise DatabaseError(f"Database error during batch operation: {str(e)}")
else:
    raise DatabaseError(f"Error during batch operation: {str(e)}")
```

### 5. トランザクション管理の改善

冗長な `BEGIN TRANSACTION` を削除し、SQLiteの標準的なトランザクション管理を使用するようになりました。エラー発生時に適切にロールバックし、詳細なエラー情報を提供します。

## 使用例

```python
from storekiss import Client

# クライアントの初期化
client = Client()

# コレクションの参照を取得
users = client.collection("users")

# バッチ処理の作成
batch = client.batch()

# バッチに操作を追加
user1_ref = users.document("user1")
user2_ref = users.document("user2")
user3_ref = users.document("user3")

batch.set(user1_ref, {"name": "User 1", "age": 30})
batch.update(user2_ref, {"status": "active"})
batch.delete(user3_ref)

# バッチをコミット
results = batch.commit()
```

## 注意点

- バッチ処理は、すべての操作が成功するか、すべての操作が失敗するかのいずれかです（アトミック性）。
- 大量の操作を一度に行う場合は、適切なサイズに分割することをお勧めします。
- エラーが発生した場合は、ログを確認して原因を特定してください。
