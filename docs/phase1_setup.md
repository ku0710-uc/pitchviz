# フェーズ1:環境構築

> 保存先:`~/projects/pitchviz/docs/phase1_setup.md`
> このフェーズの終わりには「空のサッカーピッチが表示され、GitHub に初回 push できている」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | Git / Homebrew / venv / ライブラリを整え、空のピッチを描画し、GitHub に接続して初回コミットを push する |
| 想定所要時間 | 約7時間(下の内訳を参照) |
| 終了時の「動くもの」 | Jupyter Notebook で空のピッチが表示され、`outputs/` に PNG が保存できる |

### 作業ラベルの見方

- **[Terminal]**:ターミナル(macOS 標準の「ターミナル」アプリ)での作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 今の環境を確認する(Mac / Python / Git / Homebrew) | 0.75h |
| 2 | Homebrew・Git・GitHub CLI を入れる | 1.0h |
| 3 | GitHub に接続する(HTTPS + 認証) | 0.75h |
| 4 | プロジェクトフォルダ・Git 初期化・.gitignore | 0.75h |
| 5 | 仮想環境(venv)とライブラリの導入、対応状況の確認 | 1.25h |
| 6 | VS Code と Jupyter で空のピッチを描く | 1.5h |
| 7 | コミットして GitHub へ push | 0.5h |
| 8 | 振り返り | 0.5h |
| | 合計 | 7.0h |

---

## A. 先に全体像をつかむ

### A-1. プロジェクト全体のフォルダ構成(完成形)

**置き場所**:`~/projects/pitchviz`(`~` はあなたのホームフォルダ。例:`/Users/あなたのユーザー名`)

```
~/projects/pitchviz/
├── .git/                      # Git の管理情報(git init で自動生成。触らない)
├── .gitignore                 # Git に含めないもの(.venv、キャッシュ等)を列挙
├── .venv/                     # 仮想環境(Pythonとライブラリの隔離環境。Git管理外)
├── README.md                  # プロジェクトの説明・使い方・クレジット(GitHubの表紙)
├── requirements.txt           # 必要ライブラリの一覧(再現用)
├── pyproject.toml             # パッケージ設定(フェーズ5で追加)
├── docs/                      # 作業手順書の置き場
│   ├── 00_overview.md         # 全体の流れとフォルダ構成
│   ├── phase1_setup.md        # フェーズ1の手順書(このファイル)
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

### A-2. このフェーズで作るもの

完成形のうち、このフェーズで作るのは次の部分だけです。残りは後のフェーズで増えます。

- `.git/`、`.gitignore`、`.venv/`、`README.md`(仮)、`requirements.txt`
- `docs/`(この手順書と `00_overview.md` を保存)
- `notebooks/01_setup_check.ipynb`
- `outputs/.gitkeep`、空の `src/pitchviz/`、`data/`

### A-3. 進め方のルール

- コマンドは、**どのフォルダで実行するか**を毎回書きます。迷ったら `pwd` と打つと、今いるフォルダが表示されます。
- 期待される出力は例です。バージョン番号や日付、ユーザー名はあなたの環境で違って構いません。
- 手順はチェックボックスで進捗を管理します。

---

## 手順1:今の環境を確認する

**所要時間:約0.75時間**

まず、Mac・Python・Git・Homebrew の状態を確認します。ここでは「何も変更しない」コマンドだけを使います。

### 1-1. ターミナルを開く

- [ ] **[Terminal]** Spotlight(`Command + Space`)で「ターミナル」と入力して Enter。
  - 以降のコマンドは、ここに貼り付けて Enter で実行します。
  - 開いた直後は、ホームフォルダ(`~`)にいます。

### 1-2. macOS のバージョンを確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
sw_vers
```

期待される出力の例:

```
ProductName:		macOS
ProductVersion:		15.x
BuildVersion:		xxxxxxx
```

