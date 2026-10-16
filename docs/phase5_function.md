# フェーズ5:関数化と画像保存

> 保存先:`~/projects/pitchviz/docs/phase5_function.md`
> このフェーズの終わりには「`make_pass_map(試合ID, チーム名)` や `make_shot_map(試合ID, チーム名, player_name=選手名)` を1行呼ぶだけで、PNG が `outputs/` に保存される」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | フェーズ2〜4で作った関数を、「試合とチーム(または選手)を指定すると画像を保存する」入口の関数にまとめる。`pyproject.toml` を足して、`sys.path.append("../src")` なしで `import pitchviz` できるようにする |
| 想定所要時間 | 約5時間(下の内訳を参照) |
| 終了時の「動くもの」 | Notebook で `make_maps(MATCH_ID, "Japan")` の1行を実行すると、パスマップとショットマップの2枚が保存される。選手を指定した画像(例:`shot_map_genki_haraguchi_belgium.png`)も作れる |

### 作業ラベルの見方

- **[Terminal]**:ターミナルでの作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 事前準備(状態確認・今回作るものの設計) | 0.5h |
| 2 | 試合の日付を探す関数 `find_match_date`(課題1) | 0.5h |
| 3 | `api.py` を作る(課題2・3) | 1.25h |
| 4 | `pyproject.toml` で、`pitchviz` をインストールする | 0.75h |
| 5 | `__init__.py` で、使う関数を公開する(課題4) | 0.5h |
| 6 | Notebook `05_use_function.ipynb` で、1行呼び出しを確認する | 1.0h |
| 7 | README・コミット・振り返り | 0.5h |
| | 合計 | 5.0h |

### このフェーズについての大事な前提

- **コードの確認範囲について**:この手順書の作成環境では、mplsoccer 本体と StatsBomb のデータを入手できず、実際には動かせていません。代わりに、同じ呼び出し方を受け付ける代用品と、StatsBomb と同じ列構造の架空のイベントデータで、手順書のコード(`loader.py`・`api.py`・`__init__.py`・Notebook のセル1〜9)を**最後まで実行**して確認しました。確認できたのは、チーム・選手の絞り込み、相手チームの割り出し、エラー文、ファイル名、PNG の保存、図が閉じられること(`plt.close`)、選手ごとのシュート数の合計がチーム全体と一致すること、`events` を渡しても渡さなくても同じ画像になることです。`pyproject.toml` も、ライブラリの取得を除いた形で `pip install -e .` を実行し、プロジェクトの外のフォルダから `import pitchviz` できることを確認しました(setuptools 68・pip の新しい版)。**ライブラリ本体(statsbombpy・mplsoccer など)を含めた `pip install -e .` の出力と、本物の mplsoccer での見た目は、あなたの環境で初めて確認することになります。** また、`src/pitchviz.egg-info/` は、pip と setuptools の版によって、作られる環境と作られない環境があります(手順4-3・7-3)。
- **「期待される出力」の数字や名前は例です。** あなたが選んだ試合・チーム・選手によって違います。
- **このフェーズは、フェーズ2〜4の成果を使います。** 特に、`loader.py` の `get_events`・`get_passes`・`get_shots`、`pass_map.py` の `draw_pass_map`・`save_figure`・`make_filename`、`shot_map.py` の `draw_shot_map` を呼び出します。フェーズ4が終わっていない場合は、先に終えてください。
- **リポジトリは Private のままにしてください。** Notebook の出力に、データの行や、データから作った画像が残ります。公開の前の整理は、フェーズ6で行います(StatsBomb の利用条件で、データの再配布が禁止されているためです)。
- **「チーム名」「選手名」は、データの表記を一字一句そのまま使います。** 推測で書きません。選手名は、この手順書で作る `list_players()` で確認します。

### 今回作るものの流れ

```
make_shot_map(試合ID, "Japan", player_name="Genki Haraguchi", match_date="2018-07-02")
   │  (api.py)
   ├─ loader.get_events()          … 試合のイベントを取得する(渡されていれば、それを使う)
   ├─ api.get_opponent()           … 相手チームの名前を、イベントから割り出す
   ├─ loader.get_shots()           … チームのシュートを取り出す
   ├─ api._select_player()         … 選手が指定されていれば、その選手の分だけに絞る
   ├─ shot_map.draw_shot_map()     … 描く(フェーズ4)
   ├─ pass_map.save_figure()       … PNG で保存する(フェーズ3)
   └─ plt.close(fig)               … 図を閉じて、メモリを開放する
   ▼
outputs/shot_map_genki_haraguchi_belgium.png  (保存先のパスを返す)
```

- **新しい計算は、ほとんどありません。** フェーズ2〜4で作った部品を、決まった順番でつなぐだけです。「部品を作る」から「部品をつないで、使いやすい入口を作る」に、仕事が変わります。

### 今回作る入口の関数(一覧)

| 関数 | 何をするか | 返すもの |
|---|---|---|
| `make_pass_map(match_id, team_name, player_name=None, ...)` | パスマップを保存する | 保存先のパス |
| `make_shot_map(match_id, team_name, player_name=None, ...)` | ショットマップを保存する | 保存先のパス |
| `make_maps(match_id, team_name, player_name=None, ...)` | 上の2つを続けて実行する | 保存先のパスのリスト(2つ) |
| `list_players(events, team_name)` | そのチームの選手名の一覧を返す(指定する名前の確認用) | 選手名のリスト |
| `get_teams(events)` / `get_opponent(events, team_name)` | 試合の2チーム / 相手チームを返す | チーム名のリスト / 文字列 |
| `loader.find_match_date(matches, match_id)` | 試合一覧の表から、日付を探す | 日付の文字列 |

---

## 手順1:事前準備(状態確認・今回作るものの設計)

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
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
On branch main
nothing to commit, working tree clean
```

- フェーズ4のコミットが済んでいない場合は、先にフェーズ4の手順8を終えてください(`Your branch is ahead of ...` と出ても問題ありません)。

### 1-2. フェーズ2〜4の成果が残っているか確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
ls src/pitchviz assets
```

期待される出力:

