# フェーズ4:ショットマップ

> 保存先:`~/projects/pitchviz/docs/phase4_shotmap.md`
> このフェーズの終わりには「選んだ試合の、チームごとのショットマップが `outputs/` に PNG で保存される」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | フェーズ2・3で扱ったイベントデータからシュートを取り出し、ゴール前の半面ピッチに、xG をマーカーの大きさに反映して描き、PNG として保存する |
| 想定所要時間 | 約6時間(下の内訳を参照) |
| 終了時の「動くもの」 | `outputs/shot_map_チーム名_相手チーム名.png` が、両チーム分(2枚)保存される。画像には、シュート位置、xG(マーカーの大きさ)、ゴールか否か(色と塗り)、タイトル、StatsBomb のロゴと出典が入る |

### 作業ラベルの見方

- **[Terminal]**:ターミナルでの作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 事前準備(状態確認・前フェーズの成果確認・xG とは) | 0.5h |
| 2 | Notebook の作成と、シュートの取り出し | 0.75h |
| 3 | まず1本、次に全部のシュートを描く | 0.75h |
| 4 | xG を大きさに、ゴールか否かを色に反映する(課題1・2) | 1.0h |
| 5 | 見た目を整える(タイトル・凡例・出典) | 0.75h |
| 6 | ロゴを入れて PNG として保存する | 0.5h |
| 7 | 関数にまとめる(課題3・4) | 1.0h |
| 8 | README・コミット・振り返り | 0.75h |
| | 合計 | 6.0h |

### このフェーズについての大事な前提

