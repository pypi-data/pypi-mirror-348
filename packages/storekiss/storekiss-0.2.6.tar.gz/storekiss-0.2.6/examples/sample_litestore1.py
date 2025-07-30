import os
import sys
import datetime
from dotenv import load_dotenv

# ログ出力の設定
import logkiss as logging
logging.basicConfig()
log = logging.getLogger(os.path.split(__file__)[1])
log.setLevel(level=logging.DEBUG)

'''
TEST_COLLECTIONコレクションにデータを書き込み、SQLiteデータベースに保存する

LiteStoreはSQLiteをバックエンドに使用し、Firestoreに似たAPIを提供するライブラリです。
データはSQLiteデータベースファイルに保存され、必要に応じてエクスポート/インポートが可能です。

以下のデータを書き込みます：

name:Alice
height:167.0
level: 3
dob:2000-01-02T03:04:05Z
valid: True

name:Bob
height:170.0
level: 4
dob:2000-02-03T04:05:06Z
valid: False

name:Charie
height:180.0
level: 5
dob:2000-03-04T05:06:07Z
valid: Talse
'''

# コレクション名の定義
TEST_COLLECTION_NAME = 'TEST_COLLECTION'

# SQLiteデータベースファイルのパス
DB_PATH = os.environ.get('DB_PATH', 'storekiss.db')


class LiteStoreClient:
    """
    LiteStoreクライアントクラス
    """
    def __init__(self, db_path=None):
        """
        LiteStoreクライアントの初期化
        """
        from storekiss.litestore import client
        
        # データベースパスが指定されていない場合はデフォルト値を使用
        if db_path is None:
            db_path = DB_PATH
        
        self.db = client(db_path=db_path)
        log.info('LiteStoreクライアントの初期化が完了しました')
    
    def write_test_data(self):
        """
        TEST_COLLECTIONにサンプルデータを書き込む
        """
        # Aliceのデータを追加
        doc_ref = self.db.collection(TEST_COLLECTION_NAME).document('alice')
        doc_ref.set({
            'name': 'Alice',
            'height': 167.0,
            'level': 3,
            'dob': datetime.datetime.strptime('2000-01-02T03:04:05Z', '%Y-%m-%dT%H:%M:%SZ'),
            'valid': False
        })
        
        # Bobのデータを追加
        doc_ref = self.db.collection(TEST_COLLECTION_NAME).document('bob')
        doc_ref.set({
            'name': 'Bob',
            'height': 170.0,
            'level': 4,
            'dob': datetime.datetime.strptime('2000-02-03T04:05:06Z', '%Y-%m-%dT%H:%M:%SZ'),
            'valid': False
        })
        
        # Charlieのデータを追加
        doc_ref = self.db.collection(TEST_COLLECTION_NAME).document('charlie')
        doc_ref.set({
            'name': 'Charie',  # 元のデータのスペルを維持
            'height': 180.0,
            'level': 5,
            'dob': datetime.datetime.strptime('2000-03-04T05:06:07Z', '%Y-%m-%dT%H:%M:%SZ'),
            'valid': False
        })
        
        log.info(f'{TEST_COLLECTION_NAME}コレクションにデータを書き込みました')

    def read_test_data(self):
        """
        TEST_COLLECTIONからデータを読み取って表示する
        
        Returns:
            dict: ドキュメントIDをキー、ドキュメントデータを値とする辞書
        """
        try:
            collection_ref = self.db.collection(TEST_COLLECTION_NAME)
            docs = collection_ref.get()
            
            results = {}
            print(f'\n{TEST_COLLECTION_NAME}コレクションのデータ:')
            print('=' * 50)
            
            for doc in docs:
                # DocumentSnapshotオブジェクトからデータを取得
                doc_id = doc.id
                doc_data = doc.to_dict()
                
                results[doc_id] = doc_data
                
                # データを整形して表示
                print(f'ドキュメントID: {doc_id}')
                for key, value in doc_data.items():
                    print(f'  {key}: {value}')
                print('-' * 30)
            
            log.info(f'{TEST_COLLECTION_NAME}コレクションから{len(results)}件のドキュメントを読み取りました')
            return results
        except Exception as e:
            log.error(f'データ読み取り中にエラーが発生しました: {e}')
            print(f'エラー: データ読み取り中にエラーが発生しました: {e}')
            return {}
        
    def query_by_date(self, date_str='2000-02-03T04:05:06Z'):
        """
        指定した日付より後のdob（生年月日）を持つドキュメントを検索し、
        見つかったレコードのvalidフィールドをTrueに更新する
        
        Args:
            date_str: 検索基準となる日付（ISO 8601形式）
            
        Returns:
            dict: 検索結果のドキュメントIDをキー、ドキュメントデータを値とする辞書
        """
        # 基準日時をdatetimeオブジェクトに変換
        base_date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        
        try:
            # まず、すべてのドキュメントを取得して、メモリ上でフィルタリングする
            # これはクエリの実行がうまくいかない場合の代替手段
            collection_ref = self.db.collection(TEST_COLLECTION_NAME)
            all_docs = collection_ref.get()
            
            # 結果を格納
            results = {}
            updated_docs = []
            print('\n{}より後のdob（生年月日）を持つドキュメント:'.format(date_str))
            print('=' * 50)
            
            for doc in all_docs:
                # ドキュメントID
                doc_id = doc.id
                
                # ドキュメントIDがない場合はスキップ
                if not doc_id:
                    continue
                
                # ドキュメントデータ
                doc_data = doc.to_dict()
                
                # dobフィールドがない場合はスキップ
                if 'dob' not in doc_data:
                    continue
                
                # dobがdatetimeオブジェクトでない場合はスキップ
                if not isinstance(doc_data['dob'], datetime.datetime):
                    continue
                
                # 基準日付より後のドキュメントのみを選択
                if doc_data['dob'] <= base_date:
                    continue
                
                # 条件に一致するドキュメントを処理
                results[doc_id] = doc_data
                updated_docs.append(doc_id)
                
                # 更新前のデータを表示
                print(f'ドキュメントID: {doc_id} (更新前)')
                for key, value in doc_data.items():
                    print(f'  {key}: {value}')
                print('-' * 30)
                
                try:
                    # validフィールドをTrueに更新
                    doc_ref = self.db.collection(TEST_COLLECTION_NAME).document(doc_id)
                    doc_ref.update({'valid': True})
                except Exception as e:
                    log.error(f'ドキュメント {doc_id} の更新中にエラーが発生しました: {e}')
                    print(f'エラー: ドキュメント {doc_id} の更新中にエラーが発生しました: {e}')
            
            # 更新後のデータを取得して表示
            if updated_docs:
                print('\n更新後のデータ:')
                print('=' * 50)
                
                # 再度すべてのドキュメントを取得
                updated_all_docs = collection_ref.get()
                
                for doc_id in updated_docs:
                    # 更新されたドキュメントを探す
                    for doc in updated_all_docs:
                        if doc.id == doc_id:
                            updated_data = doc.to_dict()
                            
                            # 更新後のデータを表示
                            print(f'ドキュメントID: {doc_id} (更新後)')
                            for key, value in updated_data.items():
                                print(f'  {key}: {value}')
                            print('-' * 30)
                            
                            # 結果を更新後のデータに更新
                            results[doc_id] = updated_data
                            break
            
            log.info(f'日付クエリの結果: {len(results)}件のドキュメントが見つかり、validフィールドをTrueに更新しました')
            return results
        except Exception as e:
            log.error(f'クエリ実行中にエラーが発生しました: {e}')
            print(f'エラー: クエリ実行中にエラーが発生しました: {e}')
            return {}

