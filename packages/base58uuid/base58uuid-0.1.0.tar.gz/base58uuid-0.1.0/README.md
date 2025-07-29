# Base58UUID (Python版)

UUIDをBase58エンコード/デコードするPythonライブラリです。短く、URLセーフな文字列としてUUIDを表現できます。

## インストール

pipを使用してインストールできます：

```bash
pip install base58uuid
```

## 必要条件

- Python 3.7以上

## 使用方法

### 基本的な使い方

```python
from base58uuid import Base58UUID

# 新しいUUIDを生成
b58 = Base58UUID()
uuid = b58.get_uuid()  # 例: "f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf"

# 既存のUUIDをBase58エンコード
b58 = Base58UUID('f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf')
encoded = b58.encode()  # 例: "XDY9dmBbcMBXqcRvYw8xJ2"

# Base58文字列をUUIDにデコード
decoded = b58.decode('XDY9dmBbcMBXqcRvYw8xJ2')  # 元のUUIDに戻る
```

### エラーハンドリング

```python
try:
    # 無効なUUID形式
    b58 = Base58UUID('invalid-uuid')
except ValueError as e:
    # "Invalid UUID format" エラー
    pass

try:
    # 無効なBase58文字列
    b58 = Base58UUID()
    b58.decode('invalid')
except ValueError as e:
    # "Invalid Base58 character" エラー
    pass
```

## 開発

### セットアップ

```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Linuxの場合
# または
.\venv\Scripts\activate  # Windowsの場合

# 依存関係のインストール
pip install -e ".[dev]"

# テストの実行
pytest tests/
```

### テスト

以下のテストケースが含まれています：

- 既知のUUIDのエンコード
- ハイフンなしUUIDのエンコード
- Base58文字列のデコード
- 無効な入力のエラーハンドリング
- エンコード/デコードの一貫性
- 複数回エンコードの結果の一貫性

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](../LICENSE)ファイルを参照してください。

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 作者

- Yoshitake Hatada (@htpboost) 