- **コードの確認範囲について**:この手順書の作成環境では、mplsoccer 本体を入手できず、実際には動かせていません。代わりに、同じ呼び出し方を受け付ける代用品と、StatsBomb と同じ列構造の架空のイベントデータ(PK戦のシュートも含む)で、手順書のコードを**セル1〜11まで最後まで実行**して確認しました。確認できたのは、シュートの取り出し(PK戦の除外、xG の空欄の処理を含む)、マーカーの大きさの計算、ゴールか否かの分け方、凡例・タイトル・ロゴの配置、ファイル名の生成、PNG の保存です。**本物の mplsoccer での見た目(マーカーの大きさ・半面ピッチの余白・ゴールの描かれ方)は、あなたの環境で初めて確認することになります。**
- mplsoccer の使い方は、公式ドキュメント(ギャラリーの「Plot scatter」の shot map の例)で確認した引数にもとづいています。ライブラリの更新で引数名が変わる可能性があるため、エラーが出たら手順9の対処表と、[mplsoccer 公式ドキュメント](https://mplsoccer.readthedocs.io)を確認してください。
- **「期待される出力」の数字は例です。** シュート数や xG は、あなたが選んだ試合によって違います。
- このフェーズで使うチーム名・`match_id`・日付は、**フェーズ2の手順4-7のメモの値**です(フェーズ3と同じ試合を使うと、パスマップと見比べられます)。
- **このフェーズは、フェーズ3の成果(`assets/` のロゴ、`pass_map.py` の `add_logo`・`save_figure`・`make_filename`)を使います。** フェーズ3が終わっていない場合は、先に終えてください。
- **リポジトリは Private のままにしてください。** このフェーズの Notebook にも、データの行や、データから作った画像が出力として残ります。公開の前の整理は、フェーズ6で行います(StatsBomb の利用条件で、データの再配布が禁止されているためです)。

### 今回作るものの流れ

```
events(1試合の全イベント)
   │  loader.get_shots()   … 指定チームのシュートだけにし、位置・xG・ゴールか否かを付ける
   ▼
shots(x, y, xg, is_goal)
   │  shot_map.draw_shot_map()  … 半面ピッチにマーカーを描き、タイトル・凡例・ロゴを付ける
   ▼
fig(図)
   │  pass_map.save_figure()    … フェーズ3の関数で PNG として保存する
   ▼
outputs/shot_map_japan_belgium.png
```

---

## 手順1:事前準備(状態確認・前フェーズの成果確認・xG とは)

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

- フェーズ3のコミットが済んでいない場合は、先にフェーズ3の手順9を終えてください(`Your branch is ahead of ...` と出ても問題ありません)。

### 1-2. フェーズ3の成果が残っているか確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
ls assets src/pitchviz
```

期待される出力:

```
assets:
statsbomb_logo_default.png	statsbomb_logo_white.png

src/pitchviz:
__init__.py	loader.py	pass_map.py
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、フェーズ3の関数を読み込めるか確認する。

```bash
python -c "import sys; sys.path.append('src'); from pitchviz.pass_map import add_logo, save_figure, make_filename; print('ok')"
```

期待される出力:

```
ok
```

- `ModuleNotFoundError` や `ImportError` が出たら、フェーズ3の手順8(`pass_map.py`)が終わっていません。先にそちらを終えてください。

### 1-3. フェーズ2のメモを手元に用意する

```
使うチーム名:     Japan(例:Japan)
使う match_id:    7584(例:7584)
対戦カードと日付: Belgium vs Japan(例:2018-07-02 Belgium vs Japan)
```

- 忘れた場合は、`notebooks/03_pass_map.ipynb` のセル2や、`notebooks/02_explore_data.ipynb` のセル10・11の出力で確認します。

### 1-4. xG とは(先に押さえる)

xG(エックスジー、expected goals)は、**「そのシュートが、ゴールになる確率」**を0〜1の数字で表したものです。

| xG の値 | 意味 | 例 |
|---|---|---|
| 0.03 | ゴールになる確率が約3% | ゴールから遠い位置からのシュート |
| 0.30 | 約30% | ペナルティエリア内の、やや良い位置 |
| 0.78 | 約78% | ペナルティキック(PK)など、決定機 |

- シュートの位置、角度、体の部位、状況などから、StatsBomb が計算した値が、データの `shot_statsbomb_xg` 列に入っています。
- 1試合の xG を合計すると、「そのチームが、チャンスの質から見て何点くらい取れていたか」の目安になります。実際の得点とは一致しません(それが分析の面白いところです)。

**このフェーズで使う座標の決まり**(フェーズ2・3の復習)

- シュートの位置は、`location` 列の `[x, y]` に入っています。x は 0〜120、y は 0〜80 です。
- どちらのチームも、**x が大きい方(120)のゴールに向かって攻める**向きに記録されています。
- したがって、シュートはほとんどが x = 80〜120 の付近、つまり**相手ゴール前の半分**に集まります。今回は、その半面だけを、ゴールが上になる向きで描きます。

### 手順1の完了チェック

- [ ] `(.venv)` が行頭に表示されている
- [ ] フェーズ3の `add_logo` などを読み込めた(`ok` と表示された)
- [ ] `assets/` にロゴ、`src/pitchviz/` に `loader.py` と `pass_map.py` がある
- [ ] フェーズ2のメモ(チーム名・`match_id`・日付)が手元にある
- [ ] xG が「ゴールになる確率」であることを説明できる

---

## 手順2:Notebook の作成と、シュートの取り出し

**所要時間:約0.75時間**

### 2-1. Notebook を作る

- [ ] **[VS Code]** Explorer で `notebooks` フォルダを右クリック → `New File` → `04_shot_map.ipynb` と入力して Enter。
  - **対象**:`notebooks/04_shot_map.ipynb`
  - **新規作成か編集か**:新規作成
- [ ] **[VS Code]** 右上の `Select Kernel` → `Python Environments...` → `.venv` を選ぶ。

> **セルの使い方**(これまでと同じ)
> `+ Code` でセルを追加し、`Shift + Enter` で実行します。**セルは番号順(上から順)に実行してください。** 動かなくなったら、上部の **Restart** を押し、セル1から順に実行し直します。

### 2-2. セル1:準備と、色・大きさの設定

- [ ] **[VS Code]** 最初のセルに、次を入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル1**

```python
# notebooks/04_shot_map.ipynb  セル1
%load_ext autoreload
%autoreload 2

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import VerticalPitch

# src フォルダを import の探索先に追加する(自作の loader.py などを使うため)
sys.path.append("../src")

pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 200)

# 図の色(フェーズ3と同じ暗い緑の背景)
BG_COLOR = "#22312b"      # 背景・ピッチの色
LINE_COLOR = "#c7d5cc"    # ピッチのラインの色
TEXT_COLOR = "#e8efe9"    # 文字の色
GOAL_COLOR = "#f2c14e"    # ゴールになったシュートの色(金色)
MISS_COLOR = "#6cb2eb"    # ゴールにならなかったシュートの色(青)

# マーカーの大きさ = SIZE_BASE + SIZE_SCALE × xG
SIZE_BASE = 80
SIZE_SCALE = 1000
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `from mplsoccer import VerticalPitch` | **縦向き**のピッチを描くクラス。フェーズ3の `Pitch`(横向き)の縦版 |
| `BG_COLOR` などの色 | フェーズ3と同じ。ゴールは金色の塗りつぶし、ゴールにならなかったものは青の半透明にして、**色だけでなく「塗りの濃さ」でも区別**します(色の見分けにくい人にも分かりやすくするため) |
| `SIZE_BASE` と `SIZE_SCALE` | マーカーの大きさの計算に使う2つの数字。手順4で使う |

**期待される出力**

- 何も表示されなくて正常です(エラーが出なければ成功)。

### 2-3. セル2:使う試合を指定して、イベントを読み込む

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル2**
  - **`TEAM_NAME` `MATCH_ID` `MATCH_DATE` は、手順1-3のメモの値に置き換えます。** 下の値は例です。

```python
# notebooks/04_shot_map.ipynb  セル2
from pitchviz.loader import get_events

TEAM_NAME = "Japan"       # フェーズ2のメモの値に置き換える(例)
MATCH_ID = 7584           # フェーズ2のメモの値に置き換える(例)
MATCH_DATE = "2018-07-02" # フェーズ2のメモの日付に置き換える(例)

events = get_events(MATCH_ID)
teams = list(events["team"].unique())
opponent_name = [t for t in teams if t != TEAM_NAME][0]

print(events.shape)
print(teams, "->", TEAM_NAME, "vs", opponent_name)
```

**コードの解説**

- フェーズ3のセル2と同じです。`get_events` は、フェーズ2で作った自作の関数です。
- `opponent_name` は、2チームのうち、自分のチーム**以外**の名前です。

**期待される出力の例**

```
NoAuthWarning: credentials were not supplied. Open data access only
(3xxx, 1xx)
['Belgium', 'Japan'] -> Japan vs Belgium
```

**確認すること**

- [ ] 2つのチーム名が表示され、`TEAM_NAME` が一字一句同じ文字列で含まれている

### 2-4. セル3:シュートを取り出し、位置・xG・ゴールか否かを作る

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル3**

```python
# notebooks/04_shot_map.ipynb  セル3
shots = events[(events["type"] == "Shot") & (events["team"] == TEAM_NAME)].copy()
print(shots["period"].value_counts().sort_index())   # どの時間帯のシュートか(5 は PK戦)

shots = shots[shots["period"] < 5].copy()            # PK戦(period が 5)のシュートを除く

shots["x"] = shots["location"].str[0]
shots["y"] = shots["location"].str[1]
shots["xg"] = shots["shot_statsbomb_xg"].fillna(0.0)
shots["is_goal"] = shots["shot_outcome"] == "Goal"

print("shots:", len(shots), " goals:", int(shots["is_goal"].sum()), " xG total:", round(shots["xg"].sum(), 2))
print(shots["shot_outcome"].value_counts())
shots[["minute", "period", "player", "x", "y", "xg", "shot_outcome", "shot_type", "is_goal"]].head()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `events["type"] == "Shot"` | イベントの種類が `Shot`(シュート)の行 |
| `shots["period"].value_counts().sort_index()` | どの時間帯(period)のシュートかを数える。**1と2が前半・後半、3と4が延長、5がPK戦**(仕様は、StatsBomb の仕様書で確認してください) |
| `shots[shots["period"] < 5].copy()` | `period` が5未満の行だけを残す。**PK戦のシュートは、試合中のシュートではなく、xG も付かないことがあるので、除く** |
| `shots["location"].str[0]` | シュートを打った位置 `[x, y]` の0番目(x)を取り出す。フェーズ2・3と同じ考え方 |
| `shots["shot_statsbomb_xg"].fillna(0.0)` | シュートの xG が入っている列を、短い名前 `xg` の列にコピーする。空欄(`NaN`)は 0.0 で埋める(空欄のままだと、合計やマーカーの大きさの計算で困るため) |
| `shots["shot_outcome"] == "Goal"` | 結果が `Goal` か判定する。True ならゴール |
| `value_counts()` | 結果の種類ごとの個数を数える(`Goal`、`Saved`、`Off T`、`Blocked`、`Post`、`Wayward` など) |

**期待される出力の例**

```
period
1    6
2    7
Name: count, dtype: int64
shots: 13  goals: 2  xG total: 1.62
shot_outcome
Off T      4
Blocked    3
Saved      3
Goal       2
Wayward    1
Name: count, dtype: int64
```

続いて、`minute`、`period`、`player`、`x`、`y`、`xg`、`shot_outcome`、`shot_type`、`is_goal` の表が表示されます。

**確認すること**

- [ ] `shots` の数が、数本〜20本程度になっている(パスと違って、1試合のシュートは少ないです)
- [ ] `x` が、おおむね80〜120の範囲に入っている(相手ゴール前)
- [ ] `xg` の合計が、0.5〜4程度の範囲になっている
- [ ] `goals` が、その試合のそのチームの得点と近い(**オウンゴールはシュートではない**ので、相手のオウンゴールによる得点は含まれません。**PK戦のゴールも、得点には数えない**ので、除いています)
- [ ] 1つ目の出力に `5` の行がある場合は、その試合にPK戦があった(その分は、除かれています)

> **シュートが0本だった場合**:`KeyError: 'shot_statsbomb_xg'` になることがあります。その試合・チームにシュートがなく、列そのものが作られなかったためです。`TEAM_NAME` の綴りを確認するか、別の試合を選んでください。

### 手順2の完了チェック

- [ ] カーネルが `.venv` になっている
- [ ] セル2で、2つのチーム名と対戦相手の名前が出た
- [ ] セル3で、`x`、`y`、`xg`、`is_goal` の列ができ、シュート数・ゴール数・xG の合計が表示された

---

## 手順3:まず1本、次に全部のシュートを描く

**所要時間:約0.75時間**

フェーズ3と同じく、**まず1本だけ**描いて仕組みを確認し、そのあと全部を描きます。

### 3-1. セル4:1本のシュートを描く

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル4**

```python
# notebooks/04_shot_map.ipynb  セル4
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pad_bottom=0.5, goal_type="box",
                      pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(8, 7))
fig.set_facecolor(BG_COLOR)

first = shots.head(1)   # 先頭の1行(1本のシュート)
pitch.scatter(first.x, first.y, s=300, c=MISS_COLOR, edgecolors=LINE_COLOR, ax=ax)
plt.show()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `VerticalPitch(...)` | **縦向き**のピッチの設計図。フェーズ3の `Pitch` と同じ引数に加えて、下の3つを指定する |
| `half=True` | ピッチの**半分だけ**を描く。StatsBomb の座標では、ゴールのある x が大きい側が描かれる |
| `pad_bottom=0.5` | 半分の線(ハーフウェイライン)より、少し先まで描く余白。公式ギャラリーのショットマップの例に合わせた値 |
| `goal_type="box"` | ゴールを、四角い枠で描く |
| `pitch.scatter(x, y, s=, c=, edgecolors=, ax=)` | 点(マーカー)を描く。`s` は大きさ、`c` は塗りの色、`edgecolors` は縁の色 |
| `x`、`y` の渡し方 | **縦向きでも、データの x・y をそのまま渡します。** 向きの入れ替えは、`VerticalPitch` が自動でやってくれます |

**期待される出力**

- 暗い緑の**縦長の半面ピッチ**(上がゴール側)に、青い点が**1つ**描かれる。

**確認すること**

- [ ] 点が、ゴールのある上側の半分の、`shots.head(1)` の `x`・`y` に合った位置にある(例:`x=98, y=47` なら、ゴールに近い、ほぼ中央)
- [ ] ゴールが上にある(下にある場合は、`VerticalPitch` ではなく `Pitch` を使っていないか確認する)

### 3-2. セル5:全部のシュートを描く(大きさは同じ)

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル5**

```python
# notebooks/04_shot_map.ipynb  セル5
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pad_bottom=0.5, goal_type="box",
                      pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(8, 7))
