# フェーズ7:画面を作って、デプロイする

> 保存先:`~/projects/pitchviz/docs/phase7_deploy.md`
> このフェーズの終わりには、「ブラウザで試合と選手を選ぶと、パスマップとショットマップが表示され、PNG でダウンロードもできる画面が、Streamlit Community Cloud で動いている」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | Streamlit で画面を作り、ローカルで動作確認をしてから、Streamlit Community Cloud にデプロイする |
| 想定所要時間 | 約7.5時間(下の内訳を参照) |
| 終了時の「動くもの」 | URL を開くと、試合と選手を選べる画面が出て、パスマップとショットマップが表示され、PNG をダウンロードできる(公開範囲は、手順7で決めた方)|

### 作業ラベルの見方

- **[Terminal]**:ターミナルでの作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 事前準備(状態確認・「デプロイ」とは何か・設計) | 0.5h |
| 2 | Streamlit を入れて、3行の画面を動かす | 0.5h |
| 3 | 試合と選手を選ぶ画面を作る(課題1・2) | 1.25h |
| 4 | パスマップとショットマップの表示と、PNG のダウンロード(課題3・4) | 2.0h |
| 5 | ローカルでの動作確認 | 0.5h |
| 6 | デプロイの準備(`app/requirements.txt`・コミット・push。課題5) | 0.75h |
| 7 | ロゴの扱いと、公開範囲を決める | 0.5h |
| 8 | Streamlit Community Cloud にデプロイする | 0.75h |
| 9 | デプロイ後の確認と、更新のしかた | 0.75h |
| | 合計 | 7.5h |

### このフェーズについての大事な前提

- **フェーズ6までは「コードを公開」でした。このフェーズで初めて「動いているものを、サーバーに置く」ことになります。** 使う人は、パソコンに何も入れずに、URL を開くだけで使えます。
- **StatsBomb のロゴの扱いは、まだ決まっていません。** フェーズ6の手順2で、公開するリポジトリにはロゴのファイルを入れない(B)と決めました。ところが、**サーバーには、ロゴのファイルがありません。** そのため、サーバーで作る画像には、ロゴが入りません。利用条件 1.4(公開する分析に、StatsBomb のロゴで出典を示す)との関係があるので、**手順7で、公開範囲を決めてから、デプロイします。** 手順1〜6は、ロゴの扱いに関係なく、進められます。なお、手順7の選択肢は、フェーズ6の「A・B・C」と区別するために、**道1・道2・道3** と呼びます。画面には、画像を PNG で保存する**ダウンロードボタン**も付けるので、ロゴのない画像が、他の人に渡らないよう、注意が必要です(手順7)。
- **このフェーズの手順書の作成環境では、次のものを確認できていません。**
  - **Streamlit 本体の実際の動作。** 作成環境では、Streamlit をインストールできませんでした(パッケージの配布元に接続できないため)。そのため、画面のコードは、「Streamlit のふりをする代用品」と、架空のイベントデータを使って、**処理の流れと、エラーの出方**を確認しました。確認できたのは、試合と選手の選択、2枚の画像と2つのダウンロードボタンに渡すもの(ファイル名・PNG の中身・`image/png`)、シュートのない選手でのメッセージ、同じ選択でキャッシュが効くこと、`pitchviz` をインストールしていない状態でも読み込めること、ロゴのファイルがないときに警告が出ることです。画面の見た目、ボタンの動き、キャッシュと再実行の実際の動作は、**確認できていません。** 使っている Streamlit の関数の引数(`st.image`・`st.download_button` など)は、公式ドキュメントで確認しました。
  - **Streamlit Community Cloud の画面の細かい表示。** ボタンの名前や位置は、変わることがあります。公式ドキュメントに書かれている名前(`Create app`・`Yup, I have an app` など)を使いますが、画面と違う場合は、近い名前のものを選んでください。
  - **本物の StatsBomb のデータでの動作。** 作成環境では、データを取得できません。試合の一覧の列(`match_id`・`match_date`・`home_team`・`away_team`)は、フェーズ2・5で使ったものだけを使っています。
  - **本物の mplsoccer での、画像の見た目。** フェーズ3〜6で作った画像と、同じになるはずです(同じ関数を呼びます)。
  - **無料のアカウントで、アプリを非公開にできるか。** 公式ドキュメントには、「非公開のアプリは、同時に1つだけ」と書かれていますが、無料のアカウントでの扱いは、書かれていません。手順8で、画面を見て確認してください。
- **「期待される出力」の数字や名前は例です。** あなたの試合・バージョン・ユーザー名によって違います。`あなたのユーザー名` は、あなたの GitHub のユーザー名に置き換えてください。
- **このフェーズは、法律の助言ではありません。** 判断に迷う点は、原文(`LICENSE.pdf`、Media Pack)で確認してください。

### 今回やること・やらないこと

| やること | やらないこと |
|---|---|
| Streamlit で、試合と選手を選び、画像を表示して、PNG をダウンロードできる画面を作る | StatsBomb のデータを、リポジトリに入れること |
| `app/` に、デプロイ用の依存ファイル(`requirements.txt`)を置く | 画面の見た目の作り込み(色・レイアウトの調整)|
| Streamlit Community Cloud にデプロイする | 独自ドメイン・有料のサーバー |
| ロゴの扱いを決めて、公開範囲を選ぶ | ログイン機能・データベース |

---

## 手順1:事前準備(状態確認・「デプロイ」とは何か・設計)

**所要時間:約0.5時間**

### 1-1. 作業の状態を確認する

- [ ] **[VS Code]** `~/projects/pitchviz` をフォルダとして開き、内蔵ターミナルを開く(`Terminal → New Terminal`)。行頭に `(.venv)` が出ていることを確認する。
  - 出ていなければ、次を実行します。

```bash
source .venv/bin/activate
```

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pwd
git status
git log --oneline | head -3
git remote -v
git tag
git config user.email
gh api user --jq '.id'
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
xxxxxxx 手順書の更新などのコミット
origin	https://github.com/あなたのユーザー名/pitchviz.git (fetch)
origin	https://github.com/あなたのユーザー名/pitchviz.git (push)
private	https://github.com/あなたのユーザー名/pitchviz-private.git (fetch)
private	https://github.com/あなたのユーザー名/pitchviz-private.git (push)
v0.1.0
数字+あなたのユーザー名@users.noreply.github.com
数字
```

- `origin` が、**公開側**(`pitchviz`)です。このフェーズの `git push` は、すべて `git push origin main` と、`origin` を付けて書きます(`private` は、古い履歴の保管場所なので、今後は使いません)。
- `git config user.email` の `+` の前の数字と、`gh api user --jq '.id'` の数字が、**同じ**ことを確認してください。フェーズ6で、数字が1桁足りなくて、別の人のアカウントに結びついた失敗がありました。このあと、コミットのたびに、作者を確認します。

### 1-2. 「デプロイ」とは何か

| 言葉 | 意味 | フェーズ6までと、今回 |
|---|---|---|
| 公開(パブリッシュ・リリース) | コードを、誰でも取得できる場所に置き、バージョンを付けた | フェーズ6で、やった |
| **デプロイ** | プログラムを、**サーバーなどの、動く環境**に置いて、使える状態にした | **このフェーズで、やる** |

- デプロイ先は、**Streamlit Community Cloud** です。GitHub のリポジトリを指定すると、そのコードを、Streamlit 側のサーバーが取得して、動かしてくれます(無料)。
- 動かすのは、あなたのパソコンではなく、**Streamlit のサーバー**です。パソコンを閉じても、画面は動き続けます。
- コードを更新して `git push` すると、サーバー側も、自動で更新されます。

### 1-3. Streamlit のしくみ(3つだけ)

1. **画面は、Python のファイル1つで書く。** `st.title("...")` で見出し、`st.selectbox(...)` で選択肢のボックス、`st.image(...)` で画像、のように、上から順に書く。
2. **何かを操作するたびに、ファイルが、上から下まで、もう一度実行される。** 選択肢を変えると、`selectbox` が新しい値を返して、その値で、下の処理が最初から実行される。
3. **「前と同じ入力なら、前の結果を使う」ために、キャッシュを使う。** 関数の前に `@st.cache_data` と書くと、同じ引数での2回目以降は、保存済みの結果が返る。これがないと、操作のたびに、データを取得し直して、画像を描き直してしまう。

### 1-4. 自分のパソコンと、Cloud の違い

デプロイで、いちばん多いつまずきは、「自分のパソコンでは動くのに、サーバーでは動かない」です。原因は、次の違いです。

| | 自分の Mac | Streamlit Community Cloud | このフェーズでの対応 |
|---|---|---|---|
| OS | macOS | Linux | コードは、OS に依存しない書き方(`Path`)のまま |
| インストールされているもの | `.venv` に入れたもの | **依存ファイルに書いたものだけ** | `app/requirements.txt` を作る(手順6) |
| `pip install -e .` | した | **していない** | `app/streamlit_app.py` の先頭で、`src` を import の探す場所に足す |
| `assets/` のロゴ | ある | **ない**(Git に入れていない) | 手順7で扱いを決める |
| 保存先のフォルダ | `outputs/` | サーバー上の一時的な領域(再起動で消える) | 画像は、ファイルに残さず、メモリで扱う |
| 動いている時間 | 実行中だけ | **12時間アクセスがないと、スリープする** | 開くと、起動ボタンが出る(手順9) |
| Python のバージョン | 3.13.3 など | 選べる(初期値は 3.12) | 手元と同じものを選ぶ(手順8) |

### 1-5. 今回作る画面の設計

```
┌─────────────────────────────────────────┐
│ PitchViz: 日本代表のパスマップ・ショットマップ │
│ 試合:[2018-07-02 Belgium vs Japan ▼]   │
│ 選手:[(チーム全体) ▼]                   │
│ ┌ パスマップ ┬ ショットマップ ┐           │
│ │  (画像)                      │           │
│ │  [PNG をダウンロード]         │           │
│ └──────────────────────────────┘           │
│ データ:StatsBomb Open Data(リンク)       │
└─────────────────────────────────────────┘
```

| 部品 | 使うもの | 今までのどこ |
|---|---|---|
| 試合の一覧 | `get_competitions("World Cup")` と `get_team_matches(..., "Japan")` | フェーズ2・5(`TEAM_KEYWORD`・`COMPETITION_KEYWORD` と同じ絞り込み) |
| 1試合のデータ | `get_events(match_id)` | フェーズ2 |
| 選手の一覧 | `list_players(events, team_name)` | フェーズ5 |
| 画像を作る | `make_pass_map` / `make_shot_map` | フェーズ5 |
| 画像を保存するボタン | `st.download_button` | (今回、新しく使う) |

- **チーム名は、決め打ちにしません。** 「Japan」を含む方のチームの名前を、試合の表から取り出します(男子は `Japan`、女子は `Japan Women's` のように、表記が違うことがあるため)。

