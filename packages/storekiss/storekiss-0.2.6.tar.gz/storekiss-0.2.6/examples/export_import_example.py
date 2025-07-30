#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Firestore互換エクスポート/インポート機能のサンプル

このサンプルは、storekissライブラリのFirestore互換エクスポート/インポート機能を
使用する方法を示します。
"""
import os
import sys
import logging
import tempfile
import json
import shutil

# ロギングの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 親ディレクトリをパスに追加して、storekissモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField, BooleanField


def main():
    """Firestore互換エクスポート/インポート機能のデモンストレーション"""
    logging.info("Firestore互換エクスポート/インポート機能の例を開始します")

    # スキーマを作成
    schema = Schema(
        {
            "number": NumberField(required=True),
            "name": StringField(required=True),
            "active": BooleanField(required=False),
        }
    )

    # 一時ファイルを使用してデータベースを作成
    # メモリ内データベースはテーブル作成に問題があるため、ファイルベースのデータベースを使用
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    db_path = temp_db.name

    # 一時ディレクトリを作成（エクスポート用）
    temp_export_dir = tempfile.mkdtemp()

    try:
        # Firestoreクライアントを作成
        db = litestore.client(db_path=db_path, schema=schema)

        # サンプルデータを作成
        create_sample_data(db)

        # コレクションをエクスポート
        logging.info("コレクションをエクスポートします...")
        metadata_file = db.export_collection("都道府県", temp_export_dir)
        logging.info(f"エクスポートが完了しました。メタデータファイル: {metadata_file}")

        # メタデータファイルの内容を表示
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            logging.info("メタデータ: %s", json.dumps(metadata, indent=2, ensure_ascii=False))

        # エクスポートされたJSONLファイルの内容を表示
        jsonl_file = os.path.join(temp_export_dir, "都道府県", "都道府県.jsonl")
        logging.info("エクスポートファイル: %s", jsonl_file)
        with open(jsonl_file, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i < 3:  # 最初の3行だけ表示
                    doc = json.loads(line)
                    logging.info("ドキュメント %d: %s", i+1, json.dumps(doc, indent=2, ensure_ascii=False))
                else:
                    logging.info("...")
                    break

        # 新しいデータベースを作成（インポート用）
        temp_db2 = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        temp_db2.close()
        db_path2 = temp_db2.name

        # 新しいFirestoreクライアントを作成
        db2 = litestore.client(db_path=db_path2, schema=schema)

        # エクスポートしたデータをインポート
        logging.info("エクスポートしたデータをインポートします...")
        imported_count = db2.import_collection("都道府県", temp_export_dir)
        logging.info("インポート結果: %s", imported_count)

        # インポートされたデータを確認
        logging.info("インポートされたデータを確認します...")
        imported_docs = db2.collection("都道府県").get()
        logging.info("インポートされたドキュメント数: %s", len(imported_docs))

        for i, doc in enumerate(imported_docs):
            if i < 3:  # 最初の3つだけ表示
                logging.info("ドキュメント %d: %s", i+1, doc)
            else:
                logging.info("...")
                break

        # すべてのコレクションをエクスポート
        logging.info("すべてのコレクションをエクスポートします...")

        # 別のコレクションを作成
        cities = db.collection("cities")
        cities.document("tokyo").set({"name": "東京", "population": 13960000, "number": 13})
        cities.document("osaka").set({"name": "大阪", "population": 8839000, "number": 27})
        cities.document("nagoya").set({"name": "名古屋", "population": 2296000, "number": 23})

        # すべてのコレクションをエクスポート
        all_metadata_file = db.export_all_collections(temp_export_dir)
        logging.info("エクスポートファイル: %s", all_metadata_file)

        # メタデータファイルの内容を表示
        with open(all_metadata_file, "r", encoding="utf-8") as f:
            all_metadata = json.load(f)
            logging.info("すべてのコレクションのメタデータ: %s", json.dumps(all_metadata, indent=2, ensure_ascii=False))

        # すべてのコレクションをインポート
        logging.info("すべてのコレクションをインポートします...")

        # 新しいデータベースを作成（すべてのコレクションのインポート用）
        temp_db3 = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        temp_db3.close()
        db_path3 = temp_db3.name

        # 新しいFirestoreクライアントを作成
        db3 = litestore.client(db_path=db_path3, schema=schema)

        # すべてのコレクションをインポート
        import_result = db3.import_all_collections(temp_export_dir)
        logging.info("インポート結果: %s", import_result)

        # インポートされたデータを確認
        logging.info("インポートされたデータを確認します...")

        # 都道府県コレクションを確認
        imported_prefs = db3.collection("都道府県").get()
        logging.info("インポートされた都道府県ドキュメント数: %s", len(imported_prefs))

        # citiesコレクションを確認
        imported_cities = db3.collection("cities").get()
        logging.info("インポートされたcitiesドキュメント数: %s", len(imported_cities))
        for city in imported_cities:
            logging.info("都市: %s", city)

        logging.info("Firestore互換エクスポート/インポート機能の例を終了します")

    finally:
        # 一時ファイルとディレクトリを削除
        try:
            os.unlink(db_path)
            logging.info("一時データベースファイル %s を削除しました", db_path)

            if "db_path2" in locals():
                os.unlink(db_path2)
                logging.info("一時データベースファイル %s を削除しました", db_path2)

            if "db_path3" in locals():
                os.unlink(db_path3)
                logging.info("一時データベースファイル %s を削除しました", db_path3)

            shutil.rmtree(temp_export_dir)
            logging.info("エクスポートディレクトリ %s を削除しました", temp_export_dir)
        except Exception as e:
            logging.error("エクスポート/インポート例外発生", exc_info=True)


def create_sample_data(db):
    """サンプルデータを作成します"""
    # 都道府県コレクションを取得
    prefectures = db.collection("都道府県")
    logging.info("コレクションを初期化しました: 都道府県")

    # いくつかの都道府県データを追加
    prefectures.document("hokkaido").set({"number": 1, "name": "北海道", "active": True})
    logging.info("ドキュメントを追加しました: 北海道")

    prefectures.document("tokyo").set({"number": 13, "name": "東京都", "active": True})
    logging.info("ドキュメントを追加しました: 東京都")

    prefectures.document("osaka").set({"number": 27, "name": "大阪府", "active": True})
    logging.info("ドキュメントを追加しました: 大阪府")

    prefectures.document("kyoto").set({"number": 26, "name": "京都府", "active": False})
    logging.info("ドキュメントを追加しました: 京都府")

    # ドキュメント数を確認
    all_docs = prefectures.get()
    logging.info(f"コレクション内のドキュメント数: {len(all_docs)}")
    for doc in all_docs:
        logging.info(f"  {doc['id']}: {doc['name']} (番号: {doc['number']})")


if __name__ == "__main__":
    main()