fig.set_facecolor(BG_COLOR)

pitch.scatter(shots.x, shots.y, s=300, c=MISS_COLOR, edgecolors=LINE_COLOR, alpha=0.8, ax=ax)
plt.show()
```

**期待される出力**

- 全部のシュートが、同じ大きさの青い点で描かれる。
- **ゴールになったかどうかも、xG の大きさも区別できません。** これが、次の手順4で解決する課題です。

### 手順3の完了チェック

- [ ] セル4で、縦長の半面ピッチに点が1つだけ描かれた
- [ ] セル5で、全部のシュートが描かれた
- [ ] シュートの点が、ゴールの前(上側)に集まっている

---

## 手順4:xG を大きさに、ゴールか否かを色に反映する

**所要時間:約1.0時間**

### 4-1. セル6(課題1):xG からマーカーの大きさを計算する

マーカーの大きさ `s` を、**`SIZE_BASE + SIZE_SCALE × xG`** で決めます。xG が大きい(ゴールになりやすい)シュートほど、大きな点になります。

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル6**
  - 空欄を埋めるまでは、エラーになります(正常です)。

```python
# notebooks/04_shot_map.ipynb  セル6(課題1)
shots["size"] = ____ + ____ * shots["xg"]

print(shots[["xg", "size"]].round(2).sort_values("xg").head(3))
print(shots[["xg", "size"]].round(2).sort_values("xg").tail(3))
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目の `____` | セル1で決めた、「どんな xG でも見えるように足す、最低限の大きさ」の変数 |
| 2つ目の `____` | セル1で決めた、「xG に掛ける倍率」の変数 |

**コードの解説(ヒント)**

| 記述 | 意味 |
|---|---|
| `shots["xg"]`(列を丸ごと使った計算) | 全部のシュートについて、一度にまとめて計算する(1本ずつ書かなくてよい) |
| `s` の単位 | 点の**面積**(ポイントの2乗)を表す。大きさが xG に比例するので、「面積で xG を表す」図になる |
| 最低限の大きさを足す理由 | xG がほぼ0のシュートは、足さないと点が小さすぎて見えなくなる |

**期待される出力の例**

```
       xg    size
4    0.02   101.0
9    0.04   121.0
2    0.05   130.0
       xg    size
7    0.18   260.0
11   0.31   390.0
5    0.78  1060.0
```

(`xg` が小さい順の上位3本と、大きい順の上位3本です。`xg=0.78` のように大きなものは、PK などの決定機です。)

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/04_shot_map.ipynb  セル6(課題1)
shots["size"] = SIZE_BASE + SIZE_SCALE * shots["xg"]

print(shots[["xg", "size"]].round(2).sort_values("xg").head(3))
print(shots[["xg", "size"]].round(2).sort_values("xg").tail(3))
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `SIZE_BASE`、2つ目は `SIZE_SCALE`。

**自分のコードが正解と違っても、動いていればOKな例**

- `SIZE_SCALE * shots["xg"] + SIZE_BASE` と、足す順番を逆にした → 動く。結果は同じです。
- `SIZE_BASE` と `SIZE_SCALE` の数字を、セル1で変えた(例:`SIZE_SCALE = 1500`) → 動く。マーカーの大きさの差が、より強調されます。
- `shots["size"] = 300 + 1000 * shots["xg"]` と、数字を直接書いた → 動く。ただし、あとで大きさを調整するときに何か所も直すことになるので、変数にしておくほうが便利です。

**確認の仕方**

- `xg` が大きいほど、`size` も大きくなっている。
- `xg` が0に近いシュートでも、`size` が80程度(`SIZE_BASE`)ある。

</details>

### 4-2. セル7(課題2):ゴールか否かで、色と塗りを分ける

- ゴール:金色で、**不透明に塗りつぶし**、縁を白の太線にする。
- ゴールにならなかったシュート:青で、**半透明**にする。
- ゴールのマーカーを**あとで描く**ことで、重なったときにゴールが上に見えるようにします。

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル7**

```python
# notebooks/04_shot_map.ipynb  セル7(課題2)
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pad_bottom=0.5, goal_type="box",
                      pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(8, 7))
fig.set_facecolor(BG_COLOR)

goals = shots[shots["____"]]        # ゴールになったシュート
no_goals = shots[~shots["____"]]    # ゴールにならなかったシュート

pitch.scatter(no_goals.x, no_goals.y, s=no_goals.____, c=MISS_COLOR, edgecolors=LINE_COLOR,
              alpha=0.55, linewidths=1.2, ax=ax)
pitch.scatter(goals.x, goals.y, s=goals.____, c=GOAL_COLOR, edgecolors="white",
              alpha=1.0, linewidths=2, ax=ax)
plt.show()

print(len(goals) + len(no_goals) == len(shots))
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目・2つ目の `____` | セル3で作った、「ゴールか」を表す True / False の列の名前 |
| 3つ目・4つ目の `____` | セル6で作った、マーカーの大きさが入っている列の名前 |

**コードの解説(ヒント)**

| 記述 | 意味 |
|---|---|
| `shots[shots["列"]]`、`~` | フェーズ3の手順4で練習した、True の行だけを取り出す書き方と、その反転 |
| `s=no_goals.size` | 列を丸ごと渡すと、**1本ごとに違う大きさ**で点が描かれる |
| `alpha=0.55` | 半透明にする(0.55)。重なったシュートが透けて見える |
| `linewidths=2` | 縁の太さ |

**期待される出力**

- 縦長の半面ピッチに、**大きさの違う**点が描かれる。金色の塗りつぶし(縁が白)がゴール、青の半透明がゴールにならなかったシュート。
- ゴールに近い位置のシュートほど、大きな点になっている。
- 最後の行が `True`。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/04_shot_map.ipynb  セル7(課題2)
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pad_bottom=0.5, goal_type="box",
                      pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(8, 7))
fig.set_facecolor(BG_COLOR)

goals = shots[shots["is_goal"]]        # ゴールになったシュート
no_goals = shots[~shots["is_goal"]]    # ゴールにならなかったシュート

pitch.scatter(no_goals.x, no_goals.y, s=no_goals.size, c=MISS_COLOR, edgecolors=LINE_COLOR,
              alpha=0.55, linewidths=1.2, ax=ax)
pitch.scatter(goals.x, goals.y, s=goals.size, c=GOAL_COLOR, edgecolors="white",
              alpha=1.0, linewidths=2, ax=ax)
plt.show()

print(len(goals) + len(no_goals) == len(shots))
```

**答え合わせのあとに**

- 空欄の答え:1つ目・2つ目は `is_goal`、3つ目・4つ目は `size`。

**自分のコードが正解と違っても、動いていればOKな例**

- `no_goals.size` の代わりに `no_goals["size"]` と書いた → 動く。**ドットで書くとき、`size` は表の「要素の数」を表す属性と同じ名前**です。実際には列の値が使われますが、気になる場合は `["size"]` で書くほうが確実です。
- `goals` を先に描いて、`no_goals` をあとに描いた → 動く。ただし、重なったとき、ゴールが青の下に隠れやすくなります。
- `alpha` の値を変えた(例:`0.4`) → 動く。見た目の違いだけです。

**確認の仕方**

- 金色の点と青い点の両方が描かれている(金色が1つもない場合は、`len(goals)` を確認する。ゴールがない試合・チームなら、正常です)。
- 最後の行が `True` になる。

</details>

### 手順4の完了チェック

- [ ] セル6で、`xg` が大きいほど `size` が大きくなることを確認した
- [ ] セル7で、金色(ゴール)と青(ゴールにならなかった)のマーカーが、大きさの違いつきで描かれた
- [ ] 課題1・2を解いて、答え合わせをした

---

## 手順5:見た目を整える(タイトル・凡例・出典)

**所要時間:約0.75時間**

フェーズ3と同じく、`pitch.grid()` でタイトル欄・出典欄を付けます。凡例には、**ゴールか否か**と、**大きさと xG の対応**の両方を入れます。

