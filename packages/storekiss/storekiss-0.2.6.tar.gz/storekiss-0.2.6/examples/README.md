# Storekiss サンプル集

このディレクトリには、storekiss CRUDライブラリの使用例が含まれています。

## サンプルコード一覧

| ファイル名 | 説明 | 主な機能 |
|------------|------|--------|
| `quickstart_1.py` | 関東一都六県の情報を設定し、読み出す基本的な使用例 | ドキュメントの追加、取得、クエリ、ソート |
| `quickstart_2.py` | 関東一都六県とその都市情報を別コレクションで管理する例 | 関連データの管理、サブコレクションの模倣 |
| `earthquake_example.py` | 地震データを管理する例 | スキーマ検証、日時処理、CRUD操作 |
| `boolean_example.py` | 真偽値フィールドの使用例 | 真偽値の保存と取得、フィルタリング |
| `auto_document_id_example.py` | 自動生成されるドキュメントIDの使用例 | 自動ID生成、ドキュメントの追加 |
| `delete_field_example.py` | フィールドの削除方法の例 | DELETE_FIELDセンチネル値の使用 |
| `export_import_example.py` | データのエクスポートとインポートの例 | データのバックアップと復元 |
| `Client_example.py` | Clientクラスの使用例 | Firestore風のAPIインターフェース |
| `firestore_example.py` | Firestoreクラスの使用例 | 基本的なFirestore風の操作 |
| `improved_multiple_collection.py` | 複数コレクションの改良された管理方法 | 複数コレクションの効率的な操作 |
| `multiple_collection.py` | 複数コレクションの基本的な管理方法 | 複数コレクションの基本操作 |
| `server_timestamp_example.py` | サーバータイムスタンプの使用例 | 自動タイムスタンプの追加 |

## 地震データの例

`earthquake_example.py`スクリプトは以下を示しています：

1. FireStore風のバリデーションを持つスキーマの作成
2. JSONからの地震データの読み込み
3. 時間文字列をPythonのdatetimeオブジェクトに変換
4. datetime処理を含むデータの保存と取得
5. 地震データの検索
6. 追加フィールドによるレコードの更新
7. レコードの削除

### サンプルの実行方法

```bash
cd examples
python earthquake_example.py
```

### サンプルデータ

この例では、以下の構造を持つ地震データを使用しています：

```json
{
  "id": "us6000l9l0",
  "time": "2023-05-15T12:15:47.302Z",
  "latitude": 36.9676,
  "longitude": 140.1873,
  "depth": 10.0,
  "mag": 5.2,
  "place": "Honshu, Japan",
  "type": "earthquake"
}
```

`time`フィールドは、`DateTimeField`バリデータを使用してISO形式の文字列からPythonの`datetime`オブジェクトに自動的に変換されます。

## 実演されている主な機能

- **スキーマ検証**: FireStore風の検証システムの使用
- **日時処理**: 文字列とdatetime形式の間の変換
- **CRUD操作**: レコードの作成、読み取り、更新、削除
- **検索**: さまざまな条件に基づくデータのフィルタリング