```
assets:
statsbomb_logo_default.png	statsbomb_logo_white.png

src/pitchviz:
__init__.py	loader.py	pass_map.py	shot_map.py
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、使う関数がそろっているか確認する。

```bash
grep -n "^def " src/pitchviz/loader.py src/pitchviz/pass_map.py src/pitchviz/shot_map.py
```

期待される出力の例(行番号は環境で違います):

```
src/pitchviz/loader.py:6:def get_competitions(keyword=""):
src/pitchviz/loader.py:15:def get_team_matches(competitions, team_keyword):
src/pitchviz/loader.py:30:def get_events(match_id):
src/pitchviz/loader.py:34:def add_xy(df, column="location", x_name="x", y_name="y"):
src/pitchviz/loader.py:41:def filter_events(events, event_type, team_name=None):
src/pitchviz/loader.py:52:def get_passes(events, team_name):
src/pitchviz/loader.py:64:def get_shots(events, team_name):
src/pitchviz/pass_map.py:15:def add_logo(fig, anchor_ax, logo_path, height_ratio=0.8, margin=0.01):
src/pitchviz/pass_map.py:39:def draw_pass_map(passes, team_name, opponent_name, match_date, logo_path=None):
src/pitchviz/pass_map.py:80:def save_figure(fig, path, dpi=200):
src/pitchviz/pass_map.py:87:def make_filename(team_name, opponent_name, prefix="pass_map"):
src/pitchviz/shot_map.py:16:def summarize_shots(shots):
src/pitchviz/shot_map.py:25:def draw_shot_map(shots, team_name, opponent_name, match_date, logo_path=None):
```

- `loader.py` の `get_events`・`get_passes`・`get_shots`、`pass_map.py` の `draw_pass_map`・`save_figure`・`make_filename`、`shot_map.py` の `draw_shot_map` の**7つが表示されていれば OK** です(行番号は違って構いません)。足りない関数があれば、そのフェーズに戻って終えてください。

### 1-3. フェーズ2のメモを手元に用意する

```
使うチーム名:     Japan(例:Japan)
使う match_id:    7584(例:7584)
対戦カードと日付: 2018-07-02 Belgium vs Japan(例:2018-07-02 Belgium vs Japan)
```

- 忘れた場合は、`notebooks/03_pass_map.ipynb` のセル2や、`notebooks/04_shot_map.ipynb` のセル2の値で確認します。

### 1-4. なぜ「入口の関数」を作るのか

フェーズ4までは、1枚の画像を作るのに、Notebook に次のような処理を何セルも書いていました。

1. `get_events` でイベントを取る
2. `teams` から相手チームを探す
3. `get_passes`(または `get_shots`)で取り出す
4. `draw_...` で描く
5. `make_filename` でファイル名を作る
6. `save_figure` で保存する

これを1つの関数にまとめると、次の利点があります。

| 利点 | 具体例 |
|---|---|
| 呼び出しが1行で済む | `make_pass_map(7584, "Japan")` |
| 同じ手順の書き間違いがなくなる | 相手チームの探し方を、1か所だけに書く |
| 別の試合・別の選手で、すぐ試せる | 引数の値を変えるだけ |
| あとで人に渡せる(README に使い方を1行で書ける) | フェーズ6 |

### 1-5. 今回の設計(先に決めておくこと)

| 決めること | 決め方 | 理由 |
|---|---|---|
| 選手を指定するときの引数 | `player_name=None`(渡さなければチーム全体) | 引数を増やすだけで、既存の呼び出しはそのまま動く |
| 日付の引数 | `match_date=None`(渡さなければ `"date n/a"` と表示) | イベントデータには日付がないため。試合の表(`matches`)から探す関数を、別に用意する |
| 画像の保存先 | 既定は `プロジェクトのルート/outputs` | どこから呼んでも、同じ場所に保存される |
| ロゴの場所 | 既定は `プロジェクトのルート/assets/statsbomb_logo_white.png` | 同上。ノートブックの場所に依存しない |
| 図の後始末 | 保存したら `plt.close(fig)` | 何枚も作ると、図がメモリに残り続けるため |
| 選手がいない・チーム名が違うとき | 分かりやすい `ValueError`(選べる名前の一覧つき) | 推測で別の名前に置き換えず、使える名前を見せるため |

### 手順1の完了チェック

- [ ] `(.venv)` が行頭に表示されている
- [ ] 7つの関数(`get_events`・`get_passes`・`get_shots`・`draw_pass_map`・`save_figure`・`make_filename`・`draw_shot_map`)が確認できた
- [ ] フェーズ2のメモ(チーム名・`match_id`・日付)が手元にある
- [ ] 「入口の関数」を作る理由を、自分の言葉で言える

---

## 手順2:試合の日付を探す関数 `find_match_date`(課題1)

**所要時間:約0.5時間**

イベントデータ(`events`)には、試合の日付が入っていません。日付は、フェーズ2で作った**試合の一覧(`matches`)の表**にあります。この表から、`match_id` を手がかりに日付を取り出す関数を作ります。

### 2-1. `loader.py` に追記する(課題1)

- [ ] **[VS Code]** Explorer で `src/pitchviz/loader.py` を開く。
  - **対象**:`src/pitchviz/loader.py`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:ファイルの**末尾**(`get_shots` 関数の後ろ)に、次のコードを追記する。
- [ ] **空欄(`____`)を埋めて**追記し、`Command + S` で保存する。

```python
# src/pitchviz/loader.py (末尾に追記)


def find_match_date(matches, match_id):
    """get_team_matches() の結果の表から、match_id の試合の日付(文字列)を返す。"""
    row = matches[matches["____"] == match_id]
    if len(row) == 0:
        raise ValueError(f"match_id {match_id} is not in the matches table")
    return str(row["match_date"].____[0])
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | 試合の番号が入っている列の名前(フェーズ2のセル11の表で、先頭の列) |
| 2つ目 | 「0から数えて、位置で行を取り出す」属性の名前(`[0]` と続けて、先頭の1行を取る) |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `matches[matches["match_id"] == match_id]` | 「`match_id` 列が、引数の `match_id` と等しい行」だけに絞る(フェーズ2・手順4のセル13と同じ書き方) |
| `len(row) == 0` | 1行も見つからなかった |
| `raise ValueError(f"...")` | 自分でエラーを起こして、原因をメッセージで伝える。何も返さずに進むより、原因が分かりやすい |
| `.iloc[0]` | 絞り込んだ表の、先頭の1行(行番号ではなく、位置で数える) |
| `str(...)` | 日付を文字列にそろえる(図のタイトルに使うため) |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# src/pitchviz/loader.py (末尾に追記)


def find_match_date(matches, match_id):
    """get_team_matches() の結果の表から、match_id の試合の日付(文字列)を返す。"""
    row = matches[matches["match_id"] == match_id]
    if len(row) == 0:
        raise ValueError(f"match_id {match_id} is not in the matches table")
    return str(row["match_date"].iloc[0])
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `match_id`、2つ目は `iloc`。

**自分のコードが正解と違っても、動いていればOKな例**

- `row["match_date"].values[0]` と書いた → 動く(`iloc[0]` と同じ結果。`str(...)` で文字列にしていれば、図のタイトルも同じ)。
- `matches.query("match_id == @match_id")` で絞り込んだ → 動く(別の書き方)。
- `if len(row) == 0:` の確認を書かなかった → 見つかるときは動くが、見つからないとき `IndexError` になり、原因が分かりにくい。付けるのが安全です。

**確認の仕方**

- 手順6のセル2で、本物の `matches` を使って確認します。

</details>

### 手順2の完了チェック

- [ ] `loader.py` の末尾に `find_match_date` を追記して、保存した
- [ ] 空欄を埋められた(できなければ、ヒントを見てから答えを開いた)
- [ ] `raise ValueError` が、何のためにあるか説明できる

---

## 手順3:`api.py` を作る(課題2・3)

**所要時間:約1.25時間**

### 3-1. `api.py` を作る

- [ ] **[VS Code]** Explorer で `src/pitchviz` フォルダを右クリック → `New File` → `api.py` と入力して作る。
  - **対象**:`src/pitchviz/api.py`
  - **新規作成か編集か**:新規作成
- [ ] 次の**2つの空欄(課題2・課題3)を除いた部分**まで含めて、全体を貼り付ける。**空欄(`____`)を埋めて**から、`Command + S` で保存する。