### 5-1. セル8:タイトル・凡例・出典つきの図を作る

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル8**

```python
# notebooks/04_shot_map.ipynb  セル8
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pad_bottom=0.5, goal_type="box",
                      pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, axs = pitch.grid(figheight=9, title_height=0.10, grid_height=0.78, endnote_height=0.07,
                      title_space=0, endnote_space=0, axis=False)
fig.set_facecolor(BG_COLOR)
ax = axs["pitch"]

goals = shots[shots["is_goal"]]
no_goals = shots[~shots["is_goal"]]

pitch.scatter(no_goals.x, no_goals.y, s=no_goals["size"], c=MISS_COLOR, edgecolors=LINE_COLOR,
              alpha=0.55, linewidths=1.2, ax=ax)
pitch.scatter(goals.x, goals.y, s=goals["size"], c=GOAL_COLOR, edgecolors="white",
              alpha=1.0, linewidths=2, ax=ax)

# 凡例用の見本(データを描かない、空の点)
handles = [
    ax.scatter([], [], s=250, c=GOAL_COLOR, edgecolors="white", linewidths=2,
               label=f"Goal ({len(goals)})"),
    ax.scatter([], [], s=250, c=MISS_COLOR, edgecolors=LINE_COLOR, alpha=0.55, linewidths=1.2,
               label=f"No goal ({len(no_goals)})"),
]
for sample_xg in (0.05, 0.2, 0.5):
    handles.append(ax.scatter([], [], s=SIZE_BASE + SIZE_SCALE * sample_xg, c="none",
                              edgecolors=LINE_COLOR, linewidths=1.2, label=f"xG {sample_xg}"))
ax.legend(handles=handles, loc="lower left", facecolor=BG_COLOR, edgecolor=LINE_COLOR,
          labelcolor=TEXT_COLOR, labelspacing=1.6, borderpad=1.0, fontsize=11)

total_xg = shots["xg"].sum()
axs["title"].text(0.5, 0.68, f"{TEAM_NAME} shot map vs {opponent_name}",
                  color=TEXT_COLOR, ha="center", va="center", fontsize=24,
                  transform=axs["title"].transAxes)
axs["title"].text(0.5, 0.18,
                  f"{MATCH_DATE}   |   {len(shots)} shots, {len(goals)} goals, xG {total_xg:.2f}",
                  color=LINE_COLOR, ha="center", va="center", fontsize=13,
                  transform=axs["title"].transAxes)
axs["endnote"].text(0.01, 0.5, "Data: StatsBomb Open Data   |   marker size = xG",
                    color=TEXT_COLOR, ha="left", va="center", fontsize=11,
                    transform=axs["endnote"].transAxes)
plt.show()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `pitch.grid(...)` | フェーズ3と同じ。ピッチの上下に、タイトル欄・出典欄を持つ図を作る。`VerticalPitch` でも同じ使い方 |
| `s=no_goals["size"]` | マーカーの大きさの列。`["size"]` と書くのは、ドットで書くと表の「要素の数(size)」と紛らわしいため |
| `ax.scatter([], [], ...)` | **データを描かない、空の点**を作る。凡例の見本として使うためだけの点 |
| `c="none"` | 塗りなし(縁だけ)。大きさの見本として使う |
| `for sample_xg in (0.05, 0.2, 0.5):` | xG が 0.05、0.2、0.5 のときの大きさの見本を、3つ作る(同じ処理を3回書かないため) |
| `ax.legend(handles=handles, ...)` | 凡例を表示する。`handles` に、見本の点を渡す |
| `labelspacing=1.6` | 凡例の項目の間隔。大きな点が重ならないように広げる |
| `f"... xG {total_xg:.2f}"` | xG の合計を、小数第2位まで表示する |

**期待される出力**

- 暗い緑の図の上部に、タイトル(例:`Japan shot map vs Belgium`)と、その下に日付・シュート数・ゴール数・xG の合計。
- 縦長の半面ピッチに、大きさの違うマーカー(金色の塗りつぶしと、青い半透明)。
- 凡例(左下)に、`Goal (2)`、`No goal (11)`、`xG 0.05`・`xG 0.2`・`xG 0.5` の大きさの見本。
- 下部の左端に `Data: StatsBomb Open Data   |   marker size = xG`。

**確認すること**

- [ ] 凡例の `Goal (n)` と `No goal (n)` の数が、セル3の `goals` と `shots` の数と合っている
- [ ] `xG 0.05`・`xG 0.2`・`xG 0.5` の見本が、順に大きくなっている
- [ ] 凡例が、シュートの点と重なっていない(重なる場合は、`loc="lower left"` を `"lower right"` などに変える)
- [ ] 文字がすべて**英語**になっている(日本語を入れると、文字が四角(□)になります。フェーズ3の手順5の注意と同じ)

### 手順5の完了チェック

- [ ] セル8で、タイトル・ピッチ・凡例・出典が入った図が表示された
- [ ] 凡例の数が、セル3の数字と合っている
- [ ] 大きさの見本(xG 0.05 / 0.2 / 0.5)が、順に大きくなっている

---

## 手順6:ロゴを入れて PNG として保存する

**所要時間:約0.5時間**

ロゴの置き方と保存は、**フェーズ3で作った関数をそのまま使います**。同じ関数を2つの図に使えるのが、関数にまとめた利点です。

**ロゴの扱いの方針**(フェーズ3と同じ)

- 用意されたバリエーションを、**色や形を変えずに**使う(暗い背景には、白のロゴ)。
- 大きさは変えるが、縦横比は保つ(`add_logo` が自動で保つ)。
- ロゴ・出典の扱いは、フェーズ2の利用条件のメモに従う。

### 6-1. セル9:ロゴを入れて保存する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。セル8を先に実行しておくこと。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル9**
  - ファイル名は、`shot_map_チーム名_相手チーム名.png`(小文字・スペースなし)にします。下の名前は例で、自分の試合の名前に置き換えます(手順7で、自動で作れるようにします)。

```python
# notebooks/04_shot_map.ipynb  セル9
from pitchviz.pass_map import add_logo, save_figure

LOGO_PATH = "../assets/statsbomb_logo_white.png"
OUTPUT_DIR = Path("../outputs")

add_logo(fig, axs["endnote"], LOGO_PATH)
out_path = save_figure(fig, OUTPUT_DIR / "shot_map_japan_belgium.png")   # 例。自分の試合に合わせて変える
print("saved:", out_path)
fig
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `from pitchviz.pass_map import add_logo, save_figure` | フェーズ3で作った2つの関数を読み込む |
| `add_logo(fig, axs["endnote"], LOGO_PATH)` | 図の出典欄の右端に、ロゴを置く。ロゴが見つからないと、警告を出して、何もせずに進む |
| `save_figure(fig, パス)` | PNG として保存し、保存先を返す。保存先のフォルダがなければ作る |
| 最後の `fig` | ロゴを足したあとの図を、もう一度表示する |

**期待される出力**

```
saved: ../outputs/shot_map_japan_belgium.png
```

- セルの下に、ロゴ入りの図が表示される。

**生成されるファイル**

- `outputs/shot_map_japan_belgium.png`

- [ ] **[VS Code]** Explorer で `outputs/shot_map_japan_belgium.png` を開き、次を確認する。
  - 背景が暗い緑で、白くなっていないこと。
  - タイトル・凡例・出典・**ロゴ**がすべて入っていること。

> **メモ**:`outputs/` の PNG は、`.gitignore` により Git の対象外です。

### 手順6の完了チェック

- [ ] `saved: ../outputs/shot_map_....png` と表示された
- [ ] 保存した PNG に、ロゴと `Data: StatsBomb Open Data` の両方が入っている
- [ ] 画像の背景が白くなっていない

---

## 手順7:関数にまとめる

**所要時間:約1.0時間**

フェーズ3と同じ流れで、Notebook で動いたコードを、`.py` ファイルの関数にします。

