# nand2tetris

NANDゲートから始めて、完全に動作するコンピュータシステムを構築する教育プロジェクト。

📖 [公式サイト](https://www.nand2tetris.org/) | 📘 書籍: "The Elements of Computing Systems"

## コース構成

| Chapter | 内容 |
|---------|------|
| 01-03 | 論理ゲート、ALU、メモリ（HDL） |
| 04-05 | 機械語、CPUアーキテクチャ |
| 06 | アセンブラ（Python） |
| 07-08 | VMトランスレータ（Python） |
| 10-11 | Jackコンパイラ（Python） |
| 12 | オペレーティングシステム（Jack） |

## 技術スタック

- **パッケージ管理**: [uv](https://docs.astral.sh/uv/) - Rustで書かれた高速なPythonパッケージマネージャー
- **ビルドツール**: Hatch
- **リンター**: Ruff
- **テスト**: pytest
- **型チェック**: mypy


## 環境構築

```bash
# uvを使用（推奨）
uv sync
```

## Python実装の使い方

### アセンブラ（Chapter 06）

`.asm` ファイルを `.hack` バイナリに変換します。

```bash
# 入力: 06/asm/Add.asm
# 出力: 06/outputs/Add.hack
python 06/src06/assembler.py -f Add.asm
```

**ファイル構成**:
- `06/asm/` - 入力アセンブリファイル
- `06/outputs/` - 出力バイナリファイル
- `06/answer/` - 正解ファイル（検証用）

### VMトランスレータ（Chapter 07-08）

VMコードをアセンブリに変換します。

```bash
# 入力: 08/vm/FunctionCalls/FibonacciElement/*.vm
# 出力: 08/vm/FunctionCalls/FibonacciElement/FibonacciElement.asm
python 08/src08/vmtranslator.py -d FunctionCalls -f FibonacciElement
```

**オプション**:
- `-d, --dir` - vm/配下のディレクトリ名
- `-f, --file` - ディレクトリ内のプロジェクト名

**ファイル構成**:
- `07/src07/` - Part 1（算術・メモリアクセス）
- `08/src08/` - Part 2（プログラムフロー・関数呼び出し）

### Jackコンパイラ（Chapter 10-11）

Jack言語をVMコードにコンパイルします。

```bash
# 入力: 11/jack/Square/*.jack
# 出力: 11/jack/Square/*Test.xml
python 11/src11/jackanalyzer.py -d Square
```

**オプション**:
- `-d, --dir` - jack/配下のディレクトリ名

**ファイル構成**:
- `10/src10/` - 構文解析（トークナイザ、パーサ）
- `11/src11/` - コード生成（シンボルテーブル、VMライター）

## 開発

```bash
# テスト実行
uv run pytest

# リンター
uv run ruff check .
```
