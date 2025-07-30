from storekiss import litestore as firestore
import datetime
from datetime import timezone
import logkiss as logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Firestoreクライアントを作成
db = firestore.Client()

# データを追加する
doc_ref = db.collection('testUsers').document('user_001')
doc_ref.set({
    'name': 'Taro Yamada',
    'age': 30,
    'weight': 70.12,
    'email': 'taro@example.com',
    'valid': True,
    'createdAt': firestore.SERVER_TIMESTAMP,
    'updatedAt': datetime.datetime.now(timezone.utc)
})

print("Document created!")


from storekiss import litestore

# Firestoreクライアントを作成
db = litestore.Client()

# ドキュメントを取得する
doc_ref = db.collection('testUsers').document('user_001')
doc = doc_ref.get()

# createdAt と updatedAt が datetime型であることをassertで確認する
# weightはfloat型であることをassertで確認する
# ageはint型であることをassertで確認する
# validはbool型であることをassertで確認する

if doc.exists:
    data = doc.to_dict()
    assert isinstance(data["createdAt"], datetime.datetime), f"createdAt is not datetime: {type(data['createdAt'])}"
    assert isinstance(data["updatedAt"], datetime.datetime), f"updatedAt is not datetime: {type(data['updatedAt'])}"
    assert isinstance(data["weight"], float), f"weight is not float: {type(data['weight'])}"
    assert isinstance(data["age"], int), f"age is not int: {type(data['age'])}"
    assert isinstance(data["valid"], bool), f"valid is not bool: {type(data['valid'])}"
    print(f"Document data: {data}")
else:
    print("No such document!")

