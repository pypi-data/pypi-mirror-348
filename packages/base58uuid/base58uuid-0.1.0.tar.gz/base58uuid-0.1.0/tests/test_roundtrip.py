import unittest
from uuid import UUID, uuid4
from base58uuid import uuid58_encode, uuid58_decode

class TestUuid58Roundtrip(unittest.TestCase):
    def test_random_uuid_roundtrip(self):
        """ランダムなUUIDで往復変換をテスト"""
        # 1000個のランダムなUUIDを生成してテスト
        for _ in range(1000):
            # 新しいUUIDを生成
            original_uuid = str(uuid4())
            
            # UUIDをBase58に変換
            encoded = uuid58_encode(original_uuid)
            
            # Base58をUUIDに戻す
            decoded = uuid58_decode(encoded)
            
            # 元のUUIDと一致することを確認
            self.assertEqual(decoded, original_uuid)
            
            # 長さが22文字であることを確認
            self.assertEqual(len(encoded), 22)

    def test_specific_uuid_roundtrip(self):
        """特定のUUIDで往復変換をテスト"""
        test_cases = [
            "00000000-0000-0000-0000-000000000000",  # 最小値
            "ffffffff-ffff-ffff-ffff-ffffffffffff",  # 最大値
            "f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf",  # ランダムな値
            "123e4567-e89b-12d3-a456-426614174000",  # 別のランダムな値
        ]
        
        for uuid in test_cases:
            # UUIDをBase58に変換
            encoded = uuid58_encode(uuid)
            
            # Base58をUUIDに戻す
            decoded = uuid58_decode(encoded)
            
            # 元のUUIDと一致することを確認
            self.assertEqual(decoded, uuid)
            
            # 長さが22文字であることを確認
            self.assertEqual(len(encoded), 22)

    def test_uuid_without_hyphens_roundtrip(self):
        """ハイフンなしのUUIDで往復変換をテスト"""
        test_cases = [
            "00000000000000000000000000000000",  # 最小値
            "ffffffffffffffffffffffffffffffff",  # 最大値
            "f4b247fd1f8745d4aa061c6fc0a8dfaf",  # ランダムな値
            "123e4567e89b12d3a456426614174000",  # 別のランダムな値
        ]
        
        for uuid in test_cases:
            # UUIDをBase58に変換
            encoded = uuid58_encode(uuid)
            
            # Base58をUUIDに戻す
            decoded = uuid58_decode(encoded)
            
            # 元のUUIDと一致することを確認（ハイフン付きの形式に変換される）
            expected = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
            self.assertEqual(decoded, expected)
            
            # 長さが22文字であることを確認
            self.assertEqual(len(encoded), 22)

if __name__ == "__main__":
    unittest.main() 