def main():
    """
    メイン実行関数
    """
    try:
        # コマンドライン引数の処理
        import argparse
        parser = argparse.ArgumentParser(description='LiteStoreデータを書く')
        parser.add_argument('--write', action='store_true', help='テストデータを書き込む')
        parser.add_argument('--read', action='store_true', help='テストデータを読み取る')
        parser.add_argument('--query', action='store_true', help='日付クエリを実行する')
        parser.add_argument('--date', default='2000-02-03T04:05:06Z', help='クエリの基準日付（ISO 8601形式）')
        parser.add_argument('--db-path', help='SQLiteデータベースファイルのパス')
        args = parser.parse_args()
        
        # LiteStoreクライアントの初期化
        client = LiteStoreClient(db_path=args.db_path)
        
        # TEST_COLLECTIONにデータを書き込む（--writeオプションが指定された場合）
        if args.write:
            client.write_test_data()
        
        # TEST_COLLECTIONからデータを読み取る（--readオプションが指定された場合）
        if args.read:
            client.read_test_data()
            
        # 日付クエリを実行する（--queryオプションが指定された場合）
        if args.query:
            client.query_by_date(args.date)
            client.read_test_data()
            
        # オプションが指定されていない場合は両方実行
        if not (args.write or args.read or args.query):
            print('テストデータを書き込み、読み取ります...')
            client.write_test_data()
            client.read_test_data()
    except Exception as e:
        log.error(f'エラーが発生しました: {e}')
        print(f'エラー: {e}')
        sys.exit(1)
        

if __name__ == "__main__":
    main()