```python
# src/pitchviz/api.py
"""入口の関数: 試合とチーム(または選手)を指定して、画像を保存する。"""

from pathlib import Path

import matplotlib.pyplot as plt

from .loader import get_events, get_passes, get_shots
from .pass_map import draw_pass_map, make_filename, save_figure
from .shot_map import draw_shot_map

# このファイルは「プロジェクトのルート/src/pitchviz/api.py」にある。
# parents[0] = pitchviz、parents[1] = src、parents[2] = プロジェクトのルート
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"
DEFAULT_LOGO_PATH = PROJECT_ROOT / "assets" / "statsbomb_logo_white.png"
NO_DATE = "date n/a"


def get_teams(events):
    """この試合の2チームの名前を、リストで返す。"""
    return list(events["team"].dropna().unique())


def get_opponent(events, team_name):
    """team_name の相手チームの名前を返す。team_name がこの試合にいなければ ValueError。"""
    teams = get_teams(events)
    if team_name not in teams:
        raise ValueError(f"team {team_name!r} is not in this match. teams: {teams}")
    others = [t for t in teams if t ____ team_name]
    return others[0]


def list_players(events, team_name):
    """そのチームの選手名(イベントに登場した人)を、アルファベット順のリストで返す。"""
    rows = events[events["team"] == team_name]
    return sorted(rows["player"].dropna().unique())


def _select_player(table, events, team_name, player_name, what):
    """player_name が None ならそのまま返す。指定があれば、その選手の行だけにして返す。"""
    if player_name is None:
        return table
    selected = table[table["player"] ____ player_name]
    if len(selected) == 0:
        raise ValueError(
            f"no {what} found for player {player_name!r} ({team_name}). "
            f"players: {list_players(events, team_name)}"
        )
    return selected.reset_index(drop=True)


def make_pass_map(match_id, team_name, player_name=None, match_date=None,
                  output_dir=DEFAULT_OUTPUT_DIR, logo_path=DEFAULT_LOGO_PATH, events=None):
    """パスマップを描いて PNG で保存し、保存先のパスを返す。

    player_name を渡すと、その選手のパスだけを描く。
    events を渡すと、ダウンロードを省略できる(何枚も作るときに速い)。
    """
    if events is None:
        events = get_events(match_id)
    opponent = get_opponent(events, team_name)
    passes = _select_player(get_passes(events, team_name), events, team_name, player_name, "passes")

    label = player_name or team_name
    fig = draw_pass_map(passes, label, opponent, match_date or NO_DATE, logo_path=logo_path)
    path = save_figure(fig, Path(output_dir) / make_filename(label, opponent, prefix="pass_map"))
    plt.close(fig)
    return path


def make_shot_map(match_id, team_name, player_name=None, match_date=None,
                  output_dir=DEFAULT_OUTPUT_DIR, logo_path=DEFAULT_LOGO_PATH, events=None):
    """ショットマップを描いて PNG で保存し、保存先のパスを返す。引数は make_pass_map と同じ。"""
    if events is None:
        events = get_events(match_id)
    opponent = get_opponent(events, team_name)
    shots = _select_player(get_shots(events, team_name), events, team_name, player_name, "shots")

    label = player_name or team_name
    fig = draw_shot_map(shots, label, opponent, match_date or NO_DATE, logo_path=logo_path)
    path = save_figure(fig, Path(output_dir) / make_filename(label, opponent, prefix="shot_map"))
    plt.close(fig)
    return path


def make_maps(match_id, team_name, player_name=None, match_date=None,
              output_dir=DEFAULT_OUTPUT_DIR, logo_path=DEFAULT_LOGO_PATH, events=None):
    """パスマップとショットマップの両方を保存し、保存先のパスのリスト [パス, ショット] を返す。"""
    if events is None:
        events = get_events(match_id)
    kwargs = dict(player_name=player_name, match_date=match_date, output_dir=output_dir,
                  logo_path=logo_path, events=events)
    return [
        make_pass_map(match_id, team_name, **kwargs),
        make_shot_map(match_id, team_name, **kwargs),
    ]
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 課題2(`get_opponent` の `t ____ team_name`) | 「自分以外のチーム」を取り出す条件。比較演算子で、「等しくない」を表す記号(フェーズ3のセル2で、同じ形を書いた) |
| 課題3(`_select_player` の `table["player"] ____ player_name`) | 「その選手の行」を取り出す条件。比較演算子で、「等しい」を表す記号(`=` ではなく、2文字) |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `from .loader import ...` | 同じパッケージの `loader.py` から読み込む(フェーズ4で出てきた書き方) |
| `Path(__file__).resolve().parents[2]` | このファイル(`api.py`)の場所から、2つ上のフォルダ(= プロジェクトのルート)を求める。`__file__` は「いま実行中のファイルの場所」を表す特別な変数 |
| `DEFAULT_OUTPUT_DIR = ...` | 大文字の名前は「設定値(定数)」の目印(フェーズ3・4と同じ習慣) |
| `output_dir=DEFAULT_OUTPUT_DIR` | 引数の**初期値**。渡さなければ、この値になる |
| `_select_player` の先頭の `_` | 「このファイルの中だけで使う、内部用の関数」という目印(決まりではなく、習慣) |
| `player_name or team_name` | `player_name` が `None`(または空文字)なら `team_name`、あれば `player_name`。図のタイトルとファイル名に使う |
| `match_date or NO_DATE` | 日付が渡されなければ、`"date n/a"` と表示する |
| `plt.close(fig)` | 図を閉じる。閉じないと、何枚も作るうちに図がメモリに残り続ける |
| `**kwargs` | 辞書を、`名前=値, 名前=値, ...` の形に展開して渡す書き方。`make_maps` で、同じ引数を2つの関数にそのまま渡すために使う |
| `events=None` のとき `get_events` | 渡されていなければ、自分でダウンロードする。渡されていれば、それを使う(ダウンロードは、試合ごとに1回で済む) |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

空欄の答えだけを示します(他の部分は、上のコードのままです)。

```python
# get_opponent の中(課題2)
    others = [t for t in teams if t != team_name]
```

```python
# _select_player の中(課題3)
    selected = table[table["player"] == player_name]
```

**答え合わせのあとに**

- 課題2:`!=`(等しくない)。課題3:`==`(等しい)。

**自分のコードが正解と違っても、動いていればOKな例**

- 課題2:`others = [t for t in teams if t not in (team_name,)]` と書いた → 動く(同じ結果)。
- 課題2:`others = [t for t in teams if t != team_name]` ではなく、`teams.remove(team_name)` で消して `teams[0]` を返した → 動く。ただし `teams` を直接書き換えるので、あとで `get_teams` の結果を再利用するときに注意。
- 課題3:`table[table["player"].eq(player_name)]` と書いた → 動く(`==` と同じ働き)。
- 課題3:`table.query("player == @player_name")` と書いた → 動く(別の書き方)。

**確認の仕方**

- 手順6のセルで、本物のデータを使って確認します。

</details>

### 3-2. コードの全体像を、自分の言葉で確認する

次の質問に、1〜2行で答えてみてください(答えは、確認のためのもので、提出は不要です)。

1. `make_pass_map` と `make_shot_map` は、ほとんど同じ形です。違うのは、どの行ですか?

    → `get_passes` と `get_shots`、`draw_pass_map` と `draw_shot_map`、`prefix` の3か所
2. `get_opponent` は、チーム名が違うとき、なぜ `ValueError` を起こすのですか? 黙って別のチームを返したら、何が起きますか?

    → 綴りの間違いなどで別のチームの画像を保存してしまう
3. `make_maps` が、`events` を最初に1回だけ取得するのは、なぜですか?

    → `make_pass_map` と `make_shot_map`での重複ダウンロードを防ぐため
- [ ] 1に「`get_passes` と `get_shots`、`draw_pass_map` と `draw_shot_map`、`prefix` の3か所」のように答えられる
- [ ] 2に「綴りの間違いに気づけず、別のチームの図を保存してしまうから」のように答えられる
- [ ] 3に「`make_pass_map` と `make_shot_map` が、それぞれダウンロードすると、同じデータを2回取ることになるから」のように答えられる

### 手順3の完了チェック

- [ ] `src/pitchviz/api.py` を作って、保存した
- [ ] 課題2・課題3の空欄を埋められた
- [ ] `make_pass_map` / `make_shot_map` / `make_maps` の違いを説明できる
- [ ] `ValueError` が、どんなときに起きるか説明できる

---

## 手順4:`pyproject.toml` で、`pitchviz` をインストールする

**所要時間:約0.75時間**

### 4-1. いま、何が困っているのか

フェーズ2〜4の Notebook では、毎回セル1に次の2行を書いていました。

```python
import sys
sys.path.append("../src")
```

これは「`src` フォルダの場所を、その Notebook だけに教える」書き方です。**Notebook の場所が変わると動かなくなります**(`notebooks/` 以外から開いた、別の場所にコピーした、など)。

これを、**Python の環境に「`pitchviz` というパッケージがある」と登録**することで、どこからでも `import pitchviz` できるようにします。登録に使うのが、プロジェクトの説明書である `pyproject.toml` です。

### 4-2. `pyproject.toml` を作る

- [ ] **[VS Code]** Explorer で、プロジェクトのルート(`pitchviz` フォルダ直下)の空いたところを右クリック → `New File` → `pyproject.toml` と入力して作る。
  - **対象**:`pyproject.toml`(プロジェクトのルート直下)
  - **新規作成か編集か**:新規作成
- [ ] 次の内容を貼り付け、`Command + S` で保存する。

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "pitchviz"
version = "0.1.0"
description = "Pass maps and shot maps (xG) from StatsBomb Open Data"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "statsbombpy",
    "mplsoccer",
    "matplotlib",
    "pandas",
]

[tool.setuptools.packages.find]
where = ["src"]
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `[build-system]` | 「このプロジェクトを組み立てる(パッケージにする)道具は何か」。ここでは `setuptools` を使う |
| `[project]` の `name` | パッケージの名前。`import pitchviz` で使う名前と、同じにしている |
| `version` | 版番号。今は `0.1.0` で十分 |
| `readme = "README.md"` | 説明文として使うファイル(プロジェクトのルートに `README.md` が必要) |
| `requires-python = ">=3.10"` | 動作に必要な Python の版。**この値は、手順書の作成時の目安です**。あなたの Python は 3.13.3 なので、満たしています |
| `dependencies` | 必要なライブラリの名前。**版は固定しません**(版を固定した名簿は `requirements.txt` にある) |
| `[tool.setuptools.packages.find]` と `where = ["src"]` | 「パッケージは、`src` フォルダの中を探す」。この指定がないと、手順4-3の `Multiple top-level packages discovered` エラーになる |

**確認先(公式ドキュメント)**

| 確認したいこと | 確認先 |
|---|---|
| `pyproject.toml` の書き方・`src` フォルダの指定 | setuptools の `pyproject.toml` の設定ページ(`https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html`) |
| `[build-system]`・`[project]` の意味 | Python Packaging User Guide の「Writing your pyproject.toml」(`https://packaging.python.org/en/latest/guides/writing-pyproject-toml/`) |
| `pip install -e`(編集可能インストール) | pip の「Local project installs」(`https://pip.pypa.io/en/stable/topics/local-project-installs/`) |