| 作る関数 | ファイル | 役割 |
|---|---|---|
| `get_shots()` | `src/pitchviz/loader.py`(編集) | イベントから、指定チームのシュートを取り出し、位置・xG・ゴールか否かを付ける |
| `summarize_shots()` | `src/pitchviz/shot_map.py`(新規) | シュート数・ゴール数・xG の合計をまとめる |
| `draw_shot_map()` | `src/pitchviz/shot_map.py`(新規) | ショットマップを描く(セル8の処理を移す) |

**ロゴと保存と、ファイル名は、フェーズ3の `add_logo()`・`save_figure()`・`make_filename()` を再利用します。** 新しく作る必要はありません。

### 7-1. `loader.py` に `get_shots()` を足す(課題3)

- [ ] **[VS Code]** Explorer で `src/pitchviz/loader.py` を開く。
  - **対象**:`src/pitchviz/loader.py`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:ファイルの**末尾**(`get_passes` 関数の後ろ)に、次のコードを追記する。
- [ ] 次のコードの**空欄(`____`)を埋めて**追記し、`Command + S` で保存する。

```python
# src/pitchviz/loader.py (末尾に追記)


def get_shots(events, team_name):
    """指定チームのシュートを返す。x, y(位置)、xg(xG)、is_goal(ゴールか)の列を付ける。

    PK戦(period が 5)のシュートは、試合中のシュートではないので除く。
    """
    shots = filter_events(events, "Shot", team_name)
    shots = shots[shots["____"] < 5]
    shots = add_xy(shots, "location", "x", "y")
    shots["xg"] = shots["____"].fillna(0.0)
    shots["is_goal"] = shots["shot_outcome"] == "____"
    shots = shots.dropna(subset=["x", "y"]).copy()
    return shots.reset_index(drop=True)
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | セル3で `value_counts()` した、「どの時間帯か」を表す列の名前 |
| 2つ目 | シュートの xG が入っている列の名前(セル3で `xg` にコピーした元の列) |
| 3つ目 | ゴールになったシュートの `shot_outcome` の値(セル3で `== "..."` と比べた文字列) |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `filter_events(events, "Shot", team_name)` | フェーズ2で作った関数。種類が `Shot`、チームが `team_name` の行だけを返す |
| `shots[shots["period"] < 5]` | `period` が5未満(前後半と延長)の行だけを残す。**PK戦(5)のシュートを除く** |
| `add_xy(shots, "location", "x", "y")` | フェーズ2で作った関数。`[x, y]` から、x・y の2列を作る |
| `.fillna(0.0)` | xG が空欄の行を、0.0 で埋める(空欄のままだと、合計やマーカーの大きさの計算で困るため) |
| `shots["shot_outcome"] == "Goal"` | ゴールか判定する(セル3と同じ) |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# src/pitchviz/loader.py (末尾に追記)


def get_shots(events, team_name):
    """指定チームのシュートを返す。x, y(位置)、xg(xG)、is_goal(ゴールか)の列を付ける。

    PK戦(period が 5)のシュートは、試合中のシュートではないので除く。
    """
    shots = filter_events(events, "Shot", team_name)
    shots = shots[shots["period"] < 5]
    shots = add_xy(shots, "location", "x", "y")
    shots["xg"] = shots["shot_statsbomb_xg"].fillna(0.0)
    shots["is_goal"] = shots["shot_outcome"] == "Goal"
    shots = shots.dropna(subset=["x", "y"]).copy()
    return shots.reset_index(drop=True)
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `period`、2つ目は `shot_statsbomb_xg`、3つ目は `Goal`。

**自分のコードが正解と違っても、動いていればOKな例**

- `shots[shots["period"] <= 4]` と書いた → 動く。`< 5` と同じ意味です。
- `.fillna(0.0)` を付けなかった → 動くことが多いが、xG が空欄の行があると、マーカーの大きさが空欄になって描かれない場合がある。付けるのが安全です。
- PK戦を除く行(`period` の絞り込み)を書かなかった → 動く。ただし、PK戦のある試合では、PK戦のシュートが図に混ざります(試合中のシュートだけを見たい図としては、不正確になります)。

**確認の仕方**

- 次のセル(7-3)で、`get_shots(events, TEAM_NAME)` の行数が、セル3の `shots` と一致する。

</details>

### 7-2. `shot_map.py` を作る(課題4を含む)

- [ ] **[VS Code]** Explorer で `src/pitchviz` フォルダを右クリック → `New File` → `shot_map.py` と入力して Enter。
  - **対象**:`src/pitchviz/shot_map.py`
  - **新規作成か編集か**:新規作成
- [ ] 次のコードの全文を貼り付けて、`Command + S` で保存する。**`summarize_shots` 関数の空欄(課題4)を埋めてください。**

```python
# src/pitchviz/shot_map.py
"""ショットマップを描く関数(フェーズ4)。色・ロゴはフェーズ3の pass_map.py のものを再利用する。"""

from mplsoccer import VerticalPitch

from .pass_map import BG_COLOR, LINE_COLOR, TEXT_COLOR, add_logo

GOAL_COLOR = "#f2c14e"   # ゴールになったシュート(金色)
MISS_COLOR = "#6cb2eb"   # ゴールにならなかったシュート(青)

# マーカーの大きさ = SIZE_BASE + SIZE_SCALE × xG
SIZE_BASE = 80
SIZE_SCALE = 1000


def summarize_shots(shots):
    """シュート数・ゴール数・xG の合計を、辞書で返す。"""
    return {
        "shots": len(____),
        "goals": int(shots["____"].sum()),
        "xg": float(shots["____"].sum()),
    }


def draw_shot_map(shots, team_name, opponent_name, match_date, logo_path=None):
    """1チーム分のショットマップを描いて、図(Figure)を返す。

    shots は loader.get_shots() の結果(x, y, xg, is_goal の列が必要)。
    図の中の文字は、フォントの都合で英語にする。
    """
    pitch = VerticalPitch(pitch_type="statsbomb", half=True, pad_bottom=0.5, goal_type="box",
                          pitch_color=BG_COLOR, line_color=LINE_COLOR)
    fig, axs = pitch.grid(figheight=9, title_height=0.10, grid_height=0.78, endnote_height=0.07,
                          title_space=0, endnote_space=0, axis=False)
    fig.set_facecolor(BG_COLOR)
    ax = axs["pitch"]

    sizes = SIZE_BASE + SIZE_SCALE * shots["xg"]
    goals = shots[shots["is_goal"]]
    no_goals = shots[~shots["is_goal"]]

    pitch.scatter(no_goals.x, no_goals.y, s=sizes[no_goals.index], c=MISS_COLOR,
                  edgecolors=LINE_COLOR, alpha=0.55, linewidths=1.2, ax=ax)
    pitch.scatter(goals.x, goals.y, s=sizes[goals.index], c=GOAL_COLOR,
                  edgecolors="white", alpha=1.0, linewidths=2, ax=ax)

    # 凡例用の見本(データを描かない、空の点)
    handles = [
        ax.scatter([], [], s=250, c=GOAL_COLOR, edgecolors="white", linewidths=2,
                   label=f"Goal ({len(goals)})"),
        ax.scatter([], [], s=250, c=MISS_COLOR, edgecolors=LINE_COLOR, alpha=0.55, linewidths=1.2,
                   label=f"No goal ({len(no_goals)})"),
    ]
    for sample_xg in (0.05, 0.2, 0.5):
        handles.append(ax.scatter([], [], s=SIZE_BASE + SIZE_SCALE * sample_xg, c="none",
                                  edgecolors=LINE_COLOR, linewidths=1.2, label=f"xG {sample_xg}"))
    ax.legend(handles=handles, loc="lower left", facecolor=BG_COLOR, edgecolor=LINE_COLOR,
              labelcolor=TEXT_COLOR, labelspacing=1.6, borderpad=1.0, fontsize=11)

    summary = summarize_shots(shots)
    axs["title"].text(0.5, 0.68, f"{team_name} shot map vs {opponent_name}",
                      color=TEXT_COLOR, ha="center", va="center", fontsize=24,
                      transform=axs["title"].transAxes)
    axs["title"].text(0.5, 0.18,
                      f"{match_date}   |   {summary['shots']} shots, {summary['goals']} goals, "
                      f"xG {summary['xg']:.2f}",
                      color=LINE_COLOR, ha="center", va="center", fontsize=13,
                      transform=axs["title"].transAxes)
    axs["endnote"].text(0.01, 0.5, "Data: StatsBomb Open Data   |   marker size = xG",
                        color=TEXT_COLOR, ha="left", va="center", fontsize=11,
                        transform=axs["endnote"].transAxes)

    if logo_path is not None:
        add_logo(fig, axs["endnote"], logo_path)
    return fig
