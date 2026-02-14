# 🌌 Gemini Command CLI

Gemini API を利用して、パイプライン入力やコマンドライン引数から即座にテキスト解析を行う強力なコマンドラインツールです。

## ✨ 特徴

- **🚀 高速レスポンス**: `Gemini 3 Flash Preview` モデルを採用し、爆速な回答を実現。
- **🔗 パイプ連携**: `cat file.txt | ./gemini.py` のように他のコマンドと組み合わせて利用可能。
- **🧹 自動クリーンアップ**: 標準ライブラリのみで `.env` を読み込むため、依存関係トラブルを最小限に抑制。
- **🎨 豊かな表現**: Markdown 形式での回答をサポート。

## 🛠 セットアップ

### 1. 依存関係のインストール

```bash
pip install google-generativeai
```

### 2. API キーの設定

`.env` ファイルを作成し、Google AI Studio で取得した API キーを設定します。

```env
GEMINI_API_KEY=あなたのAPIキー
```

## 📖 使い方

### 直接質問する

```bash
./gemini.py "2026年のトレンド予測を教えて"
```

### 他のコマンドの出力を解析する

```bash
cat logs.txt | ./gemini.py "このログからエラーの主要な原因を3つ要約して"
```

### システム情報を解析する

```bash
echo "CPU使用率が高いプロセスを特定して:" && ps aux | ./gemini.py
```

## 🛡 ライセンス

MIT License