### 手順1の完了チェック

- [ ] `git status` が `nothing to commit, working tree clean`
- [ ] `git remote -v` の `origin` が、公開側の `pitchviz`
- [ ] コミットのメールの ID が、`gh api user --jq '.id'` と同じ
- [ ] 「デプロイ」と「公開」の違いを、自分の言葉で言える

---

## 手順2:Streamlit を入れて、3行の画面を動かす

**所要時間:約0.5時間**

小さく始めます。まず、Streamlit が動くことだけを確認します。

### 2-1. Streamlit をインストールする

- [ ] **[Terminal]** `(.venv)` が付いた状態で、`~/projects/pitchviz` で実行。

```bash
pip install streamlit
streamlit --version
```

期待される出力の例(最後の数行):

```
Successfully installed ... streamlit-1.xx.x ...
Streamlit, version 1.xx.x
```

- [ ] **バージョンをメモする**(手順6で使います)。

```
Streamlit のバージョン:1.66.0(例:1.66.0)
```

- 時間がかかることがあります(依存するライブラリが多いため)。数分待ってください。

### 2-2. `app` フォルダと、画面のファイルを作る

- [ ] **[VS Code]** Explorer で、プロジェクトのルート(`pitchviz`)を右クリック → `New Folder` → `app` と入力して作る。
- [ ] **[VS Code]** `app` フォルダを右クリック → `New File` → `streamlit_app.py` と入力して作る。
  - **対象**:`app/streamlit_app.py`
  - **新規作成か編集か**:新規作成

> **なぜ `app/` に置くのか**:Streamlit Community Cloud は、依存ファイル(`requirements.txt`)を、「画面のファイルがあるフォルダ」→「リポジトリのルート」の順に探して、**先に見つかった方**を使います(公式ドキュメント)。`app/` に専用の `requirements.txt` を置けば、ルートにある、開発用の `requirements.txt` と分けられます(手順6)。

### 2-3. 3行の画面を書く

- [ ] 次を貼り付けて、`Command + S` で保存する。

```python
# app/streamlit_app.py
import streamlit as st

st.title("PitchViz")
st.write("この画面が出れば、Streamlit は動いています。")
```

### 2-4. 起動する

- [ ] **[Terminal]** `~/projects/pitchviz`(プロジェクトのルート)で実行。**`app` フォルダの中ではなく、ルートで**実行します。

```bash
streamlit run app/streamlit_app.py
```

期待される出力の例:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

- ブラウザが自動で開いて、`PitchViz` の見出しと、1行の文章が出れば成功です。開かないときは、ブラウザで `http://localhost:8501` を開きます。
- 最初の起動で、メールアドレスを聞かれたら、**何も入力せずに `Enter` を押して**進めます(空のままで構いません)。
- [ ] **[VS Code]** `st.write` の文章を、別の文に書き換えて保存する。ブラウザの右上に `Source file changed.` と出て、`Rerun`(再実行)のボタンが出る。`Always rerun` を選ぶと、保存するたびに、自動で画面が更新される。

### 2-5. 止める

- [ ] **[Terminal]** `Control + C` を押す。ターミナルのプロンプトが戻れば、止まっています。
  - 止めずに別のコマンドを打ちたいときは、ターミナルをもう1つ開きます(`Terminal → New Terminal`)。ただし、**開いたターミナルにも `(.venv)` が付いていること**を確認してください。

### 手順2の完了チェック

- [ ] `streamlit --version` でバージョンが表示された。バージョンをメモした
- [ ] ブラウザで、3行の画面が表示された
- [ ] 文章を書き換えて保存すると、画面が更新された
- [ ] `Control + C` で止められた

---

## 手順3:試合と選手を選ぶ画面を作る(課題1・2)

**所要時間:約1.25時間**

### 3-1. `app/streamlit_app.py` を、書き換える(課題1・2)

- [ ] **[VS Code]** `app/streamlit_app.py` を開く。
  - **対象**:`app/streamlit_app.py`
  - **新規作成か編集か**:編集(**中身を全部消して**、次のコードに置き換える)
- [ ] 次を貼り付けて、**2つの空欄(課題1・課題2)を埋めて**から、`Command + S` で保存する。

```python
# app/streamlit_app.py
"""PitchViz の画面: 試合と選手を選ぶと、パスマップとショットマップが表示される。"""

import sys
import tempfile
import threading
from io import BytesIO
from pathlib import Path

import matplotlib

# 画面のないサーバーでも、図を作れるようにする設定。pitchviz を読み込む「前」に書く。
matplotlib.use("Agg")

import streamlit as st

# 「プロジェクトのルート/src」を、import で探す場所に足す。
# pip install -e . をしていない場所(Streamlit Community Cloud)でも、pitchviz を読み込めるようにする。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from pitchviz.api import DEFAULT_LOGO_PATH, list_players, make_pass_map, make_shot_map  # noqa: E402
from pitchviz.loader import get_competitions, get_events, get_team_matches  # noqa: E402

COMPETITION_KEYWORD = "World Cup"   # フェーズ2・5と同じ絞り込み
TEAM_KEYWORD = "Japan"
ALL_PLAYERS = "(チーム全体)"
OPEN_DATA_URL = "https://github.com/statsbomb/open-data"

# 画面に何かを出す命令(st.○○)の中で、いちばん最初に書く
st.set_page_config(page_title="PitchViz")


@st.cache_data(ttl=60 * 60 * 24, show_spinner="試合の一覧を取得しています…")
def load_matches():
    """TEAM_KEYWORD を含むチームの試合の一覧(表)。1日に1回だけ、取得し直す。"""
    return get_team_matches(get_competitions(COMPETITION_KEYWORD), TEAM_KEYWORD)


@st.cache_data(max_entries=8, show_spinner="試合のデータを取得しています…")
def load_events(match_id):
    """1試合のイベントデータ。同じ試合は、2回目から、保存済みのものを使う。"""
    return get_events(match_id)


def pick_team(row):
    """この試合の2チームのうち、TEAM_KEYWORD を含む方のチーム名を返す。"""
    if TEAM_KEYWORD.lower() ____ row["home_team"].lower():
        return row["home_team"]
    return row["away_team"]


def match_label(row):
    """選択肢に表示する文字列。例: 2018-07-02  Belgium vs Japan"""
    return f'{row["match_date"]}  {row["home_team"]} vs {row["away_team"]}'


st.title("PitchViz: 日本代表のパスマップ・ショットマップ")
st.caption("StatsBomb Open Data から作った、パスマップとショットマップ(xG をマーカーの大きさで表示)です。")

if not DEFAULT_LOGO_PATH.exists():
    st.warning(
        "この環境には StatsBomb のロゴのファイルがないため、ここで作る画像には、ロゴが入りません。"
        "ロゴのない画像は、公開・配布しないでください。"
    )

matches = load_matches()
if len(matches) == 0:
    st.error("試合の一覧を取得できませんでした。少し時間をおいて、もう一度開いてください。")
    st.stop()

left, right = st.columns(2)
with left:
    match_index = st.selectbox(
        "試合",
        options=list(matches.index),
        format_func=lambda i: match_label(matches.loc[i]),
    )

row = matches.loc[match_index]
team_name = pick_team(row)
match_id = int(row["match_id"])
match_date = str(row["match_date"])

events = load_events(match_id)
players = list_players(events, team_name)

with right:
    choice = st.selectbox("選手", options=[ALL_PLAYERS] + ____)

player_name = None if choice == ALL_PLAYERS else choice

# ↓ 手順4で、この1行を消して、画像の表示に置き換える
st.write(f"選んだ試合: {match_label(row)} / チーム: {team_name} / 選手: {player_name}")
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 課題1(`pick_team` の `____`) | 「`TEAM_KEYWORD` が、`home_team` の文字列の中に含まれている」を表す、Python の演算子(2文字)。フェーズ5の `get_opponent` では、`team_name not in teams` の形で、近い書き方が出てきた |
| 課題2(`options=[ALL_PLAYERS] + ____`) | 選択肢の先頭に「(チーム全体)」を足して、そのあとに、**選手名のリスト**を続ける。選手名のリストは、すぐ上の行で、変数に入れている |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `matplotlib.use("Agg")` | 図を、画面に表示せず、メモリ上の画像として描くモードにする。サーバーには画面がないため、また、Mac で Streamlit が別のスレッドから図を作るときのエラーを避けるために、必要。**`pitchviz` を読み込む前**に書く |
| `sys.path.insert(0, str(PROJECT_ROOT / "src"))` | 「`src` フォルダの中も、import で探してください」と Python に伝える。フェーズ5の `pip install -e .` と、同じ目的 |
| `Path(__file__).resolve().parents[1]` | このファイル(`app/streamlit_app.py`)から、1つ上のフォルダ(= プロジェクトのルート)。フェーズ5では `parents[2]` だった(`api.py` は、もう1つ深い場所にあるため) |
| `# noqa: E402` | 「import が、ファイルの先頭にないよ」という、コード検査ツールの注意を、消すための印。動作には影響しない |
| `@st.cache_data(ttl=..., show_spinner=...)` | 関数の結果を保存する。`ttl` は、保存しておく秒数(`60 * 60 * 24` = 1日)。`show_spinner` の文字は、取得中に出る表示 |
| `max_entries=8` | 保存する試合の数の上限。多すぎるとサーバーのメモリを使い切るため |
| `pick_team` | 試合の表の1行(`row`)から、「Japan」を含む方のチーム名を取り出す。決め打ちを避ける |
| `st.columns(2)` / `with left:` | 画面を、左右2つに分ける。`with left:` の中に書いたものが、左側に出る |
| `st.selectbox(label, options, format_func)` | 選択肢のボックスを出して、**選ばれた値**を返す。`format_func` は、表示する文字を決める関数(返す値は、変わらない) |
| `options=list(matches.index)` | 選択肢の値は、表の行番号(0, 1, 2, ...)。表示は `match_label` が、行から文字列を作る |
| `st.stop()` | ここで、このファイルの実行を止める。下の処理に進まない |
| `DEFAULT_LOGO_PATH` | フェーズ5の `api.py` にある、ロゴのファイルの場所(`プロジェクトのルート/assets/statsbomb_logo_white.png`)。ここでは、**ファイルがあるかの確認**にだけ使う |
| `st.warning(...)` | 黄色い警告の枠を出す。ロゴのファイルがない環境(Cloud)で、「ここで作る画像には、ロゴが入らない」ことを、画面を見た人に知らせる |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

