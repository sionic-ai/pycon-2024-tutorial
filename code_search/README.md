## 시작하기 위한 커맨드 모음

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup component add rust-analyzer

export QDRANT_URL="http://localhost:6333"
bash tools/download_and_index.sh

cd frontend
pnpm i
pnpm build
```