- `ProductVersion` を控えておいてください。
- **Homebrew は、macOS Sequoia 15 以降が公式サポート対象です**(2026年10月時点の公式サイト [brew.sh](https://brew.sh) の記載)。これより古い場合は、手順2-1 の注意書きを読んでください。

### 1-3. Apple Silicon かどうかを確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
uname -m
```

期待される出力:

| 表示 | 意味 |
|---|---|
| `arm64` | Apple Silicon(M1 / M2 / M3 / M4 など)。以降の手順書はこれを前提に書いています |
| `x86_64` | Intel Mac(またはターミナルが Rosetta 上で動作中) |

もう1つ、チップ名も確認します。

```bash
sysctl -n machdep.cpu.brand_string
```

期待される出力の例:

```
Apple M2
```

- Intel Mac の場合は、Homebrew のインストール先が `/usr/local` になります(Apple Silicon は `/opt/homebrew`)。以降の手順で `/opt/homebrew/...` と書かれた部分は、`/usr/local/...` に読み替えてください。
- チップ名に「Apple」と出るのに `x86_64` になる場合は、ターミナルが Rosetta で起動している可能性があります。この場合は Claude / ChatGPT に相談してください(質問のコツは手順9)。

### 1-4. Python を確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
python3 --version
which python3
```

期待される出力の例:

```
Python 3.13.3
/usr/local/bin/python3
```

- `which python3` の場所は、環境によって違います(`/usr/local/bin/python3`、`/opt/homebrew/bin/python3`、`/usr/bin/python3` など)。どれでも構いません。
- `Python 3.13.3` と出れば、あなたの状況の前提どおりです。

### 1-5. Git を確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
git --version
```

結果は2パターンあります。

**パターンA:すでに入っている**

```
git version 2.xx.x (Apple Git-xxx)
```

**パターンB:入っていない**(ダイアログが出る、またはエラーになる)

```
xcode-select: note: No developer tools were found, requesting install.
If developer tools are located at a non-standard location, you can use
`xcode-select --switch` to specify the location.
```

- パターンBでは「コマンドラインデベロッパツールをインストールしますか?」というダイアログが出ることがあります。**ここでは「後で」または「キャンセル」で構いません**。手順2で Homebrew を入れるときに、同じツールが一緒に導入されます。

### 1-6. Homebrew を確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
brew --version
```

**入っていない場合の出力:**

```
zsh: command not found: brew
```

**入っている場合の出力の例:**

```
Homebrew 5.x.x
```

- 入っていなければ手順2へ進みます。すでに入っている場合は、手順2-1 を飛ばして 2-2 から進めます。

### 1-7. VS Code の拡張機能を確認する

- [ ] **[VS Code]** VS Code を開き、左端のアイコン列の四角が4つ並んだアイコン(Extensions)をクリック(`Command + Shift + X`)。
- [ ] 検索欄に `Python` と入力し、Microsoft 提供の **Python** がインストール済みか確認する(なければ Install)。
- [ ] 検索欄に `Jupyter` と入力し、Microsoft 提供の **Jupyter** がインストール済みか確認する(なければ Install)。

### 1-8. 確認結果をメモする

次のメモを、手元(紙でも VS Code の新規タブでも可)に書いておきます。後でエラー相談をするときに役立ちます。

```
macOS:        (例) 15.x
チップ:       (例) arm64 / Apple M2
Python:       (例) 3.13.3
Git:          (例) 入っている / 入っていない
Homebrew:     (例) 入っている / 入っていない
```

### 手順1の完了チェック

- [ ] `sw_vers` と `uname -m` の結果を控えた
- [ ] `python3 --version` で `Python 3.13.3` を確認した
- [ ] Git と Homebrew の有無がわかった
- [ ] VS Code に Python 拡張と Jupyter 拡張が入っている

---

## 手順2:Homebrew・Git・GitHub CLI を入れる

**所要時間:約1時間**

**この手順の目的**

- Homebrew:Mac にソフトを入れる道具(パッケージマネージャ)。あとで Python 3.12 が必要になった場合にも使います。
- Git:ファイルの変更履歴を記録する道具。
- GitHub CLI(`gh`):ローカルから GitHub に安全にログインするための道具。初学者にはこれが一番簡単です。

### 2-1. Homebrew を入れる(未インストールの場合のみ)

> **注意**:Homebrew のインストールコマンドは更新されることがあります。**必ず [Homebrew 公式サイト](https://brew.sh) を開き、そこに表示されているコマンドを使ってください**。以下は 2026年10月9日時点の公式サイトの表示です。
>
> macOS が Sequoia 15 より古い場合は、公式サポート対象外です。その場合は Homebrew を使わず、Git は手順1-5 のダイアログ(Xcode コマンドラインツール)で入れ、GitHub CLI は [公式サイト](https://cli.github.com)のインストーラを使う方法があります。迷ったら、手順1-8 のメモを添えて Claude / ChatGPT に相談してください。

- [ ] **[Browser]** `https://brew.sh` を開き、「Install Homebrew」のコマンドが下と同じか確認する。
- [ ] **[Terminal]** どのフォルダでも実行できます。公式サイトのコマンドをコピーして貼り付けます。

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- 実行すると、スクリプトが「何をするか」を表示して一時停止します。内容を読み、`Press RETURN/ENTER to continue or any other key to abort:` と出たら Enter を押します。
- Mac のログインパスワードを聞かれます。入力しても画面には何も表示されませんが、正常です。そのまま入力して Enter を押します。
- 「コマンドラインデベロッパツール」のインストールが始まった場合は、完了まで数分〜十数分待ちます。

期待される出力(最後のほう)の例:

```
==> Installation successful!
...
==> Next steps:
- Run these commands in your terminal to add Homebrew to your PATH:
    echo >> /Users/あなたのユーザー名/.zprofile
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/あなたのユーザー名/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2-2. Homebrew を使えるようにする(PATH の設定)

- [ ] **[Terminal]** インストーラの最後に表示された「Next steps」の3行を、**表示されたとおりに**コピーして実行する。
  - 上の例は、あなたの画面の表示と文字が少し違う場合があります。**必ず画面に出たものを使ってください**。
  - これは「ターミナルを開くたびに `brew` が使えるようにする」設定です。

- [ ] **[Terminal]** 設定できたか確認する。どのフォルダでも実行できます。

```bash
brew --version
which brew
```

期待される出力の例:

```
Homebrew 5.x.x
/opt/homebrew/bin/brew
```

### 2-3. Git を入れる(または確認する)

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
brew install git
```

期待される出力の例(最後のほう):

```
==> Pouring git--2.xx.x.arm64_sequoia.bottle.tar.gz
🍺  /opt/homebrew/Cellar/git/2.xx.x: xxx files, xx.xMB
```

- すでに Git が入っている場合は「already installed」と出ます。それで問題ありません。

- [ ] **[Terminal]** 確認する。

```bash
git --version
which git
```

期待される出力の例:

```
git version 2.xx.x
/opt/homebrew/bin/git
```

- `which git` が `/usr/bin/git` のままでも、Git として動けば問題ありません。

### 2-4. GitHub CLI(gh)を入れる

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
brew install gh
gh --version
```

期待される出力の例:

```
gh version 2.xx.x (20xx-xx-xx)
https://github.com/cli/cli/releases/tag/v2.xx.x
```

### 2-5. Git に自分の名前とメールを登録する

コミット(変更の記録)に、あなたの名前が付くようにします。

- [ ] **[Browser]** GitHub の `Settings → Emails` を開き、**「Keep my email addresses private」** の下にある noreply メールアドレス(`数字+ユーザー名@users.noreply.github.com` の形)を控える。
  - 本物のメールアドレスを公開したくない場合は、これを使うのが安全です。

- [ ] **[Terminal]** どのフォルダでも実行できます。`<...>` はあなたの内容に置き換えます。

```bash
git config --global user.name "<あなたの名前またはGitHubユーザー名>"
git config --global user.email "<noreplyメール、またはGitHubに登録したメール>"
git config --global init.defaultBranch main
```

- [ ] **[Terminal]** 設定を確認する。

```bash
git config --global --list
```

期待される出力の例(一部):

```
user.name=yourname
user.email=12345678+yourname@users.noreply.github.com
init.defaultbranch=main
```

### 手順2の完了チェック

- [ ] `brew --version` でバージョンが表示される
- [ ] `git --version` でバージョンが表示される
- [ ] `gh --version` でバージョンが表示される
- [ ] `git config --global --list` に `user.name` / `user.email` / `init.defaultbranch=main` がある

---

## 手順3:GitHub に接続する(HTTPS + 認証)

**所要時間:約0.75時間**

初学者向けには **HTTPS + GitHub CLI での認証** が一番簡単です(SSH鍵の作成・登録が不要なため)。この手順書ではこれを使います。SSH は補足で触れます。

### 3-1. GitHub CLI でログインする

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
gh auth login
```

質問が順に出るので、次のように選びます(矢印キーで選び、Enter で決定)。

| 質問(英語) | 選ぶもの |
|---|---|
| Where do you use GitHub? | `GitHub.com` |
| What is your preferred protocol for Git operations on this host? | `HTTPS` |
| Authenticate Git with your GitHub credentials? | `Y`(はい) |
| How would you like to authenticate GitHub CLI? | `Login with a web browser` |

- 続いて、8文字のワンタイムコード(例:`ABCD-1234`)が表示されます。
- [ ] **[Terminal]** コードをコピーしてから、Enter キーを押す。ブラウザが開きます。
- [ ] **[Browser]** 開いたページにコードを貼り付け、GitHub にログインして「Authorize」を押す。

期待される出力:

```
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as あなたのユーザー名
```

### 3-2. ログイン状態を確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
gh auth status
```

期待される出力の例:

```
github.com
  ✓ Logged in to github.com account yourname (keyring)
  - Active account: true
  - Git operations protocol: https
```

### 3-3. Git と GitHub の連携を確認する

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
gh auth setup-git
```

- 何も表示されなくて正常です。これで、`git push` のときに自動でログイン情報が使われます。
- 手順3-1 で「Authenticate Git with your GitHub credentials? → Y」を選んでいれば、すでに設定済みの場合もあります。そのときも実行して問題ありません。

### 補足:SSH を使いたい場合(任意。今回は使わなくてよい)

- SSH は「鍵のペアを作り、公開鍵を GitHub に登録する」方式です。手順は [GitHub Docs「SSH キーの生成」](https://docs.github.com/ja/authentication/connecting-to-github-with-ssh)に従ってください。
- 今回は HTTPS + `gh` で進めるので、SSH は設定しなくて構いません。

### 手順3の完了チェック

- [ ] `gh auth status` に `Logged in to github.com account あなたのユーザー名` と出る
- [ ] `Git operations protocol: https` と出る

---

## 手順4:プロジェクトフォルダを作り、Git を初期化する

**所要時間:約0.75時間**

### 4-1. プロジェクトフォルダを作る

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
mkdir -p ~/projects/pitchviz
cd ~/projects/pitchviz
pwd
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
```

- `mkdir -p` は「途中のフォルダ(`projects`)がなくても、まとめて作る」という意味です。
- `cd` は「そのフォルダに移動する」コマンドです。
- **これ以降、特に指定がなければ、ターミナルのコマンドは `~/projects/pitchviz` で実行します。**

### 4-2. サブフォルダを作る

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
mkdir -p docs notebooks src/pitchviz outputs data
touch outputs/.gitkeep
ls -a
```

期待される出力の例:

```
.          ..         data       docs       notebooks  outputs    src
```

- `.gitkeep` は、空のフォルダを Git に残すための目印ファイルです(Git は空のフォルダを記録しないため)。
- `ls -a` の `-a` は、`.` で始まる隠しファイルも表示するオプションです。

### 4-3. Git を初期化する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git init
git status
```

期待される出力の例:

```
Initialized empty Git repository in /Users/あなたのユーザー名/projects/pitchviz/.git/
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	outputs/

nothing added to commit but untracked files present (use "git add" to track)
```

- `On branch main` と出ればOKです(`master` と出る場合は、手順2-5 の `init.defaultBranch` 設定が反映されていません。その場合は `git branch -M main` を実行してください)。

### 4-4. VS Code でプロジェクトフォルダを開く

- [ ] **[VS Code]** メニューの `File → Open Folder...` を選び、`ホーム → projects → pitchviz` を選んで「Open」。
  - 「Do you trust the authors of the files in this folder?」と出たら `Yes, I trust the authors` を選びます。
- [ ] **[VS Code]** 左サイドバーの Explorer(`Command + Shift + E`)に `PITCHVIZ` というフォルダ名が出て、`data` `docs` `notebooks` `outputs` `src` が見えることを確認する。

> **おすすめ**:ターミナルから VS Code を開けるようにしておくと便利です。VS Code で `Command + Shift + P` → `Shell Command: Install 'code' command in PATH` を選ぶと、以降は `~/projects/pitchviz` で `code .` と打つだけで開けます。

### 4-5. VS Code の内蔵ターミナルを開く(以降はこちらを使ってもよい)

- [ ] **[VS Code]** メニューの `Terminal → New Terminal`(またはキーボードで `Control + バッククォート`)。
  - 画面下部にターミナルが開き、**すでに `~/projects/pitchviz` にいる**状態になります。
  - これ以降の **[Terminal]** は、macOS のターミナルでも VS Code 内蔵ターミナルでも、どちらで実行しても構いません。

### 4-6. `.gitignore` を作る

`.gitignore` は「Git に記録しないものの一覧」です。

- [ ] **[VS Code]** 左サイドバーの Explorer で、空いている場所(フォルダ名 `PITCHVIZ` の行)を右クリック → `New File` → `.gitignore` と入力して Enter。
  - **対象**:`.gitignore`(プロジェクトルート直下)
  - **新規作成か編集か**:新規作成
- [ ] 開いたエディタに、次の内容をすべて貼り付けて `Command + S` で保存する。

```gitignore
# .gitignore

# --- 仮想環境(自分のMacの中だけで使うもの) ---
.venv/

# --- Python が自動で作るキャッシュ ---
__pycache__/
*.pyc

# --- Jupyter が自動で作る一時ファイル ---
.ipynb_checkpoints/

# --- macOS が自動で作るファイル ---
.DS_Store

# --- 一時データ・キャッシュ置き場 ---
data/

# --- 秘密情報(今回は使わないが、事故防止のため) ---
.env

# --- VS Code の個人設定 ---
.vscode/

# --- 生成画像は、.gitkeep 以外は Git に含めない ---
# (README 用のサンプル画像をGitに含める判断は、フェーズ6で行います)
outputs/*
!outputs/.gitkeep
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `.venv/` | 仮想環境フォルダ全体を除外。ライブラリ本体は数百MBになることもあり、Git に入れるものではない |
| `__pycache__/`、`*.pyc` | Python が実行時に自動で作るキャッシュ |
| `.ipynb_checkpoints/` | Jupyter が自動保存する一時ファイル |
| `.DS_Store` | macOS がフォルダ表示設定を記録する隠しファイル |
| `data/` | 今後ダウンロードした一時データを置く場所 |
| `.env` | パスワードや API キーを置く習慣のあるファイル。万一に備えて除外 |
| `outputs/*` と `!outputs/.gitkeep` | `outputs/` の中身は無視するが、`.gitkeep` だけは例外として記録する(`!` は「除外しない」の意味) |

### 4-7. README.md(仮)を作る

- [ ] **[VS Code]** Explorer の `PITCHVIZ` の行を右クリック → `New File` → `README.md` と入力して Enter。
  - **対象**:`README.md`(プロジェクトルート直下)
  - **新規作成か編集か**:新規作成(フェーズ6で書き直します)
- [ ] 次の内容を貼り付けて保存する。

```markdown
<!-- README.md -->
# PitchViz

StatsBomb のオープンデータを使い、サッカーのパスマップとショットマップを描画するツール(作成中)。

## 進捗

- [x] フェーズ1:環境構築
```

### 4-8. この資料を docs/ に保存する

- [ ] **[VS Code]** この手順書(`phase1_setup.md`)と、前回の `00_overview.md` を、`docs/` フォルダに保存する。
  - 方法1:Finder からファイルを `docs` フォルダへドラッグ&ドロップする(VS Code の Explorer の `docs` にドロップしても可)。
  - 方法2:VS Code の Explorer で `docs` を右クリック → `New File` → `phase1_setup.md` と入力し、内容を貼り付ける。

### 手順4の完了チェック

- [ ] `pwd` で `/Users/あなたのユーザー名/projects/pitchviz` と表示される
- [ ] `git status` で `On branch main` と表示される
- [ ] Explorer に `.gitignore`、`README.md`、`docs/`、`notebooks/`、`outputs/`、`src/`、`data/` が見える
- [ ] `docs/` に `00_overview.md` と `phase1_setup.md` がある

---

## 手順5:仮想環境(venv)を作り、ライブラリを入れる

**所要時間:約1.25時間**

### 5-0. 仮想環境とは

- 仮想環境(venv)は、「このプロジェクト専用の Python とライブラリの置き場」です。
- ほかのプロジェクトや Mac 本体の Python に影響を与えず、バージョンの食い違いも起きにくくなります。
- 有効化(activate)すると、ターミナルの行頭に `(.venv)` と表示されます。

### 5-1. StatsBomb の利用条件に目を通す(必須の確認)

データを使う前に、利用条件を確認します。

- [ ] **[Browser]** `https://github.com/statsbomb/open-data` を開き、README と、そこからリンクされている利用規約(User Agreement / LICENSE)を読む。
  - **確認すること**:クレジット表記(出典の書き方)の指定、公開・共有時の条件。
  - 手順6の README で出典をどう書くかは、フェーズ6でもう一度確認します。ここでは「条件がある」ことを知っておけば十分です。

### 5-2. 仮想環境を作る

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
python3 -m venv .venv
```

- 数秒〜十数秒かかります。成功しても何も表示されません。

- [ ] **[Terminal]** `~/projects/pitchviz` で、フォルダができたか確認する。

```bash
ls -a
```

期待される出力の例(`.venv` が増えている):

```
.          .git       .venv      README.md  docs       outputs
..         .gitignore  data       notebooks  src
```

### 5-3. 仮想環境を有効化する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
source .venv/bin/activate
```

期待される出力(行頭が変わる):

```
(.venv) あなたのユーザー名@Mac pitchviz %
```

- [ ] **[Terminal]** 正しい Python が使われているか確認する。

```bash
python --version
which python
```

期待される出力の例:

```
Python 3.13.3
/Users/あなたのユーザー名/projects/pitchviz/.venv/bin/python
```

- `which python` が `.../pitchviz/.venv/bin/python` で終わっていれば成功です。
- **新しいターミナルを開くたびに、`source .venv/bin/activate` をもう一度実行する必要があります**(VS Code の内蔵ターミナルは、Python 拡張が自動で有効化してくれることが多いです)。

### 5-4. pip を新しくする

- [ ] **[Terminal]** `~/projects/pitchviz` で、仮想環境を有効化した状態で実行。

```bash
python -m pip install --upgrade pip
```

期待される出力の例(最後のほう):

```
Successfully installed pip-xx.x.x
```

- すでに最新なら `Requirement already satisfied: pip in ...` と出ます。

### 5-5. 【重要】Python 3.13.3 でライブラリが使えるか確認する

使うライブラリが Python 3.13 に対応しているかは、バージョンによって変わります。**次の2段階で確認します**。

**確認の考え方**

1. 公式のページで「対応 Python」を見る。
2. 実際に「インストールだけ試す(dry-run)」して、エラーが出ないか見る。

**(1)公式ページで確認する**

- [ ] **[Browser]** 次のページを開き、「Requires: Python >=…」(左側のメタデータ欄)や「Classifiers」の `Programming Language :: Python :: 3.13` の有無を確認する。

| ライブラリ | 確認先 |
|---|---|
| statsbombpy | PyPI `https://pypi.org/project/statsbombpy/` と GitHub `https://github.com/statsbomb/statsbombpy` |
| mplsoccer | PyPI `https://pypi.org/project/mplsoccer/` と公式ドキュメント `https://mplsoccer.readthedocs.io` |
| matplotlib | 公式ドキュメント「Installation」`https://matplotlib.org/stable/` |
| pandas | 公式ドキュメント「Installation」`https://pandas.pydata.org/docs/` |
| ipykernel | PyPI `https://pypi.org/project/ipykernel/` |

- 「3.13 の記載が見つからない」場合でも、必ずしも使えないわけではありません(Classifiers は更新が遅れることがあります)。**次の(2)の実際のテストが最終判断**です。

**(2)インストールの予行演習(dry-run)をする**

- [ ] **[Terminal]** `~/projects/pitchviz` で、仮想環境を有効化した状態で実行。

```bash
pip install --dry-run statsbombpy mplsoccer matplotlib pandas ipykernel
```

- `--dry-run` は「実際には入れず、入れられるかだけ確認する」オプションです。

**成功した場合の出力(最後のほう)**

```
Would install ... matplotlib-x.x.x ... mplsoccer-x.x.x ... pandas-x.x.x ... statsbombpy-x.x.x ...
```

- 成功 → 手順5-6 へ進みます。

**失敗した場合の出力の例**

```
ERROR: Could not find a version that satisfies the requirement ...
ERROR: No matching distribution found for ...
```

または

```
ERROR: Ignored the following versions that require a different python version: ...
```

- 失敗 → **手順5-9(Python 3.12 に切り替える代替案)** へ進みます。

### 5-6. ライブラリを入れる

- [ ] **[Terminal]** `~/projects/pitchviz` で、仮想環境を有効化した状態で実行。

```bash
pip install statsbombpy mplsoccer matplotlib pandas ipykernel
```

- 数十秒〜数分かかります。たくさんの文字が流れます。
- `ipykernel` は、VS Code の Jupyter が仮想環境の Python を使うために必要です。

期待される出力(最後のほう)の例:

```
Successfully installed ... matplotlib-x.x.x ... mplsoccer-x.x.x ... pandas-x.x.x ... statsbombpy-x.x.x ...
```

- 途中で `WARNING:` が出ても、最後に `Successfully installed` があれば成功です。
- `ERROR:` で終わった場合は、「つまずきと対処」(手順9)を見てください。

### 5-7. 入ったバージョンを確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pip list
```

期待される出力の例(一部):

```
Package         Version
--------------- -------
ipykernel       x.x.x
matplotlib      x.x.x
mplsoccer       x.x.x
pandas          x.x.x
statsbombpy     x.x.x
```

- 実際の一覧にはもっと多くのパッケージが並びます(これらが依存するパッケージです)。

### 5-8. `requirements.txt` を作る

`requirements.txt` は、「このプロジェクトで入れたライブラリの名簿」です。ほかの人(や未来の自分)が同じ環境を作り直すときに使います。

- [ ] **[Terminal]** `~/projects/pitchviz` で、仮想環境を有効化した状態で実行。

```bash
pip freeze > requirements.txt
```

- [ ] **[VS Code]** Explorer で `requirements.txt` をクリックして開き、中身を確認する。

期待される内容の例(一部。実際はもっと長い):

```
matplotlib==x.x.x
mplsoccer==x.x.x
pandas==x.x.x
statsbombpy==x.x.x
...
```

- **ファイル**:`requirements.txt`(プロジェクトルート直下)/新規作成(ターミナルのコマンドで自動生成)
- あとで再現するときは `pip install -r requirements.txt` と打てば、同じ版が入ります。

### 5-9. 【代替案】Python 3.12 に切り替える(5-5 で失敗した場合のみ)

Python 3.13.3 でライブラリが入らない・動かない場合は、**Python 3.12 を追加で入れ、仮想環境を作り直します**。Mac 本体の Python 3.13.3 は消さなくて大丈夫です。

#### 方法A:Homebrew で入れる(おすすめ)

- [ ] **[Terminal]** どのフォルダでも実行できます。

```bash
brew install python@3.12
```

- [ ] **[Terminal]** 入った場所と版を確認する。

```bash
/opt/homebrew/bin/python3.12 --version
```

期待される出力:

```
Python 3.12.x
```

- Intel Mac の場合は `/usr/local/bin/python3.12` を使います。
- 次のとおり、古い仮想環境を消して作り直します。
- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
deactivate
rm -rf .venv
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

期待される出力:

```
Python 3.12.x
```

- `rm -rf .venv` は **`.venv` フォルダだけ**を削除するコマンドです。`~/projects/pitchviz` にいることを `pwd` で確認してから実行してください(`rm -rf` は元に戻せません)。
- そのあと、手順5-4(pip の更新)と手順5-6 以降をもう一度やり直します。

#### 方法B:pyenv で入れる(上級者向け・任意)

- pyenv は、複数の Python を切り替えるツールです。`brew install pyenv` で入れられますが、シェルの設定(`~/.zshrc` への追記)が必要で、初学者には少し難しいです。
- 方法A がうまくいかない場合のみ、[pyenv 公式ドキュメント](https://github.com/pyenv/pyenv)を見ながら進めてください。

### 手順5の完了チェック

- [ ] `(.venv)` が行頭に表示されている
- [ ] `which python` が `.../pitchviz/.venv/bin/python` を指している
- [ ] `pip list` に `statsbombpy` / `mplsoccer` / `matplotlib` / `pandas` / `ipykernel` がある
- [ ] `requirements.txt` ができている
- [ ] (3.12 に切り替えた場合)`python --version` が `Python 3.12.x` になっている

---

## 手順6:VS Code と Jupyter で空のピッチを描く

**所要時間:約1.5時間**

### 6-1. Notebook ファイルを作る

- [ ] **[VS Code]** 左サイドバーの Explorer で `notebooks` フォルダを右クリック → `New File` → `01_setup_check.ipynb` と入力して Enter。
  - **対象**:`notebooks/01_setup_check.ipynb`
  - **新規作成か編集か**:新規作成
  - 拡張子 `.ipynb` で作ると、Jupyter Notebook として開きます。

### 6-2. カーネル(使う Python)を選ぶ

- [ ] **[VS Code]** Notebook の右上にある `Select Kernel` をクリックする。
  - `Python Environments...` を選ぶ。
  - `.venv (Python 3.13.3)`(または `3.12.x`)と書かれた項目を選ぶ。
    - **`Recommended` の印が付いている `.venv` を選んでください**。表示は `Python 3.13.3 (.venv)` のような形です。
  - 選び終わると、右上に `.venv (Python 3.13.3)` のように表示が変わります。

> **カーネル**とは、Notebook のコードを実際に実行するエンジンのことです。**ここで `.venv` を選ばないと、ライブラリが見つからず `ModuleNotFoundError` になります**(手順9を参照)。

### 6-3. セルの使い方

- Notebook は「セル」という箱にコードを書き、1つずつ実行します。
- セルを追加するには、Notebook の上部または各セルの下にある **`+ Code`** をクリックします。
- セルを実行するには、セルの左の ▶ ボタンを押すか、`Shift + Enter` を押します。
- 実行順に、セルの左に `[1]`、`[2]` と番号が付きます。
- **セルは、番号順(上から順)に実行してください。**

### 6-4. セル1:どの Python で動いているか確認する

- [ ] **[VS Code]** 最初のセルに、次を入力して実行する。
  - **対象**:`notebooks/01_setup_check.ipynb` の **セル1**

```python
# notebooks/01_setup_check.ipynb  セル1
import sys

print(sys.version)
print(sys.executable)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `import sys` | Python の基本情報を扱う標準ライブラリ `sys` を読み込む |
| `sys.version` | 今動いている Python のバージョン |
| `sys.executable` | 今動いている Python 本体の場所 |

**期待される出力の例**

```
3.13.3 (main, ...) [Clang ...]
/Users/あなたのユーザー名/projects/pitchviz/.venv/bin/python
```

- 2行目が `.../pitchviz/.venv/bin/python` で終わっていれば成功です。

### 6-5. セル2:ライブラリのバージョンを確認する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/01_setup_check.ipynb` の **セル2**

```python
# notebooks/01_setup_check.ipynb  セル2
from importlib.metadata import version

import matplotlib
import mplsoccer
import pandas as pd
import statsbombpy

for name in ["statsbombpy", "mplsoccer", "matplotlib", "pandas"]:
    print(f"{name:12s} {version(name)}")
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `from importlib.metadata import version` | インストール済みパッケージのバージョンを調べる関数を読み込む |
| `import matplotlib` など | ライブラリが読み込めるかを確認する(エラーが出なければ OK) |
| `import pandas as pd` | `pandas` に `pd` という短い名前を付けて読み込む(慣習) |
| `for name in [...]:` | 4つの名前を順番に取り出して繰り返す |
| `f"{name:12s} {version(name)}"` | 名前を12文字幅にそろえ、そのあとにバージョンを表示する |

**期待される出力の例**

```
statsbombpy  x.x.x
mplsoccer    x.x.x
matplotlib   x.x.x
pandas       x.x.x
```

### 6-6. セル3:空のピッチを描く

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/01_setup_check.ipynb` の **セル3**

```python
# notebooks/01_setup_check.ipynb  セル3
import matplotlib.pyplot as plt
from mplsoccer import Pitch

pitch = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white", stripe=True)
fig, ax = pitch.draw(figsize=(10, 7))
plt.show()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `import matplotlib.pyplot as plt` | グラフを描く機能を `plt` という名前で読み込む |
| `from mplsoccer import Pitch` | mplsoccer から、ピッチを描くためのクラス `Pitch` を読み込む |
| `Pitch(...)` | ピッチの見た目を決める設計図を作る |
| `pitch_type="statsbomb"` | StatsBomb のデータと同じ座標系(横120 × 縦80)を使う設定。後のフェーズで必要 |
| `pitch_color="grass"` | 芝の色にする |
| `line_color="white"` | ラインの色を白にする |
| `stripe=True` | 芝の縞模様を付ける |
| `pitch.draw(figsize=(10, 7))` | 横10 × 縦7 インチの大きさでピッチを描く。`fig`(画像全体)と `ax`(描く場所)を返す |
| `plt.show()` | 描いた図を画面に表示する |

**期待される出力**

- Notebook のセルの下に、緑の縞模様のサッカーピッチ(白いライン、ゴール、ペナルティエリア入り)が表示される。

> **mplsoccer の細かい書き方は変わる可能性があります**。引数の名前でエラーが出た場合は、[mplsoccer 公式ドキュメント](https://mplsoccer.readthedocs.io)の「Pitch」のページを確認してください。

### 6-7. セル4:ピッチを画像として保存する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/01_setup_check.ipynb` の **セル4**

```python
# notebooks/01_setup_check.ipynb  セル4
fig.savefig("../outputs/empty_pitch.png", dpi=150, bbox_inches="tight")
print("saved: ../outputs/empty_pitch.png")
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `fig.savefig(...)` | セル3 で作った `fig`(図全体)を画像ファイルとして保存する |
| `"../outputs/empty_pitch.png"` | 保存先。`..` は「1つ上のフォルダ」。Notebook は `notebooks/` にあるので、`../outputs/` が `~/projects/pitchviz/outputs/` になる |
| `dpi=150` | 解像度。数字が大きいほど細かい画像になる |
| `bbox_inches="tight"` | 図の周りの余白を詰めて保存する |

**期待される出力**

```
saved: ../outputs/empty_pitch.png
```

**生成されるファイル**

- `outputs/empty_pitch.png`(Explorer の `outputs` を開くと見える)

- [ ] **[VS Code]** Explorer で `outputs/empty_pitch.png` をクリックし、緑のピッチ画像が表示されることを確認する。

> **メモ**:`outputs/empty_pitch.png` は、`.gitignore` の `outputs/*` により Git の対象外です。これで正しい動きです(手順7の `git status` に表示されません)。

### 6-8. 保存する

- [ ] **[VS Code]** `Command + S` で Notebook を保存する。

### 6-9. 穴埋め課題

答えを見る前に、自分で考えてみてください。**課題コードは、空欄を埋めるまでエラーになります**(それは正常です)。

#### 課題1:暗い背景のピッチを描いて保存する

- [ ] **[VS Code]** `notebooks/01_setup_check.ipynb` に **セル5** を追加し、次の空欄(`____`)を埋めて実行する。

```python
# notebooks/01_setup_check.ipynb  セル5(課題1)
import matplotlib.pyplot as plt
from mplsoccer import Pitch

pitch = Pitch(pitch_type="____", pitch_color="#1f2a24", line_color="____")
fig, ax = pitch.____(figsize=(10, 7))
fig.____("../outputs/dark_pitch.png", dpi=150, bbox_inches="tight")
plt.show()
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目の `____` | セル3 で使った、StatsBomb のデータと座標が合う設定(6文字の英単語) |
| 2つ目の `____` | 暗い背景で見やすいラインの色(セル3 と同じ色でよい) |
| 3つ目の `____` | セル3 で `pitch.` のあとに書いた、ピッチを描くメソッド名 |
| 4つ目の `____` | セル4 で `fig.` のあとに書いた、画像を保存するメソッド名 |

**期待される結果**

- 暗い緑がかった背景に白いラインのピッチが表示される。
- `outputs/dark_pitch.png` が生成される。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/01_setup_check.ipynb  セル5(課題1)
import matplotlib.pyplot as plt
from mplsoccer import Pitch

pitch = Pitch(pitch_type="statsbomb", pitch_color="#1f2a24", line_color="white")
fig, ax = pitch.draw(figsize=(10, 7))
fig.savefig("../outputs/dark_pitch.png", dpi=150, bbox_inches="tight")
plt.show()
```

**答え合わせのあとに**

- 1つ目:`"statsbomb"`
- 2つ目:`"white"`(明るい色なら他の色でも動く)
- 3つ目:`draw`
- 4つ目:`savefig`

**自分のコードが正解と違っても、動いていればOKな例**

- ラインの色を `"white"` ではなく `"#cccccc"` や `"lightgray"` にした → 動く。見た目の違いだけです。
- `fig.savefig(...)` の代わりに `plt.savefig(...)` と書いた → 通常は動く(今の図に保存される)。ただし、複数の図を作っているときは意図しない図が保存されることがあるので、`fig.savefig` のほうが確実です。
- 動かなかった場合は、エラー文の**最後の行**を読んでください。`TypeError` なら引数の名前や数、`ValueError` なら値(`pitch_type` の綴りなど)を疑います。

**確認の仕方**

- エラーが出ずに最後まで実行できた。
- `outputs/dark_pitch.png` が生成され、開くとピッチが見える。

</details>

#### 課題2:バージョンを返す関数を書く

後のフェーズで、「関数」に処理をまとめます。その準備として、小さな関数を書いてみます。

- [ ] **[VS Code]** `notebooks/01_setup_check.ipynb` に **セル6** を追加し、空欄を埋めて実行する。

```python
# notebooks/01_setup_check.ipynb  セル6(課題2)
from importlib.metadata import ____


def get_version(package_name):
    """パッケージ名を受け取り、そのバージョンの文字列を返す"""
    return ____(package_name)


print(get_version("mplsoccer"))
print(get_version("____"))
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目と2つ目の `____` | セル2 で読み込んだ、バージョンを調べる関数の名前(同じものが入る) |
| 3つ目の `____` | `pip list` に出てきたライブラリの名前から、好きなもの(例:`pandas`) |

**期待される結果**

```
x.x.x
x.x.x
```

(mplsoccer と、あなたが選んだライブラリのバージョンが表示される)

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/01_setup_check.ipynb  セル6(課題2)
from importlib.metadata import version


def get_version(package_name):
    """パッケージ名を受け取り、そのバージョンの文字列を返す"""
    return version(package_name)


print(get_version("mplsoccer"))
print(get_version("pandas"))
```

**答え合わせのあとに**

- 1つ目・2つ目:`version`
- 3つ目:`pandas`、`matplotlib`、`statsbombpy` など `pip list` にあるものならどれでも可

**自分のコードが正解と違っても、動いていればOKな例**

- `import importlib.metadata` と書き、`importlib.metadata.version(package_name)` と呼び出した → 動く。書き方が違うだけです。
- 関数の引数名を `package_name` ではなく `name` にした → 動く。関数の中で同じ名前を使っていれば問題ありません。

**確認の仕方**

- エラーが出ずにバージョン文字列が表示される。
- 存在しない名前(例:`"abc"`)を入れると `PackageNotFoundError` が出る。これは正常な動きです。

</details>

### 6-10. Notebook を保存して閉じる

- [ ] **[VS Code]** `Command + S` で保存する。

### 手順6の完了チェック

- [ ] セル1で `sys.executable` が `.venv/bin/python` を指している
- [ ] セル2で4つのライブラリのバージョンが表示された
- [ ] セル3で緑の縞模様のピッチが表示された
- [ ] `outputs/empty_pitch.png` ができて、開くと画像が見える
- [ ] 課題1・2を解いて答え合わせした

---

## 手順7:コミットして GitHub へ push する

**所要時間:約0.5時間**

### 7-1. `git status` で、記録されるものを確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git status
```

期待される出力の例:

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	README.md
	docs/
	notebooks/
	outputs/
	requirements.txt

nothing added to commit but untracked files present (use "git add" to track)
```

**確認すること**

- `.venv/` が **表示されない**(`.gitignore` が効いている)。
- `data/` と `src/` は、中身が空なので表示されない(正常)。
- `outputs/` は表示されるが、中身は `.gitkeep` だけ(`empty_pitch.png` と `dark_pitch.png` は対象外)。
- もし `.venv/` や `.DS_Store` が表示された場合は、`.gitignore` の書き間違いです。手順9の「`.venv` が git status に出る」を見てください。

### 7-2. 変更をステージングする

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git add .
git status
```

期待される出力の例:

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   .gitignore
	new file:   README.md
	new file:   docs/00_overview.md
	new file:   docs/phase1_setup.md
	new file:   notebooks/01_setup_check.ipynb
	new file:   outputs/.gitkeep
	new file:   requirements.txt
```

- `git add .` は「今のフォルダ以下の変更を、次のコミットの対象にする」コマンドです。
- `Changes to be committed:`(緑色の文字)に並んだファイルが、次のコミットに入ります。

### 7-3. コミットする

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git commit -m "Phase 1: set up environment (venv, dependencies, empty pitch check)"
```

期待される出力の例:

```
[main (root-commit) abc1234] Phase 1: set up environment (venv, dependencies, empty pitch check)
 7 files changed, xxx insertions(+)
 create mode 100644 .gitignore
 ...
```

- コミットメッセージは、日本語でも構いません(例:`フェーズ1: 環境構築(venv、依存ライブラリ、空ピッチ確認)`)。**「何をしたか」が後から分かる短い文**にします。

- [ ] **[Terminal]** コミット履歴を確認する。

```bash
git log --oneline
```

期待される出力の例:

```
abc1234 (HEAD -> main) Phase 1: set up environment (venv, dependencies, empty pitch check)
```

### 7-4. GitHub にリポジトリ(置き場所)を作る

- [ ] **[Browser]** `https://github.com/new` を開く。
- [ ] 次のとおり入力する。

| 項目 | 入力・選択 |
|---|---|
| Owner | あなたのアカウント |
| Repository name | `pitchviz` |
| Description | `Pass maps and shot maps from StatsBomb open data`(任意) |
| Public / Private | **どちらでも可**。迷ったら `Private`(フェーズ6で `Public` に変更します) |
| Add a README file | **チェックしない** |
| Add .gitignore | **None** |
| Choose a license | **None**(フェーズ6で判断します) |

- [ ] **[Browser]** `Create repository` を押す。
  - 作成後のページに、`https://github.com/あなたのユーザー名/pitchviz.git` という URL が表示されます。これを使います。

> README などをここで作ってしまうと、手元の履歴とぶつかって push に失敗することがあります。手順9に対処を書いています。

> **公開してよいデータだけ**です。このプロジェクトには個人情報・業務データは含まれません。ただし、`.env` や鍵ファイルなど、秘密情報は絶対にコミットしないでください。

### 7-5. ローカルと GitHub をつなぐ

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。`あなたのユーザー名` を置き換えます。

```bash
git remote add origin https://github.com/あなたのユーザー名/pitchviz.git
git remote -v
```

期待される出力の例:

```
origin	https://github.com/あなたのユーザー名/pitchviz.git (fetch)
origin	https://github.com/あなたのユーザー名/pitchviz.git (push)
```

- `origin` は、GitHub 上のリポジトリにつけた「あだ名」です。

### 7-6. push する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git push -u origin main
```

期待される出力の例:

```
Enumerating objects: xx, done.
Counting objects: 100% (xx/xx), done.
...
To https://github.com/あなたのユーザー名/pitchviz.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

- `-u` を付けると、次回から `git push` だけで済みます。
- 認証を聞かれた場合:手順3で `gh auth login` を済ませていれば、通常は聞かれません。聞かれた場合は手順9を見てください。

### 7-7. GitHub で確認する

- [ ] **[Browser]** `https://github.com/あなたのユーザー名/pitchviz` を開き、次のファイル・フォルダが見えることを確認する。
  - `.gitignore`、`README.md`、`requirements.txt`、`docs/`、`notebooks/`、`outputs/`
  - **`.venv/` が見えない**こと。
  - README(仮)の本文が、ページの下のほうに表示されること。

### 補足:ターミナルから一発で作る方法(任意)

手順7-4〜7-6 は、`gh` を使うと1行でできます。**今回はしくみを理解するため、上の手順で進めることをおすすめします**。

```bash
gh repo create pitchviz --private --source=. --remote=origin --push
```

### 手順7の完了チェック

- [ ] `git log --oneline` にコミットが1つある
- [ ] `git remote -v` に `origin` が表示される
- [ ] GitHub のリポジトリページに、ファイルが表示されている
- [ ] `.venv/` が GitHub 上にない

---

## 手順8:振り返り

**所要時間:約0.5時間**

### 8-1. 自分の言葉で書いてみる

次の質問に、1〜2行で答えてみてください(メモ帳でも可)。答えられなければ、その部分を読み直すか、Claude / ChatGPT に質問します。

1. 仮想環境(`.venv`)は、何のために作りましたか?
2. `requirements.txt` は、何のためのファイルですか?
3. `.gitignore` に `.venv/` を書いたのはなぜですか?
4. `git add` と `git commit` の違いは何ですか?
5. `pitch_type="statsbomb"` と指定する理由は何ですか?

### 8-2. 理解度の目安

- [ ] 1に「プロジェクト専用のライブラリ置き場で、ほかと混ざらないようにするため」のように答えられる
- [ ] 2に「同じ環境を作り直すための、ライブラリの名簿」のように答えられる
- [ ] 3に「大きく、自分の Mac の中だけで使うもので、Git に入れる必要がないため」のように答えられる
- [ ] 4に「`add` は記録する対象を選ぶ、`commit` はその時点の記録を確定する」のように答えられる
- [ ] 5に「後で使う StatsBomb のデータの座標(120×80)と合わせるため」のように答えられる

### 8-3. 次のフェーズに向けた準備

- [ ] `README.md` の進捗欄に、フェーズ1の完了が反映されていることを確認する(すでに `[x]` を付けてある)。
- [ ] 手順1-8 の環境メモに、最終的に使った Python のバージョン(3.13.3 か 3.12.x か)を追記する。

---

## 手順9:つまずきやすい点と対処法

### 9-1. エラー別の対処表

| 症状・エラーメッセージの例 | 原因 | 対処 |
|---|---|---|
| `zsh: command not found: brew` | Homebrew が入っていない、または PATH が未設定 | 手順2-1 でインストールし、手順2-2 の「Next steps」のコマンドを実行する。実行したら、ターミナルを開き直す |
| `xcrun: error: invalid active developer path` | Xcode コマンドラインツールが壊れている、または未導入 | `xcode-select --install` を実行し、ダイアログが出たら「インストール」を選ぶ |
| `error: externally-managed-environment` | 仮想環境を有効化せずに `pip install` を実行した(Mac 本体の Python に入れようとした) | `source .venv/bin/activate` を実行し、行頭に `(.venv)` が出てからやり直す |
| `ERROR: Could not find a version that satisfies the requirement ...` と `No matching distribution found for ...` | ネットワーク不調、綴り間違い、または今の Python に対応するバージョンがない | 綴りを確認 → ネットワークを確認 → 手順5-5 の dry-run で原因を絞る → 解決しなければ手順5-9(Python 3.12 に切り替え) |
| `error: subprocess-exited-with-error` と `Failed building wheel for ...` | 対応ビルド済みパッケージがなく、手元でのビルドに失敗した(新しい Python でよく起きる) | 手順5-9(Python 3.12 に切り替え)を試す |
| `ModuleNotFoundError: No module named 'mplsoccer'` | Notebook のカーネルが `.venv` ではない、または未インストール | Notebook 右上のカーネルを `.venv` に切り替える(手順6-2)。それでもだめなら、ターミナルで `pip list` に入っているか確認する |
| `Running cells with '.venv' requires the ipykernel package.` | 仮想環境に `ipykernel` が入っていない | `source .venv/bin/activate` のあと `pip install ipykernel` を実行する |
| Select Kernel に `.venv` が出ない | VS Code が仮想環境を見つけていない | `Command + Shift + P` → `Python: Select Interpreter` → `.venv` を選ぶ。出ない場合は `Developer: Reload Window` を実行して再読み込みする |
| `Author identity unknown` と `Please tell me who you are.` | Git に名前とメールを登録していない | 手順2-5 のコマンドを実行する |
| `fatal: not a git repository (or any of the parent directories): .git` | `git init` をしたフォルダにいない | `cd ~/projects/pitchviz` で移動し、`pwd` で確認する |
| `fatal: remote origin already exists.` | すでに `origin` を登録済み | `git remote -v` で確認する。URL が間違っていれば `git remote set-url origin https://github.com/あなたのユーザー名/pitchviz.git` で直す |
| `remote: Support for password authentication was removed...` または `fatal: Authentication failed for ...` | HTTPS でパスワードを入力して認証しようとしている | パスワードは使えません。手順3の `gh auth login` を行い、`gh auth setup-git` を実行する |
| `fatal: could not read Username for 'https://github.com'` | 認証情報が見つからない | `gh auth status` で確認し、ログインしていなければ `gh auth login` をやり直す |
| `Permission denied (publickey).` | SSH の URL(`git@github.com:...`)を使っているが、SSH 鍵が未設定 | `git remote set-url origin https://github.com/あなたのユーザー名/pitchviz.git` で HTTPS に変える |
| `! [rejected] main -> main (fetch first)` または `Updates were rejected because the remote contains work that you do not have locally.` | GitHub 側で README などを作ってしまい、履歴が食い違っている | 下の「9-2」の手順を行う |
| `git status` に `.venv/` が出る | `.gitignore` の書き間違い、または `.gitignore` を保存していない | `.gitignore` を開き、1行目から `.venv/` があるか確認する。すでに `git add` してしまった場合は `git rm -r --cached .venv` を実行する |
| `UserWarning: credentials were not supplied. open data access only` | StatsBomb の有料 API 用の認証情報がない(**エラーではなく警告**) | 無料のオープンデータだけを使うので、無視して構いません(フェーズ2で出ます) |

### 9-2. GitHub 側で README を作ってしまい、push が失敗した場合

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git pull origin main --allow-unrelated-histories
```

- エディタが開いて「Merge branch ...」というメッセージが表示されたら、そのまま保存して閉じます。
  - ターミナル上の `vi` で開いた場合は、`Esc` → `:wq` → Enter で保存して閉じます。
- 競合(`CONFLICT (add/add): Merge conflict in README.md`)が出た場合は、**そこで止めて Claude / ChatGPT に相談してください**(質問のコツは手順10)。
- 解決したら、もう一度 `git push -u origin main` を実行します。
- 一番かんたんなのは、GitHub のリポジトリを削除して、手順7-4 から作り直すことです(中身はまだ何もないため)。

### 9-3. `rm -rf` について

- `rm -rf <フォルダ>` は、確認なしでフォルダを削除し、元に戻せません。
- 実行前に `pwd` で今いる場所を確認し、**消したいフォルダ名が合っているか**を必ず見てください。

---

## 手順10:Claude / ChatGPT に質問するときのコツ

### 10-1. 質問に必ず入れるもの

1. **やりたいこと**:「`pip install` で仮想環境にライブラリを入れたい」
2. **実行したコマンド**:実際に打ったものをそのまま
3. **エラー文の全文**:最初の行から最後の行まで
4. **環境メモ**:手順1-8 のメモ(macOS・チップ・Python のバージョン)
5. **今いるフォルダ**:`pwd` の出力
6. **仮想環境の状態**:行頭に `(.venv)` が出ているか、`which python` の出力

### 10-2. エラー文の貼り方

- 画面のスクリーンショットだけでなく、**テキストでもコピーして貼る**(検索や読み取りが正確になります)。
- コードやエラー文は、次のようにバッククォート3つで囲んで貼る。

````
```
(ここにエラー文を全部貼る)
```
````

- 長いエラー文でも、**最初の部分は省略しない**でください。原因は途中や最初にあることが多いです(一方で、いちばん下の1行が決め手になることもあります)。
- 注意:ユーザー名やパスが含まれていても問題ありませんが、**パスワード、トークン、`.env` の中身は絶対に貼らない**でください。

### 10-3. 質問の例

> macOS 15、Apple Silicon、Python 3.13.3 で、`~/projects/pitchviz` の仮想環境(`.venv`)を有効化した状態で、次のコマンドを実行しました。
>
> ```
> pip install statsbombpy mplsoccer matplotlib pandas ipykernel
> ```
>
> すると、次のエラーが出ました。
>
> ```
> (エラー全文)
> ```
>
> `which python` の結果は `/Users/.../pitchviz/.venv/bin/python` です。原因と、初学者向けの対処手順を教えてください。

### 10-4. 回答の使い方

- **1つのコマンドずつ**実行して、結果を確認する。まとめて実行しない。
- 提案されたコマンドが **何をするのか分からない場合は、実行する前に「このコマンドは何をしますか?」と聞く**。特に `rm`、`sudo`、`--force` が付くものは必ず確認する。
- 回答が古い情報の場合があります。**バージョンや仕様に関することは、公式ドキュメントで確認してください。**

---

## このフェーズ終了時のディレクトリツリー

`NEW` は、このフェーズで新しく作ったファイルです。変更したファイル(`MOD`)はありません。

```
~/projects/pitchviz/
├── .git/                         # NEW(git init で自動生成)
├── .gitignore                    # NEW
├── .venv/                        # NEW(Git管理外)
├── README.md                     # NEW(仮)
├── requirements.txt              # NEW
├── docs/
│   ├── 00_overview.md            # NEW
│   └── phase1_setup.md           # NEW
├── notebooks/
│   └── 01_setup_check.ipynb      # NEW
├── src/
│   └── pitchviz/                 # NEW(空。Git には記録されない)
├── outputs/
│   ├── .gitkeep                  # NEW
│   ├── empty_pitch.png           # NEW(Git管理外)
│   └── dark_pitch.png            # NEW(Git管理外・課題1)
└── data/                         # NEW(空。Git管理外)
```

---

## フェーズ1 最終チェックリスト

**環境**

- [ ] `uname -m` の結果を確認した(`arm64` なら Apple Silicon)
- [ ] `brew --version`、`git --version`、`gh --version` がすべて表示される
- [ ] `gh auth status` でログイン済みと表示される

**プロジェクト**

- [ ] `~/projects/pitchviz` ができ、`.venv/`、`.gitignore`、`README.md`、`requirements.txt` がある
- [ ] `pip list` に `statsbombpy` / `mplsoccer` / `matplotlib` / `pandas` / `ipykernel` がある
- [ ] Notebook のセル1の `sys.executable` が `.venv/bin/python` を指している

**動くもの**

- [ ] 空のピッチが Notebook に表示される
- [ ] `outputs/empty_pitch.png` ができている

**Git / GitHub**

- [ ] `git log --oneline` にフェーズ1のコミットがある
- [ ] GitHub のリポジトリに、ファイルが表示されている(`.venv/` は表示されない)
- [ ] StatsBomb Open Data の利用条件に目を通した

すべてにチェックが付けば、フェーズ1は完了です。

---

## 次のフェーズへ

フェーズ2では、`statsbombpy` を使って次のことを行います。

- 収録されている大会の一覧を取得する(competitions)
- 日本代表(男子・女子)が収録されているかを、実際のデータで確認する
- チーム名の正確な表記を確認する
- 試合を1つ選び、イベントデータの構造を理解する

準備ができたら「フェーズ2をお願いします」と指示してください。

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| Python / venv | Python 公式ドキュメント「venv — 仮想環境の作成」`https://docs.python.org/ja/3/library/venv.html` |
| pip | pip 公式ドキュメント `https://pip.pypa.io` |
| Homebrew | `https://brew.sh` と `https://docs.brew.sh` |
| Git | Pro Git(日本語版)`https://git-scm.com/book/ja/v2` |
| GitHub CLI | `https://cli.github.com/manual/` |
| GitHub 認証 | GitHub Docs「GitHub への認証」`https://docs.github.com/ja/authentication` |
| statsbombpy | `https://github.com/statsbomb/statsbombpy` |
| StatsBomb Open Data | `https://github.com/statsbomb/open-data` |
| mplsoccer | `https://mplsoccer.readthedocs.io` |
| matplotlib | `https://matplotlib.org/stable/` |
| pandas | `https://pandas.pydata.org/docs/` |
| VS Code Jupyter | `https://code.visualstudio.com/docs/datascience/jupyter-notebooks` |
