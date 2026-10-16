# PitchViz 作業手順書:全体の流れとフォルダ構成

> 保存先の想定:`~/projects/pitchviz/docs/00_overview.md`
> 各フェーズの詳細は、このあと `docs/phase1_setup.md` などの形で出します。

## 0. 前提として置いた仮定

- Apple Silicon かどうか、Git・Homebrew の有無はフェーズ1の冒頭で確認コマンドを実行して確かめます。
- 学習時間は 8時間 × 5日 = 約40時間とし、1フェーズを半日〜1.5日の目安で配分します。
- Python 3.13.3 と statsbombpy / mplsoccer / pandas / matplotlib の対応状況は、フェーズ1で PyPI と公式ドキュメントを確認します。問題があれば Python 3.12 に切り替える代替案(Homebrew または pyenv)を用意します。
- 日本代表の収録状況とチーム名の正確な表記は、フェーズ2で statsbombpy を使って確認します。この手順書では推測で書きません。
- 技術スタックは変更案なしで、依頼どおり Python / statsbombpy / mplsoccer / matplotlib / pandas / VS Code(Jupyter拡張)を使います。

## 1. フェーズ一覧と時間配分

| # | フェーズ | 目標 | 所要時間 | 保存先ファイル | 終了時の「動くもの」 |
|---|---|---|---|---|---|
| 1 | 環境構築 | Git / Homebrew / venv / ライブラリを整え、GitHub に接続して初回コミット | 約7時間 | `docs/phase1_setup.md` | 空のピッチが表示される |
| 2 | データ取得と構造の理解 | 日本代表の試合を探し、イベントデータの構造を理解する | 約8時間 | `docs/phase2_data.md` | 試合の events を DataFrame で絞り込める |
| 3 | パスマップ | チームごとのパスマップをピッチ上に描画する | 約9時間 | `docs/phase3_passmap.md` | `outputs/` にパスマップ PNG が保存される |
| 4 | ショットマップ | xG をマーカーの大きさに反映したショットマップを描く | 約6時間 | `docs/phase4_shotmap.md` | `outputs/` にショットマップ PNG が保存される |
| 5 | 関数化と画像保存 | 試合と選手/チームを指定すると PNG を保存する関数にまとめる | 約5時間 | `docs/phase5_function.md` | 1行の関数呼び出しで画像が保存される |
| 6 | README と公開 | README とクレジットを書き、GitHub に push して公開する | 約5時間 | `docs/phase6_publish.md` | GitHub 上で公開された完成形 |
| | 合計 | | 約40時間 | | |

### 日割りの目安

| 日 | 内容 |
|---|---|
| 1日目 | フェーズ1(7h)+ 振り返り(1h) |
| 2日目 | フェーズ2(8h) |
| 3日目 | フェーズ3(8h) |
| 4日目 | フェーズ3の残り(1h)+ フェーズ4(6h)+ 予備(1h) |
| 5日目 | フェーズ5(5h)+ フェーズ6(3h) |
| 予備 | フェーズ6の残り(2h)と、つまずき対応の余裕 |

### 各フェーズに共通する構成

- 目標と所要時間
- 作業手順(ラベル付き)
  - **[Terminal]**:ターミナルでの作業
  - **[VS Code]**:VS Code での作業
  - **[Browser]**:ブラウザでの作業
- コードの解説
- 穴埋め課題(答えは `<details>` で折りたたみ)
- 完了チェック
- つまずきと対処(エラー文の例つき)
- Claude / ChatGPT への質問のコツ
- 終了時のディレクトリツリー(NEW / MOD つき)
- `git status` → `git add` → `git commit`

### 各フェーズで必ず入れる確認事項

- **フェーズ1**:Apple Silicon 確認、Git / Homebrew の確認とインストール(Homebrew は公式サイトで最新コマンドを確認)、GitHub 接続(初学者向けに HTTPS + 認証を第一案、SSH は補足)、各ライブラリの対応 Python バージョン確認、非対応時の Python 3.12 代替案
- **フェーズ2**:competitions → matches の順に絞る手順、日本代表(男子・女子)の収録確認、チーム名表記の実データ確認、見つからない場合は他チームの試合で先に進める代替案、StatsBomb Open Data の利用条件(クレジット表記)の確認
- **フェーズ6**:README へのクレジット記載、GitHub 公開

