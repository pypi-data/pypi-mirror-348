## Firestoreの特徴

- datetimeは数値として保存される
- timezone情報を保存したい場合は別フィールド追加

# 未確認

クエリの複雑な条件にはどういうものがある?

カテゴリ
できること
SDK でのポイント
典型的な落とし穴
---
複数フィールドの不等号（< > <= >=）
10 個までのフィールドに対して 同じクエリで 範囲／不等式を並べられる
2024 Q4 以降は 追加インデックス不要（自動作成）
order_by() を指定しないと速度が落ちる 
OR コンポジットフィルタ
A OR B OR (C AND D) のようなブール演算が 1 回の呼び出しで可能
Python では Filter.or_( … ) / Filter.and_( … ) を使う
NOT IN とは併用不可／ネストが深いと読みにくい 
IN / array‑contains‑any
1 フィールドに対し 最大 30 個の値セットを列挙できる（IN と array‑contains‑any を混在可）
複合 OR を擬似的に表現できる
array-contains-any は 配列長 × 値数 で読み取りコスト増 
NOT EQUAL / NOT IN
「◯◯ではない」をサーバ側でフィルタ
!= / not-in
フィールドが 存在しない ドキュメントは返らない 
コレクション‑グループ ＋ カーソル
サブコレクション全体を対象にstartAt()/endBefore() でページング
ルートに同名サブコレクションが複数あっても 1 回で検索可

# import/export機能のテスト

- firestoreのexportした値をimport
   - ネストフィールド無い フラットなコレクション(ドキュメント3個)
- コレクション ドキュメントの値を確認 import test  その値をassert
- litestoreのコレクションを export
- exportした値と元のimport の値を検証する.



# サブコレクションの実装方法

storekissライブラリでは、Firestoreのようなネイティブなサブコレクション機能がサポートされていないため、サブコレクションを模倣するための実装方法がいくつかあります。以下に主な実装方法を紹介します。

## 1. 親参照フィールドを持つ別コレクション

これは最もシンプルな方法で、子ドキュメントに親の参照情報を追加します。

```python
# 親コレクション
prefectures = db.collection("prefectures")

# 子コレクション
cities = db.collection("cities")

# 子ドキュメントに親の参照情報を追加
city_data = {
    "name": "新宿区",
    "prefecture_id": "tokyo",  # 親への参照
    "prefecture_name": "東京都"  # 冗長データ（検索効率化のため）
}

# ドキュメントIDに親IDを含める（オプション）
city_doc_id = f"{prefecture_id}_{city_id}"
cities.document(city_doc_id).set(city_data)
```

### メリット
- シンプルで理解しやすい
- クエリが直感的

### デメリット
- データの整合性を自分で管理する必要がある

## 2. パス区切り文字を使用したドキュメントID設計

```python
# 親コレクション
prefectures = db.collection("prefectures")

# 子ドキュメントのIDを親のパスを含めて設計
city_id = f"prefectures/{prefecture_id}/cities/{city_id}"
cities = db.collection("all_documents")
cities.document(city_id).set(city_data)
```

### メリット
- 単一のコレクションでパス構造を維持できる
- 階層が深くなっても対応可能

### デメリット
- IDが長くなる
- クエリが複雑になる可能性がある

## 3. ヘルパークラスの作成（最も推奨）

サブコレクションの概念をラップするヘルパークラスを作成することで、アプリケーションコードをよりクリーンにできます：

```python
class SubcollectionHelper:
    def __init__(self, db, parent_collection, parent_id, subcollection_name):
        self.db = db
        self.parent_collection = parent_collection
        self.parent_id = parent_id
        self.subcollection_name = subcollection_name
        self.collection = db.collection(f"{parent_collection}_{subcollection_name}")
    
    def document(self, doc_id=None):
        if doc_id is None:
            # 自動生成IDの場合
            return self.collection.document()
        else:
            # 親IDを含めたドキュメントID
            full_id = f"{self.parent_id}_{doc_id}"
            return self.collection.document(full_id)
    
    def add(self, data, doc_id=None):
        # 親への参照を自動追加
        data_with_ref = data.copy()
        data_with_ref[f"{self.parent_collection}_id"] = self.parent_id
        
        # ドキュメント追加
        doc_ref = self.document(doc_id)
        doc_ref.set(data_with_ref)
        return doc_ref
    
    def get(self):
        # 親IDに関連するドキュメントのみを取得
        all_docs = self.collection.get()
        return [doc for doc in all_docs if doc.get(f"{self.parent_collection}_id") == self.parent_id]
```