- 上の表のうち、setuptools と pip のページは、この手順書の作成時に内容を確認しました(`where = ["src"]` の指定、`pip install -e` で「ソースを直すと、再インストールなしで反映される」こと)。`setuptools>=61` と `requires-python` の値は、あなたの環境の版に合わせて、公式ドキュメントで確認してください。

### 4-3. `.gitignore` に、インストールで作られるフォルダを足す

`pip install -e .` を実行すると、環境(pip と setuptools の版)によっては、`src/pitchviz.egg-info/` というフォルダ(インストールの記録)が自動で作られます。**作られない環境もあります**(新しい版では、記録は `.venv` の中に入り、`src/` には何も増えません)。どちらになっても困らないように、自動生成のファイルは Git に含めない設定を、先に足しておきます。

- [ ] **[VS Code]** Explorer で `.gitignore` を開く。
  - **対象**:`.gitignore`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:ファイルの**末尾**に、次の内容を追記する。
- [ ] 追記して `Command + S` で保存する。

```gitignore
# .gitignore (末尾に追記)

# --- pip install -e . で自動生成される、インストールの記録 ---
*.egg-info/
```

### 4-4. インストールする

- [ ] **[Terminal]** `~/projects/pitchviz` で実行(行頭に `(.venv)` があることを確認する)。

```bash
pwd
python -m pip install -e .
```

期待される出力の例(行の数や順序は、pip の版で違います):

```
/Users/あなたのユーザー名/projects/pitchviz
Obtaining file:///Users/あなたのユーザー名/projects/pitchviz
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Requirement already satisfied: statsbombpy in ./.venv/lib/python3.13/site-packages (from pitchviz==0.1.0) (x.x.x)
...(各ライブラリの「Requirement already satisfied」が並ぶ)...
Building wheels for collected packages: pitchviz
  Building editable for pitchviz (pyproject.toml) ... done
  Created wheel for pitchviz: filename=pitchviz-0.1.0-...whl size=... sha256=...
Successfully built pitchviz
Installing collected packages: pitchviz
Successfully installed pitchviz-0.1.0
```

**確認すること**

- [ ] 最後の行が `Successfully installed pitchviz-0.1.0` になっている
- [ ] `-e` は、**「編集可能(editable)」インストール**。`src/` の中のファイルを書き換えると、再インストールなしで反映される

### 4-5. インストールされたか確認する

- [ ] **[Terminal]** **`~/projects/pitchviz` ではなく、ホームフォルダ(`~`)に移動して**実行する。`pitchviz` フォルダの外からでも読み込めることを確認するためです。

```bash
cd ~
pwd
python -c "import pitchviz; print(pitchviz.__file__)"
```

期待される出力の例:

```
/Users/あなたのユーザー名
/Users/あなたのユーザー名/projects/pitchviz/src/pitchviz/__init__.py
```

- 2行目が、`.../projects/pitchviz/src/pitchviz/__init__.py` になっていれば成功です。**「編集可能インストール」なので、`site-packages` のコピーではなく、`src` の中のファイルが直接使われている**ことが分かります。
- [ ] **[Terminal]** プロジェクトに戻って、登録の記録を確認する。

```bash
cd ~/projects/pitchviz
pwd
python -m pip show pitchviz
```

期待される出力の例(版や項目の並びは違います):

```
/Users/あなたのユーザー名/projects/pitchviz
Name: pitchviz
Version: 0.1.0
Summary: Pass maps and shot maps (xG) from StatsBomb Open Data
...
Location: /Users/あなたのユーザー名/projects/pitchviz/.venv/lib/python3.13/site-packages
Editable project location: /Users/あなたのユーザー名/projects/pitchviz
Requires: matplotlib, mplsoccer, pandas, statsbombpy
```

### 4-6. `requirements.txt` は、作り直さない

- **フェーズ1で作った `requirements.txt` を、`pip freeze > requirements.txt` で上書きしないでください。** 編集可能インストールの行(`-e /Users/あなたのユーザー名/...` のような、あなたの Mac だけの場所)が混ざり、他の人の環境で `pip install -r requirements.txt` が失敗する原因になります。
- 今回は、ライブラリを新しく入れていないので、`requirements.txt` は変更不要です。
- 使い方の説明(`pip install -r requirements.txt` のあとに `pip install -e .`)は、フェーズ6の README に書きます。

### 手順4の完了チェック

- [ ] `pyproject.toml` を作って、保存した
- [ ] `.gitignore` に `*.egg-info/` を足した
- [ ] `Successfully installed pitchviz-0.1.0` と表示された
- [ ] ホームフォルダ(`~`)から `import pitchviz` でき、`.../src/pitchviz/__init__.py` が表示された
- [ ] `requirements.txt` を上書きしていない

---

## 手順5:`__init__.py` で、使う関数を公開する(課題4)

**所要時間:約0.5時間**

### 5-1. いまの `__init__.py` の役割

`src/pitchviz/__init__.py` は、フェーズ2から**空のファイル**でした。「このフォルダは、Python のパッケージ」という目印だけの役割です。

ここに「`pitchviz` から、直接読み込める名前」を書くと、次のように短く書けるようになります。

| 書き方 | `__init__.py` の記述 |
|---|---|
| `from pitchviz.api import make_pass_map`(長い) | 不要 |
| `from pitchviz import make_pass_map`(短い) | **必要** |

### 5-2. `__init__.py` を編集する(課題4)

- [ ] **[VS Code]** Explorer で `src/pitchviz/__init__.py` を開く(中身は空)。
  - **対象**:`src/pitchviz/__init__.py`
  - **新規作成か編集か**:既存ファイルの編集(空のファイルに書き込む)
- [ ] **空欄(`____`)を埋めて**貼り付け、`Command + S` で保存する。

```python
# src/pitchviz/__init__.py
"""PitchViz: StatsBomb Open Data から、パスマップとショットマップを作る。"""

from .api import ____, make_maps, make_pass_map, make_shot_map

__all__ = ["list_players", "make_maps", "make_pass_map", "make_shot_map"]
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | `api.py` で作った、選手名の一覧を返す関数の名前。`__all__` の1つ目にも書いてある |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `from .api import ...` | 同じパッケージの `api.py` から読み込む。これで `pitchviz` を読み込むと、これらの名前がすぐ使える |
| `__all__ = [...]` | 「このパッケージの、公開する名前の一覧」。`from pitchviz import *` で読み込まれる名前と、読む人への案内になる |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# src/pitchviz/__init__.py
"""PitchViz: StatsBomb Open Data から、パスマップとショットマップを作る。"""

from .api import list_players, make_maps, make_pass_map, make_shot_map

__all__ = ["list_players", "make_maps", "make_pass_map", "make_shot_map"]
```

**答え合わせのあとに**

- 空欄の答えは `list_players`。

**自分のコードが正解と違っても、動いていればOKな例**

- `from .api import list_players, make_maps, make_pass_map, make_shot_map` の並びを、別の順にした → 動く(並びは自由)。
- `__all__` を書かなかった → 動く(`from pitchviz import make_maps` は読み込める)。ただし、公開する名前の案内がなくなる。
- 4つを、1行ずつ `from .api import list_players` のように分けて書いた → 動く。