空欄の答えだけを示します(他の部分は、上のコードのままです)。

```python
# pick_team の中(課題1)
    if TEAM_KEYWORD.lower() in row["home_team"].lower():
```

```python
# 選手の selectbox(課題2)
    choice = st.selectbox("選手", options=[ALL_PLAYERS] + players)
```

**答え合わせのあとに**

- 課題1:`in`。`"japan" in "japan women's"` のように、文字列が含まれているかを調べる。
- 課題2:`players`。`[ALL_PLAYERS]` は1つだけのリストで、`+ players` で、あとに選手名を連結する。

**自分のコードが正解と違っても、動いていればOKな例**

- 課題1:`if row["home_team"].lower().find(TEAM_KEYWORD.lower()) != -1:` と書いた → 動く(`find` は、見つからないと `-1` を返す。`in` の方が読みやすい)。
- 課題1:`if TEAM_KEYWORD in row["home_team"]:`(`.lower()` なし)と書いた → 今回の `Japan` では動く。ただし、大文字・小文字が違う検索語に変えたとき、見つからなくなる。
- 課題2:`options=[ALL_PLAYERS, *players]` と書いた → 動く(同じ結果)。
- 課題2:`options=[ALL_PLAYERS] + list_players(events, team_name)` と書いた → 動く(上の行の `players` を使わず、もう一度呼ぶだけ)。

**確認の仕方**

- 手順3-2で、画面を動かして確認します。

</details>

### 3-2. 動かして確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行(すでに起動している場合は、ブラウザの `Rerun` で構いません)。

```bash
streamlit run app/streamlit_app.py
```

- [ ] **[Browser]** 次を確認する。
  - 最初に、`試合の一覧を取得しています…` という表示が、数秒出る(何度か通信するため)。
  - 「試合」の選択肢に、**フェーズ6までで使った試合**(例:`2018-07-02  Belgium vs Japan`)が入っている。
  - 試合を変えると、「選手」の選択肢が変わり、一番下の1行の「チーム」が、`Japan`(など)になる。
  - 「選手」の先頭が `(チーム全体)` で、そのときの一番下の1行の「選手」が `None` になる。選手を選ぶと、その名前になる。
  - 黄色い警告(「この環境には StatsBomb のロゴのファイルがないため…」)は、**出ていない**。自分のパソコンには `assets/` にロゴがあるためです。Cloud では出ます(手順7・8)。
- [ ] **[Terminal]** ターミナルに、`NoAuthWarning`(認証情報がない、という警告)が出ることがある。**警告であって、エラーではありません。** StatsBomb のオープンデータは、認証なしで使うためです。

> **同じ試合を選び直す**と、「試合のデータを取得しています…」が出ないか、すぐに終わります。これが、キャッシュの効果です。サーバー(`streamlit run`)を止めて起動し直すと、保存した結果は消えます。

### 手順3の完了チェック

- [ ] 試合の選択肢が出て、フェーズ6までの試合が入っている
- [ ] 試合を変えると、選手の選択肢が変わる
- [ ] チーム名が、決め打ちではなく、試合の表から出ている(`Japan` を含む方)
- [ ] 自分のパソコンでは、黄色いロゴの警告が出ていない
- [ ] 課題1・2の空欄を、自分で埋めた

---

## 手順4:パスマップとショットマップを表示して、ダウンロードできるようにする(課題3・4)

**所要時間:約2時間**

### 4-1. 画像を作って表示する部分を、書く(課題3・4)

- [ ] **[VS Code]** `app/streamlit_app.py` の**一番下**にある、次の2行を**消す**。

```python
# ↓ 手順4で、この1行を消して、画像の表示に置き換える
st.write(f"選んだ試合: {match_label(row)} / チーム: {team_name} / 選手: {player_name}")
```

- [ ] 消した位置(ファイルの末尾)に、次を貼り付ける。**2つの空欄(課題3・課題4)を埋めて**から、`Command + S` で保存する。

```python
@st.cache_resource
def get_render_lock():
    """図を描く処理を、同時に1つだけにするための鍵(全員で、同じものを共有する)。"""
    return threading.Lock()


@st.cache_data(max_entries=40, show_spinner="画像を作っています…")
def render_map(kind, match_id, team_name, player_name, match_date):
    """パスマップ("pass")またはショットマップ("shot")を作って、(ファイル名, PNG のバイト列)を返す。"""
    events = load_events(match_id)
    make = make_pass_map if kind == "pass" else make_shot_map
    with get_render_lock(), tempfile.TemporaryDirectory() as tmp_dir:
        path = make(
            match_id,
            team_name,
            player_name=player_name,
            match_date=match_date,
            output_dir=tmp_dir,
            events=events,
        )
        return Path(path).name, Path(path).read_bytes()


st.caption(f"{row['home_team']} vs {row['away_team']} ({match_date}) / 表示中: {player_name or team_name}")

tab_pass, tab_shot = st.tabs(["パスマップ", "ショットマップ"])
tab_specs = [
    (tab_pass, "pass", "この選手のパスは、データにありません。"),
    (tab_shot, "shot", "この選手のシュートは、データにありません(シュートを打っていない選手です)。"),
]

for tab, kind, empty_message in tab_specs:
    with tab:
        try:
            file_name, png = render_map(kind, match_id, team_name, player_name, match_date)
        except ____ as error:
            st.info(empty_message)
            st.caption(f"詳細: {error}")
        else:
            st.image(BytesIO(png), width="stretch")
            st.download_button(
                label="PNG をダウンロード",
                data=____,
                file_name=file_name,
                mime="____",
                on_click="ignore",
                key=f"download_{kind}",
            )

st.divider()
st.markdown(
    f"データ: [StatsBomb Open Data]({OPEN_DATA_URL})。"
    "非公式・非営利の学習用の画面です。データの正確性は保証しません。"
)
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 課題3(`except ____ as error:`) | フェーズ5で、「その選手のシュートが無い」ときに、`_select_player` が起こしたエラーの種類(`ValueError`・`KeyError`・`TypeError` のどれか)。フェーズ5の手順6-9(セル8)で、同じ形の `try / except` を書いた |
| 課題4(`data=____`) | ボタンに渡す、「ファイルの中身」。ボタンの少し上の `st.image(BytesIO(...), ...)` の、`BytesIO(...)` のカッコの中に入れている変数と、同じもの |
| 課題4(`mime="____"`) | PNG 画像を表す、ファイルの種類の名前(MIME タイプ)。`image/` のあとに、画像の形式の名前(3文字)が続く |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `@st.cache_resource` | `cache_data` と違い、結果を**コピーせず、全員で同じものを共有**する。鍵(`Lock`)のように、「1つだけ存在してほしいもの」に使う |
| `threading.Lock()` と `with get_render_lock():` | 図を描く部分に、同時に入れるのを1人にする。matplotlib の `pyplot` は、複数の人が同時に使うことを想定しておらず、図が混ざる可能性があるため |
| なぜ、鍵を `cache_resource` で作るのか | Streamlit は、操作のたびに、ファイルを上から実行し直す。単純に `Lock()` と書くと、実行のたびに新しい鍵ができて、役に立たない |
| `tempfile.TemporaryDirectory()` | 一時的なフォルダを作って、`with` を抜けると、中身ごと消す。サーバーに、画像のファイルを残さない |
| `make_pass_map(..., output_dir=tmp_dir, events=events)` | フェーズ5の関数をそのまま使う。`events=` を渡すので、再ダウンロードしない |
| `Path(path).read_bytes()` | 保存された PNG を、バイト列(画像の中身そのもの)として読む |
| `render_map` の引数に、`events`(表)を渡さない理由 | `cache_data` は、引数の値で、「前と同じか」を判断する。大きな表を引数にすると、判断に時間がかかる。そのため、`match_id` を渡して、中で `load_events` を呼ぶ |
| `player_name or team_name` | 選手が `None`(チーム全体)なら、チーム名を表示する(フェーズ5と同じ書き方) |
| `st.tabs([...])` | タブを作る。`with tab:` の中に書いたものが、そのタブに出る |
| `try / except / else` | エラーが出たら `except`、出なかったら `else` を実行する |
| `BytesIO(png)` | バイト列を、「ファイルのようなもの」に包む。`st.image` が受け取れる形にする |
| `width="stretch"` | 画像の幅を、画面の幅に合わせる(公式ドキュメントで確認した、新しい書き方) |
| `return Path(path).name, Path(path).read_bytes()` | 関数から、**2つの値**(ファイル名と、PNG の中身)を返す。ファイル名は、フェーズ5の関数が付けた名前(例:`pass_map_japan_belgium.png`)なので、ダウンロードしたファイルの名前も、`outputs/` に保存したものと揃う |
| `file_name, png = render_map(...)` | 返ってきた2つの値を、順に、2つの変数に入れる(アンパック) |
| `st.download_button(label, data, file_name, mime, ...)` | ダウンロードのボタンを出す。押すと、ブラウザが `data` を、`file_name` という名前で保存する |
| `on_click="ignore"` | 押しても、画面を**再実行しない**指定。付けないと、押すたびに、ファイルが上から実行し直される(キャッシュがあるので壊れないが、無駄)。公式ドキュメントで確認した引数 |
| `key=f"download_{kind}"` | ボタンに付ける、名前札。パスとショットで、2つのボタンが同じ見た目になると、Streamlit が区別できなくなることがあるため、`download_pass` と `download_shot` のように、別の名前を付ける |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

空欄の答えだけを示します(他の部分は、上のコードのままです)。

```python
        except ValueError as error:
