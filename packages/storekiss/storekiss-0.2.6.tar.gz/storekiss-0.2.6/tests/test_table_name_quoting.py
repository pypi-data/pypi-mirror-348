#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル名のクォート処理のテスト
"""

import os
import pytest
import sqlite3
import datetime
import tempfile
from storekiss.crud import quote_table_name
from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField, BooleanField


# quote_table_name関数が実装されているので、改良版関数は不要


@pytest.fixture
def temp_db_path():
    """一時的なデータベースパスを作成します。"""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join(
        "tests/temp_test_data", f"table_name_quoting_test_{timestamp}.db"
    )

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


@pytest.fixture
def test_collection_names():
    """テスト用のコレクション名リストを返します。"""
    return [
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


class TestTableNameMangling:
    """テーブル名マングリング関数のテストクラス"""

    def test_quote_table_name(self, test_collection_names):
        """テーブル名をクォートするquote_table_name関数のテスト"""
        # 変換結果を格納するディクショナリ
        quoted_names = {}

        # 各コレクション名を変換
        for name in test_collection_names:
            quoted = quote_table_name(name)
            quoted_names[name] = quoted

        # 変換結果の一意性を確認
        unique_quoted_names = set(quoted_names.values())
        assert len(unique_quoted_names) == len(
            test_collection_names
        ), "変換後のテーブル名が一意ではありません"

        # 特殊文字を含む
        assert quote_table_name("user-data") == '"user-data"'

        # 日本語
        assert quote_table_name("都道府県") == '"都道府県"'

        # 中国語
        assert quote_table_name("中文集合") == '"中文集合"'

        # 予約語
        assert quote_table_name("select") == '"select"'

        # ダブルクォートを含む
        assert quote_table_name('table"name') == '"table""name"'

        # 衝突がないことを確認
        assert len(unique_quoted_names) == len(
            test_collection_names
        ), f"変換後のテーブル名に衝突があります。コレクション数: {len(test_collection_names)}, 一意なテーブル名数: {len(unique_quoted_names)}"

        # 「都道府県」と「中文集合」が異なるテーブル名に変換されることを確認
        assert quote_table_name("都道府県") != quote_table_name(
            "中文集合"
        ), "「都道府県」と「中文集合」は異なるテーブル名に変換されるべき"

        # quote_table_name関数は単にダブルクォートで囲むだけなので、
        # バイト数制限のチェックは不要です。
        # データベース側で長い名前を扱う必要がある場合は、別途対応が必要です。

        # テーブル名がダブルクォートで囲まれていることを確認
        for name, quoted in quoted_names.items():
            assert quoted.startswith('"') and quoted.endswith(
                '"'
            ), f"テーブル名 '{quoted}' がダブルクォートで囲まれていません"

    def test_actual_database_operations(self, temp_db_path, test_collection_names):
        """実際のデータベース操作でテーブル名マングリング関数をテスト"""
        # スキーマを定義
        schema = Schema(
            {
                "name": StringField(required=True),
                "value": NumberField(required=True),
                "active": BooleanField(required=False),
            }
        )

        # LiteStoreクライアントを作成 (schema parameter removed as it's no longer supported)
        db = litestore.client(db_path=temp_db_path)

        # 各コレクションにデータを追加
        for i, collection_name in enumerate(test_collection_names):
            collection = db.collection(collection_name)

            # 1つのドキュメントを追加
            doc_id = f"doc_{i}"
            collection.document(doc_id).set(
                {"name": f"Item {i}", "value": i * 10, "active": i % 2 == 0}
            )

        # データベース内のテーブルを確認
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # テーブル名のリスト
        table_names = [table[0] for table in tables if table[0] != "items"]

        # 新しいマングリング処理では、日本語のテーブル名もそのまま使用される
        expected_table_count = len(test_collection_names)  # 重複はない

        # テーブル数が正しいことを確認
        assert (
            len(table_names) == expected_table_count
        ), f"テーブル数が一致しません。期待値: {expected_table_count}, 実際: {len(table_names)}"

        # 各テーブルのデータを確認
        for i, collection_name in enumerate(test_collection_names):
            collection = db.collection(collection_name)
            docs = collection.get()

            # 新しいマングリング処理では、各コレクションは独自のテーブルになる
            # ドキュメント数は1つになる
            # ドキュメント数が1つであることを確認
            assert (
                len(docs) == 1
            ), f"コレクション '{collection_name}' のドキュメント数が一致しません。期待値: 1, 実際: {len(docs)}"

            # ドキュメントのIDが正しいことを確認
            assert (
                docs[0].id == f"doc_{i}"
            ), f"コレクション '{collection_name}' のドキュメントIDが一致しません。期待値: 'doc_{i}', 実際: {docs[0].id}"

            # ドキュメントの内容が正しいことを確認
            doc = docs[0]
            doc_data = doc.to_dict()
            assert (
                doc.id == f"doc_{i}"
            ), f"ドキュメントID '{doc.id}' が期待値 'doc_{i}' と一致しません"
            assert (
                doc_data["name"] == f"Item {i}"
            ), f"ドキュメント名 '{doc_data['name']}' が期待値 'Item {i}' と一致しません"
            assert (
                doc_data["value"] == i * 10
            ), f"ドキュメント値 {doc_data['value']} が期待値 {i * 10} と一致しません"

        conn.close()

    # test_improved_implementation_proposalメソッドは削除されました。
    # 古いmangle_table_name関数とimproved_mangle_table_name関数を参照していたため、
    # quote_table_name関数に置き換えられた現在は不要です。


if __name__ == "__main__":
    pytest.main(["-v", "test_table_name_mangling.py"])