**確認の仕方**

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
python -c "from pitchviz import list_players, make_maps, make_pass_map, make_shot_map; print('ok')"
```

期待される出力:

```
ok
```

</details>

### 手順5の完了チェック

- [ ] `__init__.py` に、4つの関数を公開した
- [ ] 確認コマンドで `ok` と表示された
- [ ] `from pitchviz.api import make_pass_map` と `from pitchviz import make_pass_map` が、同じ関数を指すことを説明できる

---

## 手順6:Notebook `05_use_function.ipynb` で、1行呼び出しを確認する

**所要時間:約1.0時間**

### 6-1. Notebook を作る

- [ ] **[VS Code]** `notebooks` フォルダを右クリック → `New File` → `05_use_function.ipynb` と入力して作る。
  - **対象**:`notebooks/05_use_function.ipynb`
  - **新規作成か編集か**:新規作成
- [ ] 右上の `Select Kernel` から、`.venv` の Python(`Python Environments...` → `.venv`)を選ぶ。
  - **重要**:`pip install -e .` を実行した `.venv` と、同じ Python を選びます。違う Python を選ぶと、`ModuleNotFoundError: No module named 'pitchviz'` になります。

### 6-2. セル1:`sys.path.append` なしで、読み込む

- [ ] **[VS Code]** 最初のセルに、次を入力して実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル1**

```python
# notebooks/05_use_function.ipynb  セル1
%load_ext autoreload
%autoreload 2

from pathlib import Path

from IPython.display import Image, display

import pitchviz
from pitchviz import list_players, make_maps, make_pass_map, make_shot_map

print(pitchviz.__file__)
```

**期待される出力の例**

```
/Users/あなたのユーザー名/projects/pitchviz/src/pitchviz/__init__.py
```

**確認すること**

- [ ] **`sys.path.append("../src")` を書いていないのに**、エラーなく読み込めた(これが、手順4の成果です)
- [ ] 表示されたパスが、`.../src/pitchviz/__init__.py` になっている

### 6-3. セル2:試合を指定して、日付を探す

- [ ] **[VS Code]** 次のセルを追加し、**値をフェーズ2のメモに置き換えて**、実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル2**

```python
# notebooks/05_use_function.ipynb  セル2
from pitchviz.loader import find_match_date, get_competitions, get_events, get_team_matches

TEAM_NAME = "Japan"   # フェーズ2のメモの値に置き換える(例)
MATCH_ID = 7584       # フェーズ2のメモの値に置き換える(例)

matches = get_team_matches(get_competitions("World Cup"), "Japan")   # フェーズ2のセル9〜13と同じ絞り込み
MATCH_DATE = find_match_date(matches, MATCH_ID)
print(MATCH_DATE)
```

**期待される出力の例**(ダウンロードに数十秒かかることがあります。`NoAuthWarning` は警告で、エラーではありません)

```
2018-07-02
```

**確認すること**

- [ ] 日付が、フェーズ2のメモの日付と一致している
- `ValueError: match_id ... is not in the matches table` が出たら、`matches` に、その試合が入っていません(手順8の対処表)。フェーズ2で使った大会・チームの絞り込み(`"World Cup"`、`"Japan"`)に、あなたの試合が含まれるか確認してください。

### 6-4. セル3:パスマップを、1行で保存する

- [ ] **[VS Code]** 次のセルを追加して、実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル3**

```python
# notebooks/05_use_function.ipynb  セル3
path = make_pass_map(MATCH_ID, TEAM_NAME, match_date=MATCH_DATE)
print(path)
display(Image(filename=str(path)))
```

**期待される出力の例**

```
/Users/あなたのユーザー名/projects/pitchviz/outputs/pass_map_japan_belgium.png
```

- セルの下に、パスマップの画像が1枚表示される。
- **フェーズ3のセル12と同じ画像**になる(フェーズ3で保存した `pass_map_japan_belgium.png` が、同じ内容で上書きされる)。

**確認すること**

- [ ] 保存先のパスが `.../outputs/pass_map_チーム名_相手チーム名.png` になっている
- [ ] 画像に、タイトル・凡例・ロゴ・出典が入っている(フェーズ3と同じ見た目)
- [ ] セルの下に、図が**二重に表示されていない**(`plt.close(fig)` の効果)

### 6-5. セル4:ショットマップを、1行で保存する

- [ ] **[VS Code]** 次のセルを追加して、実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル4**

```python
# notebooks/05_use_function.ipynb  セル4
path = make_shot_map(MATCH_ID, TEAM_NAME, match_date=MATCH_DATE)
print(path)
display(Image(filename=str(path)))
```

**期待される出力の例**

```
/Users/あなたのユーザー名/projects/pitchviz/outputs/shot_map_japan_belgium.png
```

- セルの下に、ショットマップの画像が1枚表示される(フェーズ4のセル11と同じ内容)。

### 6-6. セル5:選手名の一覧を確認する

選手を指定するときは、**データの表記を一字一句そのまま**使う必要があります。まず、一覧を表示します。

- [ ] **[VS Code]** 次のセルを追加して、実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル5**

```python
# notebooks/05_use_function.ipynb  セル5
events = get_events(MATCH_ID)
players = list_players(events, TEAM_NAME)
print(len(players))
print(players)
```

**期待される出力の例**(人数と名前は、あなたの試合によって違います)

```
14
['Gaku Shibasaki', 'Gen Shōji', 'Genki Haraguchi', 'Hiroki Sakai', 'Keisuke Honda', ...]
```

**確認すること**

- [ ] 選手名の一覧が表示された
- [ ] 名前の綴りが、データの表記(英語のローマ字。`ō` のような記号つきの文字もある)のまま表示されている
- [ ] 試合に出た選手が、14人前後(スタメン11人と交代選手を含む数)になっている

### 6-7. セル6:選手を指定した画像を、保存する

- [ ] **[VS Code]** 次のセルを追加し、**`PLAYER_NAME` を、セル5の一覧から1人選んで、一字一句コピー**して実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル6**

```python
# notebooks/05_use_function.ipynb  セル6
PLAYER_NAME = "Genki Haraguchi"   # セル5の一覧から選んだ名前に置き換える(例)

shot_path = make_shot_map(MATCH_ID, TEAM_NAME, player_name=PLAYER_NAME, match_date=MATCH_DATE, events=events)
pass_path = make_pass_map(MATCH_ID, TEAM_NAME, player_name=PLAYER_NAME, match_date=MATCH_DATE, events=events)
print(shot_path.name)
print(pass_path.name)
display(Image(filename=str(shot_path)))
```

**期待される出力の例**

```
shot_map_genki_haraguchi_belgium.png
pass_map_genki_haraguchi_belgium.png
```

- セルの下に、その選手のショットマップが表示される。
- **その選手が、この試合でシュートを1本も打っていない場合は、図は作られず `ValueError: no shots found for player ...` になります**(空の図は保存されません)。一覧に名前があっても、シュートがなければ出ます。そのときは、別の選手を選ぶか、`make_shot_map` の行を飛ばして、パスマップだけ作ってください(手順8の対処表)。

**確認すること**

- [ ] ファイル名に、選手名(小文字、空白は `_`)と相手チーム名が入っている
- [ ] 図のタイトルが `Genki Haraguchi shot map vs Belgium` のように、選手名になっている
- [ ] チーム全体のショットマップより、点の数が少ない(その選手のシュートだけ)
- [ ] `events=events` を渡した2回目以降は、ダウンロードの待ち時間がほとんどない

### 6-8. セル7:両チームの、パスマップとショットマップを、1行ずつで保存する

- [ ] **[VS Code]** 次のセルを追加して、実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル7**

```python
# notebooks/05_use_function.ipynb  セル7
from pitchviz.api import get_teams

for team in get_teams(events):
    paths = make_maps(MATCH_ID, team, match_date=MATCH_DATE, events=events)
    for p in paths:
        print(p.name)
```

**期待される出力の例**(順番は、チーム名の並びによって違います)

```
pass_map_belgium_japan.png
shot_map_belgium_japan.png
pass_map_japan_belgium.png
shot_map_japan_belgium.png
```

**確認すること**

- [ ] 4行(2チーム × パスマップとショットマップ)が表示された
- [ ] `outputs/` に、4枚の PNG がそろっている

### 6-9. セル8:間違った名前で、分かりやすいエラーが出るか確認する

- [ ] **[VS Code]** 次のセルを追加して、実行する。**エラーを、わざと起こして、メッセージを確認する**セルです。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル8**

```python
# notebooks/05_use_function.ipynb  セル8
try:
    make_pass_map(MATCH_ID, "Japn", events=events)      # 綴りを、わざと間違える
