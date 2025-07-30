#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
改良版：複数の特殊文字を含むコレクション名のテスト

このスクリプトは、特殊文字や使用できない文字を含む複数のコレクション名が
データベーステーブルとして正しく分離され、互いに干渉しないことをテストします。

前回のテストで発見された問題：
- 異なるユニコード文字列（「都道府県」と「中文集合」）が同じテーブル名「____」に変換される
- これにより、データが混在し、テーブル間で干渉が発生する

改良点：
- ハッシュベースのテーブル名マングリング関数を実装
- ユニコード文字列のハッシュ値を使用して一意のテーブル名を生成
- 衝突の可能性を大幅に低減
"""

import os
import sys
import tempfile
import logging
import shutil
from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField, BooleanField
import sqlite3
import hashlib  # ハッシュ計算に使用

# ロギングの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 親ディレクトリをパスに追加して、storekissモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def improved_mangle_table_name(name):
    """
    改良版：PostgreSQLとSQLite3の両方で合法なテーブル名に変換します。

    ユニコード文字列のハッシュ値を使用して一意のテーブル名を生成し、
    異なる文字列が同じテーブル名に変換される問題を解決します。
    """
    import re

    if not name:
        return "collection_default"

    # 名前のハッシュ値を計算（MD5を使用）
    name_hash = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]

    # 英数字のみを抽出（最大10文字）
    alpha_part = re.sub(r"[^a-zA-Z0-9]", "", name)[:10]
    if not alpha_part:
        # 英数字が一つもない場合は、先頭にtをつける
        alpha_part = "t"

    # 数字で始まる場合は先頭に't_'を追加
    if alpha_part and alpha_part[0].isdigit():
        alpha_part = "t_" + alpha_part

    # 最終的なテーブル名を生成（英数字部分 + アンダースコア + ハッシュ値）
    safe_name = f"{alpha_part}_{name_hash}"

    # 63バイト以下に制限（PostgreSQLの制限）
    if len(safe_name.encode("utf-8")) > 63:
        safe_name = safe_name[: 63 - len(name_hash) - 1] + "_" + name_hash

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

            # テーブル名の変換を確認（オリジナルの関数）
            original_table_name = mangle_table_name(collection_name)

            # 改良版テーブル名の変換を確認
            improved_table_name = improved_mangle_table_name(collection_name)

            logging.info("コレクション名 '%s' の変換結果:", collection_name)
            logging.info("  オリジナル: '%s'", original_table_name)
            logging.info("  改良版: '%s'", improved_table_name)

            # 各コレクションに3つのドキュメントを追加
            for j in range(1, 4):
                doc_id = f"doc_{i}_{j}"
                collection.document(doc_id).set(
                    {"name": f"Item {i}-{j}", "value": i * 10 + j, "active": j % 2 == 0}
                )
                logging.info("  ドキュメント %s を追加しました", doc_id)

        # データベース内のテーブルを確認
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logging.info("データベース内のテーブル: %s", tables)

        # テーブル名の衝突を確認
        table_names = [table[0] for table in tables]
        if len(table_names) != len(set(table_names)):
            logging.error("テーブル名の衝突が発生しています！")

            # 衝突しているテーブル名を特定
            name_count = {}
            for name in table_names:
                if name in name_count:
                    name_count[name] += 1
                else:
                    name_count[name] = 1

            for name, count in name_count.items():
                if count > 1:
                    logging.error("  テーブル名 '%s' が %d 回使用されています", name, count)

                    # このテーブル名に対応するコレクション名を特定
                    for collection_name in collection_names:
                        if mangle_table_name(collection_name) == name:
                            logging.error("    コレクション名: '%s'", collection_name)
        else:
            logging.info("テーブル名の衝突はありません（全て一意です）")

        # 改良版関数でテーブル名の衝突がないか確認
        improved_table_names = [
            improved_mangle_table_name(name) for name in collection_names
        ]
        if len(improved_table_names) != len(set(improved_table_names)):
            logging.error("改良版関数でもテーブル名の衝突が発生しています！")

            # 衝突しているテーブル名を特定
            name_count = {}
            for name in improved_table_names:
                if name in name_count:
                    name_count[name] += 1
                else:
                    name_count[name] = 1

            for name, count in name_count.items():
                if count > 1:
                    logging.error("  テーブル名 '%s' が %d 回使用されています", name, count)

                    # このテーブル名に対応するコレクション名を特定
                    for collection_name in collection_names:
                        if improved_mangle_table_name(collection_name) == name:
                            logging.error("    コレクション名: '%s'", collection_name)
        else:
            logging.info("改良版関数ではテーブル名の衝突はありません（全て一意です）")

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
                    "  エラー: コレクション '%s' のドキュメント数が予想と一致しません。期待値: 3, 実際: %d",
                    collection_name,
                    len(docs),
                )

                # 他のコレクションのデータが混入していないか確認
                for doc in docs:
                    doc_id_parts = doc.get("id", "").split("_")
                    if len(doc_id_parts) >= 2 and doc_id_parts[0] == "doc":
                        try:
                            doc_collection_index = int(doc_id_parts[1])
                            if doc_collection_index != i:
                                logging.error(
                                    "    他のコレクションのデータが混入しています: %s (コレクションインデックス %d)",
                                    doc.get("id"),
                                    doc_collection_index,
                                )
                        except (ValueError, IndexError):
                            pass
            else:
                logging.info(
                    "  コレクション '%s' のドキュメント数: %d (OK)", collection_name, len(docs)
                )

            # 各ドキュメントの内容を表示
            for doc in docs:
                if doc.get("id", "").startswith(f"doc_{i}_"):
                    logging.info(
                        "    ID: %s, 名前: %s, 値: %d, アクティブ: %s",
                        doc.get("id"),
                        doc.get("name"),
                        doc.get("value"),
                        doc.get("active"),
                    )
                else:
                    logging.warning(
                        "    他のコレクションのデータ: ID: %s, 名前: %s",
                        doc.get("id"),
                        doc.get("name"),
                    )

        logging.info("複数の特殊文字を含むコレクション名のテストが完了しました")

        # 改良版関数の有効性を示すためのサマリー
        logging.info("\n=== テーブル名変換関数の比較 ===")
        logging.info("オリジナル関数と改良版関数の変換結果を比較します")

        for collection_name in collection_names:
            original = mangle_table_name(collection_name)
            improved = improved_mangle_table_name(collection_name)
            logging.info("コレクション名: %s", collection_name)
            logging.info("  オリジナル: '%s'", original)
            logging.info("  改良版: '%s'", improved)

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


def mangle_table_name(name):
    """
    オリジナルのテーブル名変換関数（比較用）
    PostgreSQLとSQLite3の両方で合法なテーブル名に変換します。
    """
    import re

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


if __name__ == "__main__":
    test_multiple_collections()