```

```python
            st.download_button(
                label="PNG をダウンロード",
                data=png,
                file_name=file_name,
                mime="image/png",
                on_click="ignore",
                key=f"download_{kind}",
            )
```

**答え合わせのあとに**

- 課題3:`ValueError`。フェーズ5の `_select_player` は、選手のデータが無いとき、`ValueError` を起こす設計だった。
- 課題4:`data=png`、`mime="image/png"`。`png` は、`render_map` から受け取った、PNG の中身(バイト列)。`image/png` は、「PNG 画像」を表す、決まった書き方。

**自分のコードが正解と違っても、動いていればOKな例**

- `except Exception as error:` と書いた → 動く(すべてのエラーを受け取る)。ただし、通信のエラーなど、**本当の不具合まで、「データにありません」と表示してしまう**。`ValueError` に絞る方が安全。
- `except (ValueError, KeyError) as error:` と書いた → 動く。
- 課題4:`data=BytesIO(png)` と書いた → 動く(ファイルのようなものも、受け取れる)。
- 課題4:`mime` の行を消した、または `mime="application/octet-stream"` と書いた → 動く。ただし、ブラウザによって、保存したときの扱い(拡張子や、開くアプリ)が変わることがある。`image/png` が確実。
- 課題4:`on_click="ignore"` を付けなかった → 動く。押すたびに、画面が再実行される(キャッシュがあるので、画像は作り直されない)。

**確認の仕方**

- 手順4-2で、シュートを打っていない選手を選んで、`st.info` のメッセージが出ることを確認します。
- 課題4は、同じ手順4-2で、ボタンを押して、保存された PNG を開いて確認します。

</details>

### 4-2. 動かして確認する

- [ ] **[Terminal]** (起動していなければ)`streamlit run app/streamlit_app.py`。
- [ ] **[Browser]** 次を順に確認する。

| 操作 | 期待すること |
|---|---|
| 最初の表示 | 試合は、一覧の先頭。選手は `(チーム全体)`。「画像を作っています…」が出たあと、**パスマップ**が出る |
| 「ショットマップ」のタブを押す | ショットマップが出る(最初だけ、数秒かかることがある)|
| 試合を、フェーズ6のもの(例:Belgium vs Japan)にする | 画像のタイトルに、相手チームの名前と日付が出る |
| 選手に、シュートを打った選手(例:フェーズ5で使った選手)を選ぶ | その選手だけの画像になる |
| 選手に、シュートを打っていない選手を選び、ショットマップのタブを見る | 青い枠で、「この選手のシュートは、データにありません…」と出る。**エラー(赤い画面)にならない** |
| 同じ組み合わせを、もう一度選ぶ | 「画像を作っています…」が出ず、すぐ表示される(キャッシュ) |
| パスマップのタブで、`PNG をダウンロード` を押す | ブラウザが、`pass_map_...png` のような名前の PNG を保存する。**画面は、選択が変わらず、「画像を作っています…」も出ない**(`on_click="ignore"`)。保存した PNG を開いて、画面の画像と同じか確認する |
| ショットマップのタブで、同じことをする | `shot_map_...png` が保存される |
| シュートを打っていない選手で、ショットマップのタブを見る | ダウンロードボタンは**出ない**(画像がないため) |

- [ ] 画像の見た目が、フェーズ6のサンプル画像(`docs/images/`)と同じ(タイトル・凡例・**ロゴ**・出典)。**自分のパソコンでは `assets/` にロゴがあるので、ロゴが入ります。** Cloud では入りません(手順7)。
- [ ] ダウンロードした PNG にも、ロゴが入っている(自分のパソコンの場合)。
- [ ] ターミナルに、赤いエラー(`Traceback`)が出ていない。

### 手順4の完了チェック

- [ ] パスマップとショットマップが、タブで切り替えて見られる
- [ ] 選手を選ぶと、その選手だけの画像になる
- [ ] シュートの無い選手で、赤いエラー画面ではなく、青い案内が出る
- [ ] 同じ選択を、2回目に選ぶと、速く出る
- [ ] 「PNG をダウンロード」で、画面の画像と同じ PNG が保存できた
- [ ] 課題3・4の空欄を、自分で埋めた

---

## 手順5:ローカルでの動作確認

**所要時間:約0.5時間**

デプロイする前に、自分のパソコンで、「サーバーに近い状態」でも動くことを確認します。

### 5-1. 「`pip install -e .` なし」でも動くか確認する

画面の先頭の `sys.path.insert(...)` が、働いているかの確認です。Cloud では、`pip install -e .` をしていないため、この行が頼りです。

- [ ] **[Terminal]** 起動中の `streamlit` を `Control + C` で止める。
- [ ] **[Terminal]** 次を実行する(`PitchViz` を、一時的に、アンインストールする)。

```bash
pip uninstall -y pitchviz
python -c "import pitchviz"
```

期待される出力:

```
Successfully uninstalled pitchviz-0.1.0
Traceback (most recent call last):
  ...
ModuleNotFoundError: No module named 'pitchviz'
```

- ここまでで、Cloud と同じ「`pitchviz` が、インストールされていない」状態になりました。`ModuleNotFoundError` は、**ここでは期待どおり**です。
- [ ] **[Terminal]** この状態で、画面を起動して、手順4-2の「最初の表示」が出ることを確認する。

```bash
streamlit run app/streamlit_app.py
```

- 画像が出れば、`sys.path.insert(...)` が働いています。
- [ ] **[Terminal]** 確認できたら、`Control + C` で止めて、`PitchViz` を、元に戻す。

```bash
pip install -e .
python -c "from pitchviz import make_maps; print('ok')"
```

- `ok` と出れば、元に戻っています(フェーズ5の手順4と同じ)。

### 5-2. 残りの確認

- [ ] ブラウザを更新(`Command + R`)しても、画面が壊れない。
- [ ] 別の試合・別の選手を、いくつか選んでも、赤いエラー画面が出ない。
- [ ] ダウンロードのボタンも、押して保存できる。
- [ ] [任意] ブラウザの画面を、スクリーンショットで1枚撮っておく(手順9のメモ用)。

### 手順5の完了チェック

- [ ] `pitchviz` をアンインストールした状態でも、画面が動いた
- [ ] `pip install -e .` で元に戻して、`ok` と出た
- [ ] 画面で、いくつかの組み合わせを試して、エラーが出なかった

---

## 手順6:デプロイの準備(`app/requirements.txt`・コミット・push。課題5)

**所要時間:約0.75時間**

### 6-1. デプロイ用の依存ファイル `app/requirements.txt` を作る(課題5)

Cloud は、`requirements.txt` に書かれたものだけをインストールします。画面を動かすのに必要なものは、5つです。

| 必要なもの | 何に使うか |
|---|---|
| `streamlit` | 画面 |
| `statsbombpy` | データの取得(`pitchviz.loader`) |
| `mplsoccer` | ピッチの描画(`pitchviz.pass_map`・`shot_map`) |
| `matplotlib` | 図 |
| `pandas` | 表 |

これらを、**自分のパソコンに入っているバージョンのまま**、書き出します(Cloud でも、同じバージョンで動かすため)。

- [ ] **[Terminal]** `(.venv)` が付いた状態で、`~/projects/pitchviz` で実行。**空欄(課題5)を埋めて**から実行する。

```bash
pip freeze | grep -i -E "^(streamlit|statsbombpy|mplsoccer|matplotlib|____)==" > app/requirements.txt
cat app/requirements.txt
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 課題5(`____`) | 上の表の5つのうち、まだ `grep` の条件に入っていない、最後の1つ(表を扱うライブラリ) |

