#!/usr/bin/env python3
import os
import sys
import warnings

VERSION = "0.0.0"

# バージョン表示のチェック（他の処理より優先）
if "-v" in sys.argv or "--version" in sys.argv:
    print(f"Gemini Command CLI version {VERSION}")
    sys.exit(0)

# 標準ライブラリのみで.envを読み込む（外部ライブラリへの依存を排除）
def load_env_manual(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip("'").strip('"')

# スクリプトと同じ場所にある.envを読み込む
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_env_manual(env_path)

# Suppress FutureWarning from google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai

# APIキー設定（徹底的にクリーニング）
api_key = os.environ.get("GEMINI_API_KEY", "").strip()

if not api_key:
    print(f"\n=== エラー: APIキーが見つかりません ===")
    print(f".envファイル ({env_path}) に GEMINI_API_KEY が設定されているか確認してください。")
    sys.exit(1)

genai.configure(api_key=api_key)

# 以前確実に動いていたモデル名に固定
model = genai.GenerativeModel('models/gemini-3-flash-preview')

# 標準入力の読み込み
pipe_input = sys.stdin.read() if not sys.stdin.isatty() else ""
user_query = " ".join([arg for arg in sys.argv[1:] if arg not in ("-v", "--version")])

if not user_query and not pipe_input:
    print("Usage: history | ./gemini.py '解析指示'")
    sys.exit()

# 解析の実行
try:
    response = model.generate_content(f"{pipe_input}\n\n質問: {user_query}")
    print(response.text)
except Exception as e:
    # 既存の親切なエラー表示は残す
    if "API_KEY_INVALID" in str(e) or "API key expired" in str(e):
        print(f"\n=== エラー: APIキーが無効、または期限切れです ===")
        print("以下の手順でAPIキーを確認・更新してください:\n")
        print("1. .envファイルを確認し、正しいAPIキーが設定されているか確認してください。")
        print(f"   (現在読み込んでいるキーの断片: {api_key[:8]}...{api_key[-4:]})")
        print("\n2. 必要であれば Google AI Studio で新しいキーを作成し、.envファイルを更新してください:")
        print("   https://aistudio.google.com/app/apikey")
        print(f"\n(詳細エラー: {e})\n")
    else:
        print(f"エラーが発生しました: {e}")
