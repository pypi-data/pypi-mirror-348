import unittest
from uuid import UUID
from base58uuid import (
    uuid58,
    uuid58_encode,
    uuid58_decode,
    uuid58_encode_safe,
    uuid58_decode_safe,
    Uuid58EncodeError,
    Uuid58DecodeError,
)

class TestUuid58(unittest.TestCase):
    def test_uuid58_generation(self):
        """uuid58()が22文字の文字列を生成することをテスト"""
        result = uuid58()
        self.assertEqual(len(result), 22)
        # Base58の文字セットに含まれる文字のみで構成されていることを確認
        self.assertTrue(all(c in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" for c in result))

    def test_uuid58_encode_decode_roundtrip(self):
        """UUIDのエンコードとデコードの往復変換をテスト"""
        original_uuid = "f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf"
        encoded = uuid58_encode(original_uuid)
        decoded = uuid58_decode(encoded)
        self.assertEqual(decoded, original_uuid)

    def test_uuid58_encode_without_hyphens(self):
        """ハイフンなしのUUIDでも正しくエンコードできることをテスト"""
        uuid_without_hyphens = "f4b247fd1f8745d4aa061c6fc0a8dfaf"
        encoded = uuid58_encode(uuid_without_hyphens)
        self.assertEqual(len(encoded), 22)

    def test_uuid58_encode_invalid_uuid(self):
        """無効なUUIDでエンコードを試みた場合のエラーをテスト"""
        with self.assertRaises(Uuid58EncodeError):
            uuid58_encode("invalid-uuid")

    def test_uuid58_decode_invalid_length(self):
        """無効な長さの文字列でデコードを試みた場合のエラーをテスト"""
        with self.assertRaises(Uuid58DecodeError):
            uuid58_decode("invalid")

    def test_uuid58_encode_safe_success(self):
        """安全なエンコードの成功ケースをテスト"""
        result = uuid58_encode_safe("f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 22)

    def test_uuid58_encode_safe_error(self):
        """安全なエンコードのエラーケースをテスト"""
        result = uuid58_encode_safe("invalid-uuid")
        self.assertIsInstance(result, Uuid58EncodeError)

    def test_uuid58_decode_safe_success(self):
        """安全なデコードの成功ケースをテスト"""
        encoded = uuid58_encode("f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf")
        result = uuid58_decode_safe(encoded)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf")

    def test_uuid58_decode_safe_error(self):
        """安全なデコードのエラーケースをテスト"""
        result = uuid58_decode_safe("invalid")
        self.assertIsInstance(result, Uuid58DecodeError)

    def test_multiple_uuid58_generation(self):
        """複数のUUID58が一意であることをテスト"""
        results = set()
        for _ in range(1000):
            result = uuid58()
            self.assertNotIn(result, results)
            results.add(result)

if __name__ == "__main__":
    unittest.main() 