```

**ヒント(課題4)**

| 空欄 | ヒント |
|---|---|
| 1つ目 | シュートが全部入っている表(関数の引数の名前) |
| 2つ目 | 「ゴールか」を表す True / False の列の名前(`.sum()` で、True の数 = ゴール数になる) |
| 3つ目 | xG が入っている列の名前(`.sum()` で、xG の合計になる) |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `from .pass_map import ...` | **同じフォルダ(パッケージ)の `pass_map.py` から読み込む**書き方。先頭の `.` が「同じ場所」の意味。フェーズ3で作った色と `add_logo` を再利用する |
| `summarize_shots(shots)` | シュート数、ゴール数、xG の合計を、`{"shots": 13, "goals": 2, "xg": 1.62}` のような辞書で返す。タイトルの文章に使う |
| `sizes = SIZE_BASE + SIZE_SCALE * shots["xg"]` | セル6と同じ計算。表に列を足さず、関数の中だけで使う |
| `sizes[no_goals.index]` | `sizes` から、`no_goals` に含まれる行の分だけを取り出す(`.index` は、行の番号の一覧) |
| `summary['shots']` | 辞書から、キー `shots` の値を取り出す |
| `logo_path=None` | 渡さなければロゴなし(フェーズ3と同じ) |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
def summarize_shots(shots):
    """シュート数・ゴール数・xG の合計を、辞書で返す。"""
    return {
        "shots": len(shots),
        "goals": int(shots["is_goal"].sum()),
        "xg": float(shots["xg"].sum()),
    }
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `shots`、2つ目は `is_goal`、3つ目は `xg`。

**自分のコードが正解と違っても、動いていればOKな例**

- `"shots": shots.shape[0]` と書いた → 動く。`len(shots)` と同じ意味(行数)です。
- `"goals": shots["is_goal"].sum()` と、`int()` を付けなかった → 動くことが多いが、表示するとき `np.int64(2)` のような形になる場合がある。`int()` を付けるのが安全です。
- `"xg": round(shots["xg"].sum(), 2)` と、先に丸めた → 動く。ただし、あとの計算で使うときは、丸めない値のほうが正確です。

**確認の仕方**

- 次のセル(7-3)で、`summarize_shots(get_shots(events, TEAM_NAME))` が、セル3の `shots`・`goals`・xG の合計と一致する。

</details>

### 7-3. セル10:関数を確認する

- [ ] **[VS Code]** Notebook `notebooks/04_shot_map.ipynb` に戻り、次のセルを追加して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル10**

```python
# notebooks/04_shot_map.ipynb  セル10
from pitchviz.loader import get_shots
from pitchviz.pass_map import make_filename
from pitchviz.shot_map import draw_shot_map, summarize_shots

print(make_filename("Japan", "Belgium", prefix="shot_map"))
print(make_filename("Japan Women's", "Norway Women's", prefix="shot_map"))

checked = get_shots(events, TEAM_NAME)
print(len(checked) == len(shots))
print(summarize_shots(checked))
```

**期待される出力の例**

```
shot_map_japan_belgium.png
shot_map_japan_womens_norway_womens.png
True
{'shots': 13, 'goals': 2, 'xg': 1.6203518122434616}
```

**確認すること**

- [ ] 1行目と2行目が、上の出力と一致する(フェーズ3の `make_filename` に、`prefix="shot_map"` を渡すだけで、ファイル名が作れる)
- [ ] 3行目が `True`
- [ ] 4行目の `shots`・`goals` が、セル3の `shots`・`goals` と一致し、`xg` が、セル3の `xG total` を丸める前の値になっている(`xg` の小数点以下は、長くなって構いません)

### 7-4. セル11:両チームのショットマップを、関数で保存する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/04_shot_map.ipynb` の **セル11**

```python
# notebooks/04_shot_map.ipynb  セル11
LOGO_PATH = "../assets/statsbomb_logo_white.png"
OUTPUT_DIR = Path("../outputs")

for team in teams:
    team_shots = get_shots(events, team)
    opponent = [t for t in teams if t != team][0]

    fig = draw_shot_map(team_shots, team, opponent, MATCH_DATE, logo_path=LOGO_PATH)
    out_path = save_figure(fig, OUTPUT_DIR / make_filename(team, opponent, prefix="shot_map"))
    print("saved:", out_path)
```

**コードの解説**

- フェーズ3のセル12と同じ形です。**「取り出す → 描く → 保存する」の3行**で、両チームのショットマップが作れます。`save_figure` は、セル9で読み込んだ、フェーズ3の関数です。

**期待される出力の例**(順番は、チーム名の並びによって違います)

```
saved: ../outputs/shot_map_belgium_japan.png
saved: ../outputs/shot_map_japan_belgium.png
```

- セルの下に、**2つの図**(両チームのショットマップ)が表示される。

**生成されるファイル**

- `outputs/shot_map_belgium_japan.png`
- `outputs/shot_map_japan_belgium.png`

- [ ] **[VS Code]** Explorer の `outputs/` で2つの PNG を開き、次を確認する。
  - それぞれのタイトルのチーム名と、画像の中のシュートが合っている(例:`Japan shot map vs Belgium` の画像で、ゴール数が日本のもの)
  - ロゴと出典が入っている
  - 両チームとも、ゴールが上にある

### 手順7の完了チェック

- [ ] 課題3・4を解いて、答え合わせをした
- [ ] セル10で、ファイル名と、関数の結果の確認が期待どおりに出た
- [ ] セル11で、両チームの PNG が `outputs/` に保存された
- [ ] `loader.py` と `shot_map.py` を書き換えたとき、セルの再実行だけで反映される(`%autoreload` の効果)ことを理解した

---

## 手順8:README・コミット・振り返り

**所要時間:約0.75時間**

### 8-1. README の進捗を更新する

- [ ] **[VS Code]** Explorer で `README.md` を開く。
  - **対象**:`README.md`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:`## 進捗` の下の `- [x] フェーズ3:パスマップ` の**次の行**に、次の1行を足す。
- [ ] 追記して `Command + S` で保存する。

```markdown
- [x] フェーズ4:ショットマップ
```

### 8-2. Notebook を保存する

- [ ] **[VS Code]** `Command + S` で `04_shot_map.ipynb` を保存する。

### 8-3. `git status` で、記録されるものを確認する

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
	modified:   README.md
	modified:   src/pitchviz/loader.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/phase4_shotmap.md
	notebooks/04_shot_map.ipynb
	src/pitchviz/shot_map.py

