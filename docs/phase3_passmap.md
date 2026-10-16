# フェーズ3:パスマップ

> 保存先:`~/projects/pitchviz/docs/phase3_passmap.md`
> このフェーズの終わりには「選んだ試合の、チームごとのパスマップが `outputs/` に PNG で保存される」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | フェーズ2で取り出したパスを、mplsoccer でピッチ上に矢印として描き、チームごとの PNG 画像として保存する |
| 想定所要時間 | 約9時間(下の内訳を参照) |
| 終了時の「動くもの」 | `outputs/pass_map_チーム名_相手チーム名.png` が、両チーム分(2枚)保存される。画像には、成功・失敗パスの矢印、タイトル、StatsBomb のロゴと出典が入る |

### 作業ラベルの見方

- **[Terminal]**:ターミナルでの作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 事前準備(状態確認・ロゴの配置・`.gitignore`) | 0.75h |
| 2 | Notebook の作成と、試合データの読み込み | 0.75h |
| 3 | まず1本、次に全部のパスを描く | 1.0h |
| 4 | 成功パスと失敗パスを分ける(課題1・2) | 1.25h |
| 5 | 見た目を整える(タイトル・凡例・出典) | 1.25h |
| 6 | PNG として保存する | 0.5h |
| 7 | StatsBomb のロゴを入れる(課題3) | 1.0h |
| 8 | 関数にまとめる(課題4・5) | 1.75h |
| 9 | README・コミット・振り返り | 0.75h |
| | 合計 | 9.0h |

### このフェーズについての大事な前提

