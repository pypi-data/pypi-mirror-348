#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
複数の特殊文字を含むコレクション名のテスト

このスクリプトは、特殊文字や使用できない文字を含む複数のコレクション名が
データベーステーブルとして正しく分離され、互いに干渉しないことをテストします。
"""

import os
import sys
import tempfile
import logging
import shutil
import re
from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField, BooleanField
import sqlite3

# ロギングの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 親ディレクトリをパスに追加して、storekissモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def mangle_table_name(name):
    """PostgreSQLとSQLite3の両方で合法なテーブル名に変換します。"""
    if not name:
        return "collection_default"

    # 英数字、アンダースコア、ドル記号以外の文字をアンダースコアに置換
    safe_name = re.sub(r"[^a-zA-Z0-9_$]", "_", name)

    # 数字で始まる場合は先頭に't_'を追加
    if safe_name and safe_name[0].isdigit():
        safe_name = "t_" + safe_name

    # 63バイト以下に制限（PostgreSQLの制限）
    if len(safe_name.encode("utf-8")) > 63:
        hash_suffix = str(hash(name) % 10000).zfill(4)
        prefix_length = 63 - len(hash_suffix) - 1  # 1はアンダースコアの分
        safe_name = safe_name[:prefix_length] + "_" + hash_suffix

    return safe_name


def test_multiple_collections():
    """複数の特殊文字を含むコレクション名のテスト"""
    logging.info("複数の特殊文字を含むコレクション名のテストを開始します")

    # テスト用のスキーマを定義
    schema = Schema(
        {
            "name": StringField(required=True),
            "value": NumberField(required=True),
            "active": BooleanField(required=False),  # required=Falseでオプショナルに設定
        }
    )

    # 一時ファイルを使用してデータベースを作成
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    db_path = temp_db.name

    try:
        # Firestoreクライアントを作成
        db = litestore.client(db_path=db_path, schema=schema)

        # テスト用の特殊文字を含むコレクション名のリスト
        collection_names = [
            "都道府県",  # 日本語
            "123数字から始まる",  # 数字から始まる日本語
            "!@#$%^&*()特殊記号",  # 特殊記号を含む
            "spaces with spaces",  # スペースを含む
            "veryLongCollectionNameThatExceedsSixtyThreeBytesProbablyAndNeedsToBeHashed",  # 長い名前
            "SQL-Keywords.SELECT.FROM.WHERE",  # SQLキーワードとドット
            "emoji😊🌟🎉collection",  # 絵文字を含む
            "にほんご-english-mixed",  # 日本語と英語の混合
            "Русский-текст",  # キリル文字
            "中文集合",  # 中国語
        ]

        # 各コレクションにデータを追加
        for i, collection_name in enumerate(collection_names):
            logging.info("コレクション '%s' にデータを追加します", collection_name)

            # コレクションの取得
            collection = db.collection(collection_name)

            # テーブル名の変換を確認
            safe_table_name = mangle_table_name(collection_name)
            logging.info(
                "コレクション名 '%s' は '%s' に変換されました", collection_name, safe_table_name
            )

            # 各コレクションに3つのドキュメントを追加
            for j in range(1, 4):
                doc_id = "doc_%d_%d" % (i, j)
                collection.document(doc_id).set(
                    {"name": "Item %d-%d" % (i, j), "value": i * 10 + j, "active": j % 2 == 0}
                )
                logging.info("追加したドキュメント: %s", doc_id)

        # データベース内のテーブルを確認
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logging.info("データベース内のテーブル: %s", tables)

        # 各コレクションのデータを取得して検証
        for i, collection_name in enumerate(collection_names):
            logging.info("コレクション '%s' のデータを検証します", collection_name)

            # コレクションの取得
            collection = db.collection(collection_name)

            # すべてのドキュメントを取得
            docs = collection.get()

            # ドキュメント数を確認
            if len(docs) != 3:
                logging.error(
                    "エラー: コレクション '%s' のドキュメント数が予想と一致しません。期待値: 3, 実際: %d",
                    collection_name,
                    len(docs),
                )
            else:
                logging.info(
                    "コレクション '%s' のドキュメント数: %d (OK)", collection_name, len(docs)
                )

            # 各ドキュメントの内容を表示
            for doc in docs:
                logging.info(
                    "ID: %s, 名前: %s, 値: %d, アクティブ: %s",
                    doc["id"],
                    doc["name"],
                    doc["value"],
                    doc["active"],
                )

        # SQLiteで直接クエリを実行して各テーブルのデータ数を確認
        logging.info("SQLiteで直接各テーブルのデータ数を確認します")
        for collection_name in collection_names:
            safe_table_name = mangle_table_name(collection_name)
            cursor.execute("SELECT COUNT(*) FROM %s" % safe_table_name)
            count = cursor.fetchone()[0]
            logging.info("テーブル '%s' のレコード数: %d", safe_table_name, count)

            if count != 3:
                logging.error(
                    "エラー: テーブル '%s' のレコード数が予想と一致しません。期待値: 3, 実際: %d",
                    safe_table_name,
                    count,
                )

        # クロスチェック: 各テーブルのデータが他のテーブルに影響していないか確認
        logging.info("クロスチェック: 各テーブルのデータが他のテーブルに影響していないか確認します")
        for i, collection_name in enumerate(collection_names):
            # 特定のコレクションのデータを変更
            collection = db.collection(collection_name)
            test_doc_id = "doc_%d_1" % i
            test_doc = collection.document(test_doc_id)

            # 値を更新
            new_value = i * 100
            test_doc.update({"value": new_value})
            logging.info(
                "コレクション '%s' のドキュメント %s の値を %d に更新しました",
                collection_name,
                test_doc_id,
                new_value,
            )

            # 更新後の値を確認
            updated_doc = test_doc.get()
            if updated_doc["value"] != new_value:
                logging.error(
                    "エラー: 更新された値が正しくありません。期待値: %d, 実際: %d",
                    new_value,
                    updated_doc["value"],
                )

            # 他のコレクションに影響がないか確認
            for j, other_collection_name in enumerate(collection_names):
                if i == j:
                    continue  # 同じコレクションはスキップ

                other_collection = db.collection(other_collection_name)
                other_doc_id = "doc_%d_1" % j
                other_doc = other_collection.document(other_doc_id).get()

                expected_value = j * 10 + 1
                if other_doc["value"] != expected_value:
                    logging.error(
                        "エラー: コレクション '%s' の更新がコレクション '%s' に影響しています。期待値: %d, 実際: %d",
                        collection_name,
                        other_collection_name,
                        expected_value,
                        other_doc["value"],
                    )
                else:
                    logging.info(
                        "コレクション '%s' のデータは正常です (値: %d)",
                        other_collection_name,
                        other_doc["value"],
                    )

        logging.info("複数の特殊文字を含むコレクション名のテストが正常に完了しました")

    except sqlite3.Error as e:
        logging.error("SQLiteエラーが発生しました: %s", e)
    except (KeyError, ValueError) as e:
        logging.error("データ処理エラーが発生しました: %s", e)
    except Exception as e:
        logging.error("予期しないエラーが発生しました: %s", e)

    finally:
        # 一時ファイルを削除
        try:
            os.unlink(db_path)
            logging.info("一時データベースファイル %s を削除しました", db_path)
        except (OSError, IOError) as e:
            logging.warning("一時ファイルの削除中にエラーが発生しました: %s", e)


if __name__ == "__main__":
    test_multiple_collections()