期待される出力の例(バージョンは、あなたの環境で違います):

```
matplotlib==3.x.x
mplsoccer==1.x.x
pandas==x.x.x
statsbombpy==1.xx.x
streamlit==1.xx.x
```

- **5行**あれば OK です。5行より少ないときは、`pip show 名前` で、入っているか確認してください。
- `>` は、「画面に出す代わりに、ファイルに書き出す」記号です。同じ名前のファイルがあれば、上書きします。
- `grep` に一致するものがないと、ターミナルが赤い ⊗ を出すことがあります(終了コードが 1 のため)。ファイルが空かどうかで、確認します。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```bash
pip freeze | grep -i -E "^(streamlit|statsbombpy|mplsoccer|matplotlib|pandas)==" > app/requirements.txt
```

**答え合わせのあとに**

- 課題5:`pandas`。

**自分のコードが正解と違っても、動いていればOKな例**

- バージョンを付けずに、5つの名前だけを書いた `app/requirements.txt`(`streamlit` と改行して、`statsbombpy`、…)を、VS Code で手で作った → 動く。ただし、Cloud が**そのときの最新版**を入れるので、手元と違うバージョンになり、**手元では動くのに Cloud で動かない**可能性が上がる。
- `pip freeze > app/requirements.txt`(すべてのパッケージを書き出す)と書いた → 動く可能性はあるが、`jupyter` など、画面に不要なものも入り、インストールに時間がかかる。**おすすめしない。**

**確認の仕方**

- `cat app/requirements.txt` で、5行あり、それぞれに `==バージョン` が付いていることを確認します。

</details>

- [ ] **[Terminal]** 手順2でメモした Streamlit のバージョンと、`app/requirements.txt` の `streamlit==` の番号が、同じことを確認する。

> **「`app/requirements.txt` と、ルートの `requirements.txt` が、2つある」のは、問題ありません。** ルートのもの(フェーズ1で作った、開発用)は、そのままにします。Cloud は、画面のファイル(`app/streamlit_app.py`)と同じ `app/` の方を、先に使います(公式ドキュメント)。
>
> **公式ドキュメントの注意**:依存ファイルは、**1つのフォルダに、1種類だけ**置いてください(`requirements.txt` と `pyproject.toml` などを、同じフォルダに置くと、片方が無視されます)。ルートには、`requirements.txt` と `pyproject.toml` の両方がありますが、今回は、`app/` の `requirements.txt` が使われるので、影響しません。

### 6-2. `.gitignore` に、Streamlit の秘密の設定を足す

今回は使いませんが、Streamlit は、パスワードなどを `.streamlit/secrets.toml` に書く仕組みを持っています。うっかり公開しないために、先に除外しておきます。

- [ ] **[VS Code]** `.gitignore` を開き、**末尾**に次を足して、保存する。
  - **対象**:`.gitignore`
  - **新規作成か編集か**:編集(末尾に追記)

```
# --- Streamlit の秘密の設定(今回は使わないが、うっかり入れないため) ---
.streamlit/secrets.toml
```

- [ ] **[Terminal]** 確認する。

```bash
git check-ignore -v .streamlit/secrets.toml
```

期待される出力の例:

```
.gitignore:30:.streamlit/secrets.toml	.streamlit/secrets.toml
```

- `.gitignore:行番号:` の形で、いま足した行が表示されれば OK です(何も表示されないときは、足した行の綴りを確認してください)。

### 6-3. この手順書を保存して、コミットして、push する

- [ ] **[VS Code]** この手順書を、`docs/phase7_deploy.md` として保存する(フェーズ1〜6と同じ場所)。
- [ ] **[Terminal]** `~/projects/pitchviz` で、まず、状態を確認する。

```bash
git status
```

期待される出力の例:

```
Changes not staged for commit:
	modified:   .gitignore

Untracked files:
	app/
	docs/phase7_deploy.md
```

- `app/` の中は、`streamlit_app.py` と `requirements.txt` の2つだけのはずです。
- [ ] **[Terminal]** **ファイルを1つずつ指定して**、ステージングする(`git add .` や `git add -A` は使いません。うっかりの混入を防ぐためです)。

```bash
git add app/streamlit_app.py app/requirements.txt .gitignore docs/phase7_deploy.md
git status
git ls-files | grep -E "^(assets|outputs|data|\.venv)/"
```

- `git status` の `Changes to be committed:` に、4つのファイルだけが並んでいることを確認する。
- `git ls-files ... | grep ...` は、`outputs/.gitkeep` だけが表示されれば OK(フェーズ6の手順6-5と同じ確認)。
- [ ] **[Terminal]** コミットする。

```bash
git commit -m "Phase 7: add Streamlit app and deploy requirements"
git log -1 --format='%an <%ae>'
```

- コミットメッセージの例:`Phase 7: add Streamlit app and deploy requirements`
- 2行目の出力が、`ユーザー名 <数字+ユーザー名@users.noreply.github.com>` で、**数字が `gh api user --jq '.id'` と同じ**ことを確認する。
- [ ] **[Terminal]** **公開側(`origin`)に**、push する。

```bash
git push origin main
```

期待される出力の例(最後の行):

```
   xxxxxxx..yyyyyyy  main -> main
```

- `private` には、push しません(`git push private ...` は、使いません)。
- [ ] **[Browser]** `https://github.com/あなたのユーザー名/pitchviz` を開き、`app` フォルダが増えていることと、中に `streamlit_app.py` と `requirements.txt` があることを確認する。
  - ここで、**この時点で、すべてが公開側に入ります。** `app/` の中身が、StatsBomb のデータや個人情報を含まないことを、もう一度見てください(コードと、バージョンの一覧だけです)。

### 手順6の完了チェック

- [ ] `app/requirements.txt` が5行で、Streamlit のバージョンが手元と同じ
- [ ] `git check-ignore -v .streamlit/secrets.toml` で、除外の行が表示された
- [ ] コミットの作者のメールが noreply で、ID が合っている
- [ ] `git push origin main` が成功し、GitHub に `app/` が表示された
- [ ] 課題5の空欄を、自分で埋めた

---

## 手順7:ロゴの扱いと、公開範囲を決める

**所要時間:約0.5時間**

**デプロイの前に、ここで決めます。** 先に決めておくと、「公開してしまってから、条件に反していたと気づく」ことを避けられます。

### 7-1. なぜ決める必要があるのか

| 事実 | 内容 |
|---|---|
| 利用条件 1.4 | 公開する分析には、StatsBomb のロゴで出典を示すこと(フェーズ6の手順2で確認した) |
| フェーズ6の決定(B) | ロゴの**ファイル**は、公開リポジトリに入れていない(再配布してよいかが、確認できていないため) |
| Cloud のサーバー | リポジトリの中身だけを取得するので、`assets/` の**ロゴのファイルがない** |
| 画像を作る関数 | ロゴのファイルがないと、`[warn] logo not found` と表示して、**ロゴなしで**画像を作る(フェーズ5の `add_logo`) |
| 画面のダウンロードボタン | 画像を PNG で保存できる。**ロゴのない画像が、保存されて、他の人に渡る**可能性がある |
| 結論 | **Cloud で作られる画像には、ロゴが入らない。** 誰でも見られる状態にすると、1.4 に反する可能性が高い。ダウンロードで、さらに広がる |

> この表は、法律の助言ではありません。「画面や画像が、公開する分析にあたるか」の解釈は、原文(`LICENSE.pdf`)と、StatsBomb の案内で確認してください。迷うときは、安全な側(ロゴなしでは、誰でも見られる状態にしない)を選びます。

### 7-2. 選べる道

> フェーズ6の「A・B・C」(ロゴのファイルの扱い)とは別のものなので、ここでは **道1・道2・道3** と呼びます。

| 道 | 内容 | 公開範囲 | 向いている場合 |
|---|---|---|---|
| **道1(おすすめ)** | ロゴなしのまま、**非公開で**デプロイする(自分だけが見る) | 自分(と、招待した人)だけ | ロゴの扱いが決まるまで、「デプロイして動かす」ところまで進めたい |
| **道2** | ロゴを再配布してよいと、**確認できた**ので、ロゴのファイルを公開リポジトリに入れて、**公開で**デプロイする | 誰でも | Media Pack や、StatsBomb からの回答で、確認できた |
| **道3** | StatsBomb に問い合わせる。返事が来るまでは 道1 の状態にする | 道1 のまま | 自分では判断できない |
| ✕ | ロゴなしで、公開でデプロイする | 誰でも | **おすすめしません**(1.4 に反する可能性が高い) |

