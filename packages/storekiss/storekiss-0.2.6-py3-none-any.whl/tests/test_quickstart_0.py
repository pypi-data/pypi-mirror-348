import pytest
import datetime
from datetime import timezone
from storekiss import litestore, SERVER_TIMESTAMP

@pytest.fixture
def temp_db_path(tmp_path):
    # テスト用の一時DBファイルを作成
    return str(tmp_path / "quickstart_0_test.db")


def test_quickstart_0_basic_types(temp_db_path):
    db = litestore.client(db_path=temp_db_path)
    doc_ref = db.collection('testUsers').document('user_001')
    doc_ref.set({
        'name': 'Taro Yamada',
        'age': 30,
        'weight': 70.12,
        'email': 'taro@example.com',
        'valid': True,
        'createdAt': SERVER_TIMESTAMP,
        'updatedAt': datetime.datetime.now(timezone.utc)
    })

    # ドキュメント取得
    doc = doc_ref.get()
    assert doc is not None
    data = doc.to_dict()
    assert isinstance(data["createdAt"], datetime.datetime), f"createdAt is not datetime: {type(data['createdAt'])}"
    assert isinstance(data["updatedAt"], datetime.datetime), f"updatedAt is not datetime: {type(data['updatedAt'])}"
    assert isinstance(data["weight"], float), f"weight is not float: {type(data['weight'])}"
    assert isinstance(data["age"], int), f"age is not int: {type(data['age'])}"
    assert isinstance(data["valid"], bool), f"valid is not bool: {type(data['valid'])}"
    assert data["name"] == "Taro Yamada"
    assert data["email"] == "taro@example.com"
