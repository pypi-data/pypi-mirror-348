"""
SERVER_TIMESTAMP機能のデモンストレーション。

このサンプルは、storekissライブラリのSERVER_TIMESTAMP機能を使用して、
ドキュメントの作成時と更新時に自動的にタイムスタンプを設定する方法を示します。
"""
import logkiss as logging

from storekiss import litestore
from storekiss.validation import StringField, DateTimeField

from storekiss.litestore import SERVER_TIMESTAMP


def main():
    """SERVER_TIMESTAMP機能のデモンストレーション"""
    logging.info("SERVER_TIMESTAMPの例を開始します")

    schema = litestore.Schema(
        {
            "id": StringField(required=True),
            "title": StringField(required=True),
            "created_at": DateTimeField(required=True),
            "updated_at": DateTimeField(required=True),
            "content": StringField(required=False),
        }
    )

    store = litestore.Client(db_path=":memory:", schema=schema)

    posts = store.collection("posts")
    # スキーマを必ず登録（テーブル作成）
    posts._collection.schema = schema

    logging.info("SERVER_TIMESTAMPを使用してドキュメントを作成します")
    post = posts.add(
        {
            "id": "post_001",
            "title": "最初の投稿",
            "created_at": SERVER_TIMESTAMP,  # 作成時に自動的に現在時刻が設定される
            "updated_at": SERVER_TIMESTAMP,  # 更新時に自動的に現在時刻が設定される
        }
    )

    logging.info(f"ドキュメントが作成されました: {post['id']}")
    logging.info(f"  タイトル: {post['title']}")
    logging.info(
        f"  作成日時: {post['created_at']} (型: {type(post['created_at']).__name__})"
    )
    logging.info(
        f"  更新日時: {post['updated_at']} (型: {type(post['updated_at']).__name__})"
    )

    logging.info("ドキュメントを更新します...")

    doc = posts.doc(post["id"])
    updated_post = doc.update(
        {
            "content": "これは最初の投稿の内容です。",
            "updated_at": SERVER_TIMESTAMP,  # 更新時に自動的に現在時刻が設定される
        }
    )

    logging.info(f"ドキュメントが更新されました: {updated_post['id']}")
    logging.info(f"  タイトル: {updated_post['title']}")
    logging.info(f"  内容: {updated_post['content']}")
    logging.info(f"  作成日時: {updated_post['created_at']} (変更なし)")
    logging.info(f"  更新日時: {updated_post['updated_at']} (自動更新)")

    logging.info("ネストされたオブジェクト内でSERVER_TIMESTAMPを使用します")
    nested_post = posts.add(
        {
            "title": "ネストされたタイムスタンプの例",
            "created_at": SERVER_TIMESTAMP,
            "updated_at": SERVER_TIMESTAMP,
            "metadata": {"published_at": SERVER_TIMESTAMP, "status": "published"},
        }
    )

    logging.info(f"ネストされたドキュメントが作成されました: {nested_post['id']}")
    logging.info(f"  タイトル: {nested_post['title']}")
    logging.info(f"  作成日時: {nested_post['created_at']}")
    logging.info(f"  公開日時: {nested_post['metadata']['published_at']}")

    logging.info("配列内でSERVER_TIMESTAMPを使用します")
    array_post = posts.add(
        {
            "title": "配列内タイムスタンプの例",
            "created_at": SERVER_TIMESTAMP,
            "updated_at": SERVER_TIMESTAMP,
            "revisions": [
                {"version": 1, "timestamp": SERVER_TIMESTAMP},
                {"version": 2, "timestamp": SERVER_TIMESTAMP},
            ],
        }
    )

    logging.info(f"配列を含むドキュメントが作成されました: {array_post['id']}")
    logging.info(f"  タイトル: {array_post['title']}")
    logging.info(f"  作成日時: {array_post['created_at']}")
    logging.info(f"  リビジョン1の時間: {array_post['revisions'][0]['timestamp']}")
    logging.info(f"  リビジョン2の時間: {array_post['revisions'][1]['timestamp']}")

    logging.info("SERVER_TIMESTAMPの例を終了します")


if __name__ == "__main__":
    main()