- **道1 から始めて、道2 か 道3 に進む**のが、いちばん安全で、手戻りも少ない道です。道1 のデプロイができれば、このフェーズの目的(デプロイして、動かす)は、達成できます。
- **道1・道3 のとき**:ダウンロードボタンで保存した画像にも、ロゴが入りません。**自分で見るためだけ**に使い、他の人に渡したり、どこかに公開したりしないでください。
- StatsBomb への連絡先は、`open-data` のリポジトリ(`https://github.com/statsbomb/open-data`)の README や `LICENSE.pdf` で、**あなた自身が確認**してください(手順書の作成環境では、連絡先を確認できていないため、書きません)。

- [ ] 道を選んで、メモする。

```
ロゴの扱い(フェーズ7): ______(道1 / 道2 / 道3)
決めた日:              ______
理由(1行):            ______
```

### 7-3. 道2 を選んだ場合の手順(道1・道3 の人は、飛ばす)

**前提**:Media Pack や StatsBomb からの回答で、「ロゴのファイルを、公開リポジトリに入れてよい」と、**確認できている**こと。確認した内容は、7-2 のメモの「理由」に書いておく。

- [ ] **[Terminal]** `.gitignore` で除外されているロゴを、**1つだけ**、強制的に追加する。

```bash
git check-ignore -v assets/statsbomb_logo_white.png
git add -f assets/statsbomb_logo_white.png
git status
```

- 1行目で、除外している規則が表示される(例:`.gitignore:12:assets/*	assets/statsbomb_logo_white.png`)。
- `git add -f` の `-f` は、「除外されていても、追加する」という指定です。**`statsbomb_logo_white.png` の1つだけ**を指定していることを確認してください(`assets/` 全体や、`git add -A` は、使いません)。
- `git status` の `Changes to be committed:` に、`new file:   assets/statsbomb_logo_white.png` の**1行だけ**があれば OK。
- [ ] **[VS Code]** `README.md` で、「ロゴのファイルはリポジトリに含めていません」のような文があれば、実際の状態に合わせて書き換える(`grep -n "ロゴ" README.md` で探せる)。
- [ ] **[Terminal]** コミットして、push する。

```bash
git add README.md
git commit -m "Add StatsBomb logo for credit on the deployed app"
git log -1 --format='%an <%ae>'
git push origin main
```

- コミットメッセージの例:`Add StatsBomb logo for credit on the deployed app`
- README を変えていないときは、`git add README.md` は、不要です(`git status` で、確認してください)。

### 手順7の完了チェック

- [ ] 道(道1 / 道2 / 道3)を選んで、メモした
- [ ] 「ロゴなしで、公開でデプロイしない」理由を、自分の言葉で言える
- [ ] 道2 を選んだ場合:確認した根拠をメモして、ロゴを1つだけ追加して、push した

---

## 手順8:Streamlit Community Cloud にデプロイする

**所要時間:約0.75時間**

> **操作は、Streamlit の画面で行います。** 画面のボタンの名前や位置は、変わることがあります。ここでは、公式ドキュメント(`Deploy your app`)に書かれている名前を使います。画面と違う場合は、近い名前のものを選んでください。

### 8-1. Streamlit Community Cloud に、GitHub でサインインする

- [ ] **[Browser]** `https://share.streamlit.io` を開く。
- [ ] GitHub のアカウントでサインインする(`Continue with GitHub` のような、GitHub を使うボタンを選ぶ)。
- [ ] GitHub から、「Streamlit に、アカウントの情報へのアクセスを許可しますか?」と聞かれたら、内容を読んで、許可する。
  - 許可する範囲は、画面に表示されます。**範囲が広すぎる**と感じたら、そこで止めて、公式ドキュメントで確認してください。
- メールアドレスなどの入力を求められたら、画面の案内に従う。**あなたの本物のメールを入れるかどうかは、自分で判断**してください(フェーズ6で、GitHub のコミットには、noreply を使うと決めました。これは、**Streamlit のアカウントの話**で、別の問題です)。

### 8-2. アプリを作る

- [ ] **[Browser]** 右上の `Create app` を押す。
- [ ] `Do you already have an app?` と聞かれたら、`Yup, I have an app` を選ぶ。
- [ ] 次を入力する。

| 項目 | 入力する値 |
|---|---|
| Repository | `あなたのユーザー名/pitchviz`(一覧に出なければ、`Paste GitHub URL` で、リポジトリの `app/streamlit_app.py` の URL を貼る) |
| Branch | `main` |
| Main file path | `app/streamlit_app.py` |
| App URL(任意) | 英小文字・数字・ハイフンの名前(例:`pitchviz-ku0710`)。あとで変えられる |

- **道1 を選んだ人**:App URL は、**推測されにくい名前**(例:`pitchviz-x7k2q9`)にしてください。理由は、手順8-5で説明します。

### 8-3. Python のバージョンを、手元と合わせる

- [ ] **[Terminal]** 手元のバージョンを確認する。

```bash
python --version
```

- [ ] **[Browser]** `Advanced settings` を開く。
  - `Python version`:**手元と同じ番号**(例:`3.13`)を選ぶ。公式ドキュメントでは、初期値は `3.12` です。手元より古いバージョンしか選べないときは、一番近いものを選び、手順10の対処表を見てください。
  - `Secrets`:**何も入力しない**(今回は使いません)。
- [ ] `Save` を押す。

### 8-4. デプロイする

- [ ] **[Browser]** `Deploy` のボタン(名前が違う場合は、デプロイを始めるボタン)を押す。
- [ ] 画面の右側に、起動のログが流れる。**数分**かかることがある(インストールのため)。
  - ログが見られるのは、リポジトリに書き込み権限のある人(あなた)だけです。
- [ ] アプリの画面が出たら、手順4-2の表と同じ確認をする。

| 確認 | 期待すること |
|---|---|
| 試合の一覧 | 手元と同じ試合が出る(最初は、通信で数秒〜数十秒かかることがある) |
| パスマップ・ショットマップ | 表示される |
| **画像のロゴ** | **道2 の人は入っている。道1・道3 の人は、入っていない(これは、期待どおり)** |

### 8-5. 道1・道3 を選んだ人:すぐに、非公開にする(重要)

> **公式ドキュメントでは、「公開リポジトリのアプリは、初期状態で公開」と書かれています。** 今回のリポジトリは公開なので、デプロイした直後の、アプリは、**公開の状態**です。**まだ誰にも URL を教えていなければ、実際に開く人はいないはず**ですが、制限はまだ掛かっていません。**確認が終わったら、すぐに、次の手順に進んでください。**(App URL を、推測されにくい名前にしたのは、この、ごく短い時間のためです。)

- [ ] **[Browser]** アプリの画面の右上の `Share` のボタンを開き、**`Make this app public`**(このアプリを公開する)のスイッチを、**オフ**にする。見つからないときは、アプリの設定(`App settings`)の `Sharing` の項目を開き、**`Only specific people can view this app`**(特定の人だけが、このアプリを見られる)を選んで、`Save` を押す。
  - 公式ドキュメントでは、「非公開のアプリは、そのリポジトリの開発者だけが見られて、招待した人にも見せられる」と書かれています。
  - **公式ドキュメントでは、「非公開のアプリは、同時に1つだけ」**と書かれています。無料のアカウントで使えるかは、書かれていません。**切り替えられないときは、先に進まず**、次の「切り替えられなかったとき」を見てください。
- [ ] **[Browser]** **プライベートウィンドウ**(ログインしていない状態)で、アプリの URL を開く。**アプリは表示されず、サインインを求められる**ことを確認する。

**切り替えられなかったとき**

- [ ] **[Browser]** ワークスペースのアプリ一覧で、そのアプリの右端のメニュー(縦の3点)から、`Delete app` を選んで、アプリを削除する。
  - 削除しても、GitHub のリポジトリには、影響しません。アプリの設定を消すだけです。
- 手順7に戻り、道2(確認ができたら)か、道3(StatsBomb に問い合わせる)に進んでください。

### 8-6. 道2 を選んだ人:公開のまま、確認する

- [ ] **[Browser]** プライベートウィンドウで、アプリの URL を開き、**ログインなしで、画面と画像が見える**ことを確認する。
- [ ] 画像に、**StatsBomb のロゴ**と、`Data: StatsBomb Open Data` の文字が入っていることを確認する。
- [ ] URL を、手順9のメモに控える。

### 手順8の完了チェック

- [ ] Streamlit にサインインして、アプリを作り、デプロイが終わった
- [ ] Python のバージョンを、手元と合わせた
- [ ] アプリの画面で、試合・選手を選んで、パスマップとショットマップが出た
- [ ] 道1・道3 の人:非公開にして、プライベートウィンドウで、アプリが見えないことを確認した
- [ ] 道2 の人:公開のまま、画像にロゴが入っていることを確認した

---

## 手順9:デプロイ後の確認と、更新のしかた

**所要時間:約0.75時間**

### 9-1. ログの見かた

- [ ] **[Browser]** アプリの画面の右下の `Manage app` を押すと、**Cloud のログ**が出る(開発者だけ)。

| ログに出るもの | 意味 |
|---|---|
| インストールの進行 | `app/requirements.txt` のものを、入れている |
| `[warn] logo not found: ...` | ロゴのファイルがない。**道1・道3 では、期待どおり**。道2 では、出てはいけない |
| `NoAuthWarning` | 認証なしでデータを使う、という警告。問題なし |
| `Traceback` | エラー。手順10の対処表を見る |