使用例：

```python
# 東京都の都市サブコレクションを取得
tokyo_cities = SubcollectionHelper(db, "prefectures", "tokyo", "cities")

# 都市を追加
tokyo_cities.add({"name": "新宿区", "population": 346235})

# 都市を取得
cities = tokyo_cities.get()
```

### メリット
- サブコレクションの概念をアプリケーションコードから抽象化
- 一貫性のある実装
- 拡張性が高い

### デメリット
- 追加のコードが必要

## 4. ドキュメント内にネストしたデータとして保存

小規模なサブコレクションの場合、親ドキュメント内にネストしたデータとして保存する方法もあります：

```python
prefecture_data = {
    "id": "tokyo",
    "name": "東京都",
    "population": 14047594,
    "cities": [
        {"id": "shinjuku", "name": "新宿区", "population": 346235},
        {"id": "shibuya", "name": "渋谷区", "population": 228906}
    ]
}

prefectures.document("tokyo").set(prefecture_data)
```

### メリット
- シンプルで直感的
- 一度に全データを取得できる

### デメリット
- サブコレクションが大きくなると非効率
- 部分更新が複雑になる

## 結論

最も推奨される方法は、**ヘルパークラスを作成する方法（方法3）**です。これにより、サブコレクションの概念をアプリケーションコードから抽象化し、一貫性のある実装を提供できます。また、将来的にstorekissライブラリがネイティブなサブコレクションをサポートした場合でも、ヘルパークラスの内部実装を変更するだけで対応できます。

小規模なアプリケーションでは、**親参照フィールドを持つ別コレクション（方法2）**も十分実用的です。現在のquickstart_2.pyの実装はこの方法を使用しており、多くの場合で十分に機能します。

# 最新の更新内容（2025年5月）

## Firestoreとの互換性向上

### 1. DocumentSnapshotクラスの追加

- `DocumentReference.get()`メソッドが`DocumentSnapshot`オブジェクトを返すようになりました
- Firestoreと同様に`to_dict()`, `exists()`, `get()`, `__getitem__`メソッドをサポート
- これにより、Firestoreからの移行がより簡単になります

```python
# 使用例
doc = db.collection("users").document("user123").get()

# ドキュメントが存在するか確認
if doc.exists:
    # データを辞書として取得
    data = doc.to_dict()
    # または特定のフィールドにアクセス
    name = doc["name"]
    age = doc.get("age", 0)  # デフォルト値を指定可能
```

#### DocumentSnapshotクラスの主なメソッドと属性

| メソッド/属性 | 説明 | 使用例 |
|-------------|------|-------|
| `exists` | ドキュメントが存在するかどうかを示す真偽値 | `if doc.exists:` |
| `id` | ドキュメントのID | `doc_id = doc.id` |
| `to_dict()` | ドキュメントデータを辞書として取得 | `data = doc.to_dict()` |
| `get(field, default=None)` | 特定のフィールドを取得（存在しない場合はデフォルト値） | `age = doc.get("age", 0)` |
| `__getitem__` | 辞書のようにフィールドにアクセス | `name = doc["name"]` |

#### DocumentSnapshotの注意点

- ドキュメントが存在しない場合、`doc.exists`は`False`になりますが、`doc`自体は`None`ではありません
- 存在しないドキュメントに対して`to_dict()`を呼び出すと空の辞書`{}`が返されます
- 存在しないフィールドに`__getitem__`でアクセスすると`KeyError`が発生します（`get()`メソッドを使用するとデフォルト値を指定できます）

### 2. DELETE_FIELDセンチネル値の改善

- `DELETE_FIELD`を使用してフィールドを削除する機能が改善されました
- Firestoreと同様の動作を実現

```python
from storekiss.litestore import DELETE_FIELD

# フィールドを削除
doc_ref.update({"optional_field": DELETE_FIELD})
```

#### DELETE_FIELDの使用方法

