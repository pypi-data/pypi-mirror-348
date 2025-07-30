"""
storekissライブラリで1000件のフェイクデータを作成し、collection.stream()とdoc.reference.update()を使用する
シンプルなサンプルコード

このスクリプトは、storekissライブラリを使用して1000件のフェイクデータを作成し、
collection.stream()でドキュメントを取得し、doc.reference.update()で更新する方法を示します。
"""

import os
import uuid
import time
import random
from faker import Faker
from storekiss.litestore import Client
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# パッチは不要になりました - ライブラリ本体に機能が実装されています

def create_fake_data(collection, count=1000):
    """
    フェイクデータを作成する関数
    
    Args:
        collection: データを作成するコレクション
        count: 作成するドキュメント数
    
    Returns:
        list: 作成したドキュメントIDのリスト
    """
    fake = Faker('ja_JP')  # 日本語のフェイクデータを生成
    doc_ids = []
    
    logger.info(f"{count}件のフェイクデータを作成します...")
    start_time = time.time()
    
    for i in range(count):
        doc_id = str(uuid.uuid4())
        doc_ids.append(doc_id)
        
        # フェイクデータを生成
        data = {
            'name': fake.name(),
            'email': fake.email(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'company': fake.company(),
            'job': fake.job(),
            'created_at': fake.date_time_this_year().isoformat(),
            'somefield': True,  # 更新対象のフィールド
            'random_number': random.randint(1, 1000)
        }
        
        # ドキュメントを作成
        collection.document(doc_id).set(data)
        
        # 進捗を表示
        if (i + 1) % 100 == 0:
            logger.info(f"{i + 1}件のドキュメントを作成しました")
    
    end_time = time.time()
    logger.info(f"データ作成完了: {count}件 (所要時間: {end_time - start_time:.3f}秒)")
    
    return doc_ids

def update_documents_with_stream(collection):
    """
    collection.stream()とdoc.reference.update()を使用してドキュメントを更新する関数
    
    Args:
        collection: 更新するドキュメントのコレクション
    
    Returns:
        int: 更新したドキュメント数
    """
    logger.info("collection.stream()とdoc.reference.update()を使用してドキュメントを更新します...")
    start_time = time.time()
    count = 0

    # ユーザーが要求した形式のコード
    for doc in collection.stream():
        # doc.reference.update()を使用してドキュメントを更新
        doc.reference.update({"somefield": False})
        count += 1
        
        # 進捗を表示
        if count % 100 == 0:
            logger.info(f"{count}件のドキュメントを更新しました")
    
    end_time = time.time()
    logger.info(f"更新完了: {count}件 (所要時間: {end_time - start_time:.3f}秒)")
    
    return count

def verify_updates(collection):
    """
    更新が正しく行われたかを確認する関数
    
    Args:
        collection: 確認するドキュメントのコレクション
    
    Returns:
        tuple: (更新されたドキュメント数, 全ドキュメント数)
    """
    logger.info("更新結果を確認しています...")
    start_time = time.time()
    
    # すべてのドキュメントを取得
    docs = list(collection.get())
    total_count = len(docs)
    updated_count = 0
    
    # 更新されたドキュメントをカウント
    for doc in docs:
        data = doc.to_dict()
        if data.get('somefield') is False:
            updated_count += 1
    
    end_time = time.time()
    
    # 結果を表示
    if updated_count == total_count:
        logger.info(f"✅ すべてのドキュメントが正しく更新されました ({updated_count}/{total_count})")
    else:
        logger.error(f"❌ 一部のドキュメントが更新されていません ({updated_count}/{total_count})")
    
    logger.info(f"確認完了: 所要時間: {end_time - start_time:.3f}秒")
    
    return updated_count, total_count

def main():
    """
    メイン関数
    """
    # データベースファイルのパス
    db_path = "simple_stream_update_1000.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = Client(db_path)
    
    # コレクション名
    collection_name = 'users'
    collection = db.collection(collection_name)
    
    # フェイクデータを作成
    doc_ids = create_fake_data(collection, count=1000)
    
    # ドキュメントを更新
    updated_count = update_documents_with_stream(collection)
    
    # 更新結果を確認
    verified_count, total_count = verify_updates(collection)
    
    # 最終結果
    logger.info(f"\n処理結果サマリー:")
    logger.info(f"- 作成したドキュメント数: 1000件")
    logger.info(f"- 更新したドキュメント数: {updated_count}件")
    logger.info(f"- 正しく更新されたドキュメント数: {verified_count}/{total_count}件")

if __name__ == "__main__":
    main()