- ログは、メニューから、ダウンロードもできます。

### 9-2. アプリを更新する(コードを直したとき)

- [ ] **[Terminal]** 手元でコードを直して、手順4-2のように動作確認をしたあと、いつもの流れで push する。

```bash
git status
git add app/streamlit_app.py
git commit -m "Update app: ..."
git log -1 --format='%an <%ae>'
git push origin main
```

- コミットメッセージの例:`Update app: change messages`
- push すると、**Cloud のアプリも、ほぼすぐに更新**されます。`app/requirements.txt` を変えたときは、全部のインストールをやり直すので、時間がかかります(公式ドキュメント)。
- 更新されないときは、`Manage app` → `Reboot app`(アプリの再起動)を試す。

### 9-3. スリープ

- 公式ドキュメントでは、**12時間アクセスがないと、アプリはスリープ**します。
- スリープしたアプリを開くと、「眠っている」ことを伝える画面と、**起動のボタン**(公式ドキュメントでは `Yes, get this app back up!`)が出ます。押すと、元に戻ります。戻るまでの時間は、作成環境では確認できていません。見える権限のある人なら、誰でも押せます(公式ドキュメント)。
- 「開いたら、すぐには動かなかった」のは、故障ではありません。

### 9-4. README に、アプリの URL を書く(道2 の人だけ)

**非公開のアプリ(道1・道3)の URL は、README に書きません。** 他の人が開いても、サインインを求められるだけなので、意味がありません(自分用のメモに残してください)。

- [ ] **[VS Code]** 道2 の人は、`README.md` の、サンプル画像の近くに、次のような1行を足して、保存する。

```markdown
**[アプリを開く](https://あなたのアプリの名前.streamlit.app)**(試合と選手を選ぶと、パスマップとショットマップが表示されます)
```

- `https://あなたのアプリの名前.streamlit.app` は、実際の URL に置き換える。
- [ ] **[Terminal]** コミットして、push する。さらに、リポジトリの `About` に、URL を設定する。

```bash
git add README.md
git commit -m "README: add link to the deployed app"
git log -1 --format='%an <%ae>'
git push origin main
gh repo edit --homepage "https://あなたのアプリの名前.streamlit.app"
```

- コミットメッセージの例:`README: add link to the deployed app`
- `gh repo edit --homepage` の引数は、`gh repo edit --help` で存在を確認してください。

### 9-5. 不要になったら、アプリを削除する

- [ ] **[Browser]** `share.streamlit.io` のワークスペースで、そのアプリのメニュー(縦の3点)から `Delete app` を選ぶ。
  - アプリの設定が消えるだけで、GitHub のリポジトリは、そのまま残ります。

### 9-6. 記録を残す

- [ ] 次をメモする。

```
アプリの URL:          ______
公開範囲:              ______(公開 / 非公開)
Python のバージョン:   ______(Cloud の設定)
Streamlit のバージョン:______
ロゴの扱い(フェーズ7): ______(道1 / 道2 / 道3)
```

### 手順9の完了チェック

- [ ] `Manage app` から、ログを見られた(`[warn] logo not found` の有無が、ロゴの扱いと合っている)
- [ ] コードを少し直して push すると、アプリが更新される流れを、理解した(実際に試してもよい)
- [ ] スリープのしくみを、自分の言葉で言える
- [ ] 道2 の人:README にアプリの URL を足して、push した
- [ ] 記録をメモした

---

## 手順10:つまずきやすい点と対処法

### 10-1. エラー別の対処表

| 症状・エラー | 原因 | 対処 |
|---|---|---|
| `zsh: command not found: streamlit` | `.venv` が有効でない、または、`pip install streamlit` をしていない | `(.venv)` が付いていることを確認する。付いていなければ `source .venv/bin/activate`。それでも出れば `pip install streamlit` |
| `File does not exist: app/streamlit_app.py` | `app` フォルダの中で実行している、または、ファイルの名前が違う | `pwd` で、プロジェクトのルートにいることを確認して、ルートから `streamlit run app/streamlit_app.py` を実行する |
| 手元で `ModuleNotFoundError: No module named 'pitchviz'` | `sys.path.insert(...)` の行がない、または、`parents[1]` が `parents[2]` などに間違っている | 手順3-1のコードと見比べる。`app/streamlit_app.py` は、ルートの1つ下なので `parents[1]` |
| `StreamlitAPIException: set_page_config() can only be called once per app page, and must be called as the first Streamlit command` | `st.set_page_config` が、画面に何かを出す命令(`st.title` など)より後ろにある | `st.set_page_config(...)` を、最初の `st.○○` の位置に移す(手順3-1のコードのとおり) |
| `TypeError: ... got an unexpected keyword argument 'width'`(`st.image` で) | Streamlit が古い | `pip install -U streamlit` で更新して、`app/requirements.txt` の `streamlit==` を作り直す(手順6-1) |
| Mac で、画面を操作すると、`NSWindow ... main thread` のようなエラーでアプリが落ちる | `matplotlib.use("Agg")` がない、または、`pitchviz` を読み込んだ**後**に書いている | `matplotlib.use("Agg")` を、`pitchviz` の読み込みより前に書く(手順3-1) |
| 赤い画面で `ValueError: no shots found for player ...` | `except ValueError` が、ない、または、空欄が間違っている | 手順4-1の `try / except / else` を確認する |
| ボタンの行で `TypeError: ... got an unexpected keyword argument 'on_click'` のようなエラー(`st.download_button`) | Streamlit が古くて、`on_click="ignore"` に対応していない(**この形のエラーの出方は、作成環境では確認できていません**) | `pip install -U streamlit` で更新して、`app/requirements.txt` を作り直す(手順6-1)。急ぐときは、`on_click="ignore"` の行を消す(動くが、押すたびに画面が再実行される) |
| 赤い画面で、ボタンが同じものが2つある、という意味の `Duplicate...` で始まるエラー(**名前は、Streamlit の版で違うことがあり、作成環境では確認できていません**) | `st.download_button` に `key=` がない、または、2つとも同じ `key` になっている | `key=f"download_{kind}"` を、手順4-1のコードのとおりに書く |
| ダウンロードしたファイルが、開けない、または、0バイト | `data=` に、PNG の中身ではないものを渡している(ファイル名と PNG の2つ組(タプル)のまま、など) | `file_name, png = render_map(...)` のように、2つに分けて受け取り、`data=png` と書く(手順4-1) |
| Cloud のログに `ModuleNotFoundError: No module named 'mplsoccer'`(など) | `app/requirements.txt` に、書かれていない、または、push していない | `git ls-files app` で、`app/requirements.txt` が Git に入っているか確認する。中身が5行あるか確認する |
| Cloud のログに `ModuleNotFoundError: No module named 'pitchviz'` | `src` を push していない、または、`Main file path` が違う | `git ls-files src` で `src/pitchviz/*.py` が入っているか確認する。`Main file path` が `app/streamlit_app.py` か確認する |
| Cloud のログに `Error installing requirements`(など、インストールの失敗) | `==` で固定したバージョンが、選んだ Python では、入らない | ログで、どのパッケージか確認する。Python のバージョンを、手元と同じにする(手順8-3)。それでもだめなら、そのパッケージの `==バージョン` を消して、最新版で試す |
| Cloud に、**ルートの** `requirements.txt` の中身が、入ってしまう(`jupyter` などが入る) | `app/requirements.txt` が、ない、または、Git に入っていない | `app/requirements.txt` を作って push する。画面のファイルと同じフォルダの方が優先される(公式ドキュメント) |
| `HTTPError`(429 など)や、データを取得できないエラーが、Cloud だけで出る | データの取得元(GitHub)への、アクセスの制限・一時的な不調の可能性。**確認できていません** | 少し時間をおいて、`Manage app` → `Reboot app`。何度も出るなら、ログの全文を AI や Streamlit のフォーラムに貼って質問する |
| Cloud の画像に、**ロゴが入っていない** | サーバーに、ロゴのファイルがない(Git に入れていないため) | **期待どおり**です。手順7で決めた道に従う。道2 なら、手順7-3を確認する |
| push したのに、アプリが更新されない | 反映の待ち時間、または、アプリが止まっている | 数分待つ。`Manage app` → `Reboot app` |
| アプリを開いたら、「眠っています」と出る | 12時間アクセスがなくて、スリープした | 起動のボタンを押す(手順9-3) |
| `Share` で非公開にできない | アカウントの種類・同時に1つまでの制限など | 手順8-5の「切り替えられなかったとき」へ |
| 非公開のはずなのに、プライベートウィンドウで、アプリが見える | 設定が保存されていない | `Share` を開き直して、状態を確認する。**確認できるまで、URL を、誰にも教えない** |
| コミットの作者が、自分のアカウントと違う人で表示される | `git config user.email` の ID の数字が違う(フェーズ6で起きた) | `git config user.email "$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"` で設定し直す |

### 10-2. 「動いているけれど、合っているか分からない」ときの確認方法

- **画像が合っているか**:画面の画像と、フェーズ6のサンプル画像(`docs/images/`)を、同じ試合・同じチームで比べる。タイトル・日付・凡例・ロゴの有無以外は、同じはずです。
- **キャッシュが効いているか**:同じ選択を2回目に選んだとき、「…を作っています」が出なければ、効いています。
- **チーム名が合っているか**:試合を変えたとき、画像のタイトルのチーム名が、「Japan」を含む方のチームになっているか。
- **Cloud と手元の差**:Cloud の `Manage app` のログと、手元のターミナルの出力を、見比べる。違いがあれば、そこが原因の候補です。