1. **フィールドの削除**：

   ```python
   # 特定のフィールドを削除
   doc_ref.update({"optional_field": DELETE_FIELD})
   ```

2. **ネストしたフィールドの削除**：

   ```python
   # ネストしたフィールドを削除
   doc_ref.update({"user.address": DELETE_FIELD})
   ```

3. **配列内の要素の削除**：

   ```python
   # 配列フィールド内の特定の要素を削除（現在はサポートされていません）
   # 代わりに、配列全体を更新する必要があります
   current_data = doc_ref.get().to_dict()
   tags = current_data.get("tags", [])
   tags.remove("old_tag")  # 削除したい要素を削除
   doc_ref.update({"tags": tags})
   ```

#### 注意点

- `DELETE_FIELD`は`update()`メソッドでのみ使用できます
- 存在しないフィールドに対して`DELETE_FIELD`を使用しても、エラーは発生しません
- 存在しないドキュメントに対して`update()`メソッドを使用すると、`NotFoundError`例外が発生します
- `set()`メソッドでは`DELETE_FIELD`は使用できません。代わりに、削除したいフィールドを除いた新しいデータで`set()`を呼び出してください

### 3. 環境変数によるインデックス設定

以下の環境変数を使用してインデックス作成を制御できるようになりました：

- `STOREKISS_AUTO_INDEX`: 自動インデックス作成を有効/無効（デフォルト: True）
- `STOREKISS_INDEX_ALL_FIELDS`: すべてのフィールドにインデックスを作成（デフォルト: True）

```python
import os

# 環境変数の設定例
os.environ["STOREKISS_AUTO_INDEX"] = "False"
os.environ["STOREKISS_INDEX_ALL_FIELDS"] = "True"
```

## パフォーマンス最適化

- データベース接続の管理が改善され、接続の再利用が効率化されました
- インデックスの自動作成によるクエリパフォーマンスの向上
- 大量のデータを扱う際のメモリ使用量を最適化

## エラー処理の改善

- より詳細なエラーメッセージとスタックトレース
- 存在しないドキュメントの処理が改善され、適切な例外が発生するようになりました
- テーブルが存在しない場合の自動作成機能

# リファクタリング履歴

## 2025年5月のリファクタリング

### コードクリーンアップ

- Firestoreの互換性パッチを削除し、必要な機能をコアライブラリに統合
- `DocumentSnapshot`と`Document`クラスを強化し、`doc.reference.update()`メソッドが正しく動作するように修正
- `QueryBuilder`クラスからすべてのデバッグ出力（print文）を削除
- `query`メソッドを改善し、フィルター、リミット、オフセット、並び順の処理を最適化
- `count`メソッドの実装を修正し、フィルターに基づいて正確なドキュメント数を返すように改善
- 重複するインポートを削除（`datetime`モジュールなど）
- 未使用のインポートに対して適切な`noqa`コメントを追加
- 名前の衝突を避けるためにローカルスコープでのインポート名を変更（`_Exporter`、`_Importer`）
- プレースホルダーのないf-stringを通常の文字列に修正
- `black`ツールを使用してコードスタイルを統一

### 機能強化

- テーブルが存在しない場合の自動作成機能の信頼性を向上
- SQLiteの操作とエラー処理のロギングを改善
- インメモリデータベースからファイルベースデータベースへのデフォルト設定変更による安定性向上
- バッチ処理の改善（テーブル存在確認、例外処理、ログ出力、リトライメカニズムを追加）

# 未実装

- 認証、認可
- NOTIFICATION
- トランザクション
- リアルタイムリスナー

# セキュリティールールの例

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow write: if request.resource.data.name is string &&
                      request.resource.data.age is int &&
                      request.resource.data.is_active is bool;
    }
  }
}


# 内部インデックス関数
非公開関数

コレクションに対して、 jsonのフィールドをカラムに展開してインデックスする。
crud操作時にカラムも更新する
クエリの時にインデックスがある場合は使うようにする。

インデックス 作成   
   - コレクション名
   - フィールド名リスト
     インデックスは既存ならそのまま

インデックス 削除
   - コレクション名
   - フィールド名リスト
     インデックスはあるものだけ削除

crud操作時のフックのフロー
   crud 操作時に jsonを展開し、インデックスがあるものについて、インデックスを更新する。