except ValueError as e:
    print("ValueError:", e)

try:
    make_shot_map(MATCH_ID, TEAM_NAME, player_name="Nobody Here", events=events)   # いない選手
except ValueError as e:
    print("ValueError:", e)
```

**期待される出力の例**

```
ValueError: team 'Japn' is not in this match. teams: ['Belgium', 'Japan']
ValueError: no shots found for player 'Nobody Here' (Japan). players: ['Gaku Shibasaki', 'Gen Shōji', 'Genki Haraguchi', ...]
```

**確認すること**

- [ ] 1つ目で、**この試合のチーム名の一覧**が表示される
- [ ] 2つ目で、**そのチームの選手名の一覧**が表示される
- [ ] どちらも、画像は保存されていない(`outputs/` に、`japn` や `nobody_here` のファイルがない)

### 6-10. セル9(発展):別の試合でも、1行で動くか確認する

フェーズ2〜4と**別の試合**でも、同じ関数が動くかを確かめます。**値は、フェーズ2の `japan_matches` の表から、あなたが選びます**(推測で書かないでください)。

- [ ] **[VS Code]** 次のセルを追加し、**`OTHER_MATCH_ID` と `OTHER_TEAM` を、`matches` の表から選んで**実行する。
  - **対象**:`notebooks/05_use_function.ipynb` の **セル9**

```python
# notebooks/05_use_function.ipynb  セル9(発展)
display(matches[["match_id", "match_date", "home_team", "away_team"]])   # まず表を見て、別の試合を選ぶ

OTHER_MATCH_ID = ____       # 表から選んだ match_id(数字。引用符 " " は付けない)
OTHER_TEAM = "____"         # その試合の、home_team か away_team の表記を、一字一句コピーする

other_date = find_match_date(matches, OTHER_MATCH_ID)
for p in make_maps(OTHER_MATCH_ID, OTHER_TEAM, match_date=other_date):
    print(p.name)
```

**期待される出力の例**(試合によって違います)

```
pass_map_japan_senegal.png
shot_map_japan_senegal.png
```

**確認すること**

- [ ] 別の試合でも、2枚の PNG が保存された
- [ ] ファイル名の相手チームが、選んだ試合の相手になっている
- **注意**:同じ相手と2回対戦している場合(例:グループステージと決勝トーナメント)は、ファイル名が同じになり、**上書き**されます(手順8の対処表)。

### 手順6の完了チェック

- [ ] セル1で、`sys.path.append` なしに `import pitchviz` できた
- [ ] セル3・4で、1行で2枚の画像が保存され、表示された
- [ ] セル5で選手名を確認し、セル6で選手を指定した画像を保存できた
- [ ] セル7で、両チームの4枚がそろった
- [ ] セル8で、間違った名前に対して、分かりやすいエラーが出た
- [ ] (発展)セル9で、別の試合でも動いた

---

## 手順7:README・コミット・振り返り

**所要時間:約0.5時間**

### 7-1. README の進捗を更新する

- [ ] **[VS Code]** Explorer で `README.md` を開く。
  - **対象**:`README.md`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:`## 進捗` の下の `- [x] フェーズ4:ショットマップ` の**次の行**に、次の1行を足す。
- [ ] 追記して `Command + S` で保存する。

```markdown
- [x] フェーズ5:関数化と画像保存
```

### 7-2. Notebook を保存する

- [ ] **[VS Code]** `Command + S` で `05_use_function.ipynb` を保存する。

### 7-3. `git status` で、記録されるものを確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git status
```

期待される出力の例:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .gitignore
	modified:   README.md
	modified:   src/pitchviz/__init__.py
	modified:   src/pitchviz/loader.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/phase5_function.md
	notebooks/05_use_function.ipynb
	pyproject.toml
	src/pitchviz/api.py

no changes added to commit (use "git add" and/or "git commit -a")
```

**確認すること**

- `.gitignore`・`README.md`・`__init__.py`・`loader.py` が `modified` になっている。
- `docs/phase5_function.md`、`notebooks/05_use_function.ipynb`、`pyproject.toml`、`src/pitchviz/api.py` が Untracked に出る。
- **`src/pitchviz.egg-info/` が表示されない**こと(`.gitignore` に足した `*.egg-info/` の効果。そもそも作られていない環境でも、表示されないので問題ありません)。表示される場合は、手順4-3を確認してください。
- **`outputs/` の PNG と `assets/` のロゴが表示されない**こと。
- `.venv/` や `data/` が出ていないこと。

- [ ] **[Terminal]** `~/projects/pitchviz` で、`src` の中に `egg-info` があるかを確認する。

```bash
ls src
```

- `pitchviz` だけが表示された → `egg-info` は作られていない環境です。**次のコマンドは不要**なので、飛ばして構いません。
- `pitchviz` と `pitchviz.egg-info` が表示された → 次のコマンドで、Git の対象外になっているか確認します。

```bash
git check-ignore -v src/pitchviz.egg-info
```

期待される出力の例(行番号は環境で違います):

```
.gitignore:34:*.egg-info/	src/pitchviz.egg-info
```

- **フォルダがない状態で実行すると、何も表示されません**(エラーではありません)。`*.egg-info/` の「末尾の `/`」は「フォルダ」の意味なので、実在しないものには当てはまらないためです。必ず、`ls src` で、あることを確かめてから実行してください。

### 7-4. ステージングしてコミットする

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git add .
git status
```

期待される出力の例:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   .gitignore
	modified:   README.md
	new file:   docs/phase5_function.md
	new file:   notebooks/05_use_function.ipynb
	new file:   pyproject.toml
	modified:   src/pitchviz/__init__.py
	new file:   src/pitchviz/api.py
	modified:   src/pitchviz/loader.py
```

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git commit -m "Phase 5: add make_pass_map/make_shot_map/make_maps entry functions and pyproject.toml"
```

期待される出力の例:

```
[main xxxxxxx] Phase 5: add make_pass_map/make_shot_map/make_maps entry functions and pyproject.toml
 8 files changed, xxx insertions(+)
 create mode 100644 docs/phase5_function.md
 create mode 100644 notebooks/05_use_function.ipynb
 create mode 100644 pyproject.toml
 create mode 100644 src/pitchviz/api.py
```

- コミットメッセージは、日本語でも構いません(例:`フェーズ5: 入口の関数と pyproject.toml を追加`)。
- コミットを2つに分けたいときは、`git add pyproject.toml .gitignore` のようにファイルを指定して、「パッケージ化」と「入口の関数」を別々にコミットしても構いません(例:`Add pyproject.toml for editable install` と `Add api.py entry functions`)。

### 7-5. GitHub に push する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git push
```

期待される出力の例:

```
Enumerating objects: xx, done.
...
To https://github.com/あなたのユーザー名/pitchviz.git
   xxxxxxx..yyyyyyy  main -> main
```

- [ ] **[Browser]** GitHub のリポジトリのページを開き、`pyproject.toml` と `src/pitchviz/api.py` が表示され、**`Private`** のままであることを確認する。

### 7-6. 振り返り

次の質問に、1〜2行で自分の言葉で答えてみてください。

1. `pip install -e .` の `-e` は、何のためですか? 付けないと、何が不便ですか?

    → 編集可能にするために必要で、ソースを書き換えても再インストールなしで反映させる
2. `api.py` の関数は、`events=None` を引数にしているのは、なぜですか?

    → 試合ごとに一度のダウンロードで済むため
3. チーム名や選手名が違うとき、`ValueError` で「使える名前の一覧」を見せるのは、なぜですか?

    → 間違えた場合に推測で修正するのを防ぐため。
4. `PROJECT_ROOT = Path(__file__).resolve().parents[2]` は、何をしていますか? Notebook の場所に依存しないのは、なぜですか?

    → `api.py`の場所から、プロジェクトのルートを求めている。呼び出す側の場所に関係なく、同じ`outputs/` と `assets/` を指せるため
5. `requirements.txt` を、`pip freeze` で作り直さなかったのは、なぜですか?

    → 編集可能なインストール行が混ざり、他の人の環境で失敗するため