---

## 手順11:Claude / ChatGPT に質問するときのコツ(デプロイ編)

### 11-1. デプロイの質問に、必ず入れるもの

| 入れるもの | 例 |
|---|---|
| 何をしようとしているか | 「Streamlit Community Cloud に、`app/streamlit_app.py` をデプロイしている」 |
| どこで起きたか | 「手元(Mac)では動く。Cloud の起動で、エラーが出る」 |
| **ログの全文** | `Manage app` のログを、そのまま貼る(個人情報・トークンがないか、貼る前に確認) |
| `app/requirements.txt` の中身 | 5行を貼る |
| バージョン | `python --version`、Streamlit のバージョン、Cloud で選んだ Python のバージョン |
| 自分が試したこと | 「Reboot app をした」「Python を 3.12 に変えた」 |

### 11-2. 質問の例

> Streamlit Community Cloud にデプロイしたところ、次のログのエラーが出ます。手元の Mac(Python 3.13.3、Streamlit 1.xx)では動きます。
>
> (ログを貼る)
>
> `app/requirements.txt`:
> (5行を貼る)
>
> 原因として何が考えられますか? 初学者向けに、確認する順番を教えてください。

### 11-3. 回答の使い方

- **アクセス権・公開範囲・削除に関わる操作**(アプリを公開にする、リポジトリを公開にする、アプリを削除する)を提案されたら、**実行する前に**、「これは何を変えますか? 元に戻せますか?」と質問してください。
- AI が示した Streamlit の関数の引数(`st.image(width=...)` など)は、**公式ドキュメント**(`https://docs.streamlit.io/develop/api-reference`)で、実在するか確認してください。Streamlit は、版によって引数が変わります(`use_container_width` から `width` への変更など)。
- **ログや設定ファイルを貼るとき**は、パスワード・トークン・メールアドレスが入っていないか確認してください。`secrets.toml` の中身は、貼らないでください。

---

## このフェーズ終了時のディレクトリツリー

`NEW` は新しく作ったファイル、`MOD` は変更したファイルです。

```
~/projects/pitchviz/
├── .git/
├── .gitignore                         # MOD(.streamlit/secrets.toml を除外)
├── .venv/
├── LICENSE                            # (MIT を選んだ場合)
├── README.md                          # (道2 を選んだ場合は MOD:アプリの URL)
├── pyproject.toml
├── requirements.txt                   # (開発用。変更なし)
├── app/                               # NEW
│   ├── streamlit_app.py               # NEW(画面)
│   └── requirements.txt               # NEW(デプロイ用。5行)
├── assets/
│   ├── statsbomb_logo_white.png       # (道2 を選んだ場合だけ、Git 管理に追加)
│   └── statsbomb_logo_default.png     # (Git管理外)
├── docs/
│   ├── 00_overview.md
│   ├── phase1_setup.md
│   ├── phase2_data.md
│   ├── phase3_passmap.md
│   ├── phase4_shotmap.md
│   ├── phase5_function.md
│   ├── phase6_publish.md
│   ├── phase7_deploy.md               # NEW
│   └── images/
├── notebooks/
├── src/
│   └── pitchviz/
├── outputs/
│   └── .gitkeep
└── data/                              # (空。Git管理外)
```

- **GitHub 側の状態**:`あなたのユーザー名/pitchviz`(公開・`v0.1.0` のリリース・`app/` が増えた)と、`あなたのユーザー名/pitchviz-private`(非公開・古い履歴)です。
- **Streamlit 側の状態**:`share.streamlit.io` に、アプリが1つ(公開範囲は、手順7で決めた方)あります。

---

## 手順12:振り返り

次の質問に、1〜2行で自分の言葉で答えてみてください。

1. 「公開(リリース)」と「デプロイ」は、何が違いますか?
2. Streamlit は、操作のたびに、ファイルを上から実行し直すのに、なぜ、毎回データを取得し直さないのですか?
3. `requirements.txt` を、ルートではなく、`app/` にも置いたのは、なぜですか?
4. `app/streamlit_app.py` の先頭で、`sys.path.insert(...)` を書いたのは、なぜですか?
5. ロゴなしの画像を、誰でも見られる状態でデプロイしないのは、なぜですか?
6. ダウンロードボタンに `on_click="ignore"` を付けたのは、なぜですか?

- [ ] 1に「リリースは、コードを取得できる場所に置くこと。デプロイは、サーバーで動かして、URL で使えるようにすること」のように答えられる
- [ ] 2に「`@st.cache_data` が、同じ引数の結果を保存して、2回目から使うから」のように答えられる
- [ ] 3に「Cloud は、画面のファイルと同じフォルダの依存ファイルを、先に使うから。ルートの開発用のものと分けられる」のように答えられる
- [ ] 4に「Cloud では `pip install -e .` をしていないので、`src` の中の `pitchviz` を、自分で import の探す場所に足す必要があるから」のように答えられる
- [ ] 5に「利用条件 1.4 が、公開する分析に、StatsBomb のロゴでの出典を求めているから。サーバーにはロゴのファイルがなく、画像にロゴが入らない」のように答えられる
- [ ] 6に「ボタンを押したとき、画面を、上から実行し直させないため。押しても、選択や表示は変わらず、ダウンロードだけが行われる」のように答えられる

---

## フェーズ7 最終チェックリスト

**画面(ローカル)**

- [ ] `streamlit run app/streamlit_app.py` で、試合と選手を選べる
- [ ] パスマップ・ショットマップが、タブで切り替えられる
- [ ] シュートの無い選手で、赤いエラー画面ではなく、案内が出る
- [ ] 「PNG をダウンロード」で、画面の画像と同じ PNG が保存できる
- [ ] `pitchviz` をアンインストールした状態でも動いた(その後、`pip install -e .` で元に戻した)

**デプロイの準備**

- [ ] `app/requirements.txt` が5行で、手元のバージョンと同じ
- [ ] `.gitignore` に、`.streamlit/secrets.toml` がある
- [ ] コミットの作者が noreply で、ID が `gh api user --jq '.id'` と同じ
- [ ] `git push origin main` で、公開側に `app/` が入った

**ロゴと公開範囲**

- [ ] ロゴの扱い(道1 / 道2 / 道3)を決めて、メモした
- [ ] 道1・道3:アプリを非公開にして、プライベートウィンドウで見えないことを確認した
- [ ] 道2:ロゴを確認した根拠をメモして、画像にロゴが入っている

**デプロイ**

- [ ] Streamlit Community Cloud にデプロイして、画面が動いた
- [ ] Python のバージョンを、手元と合わせた
- [ ] 記録(URL・公開範囲・バージョン・ロゴの扱い)をメモした

すべてにチェックが付けば、フェーズ7は完了です。**PitchViz は、「サーバーで動いているアプリ」になりました。**

---

## 完成の確認(最初の目標との対応)

| 最初の目標 | できたこと | どこで |
|---|---|---|
| StatsBomb Open Data を使う | データを取得して、絞り込めるようになった | フェーズ2 |
| 日本代表のパスマップを描く | ピッチ上に、パスを矢印で描いた | フェーズ3 |
| シュートを、xG をマーカーの大きさで描く | ショットマップを描いた | フェーズ4 |
| 試合とチーム/選手を指定して、画像を保存する関数 | `make_maps` / `make_shot_map` / `make_pass_map` | フェーズ5 |
| README と GitHub での公開 | README・サンプル画像・クレジット・`v0.1.0` | フェーズ6 |
| **デプロイして、URL で使えるようにする** | **Streamlit で画面(表示と PNG のダウンロード)を作り、Cloud で動かした** | **フェーズ7** |

## このあと(任意)

- **ロゴの扱いを決めて、公開に切り替える**(道1・道3 の人):道2 の条件が整ったら、手順7-3を行い、アプリの `Share` の設定を、公開に変える。切り替えのあとは、プライベートウィンドウで、画像にロゴが入っていることを確認してください。
- 画面に、ほかの機能を足す(チームの選択、複数試合の合算、`xG` の合計の表示など)。**足すたびに、手元で動作確認 → コミット → push** の流れで更新できます。
- 画面の見た目を整える(色・説明文・レイアウト)。公式ドキュメントの、テーマの設定を参照してください。
- **更新のたびに、確認する**:StatsBomb の出典・ロゴ、個人情報、データの混入(フェーズ6の手順6と同じ)。

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| Streamlit Community Cloud:アプリをデプロイする | `https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy` |
| 同:依存ファイル(`requirements.txt`・Python のバージョン) | `https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies` |
| 同:アプリを共有する(公開・非公開) | `https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app` |
| 同:アプリを管理する(スリープ・再起動・ログ) | `https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app` |
| Streamlit の関数(`st.image`・`st.selectbox`・`st.cache_data`) | `https://docs.streamlit.io/develop/api-reference` |
| 同:ダウンロードボタン(`st.download_button`) | `https://docs.streamlit.io/develop/api-reference/widgets/st.download_button` |
| StatsBomb Open Data(データ・利用条件) | `https://github.com/statsbomb/open-data`(`LICENSE.pdf`) |
| StatsBomb の Media Pack(ロゴ・Usage Rights) | `https://statsbomb.com/media-pack/` |
| GitHub CLI(`gh repo edit`) | `https://cli.github.com/manual/` |
