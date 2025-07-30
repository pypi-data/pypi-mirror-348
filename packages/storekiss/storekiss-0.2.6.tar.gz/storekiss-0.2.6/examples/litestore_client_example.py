"""
LiteStoreインターフェースのデモンストレーション。

このサンプルは、storekissライブラリのLiteStoreインターフェースを
使用する方法を示します。一般的なドキュメントデータベースと同様の構文でデータを
操作することができます。
"""
import logging
from storekiss.litestore import Client


def main():
    """LiteStoreインターフェースのデモンストレーション"""
    logging.info("LiteStoreインターフェースの例を開始します")

    # ファイルベースのデータベースを使用
    db = Client(db_path="test.db")

    # デフォルトのコレクションを使用
    prefectures = db.collection("prefecture")

    logging.info("自動生成IDでドキュメントを作成します")
    new_doc = prefectures.document()
    new_doc.set({"id": 1, "name": "北海道"})
    doc_snapshot = new_doc.get()
    logging.info("ドキュメントID: %s, データ: %s", new_doc.id, doc_snapshot.to_dict())

    logging.info("明示的なIDでドキュメントを作成します")
    tokyo_doc = prefectures.document("tokyo")
    tokyo_doc.set({"id": 13, "name": "東京都"})
    doc_snapshot = tokyo_doc.get()
    logging.info("ドキュメントID: %s, データ: %s", tokyo_doc.id, doc_snapshot.to_dict())

    logging.info("add()メソッドでドキュメントを追加します")
    osaka_data = prefectures.add({"id": 27, "name": "大阪府"})
    logging.info("追加されたドキュメント: %s", osaka_data)

    logging.info("ドキュメントを更新します")
    tokyo_doc.update({"population": 13960000})
    doc_snapshot = tokyo_doc.get()
    logging.info("更新後のデータ: %s", doc_snapshot.to_dict())

    logging.info("マージオプションでドキュメントを設定します")
    tokyo_doc.set({"area": 2194}, merge=True)
    doc_snapshot = tokyo_doc.get()
    logging.info("マージ後のデータ: %s", doc_snapshot.to_dict())

    logging.info("すべてのドキュメントを取得します")
    all_docs = prefectures.get()
    for doc in all_docs:
        doc_data = doc.to_dict()
        logging.info("  %s: %s", doc_data['id'], doc_data['name'])

    if len(all_docs) > 0:
        logging.info("フィルタ付きクエリを実行します")
        filtered_docs = prefectures.where("id", ">", 10).get()
        logging.info("ID > 10のドキュメント数: %d", len(filtered_docs))
        for doc in filtered_docs:
            doc_data = doc.to_dict()
            logging.info("  %s: %s", doc_data['id'], doc_data['name'])

    logging.info("ドキュメントを削除します")
    new_doc.delete()
    logging.info("ドキュメントが削除されました")

    remaining_docs = prefectures.get()
    logging.info("残りのドキュメント数: %d", len(remaining_docs))
    for doc in remaining_docs:
        doc_data = doc.to_dict()
        logging.info("  %s: %s", doc_data['id'], doc_data['name'])

    logging.info("LiteStoreインターフェースの例を終了します")


if __name__ == "__main__":
    main()