no changes added to commit (use "git add" and/or "git commit -a")
```

**確認すること**

- `README.md` と `loader.py` が `modified` になっている。
- `docs/phase4_shotmap.md`(この手順書)、`notebooks/04_shot_map.ipynb`、`src/pitchviz/shot_map.py` が Untracked に出る。
- **`assets/`(ロゴ画像)と、`outputs/` の PNG が表示されない**こと(`.gitignore` の効果)。
- `.venv/` や `data/` が出ていないこと。

- [ ] **[Terminal]** `~/projects/pitchviz` で、ロゴと画像が Git の対象外になっていることを確認する。

```bash
git check-ignore -v assets/statsbomb_logo_white.png outputs/shot_map_japan_belgium.png
```

期待される出力の例(行番号は環境で違います):

```
.gitignore:27:assets/*.png	assets/statsbomb_logo_white.png
.gitignore:24:outputs/*	outputs/shot_map_japan_belgium.png
```

### 8-4. ステージングしてコミットする

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
	modified:   README.md
	new file:   docs/phase4_shotmap.md
	new file:   notebooks/04_shot_map.ipynb
	modified:   src/pitchviz/loader.py
	new file:   src/pitchviz/shot_map.py
```

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git commit -m "Phase 4: draw shot maps with xG-sized markers (goal vs no goal, logo, PNG output)"
```

期待される出力の例:

```
[main xxxxxxx] Phase 4: draw shot maps with xG-sized markers (goal vs no goal, logo, PNG output)
 5 files changed, xxx insertions(+)
 create mode 100644 docs/phase4_shotmap.md
 create mode 100644 notebooks/04_shot_map.ipynb
 create mode 100644 src/pitchviz/shot_map.py
```

- コミットメッセージは、日本語でも構いません(例:`フェーズ4: ショットマップの描画と PNG 保存`)。

### 8-5. GitHub に push する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git push
```

期待される出力の例:

```
To https://github.com/あなたのユーザー名/pitchviz.git
   xxxxxxx..yyyyyyy  main -> main
```

- [ ] **[Browser]** `https://github.com/あなたのユーザー名/pitchviz` を開き、次を確認する。
  - `src/pitchviz/shot_map.py` と `notebooks/04_shot_map.ipynb` が表示される。
  - **リポジトリが `Private` のまま**である。
  - `assets/` のロゴ画像が、GitHub 上にない。

### 8-6. 振り返り

次の質問に、1〜2行で自分の言葉で答えてみてください。

1. xG とは何ですか? この図では、どこに反映されていますか?
    
    → シュートの位置、角度、体の部位、状況などから、そのシュートがゴールになる確率をStatsBomb が計算した値でマーカーの大きさに反映している
2. マーカーの大きさを `SIZE_BASE + SIZE_SCALE × xG` にして、`SIZE_BASE` を足したのは、なぜですか?

    → xG がほぼ0のシュートでも点が小さすぎて見れない状況を防ぐため
3. ゴールと、ゴールにならなかったシュートを、**色だけでなく、塗りの濃さ(透明度)でも**区別したのは、なぜですか?

    → 重なったしまった点も見えやすくするため
4. `get_shots` で `period < 5` と絞り込んだのは、なぜですか?

    → PK戦のシュートは除外するため
5. `shot_map.py` が、`pass_map.py` の `add_logo` を再利用できるのは、なぜ便利ですか?

    → 同じ処理を2回書かずに済み、直すときも1箇所で済むため

- [ ] 1に「ゴールになる確率で、マーカーの大きさに反映している」のように答えられる
- [ ] 2に「xG がほぼ0のシュートでも、点が小さすぎて見えなくならないようにするため」のように答えられる
- [ ] 3に「色の見分けにくい人にも区別しやすくするため(色だけに頼らない)」のように答えられる
- [ ] 4に「PK戦(period 5)のシュートは、試合中のシュートではなく、図に混ざらないようにするため」のように答えられる
- [ ] 5に「同じ処理を2回書かずに済み、直すときも1か所で済むため」のように答えられる

### 手順8の完了チェック

- [ ] README に、フェーズ4の進捗が追記された
- [ ] `git status` で、想定したファイルだけが表示された(ロゴと PNG は表示されない)
- [ ] `git commit` と `git push` が成功した
- [ ] GitHub のリポジトリが `Private` のままである
- [ ] 振り返りの5問に答えられた

---

## 手順9:つまずきやすい点と対処法

### 9-1. エラー別の対処表

| 症状・エラーメッセージの例 | 原因 | 対処 |
|---|---|---|
| `NoAuthWarning: credentials were not supplied. Open data access only` | 有料 API のログイン情報がない(**警告であり、エラーではない**) | 無視して構いません |
| `ImportError: cannot import name 'VerticalPitch' from 'mplsoccer'` | mplsoccer が古い、またはインストールが壊れている | `pip list` で mplsoccer の版を確認する。[公式ドキュメント](https://mplsoccer.readthedocs.io)で、`VerticalPitch` が使える版か確認する |
| `ImportError: cannot import name 'add_logo' from 'pitchviz.pass_map'` | フェーズ3の `pass_map.py` が、完成していない | フェーズ3の手順8を終える。`pass_map.py` に `add_logo` があるか確認して保存する |
| `ImportError: attempted relative import with no known parent package` | `shot_map.py` を、パッケージとしてではなく、単体のファイルとして実行しようとした | Notebook から `from pitchviz.shot_map import ...` で読み込む(`.py` ファイルを直接実行しない) |
| `ModuleNotFoundError: No module named 'pitchviz'` | セル1の `sys.path.append("../src")` を実行していない、または `src/pitchviz/__init__.py` がない | セル1を実行し直す。`src/pitchviz/__init__.py` があるか確認する |
| `ImportError: cannot import name 'get_shots' from 'pitchviz.loader'` | 課題3の関数を `loader.py` に追記していない、または保存していない | `loader.py` の末尾に関数があるか確認し、保存してから Restart する |
| `NameError: name 'shots' is not defined`(または `fig`、`axs`、`events`) | 前のセルを実行していない、または Restart のあとに実行し直していない | Restart して、セル1から順に実行する。セル9は、セル8を先に実行しておく |
| `KeyError: 'shot_statsbomb_xg'`(または `'shot_outcome'`) | その試合・チームにシュートがなく、列が作られなかった。またはチーム名の綴りが違う | セル2の `print(teams)` でチーム名を確認する。`events["type"].value_counts()` に `Shot` があるか確認する。なければ別の試合を選ぶ |
| `KeyError: 'size'` | セル6(課題1)を実行していない | セル6を実行する。または、`shots["size"] = SIZE_BASE + SIZE_SCALE * shots["xg"]` を実行する |
| `NameError: name 'SIZE_BASE' is not defined` | セル1を実行していない | セル1を実行する |
| `IndexError: list index out of range`(`opponent_name = [...][0]` の行) | `TEAM_NAME` が、`events["team"]` のどの名前とも一致しない | セル2の `print(teams)` で、チーム名の綴りを確認して、一字一句同じにする |
| `TypeError: __init__() got an unexpected keyword argument 'pad_bottom'`(または `goal_type`、`half`) | mplsoccer の更新で、引数の名前が変わった | [公式ドキュメント](https://mplsoccer.readthedocs.io)の `VerticalPitch`(API)と、ギャラリーの「Plot scatter」のショットマップの例を確認する |
| `TypeError: grid() got an unexpected keyword argument '...'` | `pitch.grid` の引数名の更新、または綴りの間違い | 公式ドキュメントの `Pitch.grid` の引数を確認する |
| 点が1つも描かれない | `shots` が空(チーム名の不一致)、または座標が `NaN` | `len(shots)` を確認する。`shots[["x", "y"]].isna().sum()` で空欄を確認する |
| ゴールが下にある、または、ピッチが横向きになる | `VerticalPitch` ではなく `Pitch` を使っている | `VerticalPitch(...)` になっているか確認する |
| 点が、ピッチの外に出る、または見当たらない | `x`、`y` を入れ替えて渡した | `pitch.scatter(shots.x, shots.y, ...)` の順(x、y)で渡す。向きの入れ替えは `VerticalPitch` がやる |
| マーカーが大きすぎて、重なって見づらい | `SIZE_SCALE` が大きい、`alpha` が高い | セル1の `SIZE_SCALE` を `600` に下げる。`alpha` を `0.45` に下げる |
| マーカーが小さすぎて、見えない | `SIZE_SCALE` や `SIZE_BASE` が小さい | セル1の `SIZE_BASE` を `120`、`SIZE_SCALE` を `1400` に上げてみる |
| 凡例が、点と重なる | 凡例の位置が、シュートの多い場所にある | `loc="lower left"` を `"lower right"`、`"upper left"` などに変える |
| 凡例の項目が重なる | 大きなマーカーの見本が、近すぎる | `labelspacing=1.6` を `2.0` に大きくする |
| `UserWarning: No artists with labels found to put in legend` | 凡例用の見本の点に、`label=` を付けていない | `ax.scatter([], [], ..., label="...")` の `label=` を確認する |
| 文字が四角(□)になる、`UserWarning: Glyph ... missing from font(s) DejaVu Sans.` | 画像の中に日本語を入れた | 画像の中の文字を英語にする(フェーズ3の手順5と同じ) |
| `[warn] logo not found: ../assets/statsbomb_logo_white.png` | ロゴのファイル名や場所が違う | ターミナルで `ls assets` を実行し、ファイル名を確認する(フェーズ3の手順1-4) |
| ロゴが横に引き伸ばされる | フェーズ3の `add_logo` の計算が、課題3の答えと違っている | フェーズ3の手順7の答えのとおりの式になっているか確認する |
| 保存した PNG の背景が白い | `save_figure` を使わず、`facecolor` なしで保存した | `save_figure(fig, パス)` を使う |
| 保存した PNG に、ロゴが入っていない | `add_logo` を呼ぶ前に、保存した | セル9のとおり、`add_logo` のあとで `save_figure` を呼ぶ |
| ゴール数が、実際のスコアと合わない | オウンゴール、PK戦、延長戦の扱いの違い | **オウンゴールは、シュートではなく、別のイベント**。PK戦(`period` が5)は、`get_shots` で除いている。延長戦のゴールは含まれる。スコアとの差は、これで説明できるか確認する |
| `xg` の合計が、極端に大きい・小さい(例:0、50) | 絞り込みの間違い、または `xg` の列が空 | `shots[["xg", "shot_outcome"]]` を表示して、中身を確認する |
| `loader.py` や `shot_map.py` を直したのに、結果が変わらない | 古い内容を読み込んだままになっている | セル1に `%autoreload 2` があるか確認する。なければ Restart してセル1から実行し直す |

### 9-2. 「描けているけれど、合っているか分からない」ときの確認方法

- **ゴール数を、実際のスコアと照らす**:試合のスコアと、図のゴール数を比べる(オウンゴールとPK戦の違いを考える)。
- **大きなマーカーの位置を見る**:xG が最大のシュートは、ゴールに近い(または PK の)位置にあるはず。遠い位置の大きな点があれば、`x`・`y` の取り出しを疑う。
- **別のチーム・別の試合でも動くか**:`TEAM_NAME` を相手チームにする、`MATCH_ID` を変えて、同じセルが動くか確認する。
- **パスマップと見比べる**:同じ試合のパスマップ(フェーズ3)と並べて、「よく攻めていたチームが、シュートの数や xG も多いか」を見る。

---

## 手順10:Claude / ChatGPT に質問するときのコツ(ショットマップ編)

### 10-1. ショットマップの質問に、必ず入れるもの

1. **やりたいこと**:「ゴールにならなかったシュートを、半透明にしたい」
2. **実行したセルのコード全文**
3. **エラー文の全文**(最初の `Traceback` から、最後のエラー名の行まで)。**エラーが出ない場合は、「何が期待と違うか」**(例:ゴールが下にある、マーカーが見えない)
4. **データの確認結果**:`shots.shape`、`shots[["x", "y", "xg", "is_goal", "size"]].head()`、`shots["shot_outcome"].value_counts()`
5. **環境**:`pip list | grep -i -E "mplsoccer|matplotlib|pandas"` の出力(ターミナルで実行する)

### 10-2. 画像の質問のしかた

- **出てきた画像を、スクリーンショットで添える**。「どこが」「どう」おかしいかも書きます(例:「凡例が、左下のシュートに重なっている」)。
- 直したい点が複数あるときは、**1つずつ**質問する。
- 「`shot_map.py` の**この関数だけ**を直してください」と、範囲を限定する。
- 見た目の調整(大きさ・色・位置)は、**数値を少しずつ変えて、画像で確認**する。

### 10-3. 質問の例

> macOS、Python 3.13.3、VS Code の Jupyter で、mplsoccer の `VerticalPitch(half=True)` でショットマップを描いています。次のセルで、凡例の大きなマーカーの見本が重なってしまいます。
>
> ```python
> ax.legend(handles=handles, loc="lower left", labelspacing=1.6, fontsize=11)
> ```
>
> 凡例に入れている見本のマーカーの大きさは、`s=130`、`s=280`、`s=580` です。重ならないようにするには、どう直せばよいですか? 初学者向けに、理由も教えてください。
>
> `pip list` の出力(抜粋):
>
> ```
> matplotlib   x.x.x
> mplsoccer    x.x.x
> ```

### 10-4. 回答の使い方

- AI が示した引数名や関数名は、**必ず公式ドキュメント(mplsoccer の API とギャラリー)か、`help(VerticalPitch)` で実在を確認**する。ライブラリの版によって違うことがあります。
- 分からないまま貼らず、「この1行は何をしますか?」と聞いてから実行する。

---

## このフェーズ終了時のディレクトリツリー

`NEW` は新しく作ったファイル、`MOD` は変更したファイルです。

```
~/projects/pitchviz/
├── .git/
├── .gitignore
├── .venv/
├── README.md                          # MOD(進捗を追記)
├── requirements.txt
├── assets/
│   ├── statsbomb_logo_white.png       # (フェーズ3。Git管理外)
│   └── statsbomb_logo_default.png     # (フェーズ3。Git管理外)
├── docs/
│   ├── 00_overview.md
│   ├── phase1_setup.md
│   ├── phase2_data.md
│   ├── phase3_passmap.md
│   └── phase4_shotmap.md              # NEW
├── notebooks/
│   ├── 01_setup_check.ipynb
│   ├── 02_explore_data.ipynb
│   ├── 03_pass_map.ipynb
│   └── 04_shot_map.ipynb              # NEW
├── src/
│   └── pitchviz/
│       ├── __init__.py
│       ├── loader.py                  # MOD(get_shots を追加)
│       ├── pass_map.py
│       └── shot_map.py                # NEW(summarize_shots / draw_shot_map)
├── outputs/
│   ├── .gitkeep
│   ├── empty_pitch.png                # (フェーズ1。Git管理外)
│   ├── dark_pitch.png                 # (フェーズ1。Git管理外)
│   ├── pass_map_japan_belgium.png     # (フェーズ3。Git管理外)
│   ├── pass_map_belgium_japan.png     # (フェーズ3。Git管理外)
│   ├── shot_map_japan_belgium.png     # NEW(Git管理外)
│   └── shot_map_belgium_japan.png     # NEW(Git管理外)
└── data/                              # (空。Git管理外)
```

---

## フェーズ4 最終チェックリスト

**データと描画**

- [ ] `get_shots()` で、チームごとのシュート(`x`、`y`、`xg`、`is_goal`)を取り出せる
- [ ] xG をマーカーの大きさに反映して描ける
- [ ] ゴールとゴールにならなかったシュートを、色と塗りで区別して描ける
- [ ] タイトル・凡例(大きさと xG の対応を含む)・出典・ロゴの入った図を描ける

**動くもの**

- [ ] `outputs/shot_map_チーム名_相手チーム名.png` が、両チーム分保存されている
- [ ] 保存した画像に、StatsBomb のロゴと `Data: StatsBomb Open Data` が入っている
- [ ] フェーズ3の `add_logo`・`save_figure`・`make_filename` を再利用できている

**Git / GitHub**

- [ ] `git log --oneline` に、フェーズ4のコミットがある
- [ ] ロゴ画像と PNG が、Git の対象外になっている
- [ ] GitHub のリポジトリが `Private` のままである

すべてにチェックが付けば、フェーズ4は完了です。

---

## 次のフェーズへ

フェーズ5では、ここまでに作ったものを、**「試合とチーム(または選手)を指定すると、画像を保存する関数」**にまとめます。

- `src/pitchviz/api.py` に、入口になる関数を作る(試合の探索・イベント取得・描画・保存を、1行の呼び出しにまとめる)
- `pyproject.toml` を追加して、`sys.path.append("../src")` を書かなくても、`pitchviz` を読み込めるようにする
- `notebooks/05_use_function.ipynb` で、1行の呼び出しで、パスマップとショットマップが保存されることを確認する

準備ができたら「フェーズ5をお願いします」と指示してください。

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| mplsoccer(API・ギャラリー) | `https://mplsoccer.readthedocs.io`(`VerticalPitch`、`Pitch.scatter`、「Plot scatter」のショットマップの例) |
| matplotlib | `https://matplotlib.org/stable/`(`Axes.scatter`、`Axes.legend`) |
| pandas | `https://pandas.pydata.org/docs/`(`Series.str`、`Series.fillna`) |
| StatsBomb Open Data(データ・仕様書・利用条件) | `https://github.com/statsbomb/open-data`(`doc` フォルダ、`LICENSE.pdf`) |
| statsbombpy | `https://github.com/statsbomb/statsbombpy` |
