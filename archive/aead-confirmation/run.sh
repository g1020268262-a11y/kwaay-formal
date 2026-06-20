#!/usr/bin/env bash
set -euo pipefail

echo "[baseline] 正在运行原始 K-Waay core baseline..."
proverif ../../kwaay-core-public-channel.pv | tee results/baseline.out

echo "[aead] 正在运行 AEAD confirmation 变体..."
proverif kwaay-core-public-channel-aead.pv | tee results/aead.out

echo "完成。输出结果保存在 results/ 目录。"
