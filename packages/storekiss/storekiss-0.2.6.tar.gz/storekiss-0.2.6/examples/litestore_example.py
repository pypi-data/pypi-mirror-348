"""
LiteStore interface example for storekiss.

This example demonstrates how to use the LiteStore interface
of the storekiss library with earthquake data.
"""
import json
import logkiss as logging
from pathlib import Path

from storekiss import litestore


def load_earthquake_data():
    """地震データをJSONファイルから読み込みます。"""
    data_path = Path(__file__).parent / "earthquake_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """メイン関数"""
    logging.info("LiteStoreインターフェースの例を開始します")

    
    store = litestore.Client(db_path=":memory:", )

    earthquakes = store.collection("earthquakes")


    earthquake_data = load_earthquake_data()
    logging.info(f"{len(earthquake_data)}件の地震データを読み込みました")

    for quake in earthquake_data:
        doc = earthquakes.add(quake)
        logging.info(f"地震データを追加しました: {doc['id']} - {doc['place']}")

    results = earthquakes.where("mag", "==", 5.2).get()
    logging.info(f"マグニチュード5.2の地震: {len(results)}件")
    for quake in results:
        logging.info(f"  {quake['id']} - {quake['place']} (M{quake['mag']})")

    results = earthquakes.where("place", "==", "Honshu, Japan").get()
    logging.info(f"本州の地震: {len(results)}件")
    for quake in results:
        logging.info(f"  {quake['id']} - {quake['time']} (M{quake['mag']})")

    results = earthquakes.order_by("mag", direction="DESC").limit(2).get()
    logging.info("マグニチュード順（降順）の上位2件:")
    for quake in results:
        logging.info(f"  {quake['id']} - {quake['place']} (M{quake['mag']})")

    doc_id = earthquake_data[0]["id"]
    doc = earthquakes.document(doc_id)
    quake_data = doc.get()
    logging.info(f"ドキュメント取得: {quake_data['id']} - {quake_data['place']}")

    updated = doc.update({"mag": 5.5, "updated": True})
    logging.info(f"ドキュメント更新: {updated['id']} - マグニチュード {updated['mag']}")

    updated_data = doc.get()
    logging.info(
        f"更新後のデータ: {updated_data['mag']} (更新フラグ: {updated_data.get('updated')})"
    )

    count = len(earthquakes.get())
    logging.info(f"地震データの総数: {count}件")

    count = len(earthquakes.where("mag", "==", 5.5).get())
    logging.info(f"マグニチュード5.5の地震: {count}件")

    doc.delete()
    logging.info(f"ドキュメント {doc_id} を削除しました")

    count = len(earthquakes.get())
    logging.info(f"削除後の地震データの総数: {count}件")

    logging.info("LiteStoreインターフェースの例を終了します")


if __name__ == "__main__":
    main()