## 2. プロジェクト全体のフォルダ構成(完成形)

**置き場所**:`~/projects/pitchviz`

```
~/projects/pitchviz/
├── .git/                      # Git の管理情報(git init で自動生成。触らない)
├── .gitignore                 # Git に含めないもの(.venv、キャッシュ等)を列挙
├── .venv/                     # 仮想環境(Pythonとライブラリの隔離環境。Git管理外)
├── README.md                  # プロジェクトの説明・使い方・クレジット(GitHubの表紙)
├── requirements.txt           # 必要ライブラリの一覧(再現用)
├── pyproject.toml             # パッケージ設定(フェーズ5で追加。notebooksからimportするため)
├── docs/                      # 作業手順書の置き場(この手順書を保存する)
│   ├── 00_overview.md         # 全体の流れとフォルダ構成(このファイル)
│   ├── phase1_setup.md        # フェーズ1の手順書
│   ├── phase2_data.md         # フェーズ2の手順書
│   ├── phase3_passmap.md      # フェーズ3の手順書
│   ├── phase4_shotmap.md      # フェーズ4の手順書
│   ├── phase5_function.md     # フェーズ5の手順書
│   └── phase6_publish.md      # フェーズ6の手順書
├── notebooks/                 # 試しながら書く Jupyter Notebook の置き場
│   ├── 01_setup_check.ipynb   # フェーズ1:環境の動作確認(空のピッチ表示)
│   ├── 02_explore_data.ipynb  # フェーズ2:大会・試合・イベントの調査
│   ├── 03_pass_map.ipynb      # フェーズ3:パスマップの試作
│   ├── 04_shot_map.ipynb      # フェーズ4:ショットマップの試作
│   └── 05_use_function.ipynb  # フェーズ5:完成した関数の呼び出し確認
├── src/
│   └── pitchviz/              # 完成したコードをまとめる Python パッケージ
│       ├── __init__.py        # パッケージの目印(使う関数をここから公開)
│       ├── loader.py          # StatsBomb データの取得・絞り込み関数
│       ├── pass_map.py        # パスマップ描画関数
│       ├── shot_map.py        # ショットマップ描画関数
│       └── api.py             # 「試合と選手/チームを指定→PNG保存」する入口の関数
├── outputs/                   # 生成した画像(PNG)の保存先
│   └── .gitkeep               # 空フォルダをGitに残すための目印ファイル
└── data/                      # 一時データ・キャッシュ(Git管理外)
```

### 補足

- `.git/`、`.venv/`、`data/` は `.gitignore` に書き、Git に含めません(手順はフェーズ1で説明)。
- `outputs/` の画像は、サンプル数枚だけ README 用に Git へ含める方針です。判断はフェーズ6で説明します。
- `src/pitchviz/` の各ファイルは、フェーズ3〜5で「ノートブックで試す → 動いたら .py に移す」の順に作ります。最初から全部は作りません。
- `LICENSE`(ライセンスファイル)は、フェーズ6で公開時に追加するか判断します。

### どのフェーズで何が増えるか

| フェーズ | 追加されるもの |
|---|---|
| 1 | `.gitignore`、`requirements.txt`、`README.md`(仮)、`notebooks/01_...`、`outputs/.gitkeep`、`docs/00_overview.md`、`docs/phase1_setup.md` |
| 2 | `notebooks/02_...`、`src/pitchviz/loader.py`(最小版)、`docs/phase2_data.md` |
| 3 | `notebooks/03_...`、`src/pitchviz/pass_map.py`、`docs/phase3_passmap.md`、`outputs/` に PNG |
| 4 | `notebooks/04_...`、`src/pitchviz/shot_map.py`、`docs/phase4_shotmap.md`、`outputs/` に PNG |
| 5 | `src/pitchviz/api.py`、`__init__.py`、`pyproject.toml`、`notebooks/05_...`、`docs/phase5_function.md` |
| 6 | `README.md`(完成版)、`docs/phase6_publish.md`、(任意)`LICENSE` |

---

準備ができたら「フェーズ1をお願いします」と指示してください。
