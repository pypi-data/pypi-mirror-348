"""
examples ディレクトリ内の全サンプルスクリプトを一括実行し、エラーの有無を確認するユーティリティ。
"""
import subprocess
import os
import sys

EXCLUDE = {"README.md", "earthquake_data.json", "performance_results", "run_all_examples.py"}

examples_dir = os.path.dirname(os.path.abspath(__file__))
files = [f for f in os.listdir(examples_dir) if f.endswith(".py") and f not in EXCLUDE]

success = []
failure = []

for fname in files:
    fpath = os.path.join(examples_dir, fname)
    print(f"\n=== 実行: {fname} ===")
    try:
        result = subprocess.run([sys.executable, fpath], capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.returncode == 0:
            success.append(fname)
        else:
            print(result.stderr)
            failure.append((fname, result.returncode, result.stderr))
    except Exception as e:
        print(f"[ERROR] {fname}: {e}")
        failure.append((fname, "EXCEPTION", str(e)))

print("\n==============================")
print(f"成功: {len(success)} 件")
for f in success:
    print(f"  [OK] {f}")
if failure:
    print(f"失敗: {len(failure)} 件")
    for f, code, err in failure:
        print(f"  [NG] {f} (code={code})\n    {err}")
else:
    print("全て成功！")
