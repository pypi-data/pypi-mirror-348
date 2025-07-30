"""
storekiss CRUDライブラリを使用した地震データの例。

この例は以下を示しています：
1. datetime検証を持つスキーマの作成
2. JSONからの地震データの読み込み
3. datetime変換を含むデータの保存と取得
4. 地震データの検索
"""
import json
import datetime
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storekiss.litestore import client
from storekiss.exceptions import ValidationError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_earthquake_data():
    """JSONファイルから地震データを読み込む。ISO8601形式の時間文字列をdatetime型に変換する。"""
    data_path = Path(__file__).parent / "earthquake_data.json"
    with open(data_path, "r") as f:
        earthquakes = json.load(f)
        
    for quake in earthquakes:
        if "time" in quake and isinstance(quake["time"], str):
            # "Z"をUTCを表す"+00:00"に置き換えてからdatetimeに変換
            quake["time"] = datetime.datetime.fromisoformat(quake["time"].replace("Z", "+00:00"))
            
    return earthquakes


def main():
    """地震データの例を実行する。"""
    logging.info("地震データベースを作成中...")
    db = client(db_path="earthquakes.db")
    store = db.collection("earthquakes")

    earthquakes = load_earthquake_data()
    logging.info(f"JSONから{len(earthquakes)}件の地震データを読み込みました")

    for quake in earthquakes:
        try:
            stored = store.add(quake, id=quake["id"])
            logging.info(f"地震データを保存しました: {stored['id']} - {stored['place']}")

            logging.info(f"  時間: {stored['time']} (型: {type(stored['time']).__name__})")
        except ValidationError as e:
            logging.error(f"{quake['id']}の検証エラー: {e}")

    logging.info("すべての地震データを取得:")
    all_quakes = store.get()
    for quake in all_quakes:
        quake_data = quake.to_dict()
        # timeがstrならdatetimeに変換
        if isinstance(quake_data["time"], str):
            time_val = datetime.datetime.fromisoformat(quake_data["time"].replace("Z", "+00:00"))
        else:
            time_val = quake_data["time"]
        time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
        logging.info(
            f"{quake.id} - {time_str} - マグニチュード {quake_data['mag']} - {quake_data['place']}"
        )

    logging.info("マグニチュード5.0以上の地震を検索:")
    strong_quakes = []
    for quake in all_quakes:
        quake_data = quake.to_dict()
        if quake_data["mag"] >= 5.0:
            strong_quakes.append(quake)

    for quake in strong_quakes:
        quake_data = quake.to_dict()
        # timeがstrならdatetimeに変換
        if isinstance(quake_data["time"], str):
            time_val = datetime.datetime.fromisoformat(quake_data["time"].replace("Z", "+00:00"))
        else:
            time_val = quake_data["time"]
        time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
        logging.info(
            f"{quake.id} - {time_str} - マグニチュード {quake_data['mag']} - {quake_data['place']}"
        )

    logging.info("日本の地震を検索:")
    japan_quakes = []
    for quake in all_quakes:
        quake_data = quake.to_dict()
        if "Japan" in quake_data["place"]:
            japan_quakes.append(quake)

    for quake in japan_quakes:
        quake_data = quake.to_dict()
        # timeがstrならdatetimeに変換
        if isinstance(quake_data["time"], str):
            time_val = datetime.datetime.fromisoformat(quake_data["time"].replace("Z", "+00:00"))
        else:
            time_val = quake_data["time"]
        time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
        logging.info(
            f"{quake.id} - {time_str} - マグニチュード {quake_data['mag']} - {quake_data['place']}"
        )

    logging.info("東京の地震データに追加情報を更新:")
    tokyo_id = "us7000joqp"
    try:
        tokyo_doc_ref = store.document(tokyo_id)
        
        tokyo_doc = tokyo_doc_ref.get()
        
        tokyo_data = tokyo_doc.to_dict()
        
        tokyo_data.update({
            "felt": 1200,  # 地震を感じた人の数
            "tsunami": False,  # 津波警報が発令されたかどうか
            "updated": datetime.datetime.now(),  # このレコードが更新された時間
        })
        
        updated = tokyo_doc_ref.set(tokyo_data)

        logging.info("東京の地震データを更新しました:")
        logging.info(f"{updated}")
    except ValidationError as e:
        logging.error(f"検証エラー: {e}")

    logging.info("地震レコードの削除:")
    tonga_id = "us6000l9r3"
    store.document(tonga_id).delete()
    logging.info(f"地震データ {tonga_id} を削除しました")

    try:
        store.document(tonga_id).get()
        logging.error("エラー: レコードがまだ存在しています!")
    except Exception as e:
        logging.info(f"確認成功: {e}")

    all_docs = store.get()
    count = len(all_docs)
    logging.info(f"残りの地震レコード数: {count}")

    logging.info("特定の時間範囲内の地震を検索:")
    reference_time_str = "2023-05-16T08:32:19.546Z"
    reference_time = datetime.datetime.fromisoformat(reference_time_str.replace("Z", "+00:00"))
    
    one_day_before = reference_time - datetime.timedelta(hours=24)
    one_day_after = reference_time + datetime.timedelta(hours=24)
    
    logging.info(f"検索時間範囲: {one_day_before.isoformat()} から {one_day_after.isoformat()}")
    
    time_range_query = store.where("time", ">=", one_day_before).where("time", "<=", one_day_after)
    time_range_quakes = time_range_query.get()
    
    logging.info(f"時間範囲内の地震数: {len(time_range_quakes)}")
    for quake in time_range_quakes:
        quake_data = quake.to_dict()
        # timeがstrならdatetimeに変換
        if isinstance(quake_data["time"], str):
            time_val = datetime.datetime.fromisoformat(quake_data["time"].replace("Z", "+00:00"))
        else:
            time_val = quake_data["time"]
        time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
        logging.info(
            f"{quake.id} - {time_str} - マグニチュード {quake_data['mag']} - {quake_data['place']}"
        )


if __name__ == "__main__":
    main()