- [ ] 1に「ソースを書き換えたら、再インストールなしで反映されるようにするため」のように答えられる
- [ ] 2に「何枚も作るとき、同じ試合のデータを何度もダウンロードしなくて済むため」のように答えられる
- [ ] 3に「綴りの間違いに気づけて、推測で別の名前に置き換えるミスも防げるため」のように答えられる
- [ ] 4に「`api.py` の場所から、プロジェクトのルートを求めている。呼び出す側の場所に関係なく、同じ `outputs/` と `assets/` を指せるため」のように答えられる
- [ ] 5に「`-e /Users/...` のような、自分の Mac だけの行が混ざって、他の人の環境で失敗するため」のように答えられる

### 手順7の完了チェック

- [ ] README の進捗に、フェーズ5の行を足した
- [ ] `git status` で、`egg-info` が出ていない(もともと作られていなくても OK)
- [ ] `git commit` で、フェーズ5のコミットを作った
- [ ] `git push` が成功し、GitHub のリポジトリが `Private` のままである

---

## 手順8:つまずきやすい点と対処法

### 8-1. エラー別の対処表

| 症状・エラーメッセージの例 | 原因 | 対処 |
|---|---|---|
| `ERROR: file:///Users/.../pitchviz does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found.` | `pip install -e .` を、`pyproject.toml` のないフォルダで実行した | `cd ~/projects/pitchviz` で移動し、`pwd` と `ls pyproject.toml` で確認してから、やり直す |
| `error: Multiple top-level packages discovered in a flat-layout: ['assets', 'notebooks', 'docs', 'src', ...].` | `pyproject.toml` の `[tool.setuptools.packages.find]` と `where = ["src"]` がない、または綴りが違う | 手順4-2のとおりに、2行を確認する(`where = ["src"]` の `[ ]` と引用符も) |
| `ERROR: Could not find a version that satisfies the requirement setuptools>=61 (from versions: none)` | ネットワークにつながっていない、または pip がインターネットの索引にアクセスできない | ネットワークを確認して、やり直す。会社・学校のネットワークでは、プロキシの設定が必要な場合がある |
| `pyproject.toml` の読み込みで、構文や値のエラーが出る(例:`Invalid statement` や `configuration error: ...`。表示は pip・setuptools の版で違う) | `pyproject.toml` の書き間違い(`"` の閉じ忘れ、`[ ]` の閉じ忘れ、`=` の抜けなど) | エラー文に出る**行番号**の行を確認する。手順4-2の内容と1行ずつ見比べる |
| `ModuleNotFoundError: No module named 'pitchviz'`(Notebook) | Notebook のカーネルが、`pip install -e .` を実行した `.venv` ではない | 右上の `Select Kernel` で `.venv` を選ぶ。セル1の上に `import sys; print(sys.executable)` を足して、`.../pitchviz/.venv/bin/python` になっているか確認する |
| `ModuleNotFoundError: No module named 'pitchviz'`(ターミナル) | `(.venv)` が有効でない、またはインストールしていない | `source .venv/bin/activate` のあと、`python -m pip show pitchviz` で確認する。出なければ、手順4-4をやり直す |
| `ImportError: cannot import name 'make_maps' from 'pitchviz'`(または `list_players` など) | `__init__.py` に書いていない、保存していない、または Notebook が古い `__init__.py` を覚えている | `__init__.py` を確認して保存する。**`%autoreload` は `__init__.py` の変更を拾わないことがある**ので、Notebook の上部の **Restart** で、カーネルを再起動してから、セル1を実行する |
| `ImportError: cannot import name 'find_match_date' from 'pitchviz.loader'` | 手順2の追記を、していない、または保存していない | `loader.py` の末尾を確認して、保存し、Restart する |
| `ImportError: cannot import name 'draw_shot_map' from 'pitchviz.shot_map'`(`api.py` の読み込み時) | フェーズ4の `shot_map.py` が完成していない | フェーズ4の手順7を終える |
| `ImportError: attempted relative import with no known parent package` | `api.py` を、パッケージとしてではなく、単体のファイルとして実行しようとした | `python src/pitchviz/api.py` のように直接実行せず、Notebook から `from pitchviz import ...` で読み込む |
| `ValueError: team 'Japn' is not in this match. teams: ['Belgium', 'Japan']` | チーム名の綴りが、データの表記と違う | エラー文の `teams: [...]` の中から、**一字一句コピー**して使う(`Japan Women's` の `'` の形に注意) |
| `ValueError: no shots found for player '...' (Japan). players: [...]`(または `no passes found`) | 選手名の綴りが違う、または、その選手が、この試合でシュート(パス)をしていない。**PK戦(延長後のPK)のシュートは、ショットマップに含めない**ため、PK戦だけで蹴った選手も該当する | `players: [...]` の一覧から、一字一句コピーして使う。一覧にいるのに出る場合は、その選手の、その種類のイベントがなかっただけ(例:シュートを打っていない)。別の選手を選ぶ |
| `ValueError: match_id 7584 is not in the matches table` | `matches` が、その試合を含まない大会・チームの絞り込みで作られている | セル2の `get_competitions("World Cup")` と `get_team_matches(..., "Japan")` の絞り込みを、フェーズ2のあなたの手順に合わせる。`matches[["match_id", "match_date"]]` を表示して、あなたの `match_id` があるか確認する |
| `TypeError: make_pass_map() got an unexpected keyword argument 'player'` | 引数の名前の間違い。正しくは `player_name` | `make_pass_map(MATCH_ID, TEAM_NAME, player_name=...)` に直す |
| `TypeError: make_pass_map() missing 1 required positional argument: 'team_name'` | 必須の引数(`match_id`、`team_name`)が足りない | 最初の2つは、`match_id`、`team_name` の順に必ず渡す |
| `UnicodeEncodeError` や、文字が `?`/`□` になる(ファイル名や図のタイトル) | 選手名に、`ō` のような記号つきの文字が入っている | **ファイル名**は、`make_filename` が英小文字と数字以外を `_` に置き換える(例:`Gen Shōji` → `gen_sh_ji`)ので、保存はできる。図の中の文字が `□` になるときは、フォントの問題(フェーズ3の手順5と同じ) |
| 同じ相手と2回対戦した試合の画像が、上書きされる | ファイル名が `種別_チーム名_相手チーム名.png` で、`match_id` や日付を含まない | `output_dir=...` で保存先のフォルダを分ける(例:`output_dir=PROJECT_ROOT / "outputs" / "match_7584"`)。ファイル名に `match_id` を足す改造は、発展課題として、フェーズ6のあとで考える |
| `[warn] logo not found: /Users/.../assets/statsbomb_logo_white.png` | ロゴのファイルがない、または名前が違う(`api.py` は、プロジェクトのルートの `assets/` を見る) | ターミナルで `ls assets` を実行して、ファイル名を確認する(フェーズ3の手順1-4)。ロゴなしで保存したいときは、`logo_path=None` を渡す |
| `RuntimeWarning: More than 20 figures have been opened.` | 自分で `draw_...` を呼んで、`plt.close(fig)` せずに、何枚も作った | `make_...` 関数を使う(`plt.close(fig)` が入っている)。自分で `draw_...` を呼ぶときは、`plt.close(fig)` を忘れない |
| `api.py` を直したのに、結果が変わらない | 古い内容を覚えたままになっている | セル1に `%autoreload 2` があるか確認する。なければ Restart してセル1から実行し直す |
| `git check-ignore -v src/pitchviz.egg-info` を実行しても、何も表示されない | `src/pitchviz.egg-info` というフォルダが、そもそも存在しない(新しい pip・setuptools では作られない)。または、`.gitignore` の追記漏れ | `ls src` で、フォルダがあるか確認する。ない場合は正常なので、確認不要。ある場合は、`.gitignore` に `*.egg-info/` があるか確認する |
| `git status` に `src/pitchviz.egg-info/` が出る | `.gitignore` に `*.egg-info/` を足していない | 手順4-3を確認して保存する。すでに `git add` してしまったときは、`git rm -r --cached src/pitchviz.egg-info` で、Git の記録だけから外す |
| `requirements.txt` に `-e /Users/...` の行が入ってしまった | `pip freeze > requirements.txt` を、再実行した | `git restore requirements.txt` で、コミット済みの版に戻す(コミット前に気づいたとき) |
| Notebook に、前の画像が残っていて、新しい画像か分からない | セルの出力が、古いまま | セルを再実行して、出力を更新する。保存先のファイルの更新時刻は、`ls -l outputs` で確認できる |