- **このフェーズのコードは、手順書の作成環境で mplsoccer 本体を実際に動かして確認できていません。** mplsoccer の使い方は、公式ドキュメント(API と、ギャラリーの「Plot arrows」「Pass network」の例)で確認した引数にもとづいています。
  - 作成環境では、mplsoccer の代わりに「同じ呼び出し方を受け付ける代用品」と、StatsBomb と同じ列構造の架空のイベントデータを使い、手順書のコードを**セル1〜12まで最後まで実行**できることを確認しました。ここまでで確認できたのは、データの絞り込み(`get_passes`)、ファイル名の生成(`make_filename`)、タイトル・凡例・出典の配置、ロゴが縦横比を保って置かれること、PNG の保存です。
  - **確認できていないのは、本物の mplsoccer での矢印の見た目(太さ・矢じりの大きさ)です。** 矢印が太すぎる・細すぎる場合は、`width`、`headwidth`、`headlength` の数値を調整してください(手順10-1の表も参照)。
  - ライブラリの更新で引数名が変わる可能性があるため、エラーが出たら手順10の対処表と、[mplsoccer 公式ドキュメント](https://mplsoccer.readthedocs.io)を確認してください。
- **「期待される出力」の数字は例です。** パス数や成功率は、あなたが選んだ試合によって違います。
- このフェーズで使うチーム名・`match_id`・日付は、**フェーズ2の手順4-7のメモの値**です。
- **リポジトリは Private のままにしてください。** このフェーズの Notebook には、データの行や、データから作った画像が出力として残ります。公開の前の整理は、フェーズ6で行います(StatsBomb の利用条件で、データの再配布が禁止されているためです)。

### 今回作るものの流れ

```
events(1試合の全イベント)
   │  loader.get_passes()   … 指定チームのパスだけにし、座標と成功フラグを付ける
   ▼
passes(x, y, end_x, end_y, is_complete)
   │  pass_map.draw_pass_map()  … ピッチに矢印を描き、タイトル・凡例・ロゴを付ける
   ▼
fig(図)
   │  pass_map.save_figure()    … PNG として保存する
   ▼
outputs/pass_map_japan_belgium.png
```

---

## 手順1:事前準備(状態確認・ロゴの配置・`.gitignore`)

**所要時間:約0.75時間**

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

- フェーズ2のコミットが済んでいない場合は、先にフェーズ2の手順8を終えてください(`Your branch is ahead of ...` と出ても問題ありません)。

### 1-2. フェーズ2のメモを手元に用意する

次の3つを、メモから見える場所に用意します(フェーズ2の手順4-7で書き留めたものです)。

```
使うチーム名:     Japan(例:Japan)
使う match_id:    7584(例:7584)
対戦カードと日付:2018-07-02 Belgium vs Japan(例:2018-07-02 Belgium vs Japan)
```

- 忘れた場合は、`notebooks/02_explore_data.ipynb` を開き、セル10・11の出力で確認します。

### 1-3. ロゴ用のフォルダ `assets/` を作る

画像にロゴを入れるので、ロゴの置き場を作ります。**`00_overview.md` のフォルダ構成にはなかったフォルダなので、ここで追加します。**

- [ ] **[VS Code]** Explorer(`Command + Shift + E`)で、`PITCHVIZ` の行(フォルダ名)を右クリック → `New Folder` → `assets` と入力して Enter。
  - **対象**:`assets/`(プロジェクトルート直下)
  - **新規作成か編集か**:新規作成

### 1-4. ロゴ画像を `assets/` に置く

フェーズ2の途中で、Media Pack から次の2つをダウンロードしているはずです。

| ダウンロードしたファイル(例) | このプロジェクトでの名前 | 使う場面 |
|---|---|---|
| `hudl-statsbomb-logo-white`(白1色) | `statsbomb_logo_white.png` | **このフェーズ**。暗い背景の画像に入れる |
| `hudl-statsbomb-logo-default`(オレンジ+黒の文字) | `statsbomb_logo_default.png` | フェーズ6。明るい背景の README に入れる |

- [ ] **[Browser]** まだダウンロードしていなければ、Media Pack(`https://statsbomb.com/media-pack/` から開けるロゴのコレクション)から、上の2つをダウンロードする。
  - 一括ダウンロードで ZIP になった場合は、Finder でダブルクリックして展開します。
  - 手順書のロゴの使い方は、**フェーズ2の手順1-2・1-3のメモ(ロゴは加工せず、用意されたバリエーションを使う)** に従います。
- [ ] **[VS Code]** Finder から、2つの PNG ファイルを、VS Code の Explorer の `assets` フォルダにドラッグ&ドロップする。
- [ ] **[VS Code]** Explorer で、それぞれのファイルを右クリック → `Rename...` → 上の表の名前に変える。

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
ls assets
```

期待される出力:

```
statsbomb_logo_default.png	statsbomb_logo_white.png
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、画像が読み込めるか確認する。

```bash
python -c "import matplotlib.pyplot as plt; im = plt.imread('assets/statsbomb_logo_white.png'); print(im.shape)"
```

期待される出力の例:

```
(240, 960, 4)
```

- 3つの数字は(縦のピクセル数, 横のピクセル数, 色のチャンネル数)です。**最後が `4` なら、透明部分を持つ画像で、重ねる用途に向いています。** 縦横の数字は違って構いません。
- `FileNotFoundError` が出た場合は、ファイル名の綴りと、`assets` の場所(プロジェクトルート直下)を確認します。

### 1-5. ロゴを Git に含めない設定にする

StatsBomb のロゴを、リポジトリに入れて再配布してよいかは、**まだ確認できていません**(フェーズ2のメモの「ロゴの使い方」)。確認が終わるフェーズ6まで、ロゴ画像は Git の対象から外します。

- [ ] **[VS Code]** Explorer で `.gitignore`(プロジェクトルート直下)を開く。
  - **対象**:`.gitignore`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:ファイルの**末尾**(`!outputs/.gitkeep` の行の後ろ)に、次の内容(コメント2行と、`assets/*.png` の1行)を追記する。
- [ ] 追記して `Command + S` で保存する。

```gitignore
# .gitignore (末尾に追記)

# --- StatsBomb ロゴ(再配布の可否が未確認のため、フェーズ6まで Git に含めない) ---
assets/*.png
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `assets/*.png` | `assets` フォルダの中の PNG ファイルをすべて Git の対象外にする |

- [ ] **[Terminal]** `~/projects/pitchviz` で、設定が効いているか確認する。

```bash
git check-ignore -v assets/statsbomb_logo_white.png
```

期待される出力の例(行番号は環境で違います):

```
.gitignore:27:assets/*.png	assets/statsbomb_logo_white.png
```

- 何も表示されない場合は、`.gitignore` に追記した行が保存されていません。もう一度確認します。

### 手順1の完了チェック

- [ ] `(.venv)` が行頭に表示されている
- [ ] フェーズ2のメモ(チーム名・`match_id`・日付)が手元にある
- [ ] `assets/` に `statsbomb_logo_white.png` と `statsbomb_logo_default.png` がある
- [ ] `plt.imread` の確認で、`(縦, 横, 4)` が表示された
- [ ] `git check-ignore -v` で、ロゴが Git の対象外と表示された

---

## 手順2:Notebook の作成と、試合データの読み込み

**所要時間:約0.75時間**

### 2-1. Notebook を作る

- [ ] **[VS Code]** Explorer で `notebooks` フォルダを右クリック → `New File` → `03_pass_map.ipynb` と入力して Enter。
  - **対象**:`notebooks/03_pass_map.ipynb`
  - **新規作成か編集か**:新規作成
- [ ] **[VS Code]** 右上の `Select Kernel` → `Python Environments...` → `.venv` を選ぶ。

> **セルの使い方**(これまでと同じ)
> `+ Code` でセルを追加し、`Shift + Enter` で実行します。**セルは番号順(上から順)に実行してください。** 動かなくなったら、上部の **Restart** を押し、セル1から順に実行し直します。

### 2-2. セル1:準備と、色の設定

- [ ] **[VS Code]** 最初のセルに、次を入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル1**

```python
# notebooks/03_pass_map.ipynb  セル1
%load_ext autoreload
%autoreload 2

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import Pitch

# src フォルダを import の探索先に追加する(自作の loader.py などを使うため)
sys.path.append("../src")

pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 200)

# 図の色(暗い緑の背景に合う色。青とオレンジは、色の見分けにくい人にも区別しやすい組み合わせ)
BG_COLOR = "#22312b"      # 背景・ピッチの色
LINE_COLOR = "#c7d5cc"    # ピッチのラインの色
TEXT_COLOR = "#e8efe9"    # 文字の色
OK_COLOR = "#6cb2eb"      # 成功パスの色(青)
NG_COLOR = "#f28e4b"      # 失敗パスの色(オレンジ)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `%load_ext autoreload` と `%autoreload 2` | `.py` ファイルを書き換えたとき、Notebook を再起動しなくても反映する設定(フェーズ2と同じ) |
| `from pathlib import Path` | ファイルの場所を扱いやすくする標準ライブラリ。保存先の指定で使う |
| `import matplotlib.pyplot as plt` | 図を扱う基本のライブラリ。`plt` と略す慣習 |
| `from mplsoccer import Pitch` | サッカーのピッチを描くためのクラス |
| `BG_COLOR = "#22312b"` | 色の指定。`#` と6桁の英数字(16進数)で色を表す。大文字のとおりの名前の変数は「変えない値(定数)」を表す習慣 |

**期待される出力**

- 何も表示されなくて正常です(エラーが出なければ成功)。

### 2-3. セル2:使う試合を指定して、イベントを読み込む

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル2**
  - **`TEAM_NAME` `MATCH_ID` `MATCH_DATE` は、手順1-2のメモの値に置き換えます。** 下の値は例です。

```python
# notebooks/03_pass_map.ipynb  セル2
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

| 記述 | 意味 |
|---|---|
| `from pitchviz.loader import get_events` | フェーズ2で作った自作の関数を読み込む |
| `events["team"].unique()` | この試合に登場するチーム名(2つ) |
| `[t for t in teams if t != TEAM_NAME][0]` | チーム名の一覧から、自分のチーム**以外**を取り出し、その先頭(= 相手チーム)を取る |

**期待される出力の例**

```
NoAuthWarning: credentials were not supplied. Open data access only
(3xxx, 1xx)
['Belgium', 'Japan'] -> Japan vs Belgium
```

**確認すること**

- [ ] 2つのチーム名が表示され、`TEAM_NAME` が一字一句同じ文字列で含まれている(違うと `opponent_name` が間違った値になります)
- [ ] `opponent_name` に、相手チームの名前が入っている

### 2-4. セル3:パスを取り出し、座標と成功フラグを作る

フェーズ2で練習した絞り込みを、そのまま使います。今回は、パスの**終点**の座標と、**成功したかどうか**も追加します。

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル3**

```python
# notebooks/03_pass_map.ipynb  セル3
passes = events[(events["type"] == "Pass") & (events["team"] == TEAM_NAME)].copy()

passes["x"] = passes["location"].str[0]
passes["y"] = passes["location"].str[1]
passes["end_x"] = passes["pass_end_location"].str[0]
passes["end_y"] = passes["pass_end_location"].str[1]
passes["is_complete"] = passes["pass_outcome"].isna()

print("passes:", len(passes), " complete:", int(passes["is_complete"].sum()))
print("mean forward (end_x - x):", round((passes["end_x"] - passes["x"]).mean(), 1))
passes[["minute", "player", "x", "y", "end_x", "end_y", "pass_outcome", "is_complete"]].head()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `(条件A) & (条件B)` | 「AかつB」。**それぞれを丸括弧 `( )` で囲む**のが決まり。ここでは「イベントがパス」かつ「自分のチーム」 |
| `passes["pass_end_location"].str[0]` | パスの終点 `[x, y]` の、0番目(x)を取り出す。フェーズ2の `location` と同じ考え方 |
| `passes["pass_outcome"].isna()` | `pass_outcome` が空欄(`NaN`)か判定する。**空欄 = 成功したパス**(失敗などのときだけ値が入る) |
| `.sum()` | `True` を1として数える。つまり成功パスの数 |
| `(end_x - x).mean()` | 各パスの「ゴール方向(x の増える向き)への進み」の平均。確認のために出す |

**期待される出力の例**

```
passes: 412  complete: 351
mean forward (end_x - x): 6.3
```

続いて、`minute`、`player`、`x`、`y`、`end_x`、`end_y`、`pass_outcome`、`is_complete` の表が表示されます。

**確認すること**

- [ ] `passes` の数が数百になっている
- [ ] 成功パス(`complete`)が、全体の7〜9割程度である
- [ ] `mean forward` が、多くの場合は**正の数**になっている(StatsBomb のデータは、どちらのチームも「右(x が大きい方)のゴールに向かって攻める」向きに記録されるため。負の大きな値なら、座標の取り出しを見直します)
- [ ] `is_complete` が `True` の行は `pass_outcome` が `NaN`、`False` の行は `Incomplete` などの値が入っている

### 手順2の完了チェック

- [ ] カーネルが `.venv` になっている
- [ ] セル2で、2つのチーム名と対戦相手の名前が出た
- [ ] セル3で、`x`、`y`、`end_x`、`end_y`、`is_complete` の列ができた

---

## 手順3:まず1本、次に全部のパスを描く

**所要時間:約1.0時間**

いきなり全部は描きません。**まず1本だけ**描いて、描き方の仕組みを確認します。

### 3-1. セル4:1本のパスを矢印で描く

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル4**

```python
# notebooks/03_pass_map.ipynb  セル4
pitch = Pitch(pitch_type="statsbomb", pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(12, 8))
fig.set_facecolor(BG_COLOR)

first = passes.head(1)   # 先頭の1行(1本のパス)
pitch.arrows(first.x, first.y, first.end_x, first.end_y,
             width=2, headwidth=8, headlength=8, color=OK_COLOR, ax=ax)
plt.show()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `Pitch(pitch_type="statsbomb", ...)` | StatsBomb の座標(横120 × 縦80)に合ったピッチの設計図。色も指定する |
| `pitch.draw(figsize=(12, 8))` | ピッチを描く。`fig`(図全体)と `ax`(描く場所)を返す |
| `fig.set_facecolor(BG_COLOR)` | 図全体の背景色を、ピッチと同じ色にする(余白が白くならない) |
| `passes.head(1)` | 先頭の1行だけを取り出す(表のまま) |
| `pitch.arrows(始点x, 始点y, 終点x, 終点y, ...)` | 始点から終点へ向かう矢印を描く。4つの座標を、この順に渡す |
| `width`、`headwidth`、`headlength` | 矢印の軸の太さ、矢じりの幅、矢じりの長さ |
| `ax=ax` | どの描く場所に描くか |

**期待される出力**

- 暗い緑のピッチに、**矢印が1本**だけ描かれる(色は青)。

**確認すること**

- [ ] 矢印の始点と終点が、`passes.head(1)` の `x`・`y` と `end_x`・`end_y` の位置と合っている(例:`x=61, y=40` なら、ピッチの中央付近)

### 3-2. セル5:全部のパスを描く

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル5**

```python
# notebooks/03_pass_map.ipynb  セル5
pitch = Pitch(pitch_type="statsbomb", pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(12, 8))
fig.set_facecolor(BG_COLOR)

pitch.arrows(passes.x, passes.y, passes.end_x, passes.end_y,
             width=2, headwidth=6, headlength=6, color=OK_COLOR, alpha=0.8, ax=ax)
plt.show()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `passes.x`(列を丸ごと渡す) | 1行ではなく、全部のパスの x をまとめて渡す。矢印が一度に全部描かれる |
| `alpha=0.8` | 透明度。1が不透明、0が透明。重なった矢印が見分けやすくなる |

**期待される出力**

- 数百本の青い矢印が、ピッチ全体に描かれる。
- **成功と失敗が区別できません。** これが、次の手順4で解決する課題です。

### 手順3の完了チェック

- [ ] セル4で矢印が1本だけ描かれた
- [ ] セル5で、数百本の矢印が描かれた
- [ ] 矢印の多くが、右(ゴールのある側)に向かっている

---

## 手順4:成功パスと失敗パスを分ける

**所要時間:約1.25時間**

### 4-1. セル6(課題1):成功と失敗で、色を分ける

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル6**
  - 空欄を埋めるまでは、エラーになります(正常です)。

```python
# notebooks/03_pass_map.ipynb  セル6(課題1)
pitch = Pitch(pitch_type="statsbomb", pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(12, 8))
fig.set_facecolor(BG_COLOR)

complete = passes[passes["____"]]      # 成功したパスだけ
failed = passes[~passes["____"]]       # 失敗したパスだけ

pitch.arrows(complete.____, complete.____, complete.____, complete.____,
             width=2, headwidth=6, headlength=6, color=OK_COLOR, alpha=0.85, ax=ax)
pitch.arrows(failed.x, failed.y, failed.end_x, failed.end_y,
             width=2, headwidth=6, headlength=6, color=NG_COLOR, alpha=0.85, ax=ax)
plt.show()
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目・2つ目の `____` | セル3で作った、「成功したか」を表す True / False の列の名前 |
| 3つ目〜6つ目の `____` | 矢印の4つの座標。始点x、始点y、終点x、終点yの順(`failed` の行と同じ形) |

**コードの解説(ヒント)**

| 記述 | 意味 |
|---|---|
| `passes[passes["列"]]` | True の行だけを取り出す(手順2で練習した絞り込み。列が True / False のとき、`== True` を書かなくてよい) |
| `~` | 「ではない」(True と False を反転する)。`~passes["列"]` で、失敗したパスの行を取り出せる |

**期待される出力**

- 青い矢印(成功)と、オレンジの矢印(失敗)が描かれる。
- 青の矢印のほうが、オレンジより多い。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/03_pass_map.ipynb  セル6(課題1)
pitch = Pitch(pitch_type="statsbomb", pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, ax = pitch.draw(figsize=(12, 8))
fig.set_facecolor(BG_COLOR)

complete = passes[passes["is_complete"]]      # 成功したパスだけ
failed = passes[~passes["is_complete"]]       # 失敗したパスだけ

pitch.arrows(complete.x, complete.y, complete.end_x, complete.end_y,
             width=2, headwidth=6, headlength=6, color=OK_COLOR, alpha=0.85, ax=ax)
pitch.arrows(failed.x, failed.y, failed.end_x, failed.end_y,
             width=2, headwidth=6, headlength=6, color=NG_COLOR, alpha=0.85, ax=ax)
plt.show()
```

**答え合わせのあとに**

- 空欄の答え:1つ目・2つ目は `is_complete`、3つ目〜6つ目は `x`、`y`、`end_x`、`end_y`。

**自分のコードが正解と違っても、動いていればOKな例**

- `passes[passes.is_complete]` と、ドットで列を取り出した → 動く(別の書き方)。
- `passes[passes["pass_outcome"].isna()]` で成功パスを取り出した → 動く。結果は同じです(`is_complete` はそれを列にしたものです)。
- `passes.query("is_complete")` と書いた → 動く(pandas の別の書き方)。
- `failed` を `passes[passes["is_complete"] == False]` と書いた → 動く。ただし `~` を使うほうが一般的で、読みやすいです。

**確認の仕方**

- 青とオレンジの両方が描かれている(オレンジが1本も出ない場合は、`failed` が空になっていないか `len(failed)` で確認する)。
- `len(complete) + len(failed) == len(passes)` が `True` になる(次のセルで確かめます)。

</details>

### 4-2. セル7(課題2):パス成功率を計算する

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル7**

```python
# notebooks/03_pass_map.ipynb  セル7(課題2)
n_total = len(____)       # 全部のパスの数
n_complete = len(____)    # 成功したパスの数
rate = n_complete / n_total * 100

print(f"{TEAM_NAME}: {n_complete}/{n_total} passes completed ({rate:.1f}%)")
print(len(complete) + len(failed) == len(passes))
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | 全部のパスが入っている表 |
| 2つ目 | 成功したパスだけが入っている表(セル6で作った) |

**コードの解説(ヒント)**

| 記述 | 意味 |
|---|---|
| `len(表)` | 表の行数(= パスの本数) |
| `{rate:.1f}` | 小数第1位まで表示する書式(f文字列の中の `:.1f`) |

**期待される出力の例**

```
Japan: 351/412 passes completed (85.2%)
True
```

- 成功率は、多くの試合で70〜90%台になります(チームや試合で違います)。
- 2行目が `True` なら、成功と失敗の合計が全体と合っています。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/03_pass_map.ipynb  セル7(課題2)
n_total = len(passes)         # 全部のパスの数
n_complete = len(complete)    # 成功したパスの数
rate = n_complete / n_total * 100

print(f"{TEAM_NAME}: {n_complete}/{n_total} passes completed ({rate:.1f}%)")
print(len(complete) + len(failed) == len(passes))
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `passes`、2つ目は `complete`。

**自分のコードが正解と違っても、動いていればOKな例**

- `n_complete = int(passes["is_complete"].sum())` と書いた → 動く(`True` を1として数える)。結果は同じです。
- `n_complete = passes["is_complete"].mean() * 100` で成功率を直接出した → 動く(`True` の割合 = 成功率)。別の考え方です。

**確認の仕方**

- 2行目が `True` になる。
- 成功率が0〜100%の範囲に収まっている。

</details>

### 手順4の完了チェック

- [ ] セル6で、青とオレンジの矢印が描かれた
- [ ] セル7で、成功率が表示され、2行目が `True` だった
- [ ] 課題1・2を解いて、答え合わせをした

---

## 手順5:見た目を整える(タイトル・凡例・出典)

**所要時間:約1.25時間**

画像として人に見せるため、タイトルと凡例(色の説明)、出典を付けます。

### 5-1. セル8:タイトル欄・出典欄つきの図を作る

mplsoccer の `pitch.grid()` を使うと、ピッチの上に「タイトル欄」、下に「出典欄」が自動で用意されます。

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル8**

```python
# notebooks/03_pass_map.ipynb  セル8
pitch = Pitch(pitch_type="statsbomb", pitch_color=BG_COLOR, line_color=LINE_COLOR)
fig, axs = pitch.grid(figheight=9, title_height=0.08, grid_height=0.80, endnote_height=0.07,
                      title_space=0, endnote_space=0, axis=False)
fig.set_facecolor(BG_COLOR)
ax = axs["pitch"]

complete = passes[passes["is_complete"]]
failed = passes[~passes["is_complete"]]

pitch.arrows(complete.x, complete.y, complete.end_x, complete.end_y,
             width=2, headwidth=6, headlength=6, color=OK_COLOR, alpha=0.85,
             label=f"Completed ({len(complete)})", ax=ax)
pitch.arrows(failed.x, failed.y, failed.end_x, failed.end_y,
             width=2, headwidth=6, headlength=6, color=NG_COLOR, alpha=0.85,
             label=f"Failed ({len(failed)})", ax=ax)

ax.legend(facecolor=BG_COLOR, edgecolor=LINE_COLOR, labelcolor=TEXT_COLOR,
          loc="upper left", fontsize=12)

axs["title"].text(0.5, 0.68, f"{TEAM_NAME} pass map vs {opponent_name}",
                  color=TEXT_COLOR, ha="center", va="center", fontsize=24,
                  transform=axs["title"].transAxes)
axs["title"].text(0.5, 0.18, f"{MATCH_DATE}   |   attacking left to right",
                  color=LINE_COLOR, ha="center", va="center", fontsize=13,
                  transform=axs["title"].transAxes)
axs["endnote"].text(0.01, 0.5, "Data: StatsBomb Open Data",
                    color=TEXT_COLOR, ha="left", va="center", fontsize=11,
                    transform=axs["endnote"].transAxes)
plt.show()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `pitch.grid(...)` | ピッチの上下に、タイトル欄・出典欄を持つ図を作る。`fig` と、場所の辞書 `axs` を返す |
| `figheight=9` | 図の高さ(インチ)。幅は、ピッチの形に合わせて自動で決まる |
| `title_height`、`grid_height`、`endnote_height` | 図全体を1としたときの、タイトル欄・ピッチ・出典欄の高さの割合 |
| `title_space=0`、`endnote_space=0` | 各欄とピッチの間の隙間をなくす |
| `axis=False` | タイトル欄・出典欄の枠線や目盛りを消す |
| `axs["pitch"]`、`axs["title"]`、`axs["endnote"]` | ピッチ・タイトル欄・出典欄の「描く場所」 |
| `label=f"Completed ({len(complete)})"` | 凡例に出す名前。成功パスの本数も入れる |
| `ax.legend(...)` | 凡例を表示する。`labelcolor` で文字色、`loc` で位置(左上)を決める |
| `ax.text(x, y, 文字, ...)` | 文字を描く。`transform=....transAxes` を付けると、位置を「その欄の左下を (0,0)、右上を (1,1)」で指定できる |
| `ha="center"`、`va="center"` | 文字の水平・垂直の基準を中央にする |

**期待される出力**

- 暗い緑の図の上部に、タイトル(例:`Japan pass map vs Belgium`)と、その下に日付と `attacking left to right`。
- 中央にピッチと、青・オレンジの矢印。左上に凡例(`Completed (351)`、`Failed (61)`)。
- 下部の左端に `Data: StatsBomb Open Data`。

**確認すること**

- [ ] タイトルの `vs` の右が、相手チーム名になっている
- [ ] 凡例の本数が、セル7の数字と合っている
- [ ] 文字が背景に埋もれず、読める
- [ ] 画像の中の文字がすべて**英語**になっている(次の注意を読む)

> **注意:画像の中の文字を日本語にすると、文字が四角(□)になります。** matplotlib の標準フォントに、日本語の文字が入っていないためです。実行すると、`UserWarning: Glyph ... missing from font(s) DejaVu Sans.` という警告も出ます。このプロジェクトでは、画像の中の文字は英語に統一します(出典の表記にも合います)。

### 手順5の完了チェック

- [ ] セル8で、タイトル・ピッチ・凡例・出典が入った図が表示された
- [ ] 凡例の本数が、成功・失敗パスの数と合っている

---

## 手順6:PNG として保存する

**所要時間:約0.5時間**

### 6-1. セル9:図を PNG ファイルとして保存する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル9**
  - ファイル名は、`pass_map_チーム名_相手チーム名.png`(小文字・スペースなし)にします。下の名前は例で、自分の試合の名前に置き換えます(関数にまとめる手順8で、自動で作れるようにします)。

```python
# notebooks/03_pass_map.ipynb  セル9
OUTPUT_DIR = Path("../outputs")
out_path = OUTPUT_DIR / "pass_map_japan_belgium.png"   # 例。自分の試合に合わせて変える

fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
print("saved:", out_path)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `Path("../outputs")` | ファイルの場所。Notebook は `notebooks/` にあるので、`..`(1つ上)の `outputs/` を指す |
| `OUTPUT_DIR / "ファイル名"` | フォルダとファイル名をつなぐ(`Path` の書き方) |
| `fig.savefig(場所, dpi=200, ...)` | 図を画像として保存する。`dpi` は解像度(大きいほど細かい) |
| `facecolor=fig.get_facecolor()` | 保存する画像の背景色を、図の背景色と同じにする。付けないと、背景が白になることがある |

**期待される出力**

```
saved: ../outputs/pass_map_japan_belgium.png
```

**生成されるファイル**

- `outputs/pass_map_japan_belgium.png`

- [ ] **[VS Code]** Explorer で `outputs/pass_map_japan_belgium.png` をクリックして開き、保存した画像が表示されることを確認する。
  - 背景が暗い緑で、白くなっていないこと。タイトル・凡例・出典が、Notebook の表示と同じように入っていること。

> **メモ**:`outputs/` の PNG は、`.gitignore` により Git の対象外です(手順9の `git status` に表示されません)。

### 手順6の完了チェック

- [ ] `saved: ../outputs/pass_map_....png` と表示された
- [ ] Explorer の `outputs/` に PNG が増え、開いて内容が確認できた
- [ ] 画像の背景が白くなっていない

---

## 手順7:StatsBomb のロゴを入れる

**所要時間:約1.0時間**

StatsBomb のデータから作った分析を公開するときは、**ロゴで出典を示す**必要があります(LICENSE.pdf の 1.4。フェーズ2の手順1-2のメモ)。画像にロゴを入れる関数を作ります。

**ロゴの扱いの方針**

- 用意されたバリエーションを、**色や形を変えずに**使う。
- 大きさは変えるが、**縦横の比率は保つ**(引き伸ばさない)。
- 暗い背景には、白のロゴ(`statsbomb_logo_white.png`)を使う。

### 7-1. セル10(課題3):ロゴを置く関数を書く

出典欄(`axs["endnote"]`)の右端に、ロゴを置きます。

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル10**
  - セル8で作った `fig` と `axs` を使うので、**セル8を先に実行しておく**こと。

```python
# notebooks/03_pass_map.ipynb  セル10(課題3)
def add_logo(fig, anchor_ax, logo_path, height_ratio=0.8, margin=0.01):
    """anchor_ax(ロゴを置く欄)の右端に、ロゴ画像を縦横比そのままで置く。"""
    logo_path = Path(logo_path)
    if not logo_path.exists():
        print(f"[warn] logo not found: {logo_path}")
        return None

    img = plt.____(logo_path)               # 画像ファイルを読み込む
    img_h, img_w = img.____[:2]             # 画像の(縦, 横)のピクセル数

    box = anchor_ax.get_____()              # 欄の位置(図全体を0〜1とした割合)
    fig_w, fig_h = fig.get_size_inches()    # 図の大きさ(インチ)

    logo_h = box.height * height_ratio                    # ロゴの高さ(図に対する割合)
    logo_w = logo_h * (img_w / img_h) * (fig_h / fig_w)   # 縦横比を保った幅(割合)
    left = box.x1 - logo_w - margin                       # 欄の右端から、少し内側
    bottom = box.y0 + (box.height - logo_h) / 2           # 欄の上下の中央

    logo_ax = fig.____([left, bottom, logo_w, logo_h])    # ロゴ用の描く場所を追加する
    logo_ax.imshow(img)
    logo_ax.axis("off")
    return logo_ax


LOGO_PATH = "../assets/statsbomb_logo_white.png"
add_logo(fig, axs["endnote"], LOGO_PATH)
fig
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | 手順1-4の確認で使った、画像を読み込む関数(`plt.` のあと) |
| 2つ目 | 配列の形(縦・横・色のチャンネル数)を返す属性の名前。手順1-4で `print` したもの |
| 3つ目 | 欄の「位置」を取り出すメソッドの名前(`get_` のあと。「位置」を意味する英語) |
| 4つ目 | 図に、新しい「描く場所」を追加するメソッドの名前(`add_` のあと。`axes`) |

**コードの解説(ヒント)**

| 記述 | 意味 |
|---|---|
| `Path(logo_path).exists()` | ファイルが実在するか。なければ、警告を出して何もせずに戻る(ロゴがなくても、他の処理は止まらない) |
| `box.height`、`box.x1`、`box.y0` | 欄の高さ、右端、下端(図全体を1としたときの割合) |
| `(img_w / img_h) * (fig_h / fig_w)` | 画像の縦横比に、図の縦横比を掛けて補正する。**これで、ロゴが引き伸ばされない** |
| `logo_ax.imshow(img)` | 画像を、追加した「描く場所」に表示する |
| `logo_ax.axis("off")` | 枠線と目盛りを消す |
| 最後の行の `fig` | 図をもう一度、セルの出力に表示する(ロゴを足したあとの姿を見るため) |

**期待される出力**

- 図の下部、出典欄の**右端**に、白い StatsBomb のロゴが表示される(縦横比が正しい)。
- ロゴが見つからないと、`[warn] logo not found: ...` と表示される。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/03_pass_map.ipynb  セル10(課題3)
def add_logo(fig, anchor_ax, logo_path, height_ratio=0.8, margin=0.01):
    """anchor_ax(ロゴを置く欄)の右端に、ロゴ画像を縦横比そのままで置く。"""
    logo_path = Path(logo_path)
    if not logo_path.exists():
        print(f"[warn] logo not found: {logo_path}")
        return None

    img = plt.imread(logo_path)             # 画像ファイルを読み込む
    img_h, img_w = img.shape[:2]            # 画像の(縦, 横)のピクセル数

    box = anchor_ax.get_position()          # 欄の位置(図全体を0〜1とした割合)
    fig_w, fig_h = fig.get_size_inches()    # 図の大きさ(インチ)

    logo_h = box.height * height_ratio                    # ロゴの高さ(図に対する割合)
    logo_w = logo_h * (img_w / img_h) * (fig_h / fig_w)   # 縦横比を保った幅(割合)
    left = box.x1 - logo_w - margin                       # 欄の右端から、少し内側
    bottom = box.y0 + (box.height - logo_h) / 2           # 欄の上下の中央

    logo_ax = fig.add_axes([left, bottom, logo_w, logo_h])    # ロゴ用の描く場所を追加する
    logo_ax.imshow(img)
    logo_ax.axis("off")
    return logo_ax


LOGO_PATH = "../assets/statsbomb_logo_white.png"
add_logo(fig, axs["endnote"], LOGO_PATH)
fig
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `imread`、2つ目は `shape`、3つ目は `position`(`get_position`)、4つ目は `axes`(`add_axes`)。

**自分のコードが正解と違っても、動いていればOKな例**

- `height_ratio` を `0.8` ではなく `0.6` や `1.0` にした → 動く。ロゴの大きさが変わるだけです(大きくしすぎると、ピッチに重なることがあります)。
- ロゴを右端ではなく左端に置いた(`left = box.x0 + margin`) → 動く。ただし、出典の文字(左端)と重なるので、出典の位置も変えてください。
- `logo_w` の計算で `(fig_h / fig_w)` を付け忘れた → 動くが、**ロゴが横に引き伸ばされて見える**。見た目で確認できます。

**確認の仕方**

- ロゴが出典欄の右端に、変形せずに表示される。
- ロゴを入れたまま、次の手順で画像を保存し直す。

</details>

### 7-2. セル9を、もう一度実行する(ロゴ入りで保存し直す)

- [ ] **[VS Code]** セル9(保存のセル)を、もう一度実行する。
  - セル10でロゴを足した `fig` が、同じファイル名で上書き保存されます。

期待される出力:

```
saved: ../outputs/pass_map_japan_belgium.png
```

- [ ] **[VS Code]** Explorer で `outputs/pass_map_japan_belgium.png` を開き直し、**ロゴが入っている**ことを確認する。

> **Explorer に古い画像が出る場合**:ファイルのタブを一度閉じてから、もう一度開きます。

### 手順7の完了チェック

- [ ] セル10(課題3)を解いて、答え合わせをした
- [ ] 図の下部右端に、白いロゴが縦横比のまま表示された
- [ ] 保存し直した PNG に、ロゴと `Data: StatsBomb Open Data` の両方が入っている

---

## 手順8:関数にまとめる

**所要時間:約1.75時間**

Notebook で動いたコードを、`.py` ファイルの関数にして、**何度でも呼び出せる**ようにします。フェーズ5で「試合とチームを指定して PNG を保存する関数」にまとめるための土台になります。

| 作る関数 | ファイル | 役割 |
|---|---|---|
| `get_passes()` | `src/pitchviz/loader.py`(編集) | イベントから、指定チームのパスを取り出し、座標と成功フラグを付ける |
| `add_logo()` | `src/pitchviz/pass_map.py`(新規) | 図にロゴを置く(セル10の関数を移す) |
| `draw_pass_map()` | `src/pitchviz/pass_map.py`(新規) | パスマップを描く(セル8の処理を移す) |
| `save_figure()` | `src/pitchviz/pass_map.py`(新規) | 図を PNG として保存する(セル9の処理を移す) |
| `make_filename()` | `src/pitchviz/pass_map.py`(新規) | `pass_map_チーム名_相手チーム名.png` というファイル名を作る |

### 8-1. `loader.py` に `get_passes()` を足す(課題4)

- [ ] **[VS Code]** Explorer で `src/pitchviz/loader.py` を開く。
  - **対象**:`src/pitchviz/loader.py`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:ファイルの**末尾**(`filter_events` 関数の後ろ)に、次のコードを追記する。
- [ ] 次のコードの**空欄(`____`)を埋めて**追記し、`Command + S` で保存する。

```python
# src/pitchviz/loader.py (末尾に追記)


def get_passes(events, team_name):
    """指定チームのパスを返す。x, y, end_x, end_y(座標)と is_complete(成功パスか)の列を付ける。"""
    passes = filter_events(events, "Pass", team_name)
    passes = add_xy(passes, "location", "x", "y")
    passes = add_xy(passes, "____", "end_x", "end_y")
    passes["is_complete"] = passes["pass_outcome"].____()
    passes = passes.dropna(subset=["x", "y", "end_x", "end_y"]).copy()
    passes[["x", "y", "end_x", "end_y"]] = passes[["x", "y", "end_x", "end_y"]].astype(float)
    return passes.reset_index(drop=True)
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | パスの終点の座標が入っている列(セル3で `.str[0]` を取り出した列) |
| 2つ目 | 「空欄(`NaN`)か」を判定するメソッド名(セル3で使った) |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `filter_events(events, "Pass", team_name)` | フェーズ2で作った関数。種類が `Pass`、チームが `team_name` の行だけを返す |
| `add_xy(passes, "location", "x", "y")` | フェーズ2で作った関数。`[x, y]` の列から、x・y の2列を作る。**列の名前を変えれば、終点にも使える** |
| `dropna(subset=[...])` | 指定した列のどれかが空欄の行を取り除く(念のための安全策) |
| `.astype(float)` | 数値の型をそろえる |
| `reset_index(drop=True)` | 行番号を0から振り直す |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# src/pitchviz/loader.py (末尾に追記)


def get_passes(events, team_name):
    """指定チームのパスを返す。x, y, end_x, end_y(座標)と is_complete(成功パスか)の列を付ける。"""
    passes = filter_events(events, "Pass", team_name)
    passes = add_xy(passes, "location", "x", "y")
    passes = add_xy(passes, "pass_end_location", "end_x", "end_y")
    passes["is_complete"] = passes["pass_outcome"].isna()
    passes = passes.dropna(subset=["x", "y", "end_x", "end_y"]).copy()
    passes[["x", "y", "end_x", "end_y"]] = passes[["x", "y", "end_x", "end_y"]].astype(float)
    return passes.reset_index(drop=True)
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `pass_end_location`、2つ目は `isna`。

**自分のコードが正解と違っても、動いていればOKな例**

- `passes["is_complete"] = passes["pass_outcome"].isnull()` と書いた → 動く(`isna` と同じ働き)。
- `passes["is_complete"] = passes["pass_outcome"].isna()` を、`dropna` のあとに移した → 動く。結果は同じです。
- `astype(float)` を付けなかった → 動くことが多いが、描画のときに型の違いで警告が出る場合がある。付けるのが安全です。

**確認の仕方**

- 次のセル(8-4)で、`get_passes(events, TEAM_NAME)` の行数が、セル3の `len(passes)` と一致する。

</details>

### 8-2. `pass_map.py` を作る

- [ ] **[VS Code]** Explorer で `src/pitchviz` フォルダを右クリック → `New File` → `pass_map.py` と入力して Enter。
  - **対象**:`src/pitchviz/pass_map.py`
  - **新規作成か編集か**:新規作成
- [ ] 次のコードの全文を貼り付けて、`Command + S` で保存する。**`make_filename` 関数は、次の8-3の課題5で追記します。**

```python
# src/pitchviz/pass_map.py
"""パスマップを描いて保存する関数(フェーズ3)。"""

import re  # make_filename で使う
from pathlib import Path

import matplotlib.pyplot as plt
from mplsoccer import Pitch

# 図の色(暗い緑の背景。青とオレンジは、色の見分けにくい人にも区別しやすい組み合わせ)
BG_COLOR = "#22312b"
LINE_COLOR = "#c7d5cc"
TEXT_COLOR = "#e8efe9"
OK_COLOR = "#6cb2eb"   # 成功パス
NG_COLOR = "#f28e4b"   # 失敗パス


def add_logo(fig, anchor_ax, logo_path, height_ratio=0.8, margin=0.01):
    """anchor_ax(ロゴを置く欄)の右端に、ロゴ画像を縦横比そのままで置く。"""
    logo_path = Path(logo_path)
    if not logo_path.exists():
        print(f"[warn] logo not found: {logo_path}")
        return None

    img = plt.imread(logo_path)
    img_h, img_w = img.shape[:2]

    box = anchor_ax.get_position()
    fig_w, fig_h = fig.get_size_inches()

    logo_h = box.height * height_ratio
    logo_w = logo_h * (img_w / img_h) * (fig_h / fig_w)
    left = box.x1 - logo_w - margin
    bottom = box.y0 + (box.height - logo_h) / 2

    logo_ax = fig.add_axes([left, bottom, logo_w, logo_h])
    logo_ax.imshow(img)
    logo_ax.axis("off")
    return logo_ax


def draw_pass_map(passes, team_name, opponent_name, match_date, logo_path=None):
    """1チーム分のパスマップを描いて、図(Figure)を返す。

    passes は loader.get_passes() の結果(x, y, end_x, end_y, is_complete の列が必要)。
    図の中の文字は、フォントの都合で英語にする。
    """
    pitch = Pitch(pitch_type="statsbomb", pitch_color=BG_COLOR, line_color=LINE_COLOR)
    fig, axs = pitch.grid(figheight=9, title_height=0.08, grid_height=0.80, endnote_height=0.07,
                          title_space=0, endnote_space=0, axis=False)
    fig.set_facecolor(BG_COLOR)
    ax = axs["pitch"]

    complete = passes[passes["is_complete"]]
    failed = passes[~passes["is_complete"]]

    for subset, color, name in [(complete, OK_COLOR, "Completed"), (failed, NG_COLOR, "Failed")]:
        if len(subset) == 0:
            continue
        pitch.arrows(subset.x, subset.y, subset.end_x, subset.end_y,
                     width=2, headwidth=6, headlength=6, color=color, alpha=0.85,
                     label=f"{name} ({len(subset)})", ax=ax)

    if len(complete) + len(failed) > 0:
        ax.legend(facecolor=BG_COLOR, edgecolor=LINE_COLOR, labelcolor=TEXT_COLOR,
                  loc="upper left", fontsize=12)

    axs["title"].text(0.5, 0.68, f"{team_name} pass map vs {opponent_name}",
                      color=TEXT_COLOR, ha="center", va="center", fontsize=24,
                      transform=axs["title"].transAxes)
    axs["title"].text(0.5, 0.18, f"{match_date}   |   attacking left to right",
                      color=LINE_COLOR, ha="center", va="center", fontsize=13,
                      transform=axs["title"].transAxes)
    axs["endnote"].text(0.01, 0.5, "Data: StatsBomb Open Data",
                        color=TEXT_COLOR, ha="left", va="center", fontsize=11,
                        transform=axs["endnote"].transAxes)

    if logo_path is not None:
        add_logo(fig, axs["endnote"], logo_path)
    return fig


def save_figure(fig, path, dpi=200):
    """図を PNG として保存する。保存先のフォルダがなければ作る。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, facecolor=fig.get_facecolor())
    return path
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| ファイルの先頭の `"""..."""` | このファイルの説明(docstring)。何をするファイルかを書く習慣 |
| `BG_COLOR = ...`(ファイルの上のほう) | Notebook のセル1と同じ色の定数。**ファイルの中で、色を1か所にまとめておく** |
| `def add_logo(...)` | セル10で書いた関数と同じもの |
| `def draw_pass_map(passes, team_name, opponent_name, match_date, logo_path=None)` | セル8の処理をまとめた関数。パス、チーム名、相手チーム名、日付を受け取り、図を返す。`logo_path=None` は「渡さなければロゴなし」 |
| `for subset, color, name in [(...), (...)]:` | 成功パスと失敗パスの2つについて、同じ処理を繰り返す(同じコードを2回書かない) |
| `if len(subset) == 0: continue` | そのグループにパスが1本もなければ、描かずに次へ進む(失敗パスが0本の場合の安全策) |
| `if logo_path is not None:` | ロゴの場所が渡されたときだけ、ロゴを入れる |
| `def save_figure(fig, path, dpi=200)` | セル9の処理をまとめた関数 |
| `path.parent.mkdir(parents=True, exist_ok=True)` | 保存先のフォルダがなければ作る(あっても、エラーにしない) |

### 8-3. `make_filename()` を足す(課題5)

画像のファイル名を、チーム名と相手チーム名から自動で作る関数です。チーム名のスペースや `'`(アポストロフィ)をそのまま使うと、ファイル名として扱いにくいため、小文字に直し、記号を `_` に置き換えます。

- [ ] **[VS Code]** `src/pitchviz/pass_map.py` の**末尾**(`save_figure` 関数の後ろ)に、次のコードを追記する。
  - **対象**:`src/pitchviz/pass_map.py`
  - **新規作成か編集か**:既存ファイルの編集
- [ ] **空欄(`____`)を埋めて**追記し、`Command + S` で保存する。

```python
# src/pitchviz/pass_map.py (末尾に追記)


def make_filename(team_name, opponent_name, prefix="pass_map"):
    """例: ("Japan", "Belgium") -> "pass_map_japan_belgium.png" """
    names = [prefix, team_name, opponent_name]
    parts = []
    for name in names:
        name = name.____().replace("'", "")
        name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
        parts.append(name)
    return "_".____(parts) + "____"
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | 文字列を小文字にするメソッド名 |
| 2つ目 | リストの要素を、`_` でつないで1つの文字列にするメソッド名 |
| 3つ目 | 画像の拡張子(ドット付き) |

**コードの解説(ヒント)**

| 記述 | 意味 |
|---|---|
| `.replace("'", "")` | `'` を取り除く(例:`Women's` → `womens`) |
| `re.sub(r"[^a-z0-9]+", "_", name)` | 「英小文字・数字以外が連続する部分」を、`_` 1つに置き換える |
| `.strip("_")` | 先頭と末尾の `_` を取り除く |
| `"_".join(parts)` | `parts` の要素を `_` でつなぐ(`["a", "b"]` → `"a_b"`) |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# src/pitchviz/pass_map.py (末尾に追記)


def make_filename(team_name, opponent_name, prefix="pass_map"):
    """例: ("Japan", "Belgium") -> "pass_map_japan_belgium.png" """
    names = [prefix, team_name, opponent_name]
    parts = []
    for name in names:
        name = name.lower().replace("'", "")
        name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
        parts.append(name)
    return "_".join(parts) + ".png"
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `lower`、2つ目は `join`、3つ目は `.png`。

**自分のコードが正解と違っても、動いていればOKな例**

- `.strip("_")` を付けなかった → 動くが、名前の先頭や末尾が記号のチーム名で `_` が余る場合がある。
- 先に `name.replace(" ", "_")` で、スペースだけを置き換えた → 動く。ただし `'` など他の記号は別に処理が必要になります。この手順書の `re.sub` なら、まとめて処理できます。
- `f"{prefix}_{team}_{opponent}.png"` のように、f文字列で組み立てた → 動く(各名前を整えたあとなら、同じ結果)。

**確認の仕方**

- 次のセル11で、`make_filename("Japan", "Belgium")` が `pass_map_japan_belgium.png` になる。

**注意**

- チーム名にアクセント付きの文字(例:`Côte d'Ivoire`)があると、その文字は `_` に置き換わります(例:`c_te_d_ivoire`)。ファイル名として使うには問題ありません。

</details>

### 8-4. セル11:ファイル名の関数を確認する

- [ ] **[VS Code]** Notebook `notebooks/03_pass_map.ipynb` に戻り、次のセルを追加して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル11**

```python
# notebooks/03_pass_map.ipynb  セル11
from pitchviz.loader import get_passes
from pitchviz.pass_map import draw_pass_map, make_filename, save_figure

print(make_filename("Japan", "Belgium"))
print(make_filename("Japan Women's", "Norway Women's"))
print(len(get_passes(events, TEAM_NAME)) == len(passes))
```

**期待される出力**

```
pass_map_japan_belgium.png
pass_map_japan_womens_norway_womens.png
True
```

**確認すること**

- [ ] 1行目と2行目が、上の出力と一致する
- [ ] 3行目が `True`(`get_passes` の結果が、セル3の手作りの `passes` と同じ行数になっている)

### 8-5. セル12:両チームのパスマップを、関数で保存する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/03_pass_map.ipynb` の **セル12**

```python
# notebooks/03_pass_map.ipynb  セル12
LOGO_PATH = "../assets/statsbomb_logo_white.png"
OUTPUT_DIR = Path("../outputs")

for team in teams:
    team_passes = get_passes(events, team)
    opponent = [t for t in teams if t != team][0]

    fig = draw_pass_map(team_passes, team, opponent, MATCH_DATE, logo_path=LOGO_PATH)
    out_path = save_figure(fig, OUTPUT_DIR / make_filename(team, opponent))
    print("saved:", out_path)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `for team in teams:` | この試合の2つのチームを、順番に処理する |
| `[t for t in teams if t != team][0]` | 自分以外のチーム(= 相手)を取り出す |
| `draw_pass_map(...)` | パスマップを描いて、図を返す |
| `save_figure(fig, パス)` | 保存して、保存先を返す |

**期待される出力の例**(順番は、チーム名の並びによって違います)

```
saved: ../outputs/pass_map_belgium_japan.png
saved: ../outputs/pass_map_japan_belgium.png
```

- セルの下に、**2つの図**(両チームのパスマップ)が表示される。

**生成されるファイル**

- `outputs/pass_map_belgium_japan.png`
- `outputs/pass_map_japan_belgium.png`

- [ ] **[VS Code]** Explorer の `outputs/` で2つの PNG を開き、次を確認する。
  - それぞれのタイトルのチーム名が、画像の中のパスの持ち主のチームと合っている(例:`Japan pass map vs Belgium` の画像で、凡例のパス数が日本のもの)
  - ロゴと出典が入っている
  - 両チームとも、右向きに攻めている(StatsBomb のデータの記録のしかた)

### 手順8の完了チェック

- [ ] 課題4・5を解いて、答え合わせをした
- [ ] セル11で、ファイル名の確認が期待どおりに出た
- [ ] セル12で、両チームの PNG が `outputs/` に保存された
- [ ] `loader.py` と `pass_map.py` を書き換えたとき、セルの再実行だけで反映される(`%autoreload` の効果)ことを理解した

---

## 手順9:README・コミット・振り返り

**所要時間:約0.75時間**

### 9-1. README の進捗を更新する

- [ ] **[VS Code]** Explorer で `README.md` を開く。
  - **対象**:`README.md`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:`## 進捗` の下の `- [x] フェーズ2:データ取得と構造の理解` の**次の行**に、次の1行を足す。
- [ ] 追記して `Command + S` で保存する。

```markdown
- [x] フェーズ3:パスマップ
```

### 9-2. Notebook を保存する

- [ ] **[VS Code]** `Command + S` で `03_pass_map.ipynb` を保存する。

### 9-3. `git status` で、記録されるものを確認する

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
	modified:   src/pitchviz/loader.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/phase3_passmap.md
	notebooks/03_pass_map.ipynb
	src/pitchviz/pass_map.py

no changes added to commit (use "git add" and/or "git commit -a")
```

**確認すること**

- `.gitignore`、`README.md`、`loader.py` が `modified` になっている。
- `docs/phase3_passmap.md`(この手順書)、`notebooks/03_pass_map.ipynb`、`src/pitchviz/pass_map.py` が Untracked に出る。
- **`assets/`(ロゴ画像)と、`outputs/` の PNG が表示されない**こと(`.gitignore` の効果)。
- `.venv/` や `data/` が出ていないこと。

- [ ] **[Terminal]** `~/projects/pitchviz` で、ロゴと画像が Git の対象外になっていることを確認する。

```bash
git check-ignore -v assets/statsbomb_logo_white.png outputs/pass_map_japan_belgium.png
```

期待される出力の例(行番号は環境で違います):

```
.gitignore:27:assets/*.png	assets/statsbomb_logo_white.png
.gitignore:24:outputs/*	outputs/pass_map_japan_belgium.png
```

### 9-4. ステージングしてコミットする

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
	new file:   docs/phase3_passmap.md
	new file:   notebooks/03_pass_map.ipynb
	modified:   src/pitchviz/loader.py
	new file:   src/pitchviz/pass_map.py
```

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git commit -m "Phase 3: draw pass maps with mplsoccer (completed vs failed, logo, PNG output)"
```

期待される出力の例:

```
[main xxxxxxx] Phase 3: draw pass maps with mplsoccer (completed vs failed, logo, PNG output)
 6 files changed, xxx insertions(+)
 create mode 100644 docs/phase3_passmap.md
 create mode 100644 notebooks/03_pass_map.ipynb
 create mode 100644 src/pitchviz/pass_map.py
```

- コミットメッセージは、日本語でも構いません(例:`フェーズ3: パスマップの描画と PNG 保存`)。

### 9-5. GitHub に push する

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
  - `src/pitchviz/pass_map.py` と `notebooks/03_pass_map.ipynb` が表示される。
  - **リポジトリが `Private` のまま**である(ページ名の横に `Private` と表示される)。
  - `assets/` のロゴ画像が、GitHub 上にない。

### 9-6. 振り返り

次の質問に、1〜2行で自分の言葉で答えてみてください。

1. `pass_outcome` が空欄(`NaN`)のパスが「成功」なのは、なぜですか?
    → 失敗のときのみ、`pass_outcome`に値が入る仕様のため
2. `passes[~passes["is_complete"]]` の `~` は、何をしていますか?
    → 失敗のパスのみを抽出している（成功ではない）
3. 画像の中の文字を、英語にしたのはなぜですか?
    
    →　標準フォントに日本語が含まれていないため
4. ロゴを置くときに `(fig_h / fig_w)` を掛けるのは、なぜですか?
    
    →　画像と図の縦横比の違いを補正して、ロゴが引き伸ばされないようにするため
5. ロゴ画像を、`.gitignore` で Git の対象外にしたのは、なぜですか?

    → 未確定情報のまま、GitHubに公開させないため

- [ ] 1に「失敗などのときだけ `pass_outcome` に値が入る仕様のため」のように答えられる
- [ ] 2に「True と False を反転して、失敗したパスの行を取り出している」のように答えられる
- [ ] 3に「標準フォントに日本語が入っておらず、文字が四角(□)になるため」のように答えられる
- [ ] 4に「画像と図の縦横比の違いを補正して、ロゴが引き伸ばされないようにするため」のように答えられる
- [ ] 5に「ロゴを再配布してよいかが未確認で、確認できるフェーズ6まで公開しないため」のように答えられる

### 手順9の完了チェック

- [ ] README に、フェーズ3の進捗が追記された
- [ ] `git status` で、想定したファイルだけが表示された(ロゴと PNG は表示されない)
- [ ] `git commit` と `git push` が成功した
- [ ] GitHub のリポジトリが `Private` のままである
- [ ] 振り返りの5問に答えられた

---

## 手順10:つまずきやすい点と対処法

### 10-1. エラー別の対処表

| 症状・エラーメッセージの例 | 原因 | 対処 |
|---|---|---|
| `NoAuthWarning: credentials were not supplied. Open data access only` | 有料 API のログイン情報がない(**警告であり、エラーではない**) | 無視して構いません |
| `ModuleNotFoundError: No module named 'mplsoccer'` | Notebook のカーネルが `.venv` ではない | 右上のカーネルを `.venv` に切り替える。それでもだめなら、ターミナルで `pip list` に `mplsoccer` があるか確認する |
| `ModuleNotFoundError: No module named 'pitchviz'` | セル1の `sys.path.append("../src")` を実行していない、または `src/pitchviz/__init__.py` がない | セル1を実行し直す。`src/pitchviz/__init__.py` があるか確認する |
| `ImportError: cannot import name 'get_passes' from 'pitchviz.loader'` | 課題4の関数を `loader.py` に追記していない、または保存していない | `loader.py` の末尾に関数があるか確認し、保存してから Restart する |
| `ImportError: cannot import name 'make_filename' from 'pitchviz.pass_map'` | 課題5の関数を追記していない、または保存していない | `pass_map.py` の末尾に関数があるか確認して保存する |
| `NameError: name 'passes' is not defined`(または `fig`、`axs`、`events`) | 前のセルを実行していない、または Restart のあとに実行し直していない | Restart して、セル1から順に実行する。セル10は、セル8を先に実行しておく |
| `KeyError: 'pass_end_location'` | 取得した `events` に、その列がない(パスのない試合、列名の違い) | `print(list(events.columns))` で列名を確認する。`events["type"].value_counts()` で `Pass` があるか確認する |
| `KeyError: 'is_complete'` | セル3(または `get_passes`)を実行していない | セル3を実行する。関数を使う場合は、`passes = get_passes(events, TEAM_NAME)` で作る |
| `TypeError: arrows() got an unexpected keyword argument '...'` | mplsoccer の更新で、引数の名前が変わった | `pip list` で mplsoccer の版を確認し、[公式ドキュメント](https://mplsoccer.readthedocs.io)の `Pitch.arrows`(API)と、ギャラリーの「Plot arrows」の例を確認する |
| `TypeError: grid() got an unexpected keyword argument '...'` | `pitch.grid` の引数名の更新、または綴りの間違い | 公式ドキュメントの `Pitch.grid` の引数を確認する |
| `IndexError: list index out of range`(`opponent_name = [...][0]` の行) | `TEAM_NAME` が、`events["team"]` のどの名前とも一致せず、リストが空になった | セル2の `print(teams)` で、チーム名の綴りを確認して、一字一句同じにする(`'` の形に注意) |
| 矢印が1本も描かれない | `passes` が空(チーム名の不一致)、または座標が `NaN` | `len(passes)` を確認する。`passes[["x", "y", "end_x", "end_y"]].isna().sum()` で空欄を確認する |
| 凡例が出ない、または `No artists with labels found to put in legend` | `pitch.arrows` に `label=` を付けていない、または描くデータが0本 | `label=` の付け忘れを確認する。`len(complete)`、`len(failed)` を確認する |
| 文字が四角(□)になる、`UserWarning: Glyph ... missing from font(s) DejaVu Sans.` | 画像の中に日本語を入れた | 画像の中の文字を英語にする(手順5) |
| `FileNotFoundError: [Errno 2] No such file or directory: '../outputs/...'`(`Path.cwd()` の確認) | Notebook の場所が想定と違う、または `outputs/` がない | セルで `print(Path.cwd())` を実行して、`.../pitchviz/notebooks` になっているか確認する。`save_figure` を使えば、フォルダは自動で作られる |
| `[warn] logo not found: ../assets/statsbomb_logo_white.png` | ロゴのファイル名や場所が違う | ターミナルで `ls assets` を実行し、ファイル名を確認する(手順1-4) |
| ロゴが横に引き伸ばされる、または極端に大きい・小さい | `logo_w` の計算で `(fig_h / fig_w)` を付け忘れた、`height_ratio` の値が大きい | 課題3の答えのとおりの式になっているか確認する。`height_ratio` を `0.6` に下げる |
| ロゴが背景に溶けて見えない | 暗い背景に黒いロゴ(`default`)を使っている | 暗い背景には `statsbomb_logo_white.png` を使う |
| 保存した PNG の背景が白い | `facecolor=fig.get_facecolor()` を付けていない | `fig.savefig(..., facecolor=fig.get_facecolor())` にする(`save_figure` を使えば付いています) |
| 保存した PNG が、Notebook の表示と違う | ロゴを足す前に保存した | セル10のあとで、セル9を実行し直す |
| 矢印が多すぎて、重なって見づらい | 1試合に数百本のパスがあるため | `alpha`(透明度)を `0.6` に下げる、`width` を `1.5` にするなど調整する |
| 矢印が太すぎて、ピッチが塗りつぶされる。または細すぎて見えない | `width`、`headwidth`、`headlength` の数値が、図の大きさに合っていない | 公式ギャラリーの例(`width=2`、`headwidth=10`、`headlength=10`)を出発点にして、数値を少しずつ変えて画像で確認する。`figsize` の大きさを変えても見え方が変わる |
| `ValueError: Image size of ... pixels is too large` | `dpi` や `figheight` が大きすぎる | `dpi=200` を `150` に下げる |
| `TypeError: draw_pass_map() missing 1 required positional argument` | 引数の数が足りない | `draw_pass_map(passes, team, opponent, match_date, logo_path=...)` の5つの引数を確認する |
| `loader.py` や `pass_map.py` を直したのに、結果が変わらない | 古い内容を読み込んだままになっている | セル1に `%autoreload 2` があるか確認する。なければ Restart してセル1から実行し直す |
| ロゴ画像が `git status` に出る(`assets/` が Untracked) | `.gitignore` に `assets/*.png` を追記していない、または保存していない | 手順1-5を確認する。すでに `git add` してしまった場合は、`git rm --cached assets/statsbomb_logo_white.png` を実行する |

### 10-2. 「描けているけれど、合っているか分からない」ときの確認方法

- **件数を、手計算の数字と照らす**:`len(passes)` が、試合の公式記録のパス数にあたる数字の規模(数百本)になっているか。
- **別のチームでも動くか**:`TEAM_NAME` を相手チームにして、同じセルが動くか確認する(動けば、チームに依存しないコードになっています)。
- **別の試合でも動くか**:`MATCH_ID` を別の試合に変えて、セル2から実行し直す。
- **目で確かめる**:矢印の向きが、おおむねゴール側(右)に向かっているか。自陣(左)から相手陣(右)への長い矢印が、少数あるか。

---

## 手順11:Claude / ChatGPT に質問するときのコツ(描画編)

### 11-1. 描画の質問に、必ず入れるもの

1. **やりたいこと**:「パスマップの矢印を、成功と失敗で色を分けたい」
2. **実行したセルのコード全文**
3. **エラー文の全文**(最初の `Traceback` から、最後のエラー名の行まで)。**エラーが出ない場合は、「何が期待と違うか」**(例:矢印が1本も出ない、ロゴが引き伸ばされる)
4. **データの確認結果**:`passes.shape`、`passes[["x", "y", "end_x", "end_y", "is_complete"]].head()`、`passes["is_complete"].value_counts()`
5. **環境**:`pip list | grep -i -E "mplsoccer|matplotlib|pandas"` の出力(ターミナルで実行する)

### 11-2. 画像の質問のしかた

- **出てきた画像を、スクリーンショットで添える**。文章だけでは伝わらない崩れ(文字のはみ出し、重なり)が、画像だと一目で伝わります。
- 画像に**「どこが」「どう」おかしいか**を書く(例:「左上の凡例が、ピッチの矢印に重なっている」)。
- 直したい点が複数あるときは、**1つずつ**質問する。一度に直すと、どの変更が効いたか分からなくなります。
- 「`pass_map.py` の**この関数だけ**を直してください」と、範囲を限定すると、他の部分が意図せず変わるのを防げます。

### 11-3. 質問の例

> macOS、Python 3.13.3、VS Code の Jupyter で、mplsoccer でパスマップを描いています。次のセルで、ロゴが横に引き伸ばされて表示されます。
>
> ```python
> logo_w = logo_h * (img_w / img_h)
> ```
>
> 図の大きさは `fig.get_size_inches()` で `(11.2, 9.0)`、ロゴ画像の `shape` は `(240, 960, 4)` です。縦横比を保つには、どう直せばよいですか? 初学者向けに、理由も教えてください。
>
> `pip list` の出力(抜粋):
>
> ```
> matplotlib   x.x.x
> mplsoccer    x.x.x
> ```

### 11-4. 回答の使い方

- AI が示した引数名や関数名は、**必ず公式ドキュメント(mplsoccer の API とギャラリー)か、`help(pitch.arrows)` で実在を確認**する。ライブラリの版によって違うことがあります。
- 見た目の調整(色・大きさ・位置)は、**数値を少しずつ変えて、画像で確認**する。
- 分からないまま貼らず、「この1行は何をしますか?」と聞いてから実行する。

---

## このフェーズ終了時のディレクトリツリー

`NEW` は新しく作ったファイル、`MOD` は変更したファイルです。

```
~/projects/pitchviz/
├── .git/
├── .gitignore                         # MOD(assets/*.png を追記)
├── .venv/
├── README.md                          # MOD(進捗を追記)
├── requirements.txt
├── assets/                            # NEW(ロゴの置き場)
│   ├── statsbomb_logo_white.png       # NEW(Git管理外)
│   └── statsbomb_logo_default.png     # NEW(Git管理外)
├── docs/
│   ├── 00_overview.md
│   ├── phase1_setup.md
│   ├── phase2_data.md
│   └── phase3_passmap.md              # NEW
├── notebooks/
│   ├── 01_setup_check.ipynb
│   ├── 02_explore_data.ipynb
│   └── 03_pass_map.ipynb              # NEW
├── src/
│   └── pitchviz/
│       ├── __init__.py
│       ├── loader.py                  # MOD(get_passes を追加)
│       └── pass_map.py                # NEW(add_logo / draw_pass_map / save_figure / make_filename)
├── outputs/
│   ├── .gitkeep
│   ├── empty_pitch.png                # (フェーズ1。Git管理外)
│   ├── dark_pitch.png                 # (フェーズ1。Git管理外)
│   ├── pass_map_japan_belgium.png     # NEW(Git管理外)
│   └── pass_map_belgium_japan.png     # NEW(Git管理外)
└── data/                              # (空。Git管理外)
```

---

## フェーズ3 最終チェックリスト

**データと描画**

- [ ] `get_passes()` で、チームごとのパス(`x`、`y`、`end_x`、`end_y`、`is_complete`)を取り出せる
- [ ] 成功パスと失敗パスを、色で区別して描ける
- [ ] パス成功率を計算できる
- [ ] タイトル・凡例・出典・ロゴの入った図を描ける

**動くもの**

- [ ] `outputs/pass_map_チーム名_相手チーム名.png` が、両チーム分保存されている
- [ ] 保存した画像に、StatsBomb のロゴと `Data: StatsBomb Open Data` が入っている
- [ ] `make_filename()` で、ファイル名を自動で作れる

**Git / GitHub**

- [ ] `git log --oneline` に、フェーズ3のコミットがある
- [ ] ロゴ画像と PNG が、Git の対象外になっている
- [ ] GitHub のリポジトリが `Private` のままである

すべてにチェックが付けば、フェーズ3は完了です。

---

## 次のフェーズへ

フェーズ4では、同じ試合のシュートを使って、次のことを行います。

- シュートの位置を、ピッチ上にマーカーで描く(ゴール前の半分だけを描く)
- マーカーの大きさに xG を、色や形に結果(ゴール・セーブなど)を反映する
- ショットマップを `outputs/` に PNG で保存する(ロゴと出典つき)

今回作った `pass_map.py` の `add_logo()` や `save_figure()` は、フェーズ4でもそのまま使えます。

準備ができたら「フェーズ4をお願いします」と指示してください。

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| mplsoccer(API・ギャラリー) | `https://mplsoccer.readthedocs.io`(`Pitch`、`Plot arrows`、`Pass network`) |
| matplotlib | `https://matplotlib.org/stable/`(`Axes.legend`、`Figure.savefig`、`Figure.add_axes`、`imread`) |
| pandas | `https://pandas.pydata.org/docs/`(`Series.str`、`DataFrame.dropna`) |
| StatsBomb Open Data(データ・仕様書・利用条件) | `https://github.com/statsbomb/open-data`(`doc` フォルダ、`LICENSE.pdf`) |
| statsbombpy | `https://github.com/statsbomb/statsbombpy` |
