"""
自動ドキュメントID生成機能のデモンストレーション。

このサンプルは、storekissライブラリのFirestoreライクな自動ドキュメントID生成機能を
使用する方法を示します。
"""
import os
import logkiss as logging
import tempfile
import csv
import sqlite3
import json
from storekiss import litestore
from storekiss.validation import NumberField, StringField

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    """自動ドキュメントID生成機能のデモンストレーション"""
    logger.info("自動ドキュメントID生成の例を開始します")

    # スキーマを作成
    schema = litestore.Schema(
        {"number": NumberField(required=True), "name": StringField(required=True)}
    )

    # 一時ファイルを使用してデータベースを作成
    # メモリ内データベースはテーブル作成に問題があるため、ファイルベースのデータベースを使用
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    db_path = temp_db.name

    try:
        # Firestoreクライアントを作成
        db = litestore.client(db_path=db_path, )

        # 都道府県コレクションを取得
        prefectures = db.collection("都道府県")
        logger.info("コレクションを初期化しました: 都道府県")

        logger.info("IDを指定せずにドキュメントを作成します")
        doc_ref = prefectures.document()  # IDを指定しない
        doc_id = doc_ref.id
        logger.info("生成されたドキュメントID: %s", doc_id)

        # ドキュメントデータを設定
        doc_ref.set({"number": 1, "name": "北海道"})

        # ドキュメントを取得
        hokkaido = doc_ref.get()
        logger.info(
            "ドキュメントデータ: id=%s, number=%s, name=%s",
            hokkaido['id'], hokkaido['number'], hokkaido['name']
        )

        logger.info("add()メソッドを使用して自動IDでドキュメントを作成します")
        tokyo = prefectures.add({"number": 13, "name": "東京都"})
        logger.info("生成されたドキュメントID: %s", tokyo['id'])
        logger.info(
            "ドキュメントデータ: id=%s, number=%s, name=%s",
            tokyo['id'], tokyo['number'], tokyo['name']
        )

        logger.info("IDを明示的に指定してドキュメントを作成します")
        osaka_ref = prefectures.document("osaka")
        osaka_ref.set({"number": 27, "name": "大阪府"})

        osaka = osaka_ref.get()
        logger.info(
            "ドキュメントデータ: id=%s, number=%s, name=%s",
            osaka['id'], osaka['number'], osaka['name']
        )

        logger.info("add()メソッドでIDを明示的に指定します")
        kyoto = prefectures.add({"number": 26, "name": "京都府"}, id="kyoto")
        logger.info("指定したドキュメントID: %s", kyoto['id'])
        logger.info(
            "ドキュメントデータ: number=%s, name=%s",
            kyoto['number'], kyoto['name']
        )

        all_docs = prefectures.get()
        logger.info("コレクション内のドキュメント数: %d", len(all_docs))
        for doc in all_docs:
            logger.info(
                "  %s: %s (番号: %s)",
                doc['id'], doc['name'], doc['number']
            )

        # 特別処理: データベースに直接アクセスしてCSVファイルを生成
        logger.info("データベースパス: %s", db_path)
        logger.info("特別処理: データベースからCSVファイルを生成します")

        # データベース内のテーブルを確認
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info("データベース内のテーブル: %s", tables)
        conn.close()

        export_to_csv(db_path, "都道府県", "都道府県_export.csv")

        logger.info("自動ドキュメントID生成の例を終了します")

    finally:
        # 一時ファイルを削除
        try:
            os.unlink(db_path)
        except Exception:
            pass


def export_to_csv(db_path: str, collection_name: str, csv_filename: str) -> None:
    """SQLiteデータベースのテーブルをCSVファイルにエクスポートします。

    Args:
        db_path: SQLiteデータベースのパス
        collection_name: エクスポートするコレクション名
        csv_filename: 出力するCSVファイル名
    """
    try:
        # SQLiteに接続
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        safe_table_name = collection_name
        logger.info("コレクション名: %s", collection_name)

        # テーブルからデータを取得
        # コレクション名が「都道府県」の場合も、テーブル名はそのまま「都道府県」としてアクセス
        if collection_name == "都道府県":
            cursor.execute("SELECT id, data, created_at, updated_at FROM 都道府県")
        else:
            cursor.execute(
                f"SELECT id, data, created_at, updated_at FROM {safe_table_name}"
            )
        rows = cursor.fetchall()

        # CSVファイルに書き込み
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # ヘッダー行を書き込み
            writer.writerow(["id", "number", "name", "created_at", "updated_at"])

            # データをCSVに書き込む
            for row in rows:
                data = json.loads(row["data"])
                writer.writerow(
                    [
                        row["id"],
                        data.get("number"),
                        data.get("name"),
                        row["created_at"],
                        row["updated_at"],
                    ]
                )

        logger.info("CSVファイル %s をエクスポートしました", csv_filename)
        # CSVファイルの内容を表示
        with open(csv_filename, "r", encoding="utf-8") as f:
            logger.info("CSVファイルの内容:\n%s", f.read())

    except Exception as e:
        logger.error("CSVファイルの生成中にエラーが発生しました: %s", e)
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()