### 8-2. 「動いているけれど、合っているか分からない」ときの確認方法

- **フェーズ3・4の画像と見比べる**:`make_pass_map(MATCH_ID, TEAM_NAME)` の画像は、フェーズ3のセル12と同じ内容のはず。違えば、`api.py` の接続(`get_passes` の引数など)を疑う。
- **選手の図は、チームの図の「一部」になる**:選手のシュートの数は、チームのシュートの数以下。選手全員を足すと、チーム全体の数になる。
- **相手チームの図と取り違えていないか**:`make_shot_map(MATCH_ID, "Belgium")` の図のタイトルが `Belgium shot map vs Japan` になっているか確認する(`get_opponent` の動作確認)。
- **`events` を渡した場合と、渡さない場合で、同じ画像になるか**:`events=events` を省いた呼び出しと、同じファイルができるか確認する(ダウンロードが入るぶん、遅いだけ)。

---

## 手順9:Claude / ChatGPT に質問するときのコツ(関数化・パッケージ化編)

### 9-1. 関数化・パッケージ化の質問に、必ず入れるもの

1. **やりたいこと**:「`pip install -e .` で、`pitchviz` を読み込めるようにしたい」
2. **実行したコマンドと、その出力の全文**(最初のエラー行から、最後まで)
3. **`pyproject.toml` の全文**(貼るとき、コードブロックにする)
4. **環境の確認結果**:ターミナルで次を実行した出力

```bash
pwd
which python
python --version
python -m pip show pitchviz
```

5. **ファイルの構成**:`ls src/pitchviz` の出力
6. **Notebook の場合**:`import sys; print(sys.executable)` の出力(どの Python を使っているかを示す)

### 9-2. 質問の例

> macOS、Python 3.13.3、VS Code の Jupyter で、`src` レイアウトの Python パッケージ(`src/pitchviz/`)を、`pip install -e .` でインストールしました。ターミナルでは `import pitchviz` できるのですが、Notebook では `ModuleNotFoundError: No module named 'pitchviz'` になります。
>
> `sys.executable` の出力は `/usr/local/bin/python3` でした。`pip show pitchviz` の `Location` は `.../pitchviz/.venv/lib/python3.13/site-packages` です。
>
> 原因として何が考えられますか? 初学者向けに、確認の手順を教えてください。

### 9-3. 回答の使い方

- AI が示した `pyproject.toml` の項目名(`[project]`、`[tool.setuptools...]` など)は、**必ず公式ドキュメント(setuptools、Python Packaging User Guide)で実在を確認**する。版によって、書き方が変わることがあります。
- 「`setup.py` を作る」「`PYTHONPATH` を変える」と提案されたら、**手順4の方法(`pyproject.toml` + `pip install -e .`)と、何が違うのか**を質問してから、実行する。
- 分からないまま貼らず、「この1行は何をしますか?」と聞いてから実行する。

---

## このフェーズ終了時のディレクトリツリー

`NEW` は新しく作ったファイル、`MOD` は変更したファイルです。

```
~/projects/pitchviz/
├── .git/
├── .gitignore                         # MOD(*.egg-info/ を追加)
├── .venv/
├── README.md                          # MOD(進捗を追記)
├── pyproject.toml                     # NEW(パッケージ設定)
├── requirements.txt
├── assets/
│   ├── statsbomb_logo_white.png       # (フェーズ3。Git管理外)
│   └── statsbomb_logo_default.png     # (フェーズ3。Git管理外)
├── docs/
│   ├── 00_overview.md
│   ├── phase1_setup.md
│   ├── phase2_data.md
│   ├── phase3_passmap.md
│   ├── phase4_shotmap.md
│   └── phase5_function.md             # NEW
├── notebooks/
│   ├── 01_setup_check.ipynb
│   ├── 02_explore_data.ipynb
│   ├── 03_pass_map.ipynb
│   ├── 04_shot_map.ipynb
│   └── 05_use_function.ipynb          # NEW
├── src/
│   ├── pitchviz.egg-info/             # NEW?(pip の版によっては作られない。作られても Git管理外)
│   └── pitchviz/
│       ├── __init__.py                # MOD(4つの関数を公開)
│       ├── loader.py                  # MOD(find_match_date を追加)
│       ├── pass_map.py
│       ├── shot_map.py
│       └── api.py                     # NEW(make_pass_map / make_shot_map / make_maps など)
├── outputs/
│   ├── .gitkeep
│   ├── empty_pitch.png                # (フェーズ1。Git管理外)
│   ├── dark_pitch.png                 # (フェーズ1。Git管理外)
│   ├── pass_map_japan_belgium.png     # (フェーズ3。Git管理外。今回上書きされる)
│   ├── pass_map_belgium_japan.png     # (フェーズ3。Git管理外。今回上書きされる)
│   ├── shot_map_japan_belgium.png     # (フェーズ4。Git管理外。今回上書きされる)
│   ├── shot_map_belgium_japan.png     # (フェーズ4。Git管理外。今回上書きされる)
│   ├── pass_map_genki_haraguchi_belgium.png   # NEW(選手指定。例。Git管理外)
│   └── shot_map_genki_haraguchi_belgium.png   # NEW(選手指定。例。Git管理外)
└── data/                              # (空。Git管理外)
```

- `00_overview.md` の完成形のツリーと比べると、`assets/`(フェーズ3で追加)と `outputs/` の各画像、`src/pitchviz.egg-info/`(自動生成。環境によっては作られません)が増えています。いずれも、手順書の進行上、必要になって増えたものです。

---

## フェーズ5 最終チェックリスト

**関数とパッケージ**

- [ ] `src/pitchviz/api.py` に、`make_pass_map`・`make_shot_map`・`make_maps`・`list_players` がある
- [ ] `pyproject.toml` があり、`pip install -e .` が成功している
- [ ] ホームフォルダ(`~`)から `import pitchviz` できる
- [ ] Notebook に `sys.path.append("../src")` を書かなくても、`from pitchviz import ...` できる

**動くもの**

- [ ] `make_pass_map(MATCH_ID, TEAM_NAME, match_date=...)` の1行で、パスマップが保存される
- [ ] `make_shot_map(...)` の1行で、ショットマップが保存される
- [ ] `player_name=` を渡すと、その選手だけの画像が保存される
- [ ] `make_maps(...)` で、パスマップとショットマップの2枚が保存される
- [ ] 間違ったチーム名・選手名で、使える名前の一覧つきの `ValueError` が出る

**Git / GitHub**

- [ ] `git log --oneline` に、フェーズ5のコミットがある
- [ ] `outputs/` の PNG が Git の対象外になっている(`src/pitchviz.egg-info/` がある環境では、それも対象外になっている)
- [ ] `requirements.txt` に `-e` の行が入っていない
- [ ] GitHub のリポジトリが `Private` のままである

すべてにチェックが付けば、フェーズ5は完了です。

---

## 次のフェーズへ

フェーズ6では、**README を完成させて、GitHub で公開する準備**をします。

- `README.md` に、このツールの説明・インストール方法(`pip install -r requirements.txt` と `pip install -e .`)・使い方(`make_maps(...)` の1行)・サンプル画像・StatsBomb のクレジットを書く
- StatsBomb のロゴと、Notebook に残ったデータ・画像を、公開してよいかを整理する(利用条件の再確認)
- Notebook の出力を消して、公開前の確認をする
- リポジトリを `Public` にするかを決めて、GitHub で公開する

準備ができたら「フェーズ6をお願いします」と指示してください。

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| setuptools(`pyproject.toml`・`src` レイアウト) | `https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html` |
| Python Packaging User Guide | `https://packaging.python.org/en/latest/guides/writing-pyproject-toml/` |
| pip(編集可能インストール) | `https://pip.pypa.io/en/stable/topics/local-project-installs/` |
| matplotlib(`pyplot.close`) | `https://matplotlib.org/stable/`(`matplotlib.pyplot.close`) |
| mplsoccer(API・ギャラリー) | `https://mplsoccer.readthedocs.io` |
| pandas(`DataFrame.iloc`・`Series.dropna`) | `https://pandas.pydata.org/docs/` |
| StatsBomb Open Data(データ・仕様書・利用条件) | `https://github.com/statsbomb/open-data`(`doc` フォルダ、`LICENSE.pdf`) |
