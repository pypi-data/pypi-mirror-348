"""
DELETE_FIELDセンチネル値とマージ機能のデモンストレーション。

このサンプルは、storekissライブラリのDELETE_FIELDセンチネル値と
マージ機能を使用する方法を示します。
"""
import logkiss as logging
from storekiss import litestore
from storekiss.litestore import DELETE_FIELD


def main():
    """DELETE_FIELDセンチネル値とマージ機能のデモンストレーション"""
    logging.info("DELETE_FIELDセンチネル値とマージ機能の例を開始します")

    db = litestore.client(db_path="test.db", default_collection="cities")

    cities = db.collection("cities")

    tokyo_doc = cities.document("tokyo")
    tokyo_doc.set(
        {
            "name": "東京",
            "country": "日本",
            "population": 13960000,
            "area": 2194,
            "landmarks": ["東京タワー", "スカイツリー", "皇居"],
            "details": {"founded": 1457, "mayor": "小池百合子", "wards": 23},
        }
    )

    logging.info("初期データ:")
    logging.info(tokyo_doc.get())

    logging.info("\nDELETE_FIELDを使用してフィールドを削除します")
    tokyo_doc.update({"area": DELETE_FIELD, "details": {"mayor": DELETE_FIELD}})

    logging.info("フィールド削除後のデータ:")
    logging.info(tokyo_doc.get())

    logging.info("\nマージオプションでドキュメントを更新します")
    tokyo_doc.set(
        {
            "name": "東京都",
            "landmarks": ["東京タワー", "スカイツリー", "東京駅"],
            "details": {"founded": 1603},  # 江戸時代の始まりに変更
        },
        merge=True,
    )

    logging.info("マージ後のデータ:")
    logging.info(tokyo_doc.get())

    logging.info("\nマージなしでドキュメントを設定します（完全に置き換え）")
    tokyo_doc.set({"name": "Tokyo", "country": "Japan", "population": 14000000})

    logging.info("置き換え後のデータ:")
    logging.info(tokyo_doc.get())

    osaka_doc = cities.document("osaka")
    osaka_doc.set(
        {
            "name": "大阪",
            "country": "日本",
            "population": 8800000,
            "area": 1905,
            "landmarks": ["大阪城", "通天閣", "ユニバーサルスタジオ"],
            "details": {"founded": 1889, "mayor": "松井一郎", "wards": 24},
        }
    )

    logging.info("\n大阪の初期データ:")
    logging.info(osaka_doc.get())

    logging.info("\n複数のフィールドを一度に削除します")
    osaka_doc.update(
        {
            "area": DELETE_FIELD,
            "landmarks": DELETE_FIELD,
            "details": {"mayor": DELETE_FIELD, "wards": DELETE_FIELD},
        }
    )

    logging.info("複数フィールド削除後のデータ:")
    logging.info(osaka_doc.get())

    tokyo_doc.delete()
    osaka_doc.delete()

    logging.info("\nDELETE_FIELDセンチネル値とマージ機能の例を終了します")


if __name__ == "__main__":
    main()
