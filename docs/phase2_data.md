# フェーズ2:データ取得と構造の理解

> 保存先:`~/projects/pitchviz/docs/phase2_data.md`
> このフェーズの終わりには「日本代表の試合を1つ選び、その試合のイベントデータをパスとシュートに絞り込み、座標を取り出せる」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | StatsBomb Open Data から日本代表の試合を探し、イベントデータ(パス・シュート)の構造を理解する |
| 想定所要時間 | 約8時間(下の内訳を参照) |
| 終了時の「動くもの」 | 選んだ試合の events を DataFrame で取得し、パスとシュートに絞り込み、x / y 座標の列を作れる |

### 作業ラベルの見方

- **[Terminal]**:ターミナルでの作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 事前準備と利用条件の確認 | 0.5h |
| 2 | Notebook の作成と pandas 入門 | 0.75h |
| 3 | 大会一覧(competitions)を調べる | 1.0h |
| 4 | 試合一覧(matches)から日本代表を探す | 1.75h |
| 5 | 試合を1つ選び、イベントデータを取得する | 1.25h |
| 6 | パスとシュートに絞り込み、座標を取り出す | 1.25h |
| 7 | 動いたコードを `loader.py` に移す | 0.75h |
| 8 | README にクレジットを入れ、コミット・振り返り | 0.75h |
| | 合計 | 8.0h |

### このフェーズについての大事な前提

- **データの中身は、実際に実行して確かめます。** この手順書の「期待される出力」には、2026年10月9日に公式データを確認した際の内容を「例」として載せています。ただし、StatsBomb 側でデータは更新されることがあります。**あなたの画面の出力が正解です。**
- **チーム名の表記は、データ上の文字列をそのまま使います。** 推測で書かず、手順4で出力された文字列をコピーして使ってください。
- **このフェーズのコードは、手順書の作成時にインターネット上の実データに対して実行して確認したものではありません。** ライブラリの仕様や列名が違う場合は、エラー文や `columns` の出力を見て、手順9の対処や、手順10の質問のコツを使ってください。仕様は [statsbombpy の GitHub](https://github.com/statsbomb/statsbombpy) と [StatsBomb Open Data の公式リポジトリ](https://github.com/statsbomb/open-data) で確認してください。
- このフェーズは**インターネットに接続した状態**で行います(データを GitHub から都度取得するため)。

---

## 手順1:事前準備と利用条件の確認

**所要時間:約0.5時間**

### 1-1. ターミナルを開き、仮想環境を有効化する

- [ ] **[VS Code]** `~/projects/pitchviz` をフォルダとして開く(`File → Open Folder...` → `projects → pitchviz`)。
- [ ] **[VS Code]** 内蔵ターミナルを開く(`Terminal → New Terminal`)。行頭に `(.venv)` が出ていることを確認する。
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
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

- `working tree clean` と出ない場合は、フェーズ1の内容がコミットされていません。フェーズ1の手順7を先に終えてください(自作の追加ファイルがある場合は、それらが表示されても構いません)。

### 1-2. StatsBomb Open Data の利用条件を確認する(必須)

データを使う前に、利用条件を読みます。**これはこのフェーズの必須作業です。**

- [ ] **[Browser]** `https://github.com/statsbomb/open-data` を開く。
- [ ] ページの下のほうにある **Terms & Conditions(利用条件)** の節を読む。
- [ ] ファイル一覧にある **`LICENSE.pdf`** を開いて読む。

**確認すること**

| 確認項目 | 内容 |
|---|---|
| クレジット表記 | 研究・分析・その結果を公開・共有する場合の、データ元の書き方 |
| ロゴの使用 | StatsBomb のロゴを使う指定があるか。ある場合、ロゴの入手先(StatsBomb の Media Pack)も確認する |
| その他の条件 | 公開・共有・再配布に関する条件 |

- 2026年10月9日に README を確認した時点では、成果を公開・共有するときは**データ元を StatsBomb と明記し、StatsBomb のロゴを使う**旨の記載がありました。**ただし、この要約は正確な条文ではありません。必ずご自身で原文を読んで、最新の条件を確認してください。**
- このプロジェクトでは、GitHub でコードと画像を公開するため、**この条件が直接関係します**。フェーズ6でロゴ・クレジットを README に反映します。ここでは手順8で、先にクレジットの文章だけ README に入れます。

- [ ] 確認した内容(クレジットの書き方、ロゴの要否)を、メモに1〜2行で書き留める。

### 1-3. データの仕様書の場所を知る

- [ ] **[Browser]** `https://github.com/statsbomb/open-data` の `doc` フォルダを開き、PDF の一覧を確認する。
  - イベントデータ(Events)や、データ全体の仕様を説明する PDF があります。**今すぐ読まなくて構いません**。分からない列が出てきたときの辞書として使います。

### 手順1の完了チェック

- [ ] `(.venv)` が行頭に表示されている
- [ ] `git status` で `working tree clean`(またはフェーズ1の自作ファイルのみ)と出る
- [ ] StatsBomb の利用条件を読み、クレジット・ロゴについてメモした

---

## 手順2:Notebook の作成と pandas 入門

**所要時間:約0.75時間**

pandas は「表(DataFrame)を扱うライブラリ」です。StatsBomb のデータはすべて表として届くので、先に最小限の使い方を練習します。

### 2-1. Notebook を作る

- [ ] **[VS Code]** 左サイドバーの Explorer で `notebooks` フォルダを右クリック → `New File` → `02_explore_data.ipynb` と入力して Enter。
  - **対象**:`notebooks/02_explore_data.ipynb`
  - **新規作成か編集か**:新規作成
- [ ] **[VS Code]** 右上の `Select Kernel` → `Python Environments...` → `.venv`(`Python 3.13.3 (.venv)` など)を選ぶ。

> **セルの使い方**(フェーズ1と同じ)
> `+ Code` でセルを追加し、`Shift + Enter` で実行します。**セルは番号順(上から順)に実行してください。** 動かなくなったら、上部の **Restart**(カーネル再起動)を押し、セル1から順に実行し直します。

### 2-2. セル1:準備

- [ ] **[VS Code]** 最初のセルに、次を入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル1**

```python
# notebooks/02_explore_data.ipynb  セル1
%load_ext autoreload
%autoreload 2

import sys

import pandas as pd
from statsbombpy import sb

# src フォルダを import の探索先に追加する(後で自作の loader.py を使うため)
sys.path.append("../src")

# 表の表示設定(列が省略されにくくなる)
pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 200)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `%load_ext autoreload` と `%autoreload 2` | Notebook の特別な命令。`.py` ファイルを書き換えたとき、再起動しなくても最新の内容が反映される |
| `from statsbombpy import sb` | StatsBomb のデータを取得するための道具 `sb` を読み込む |
| `sys.path.append("../src")` | Python が自作モジュールを探す場所に `src` フォルダを追加する。Notebook は `notebooks/` にあるので、`..`(1つ上)の `src` を指す |
| `pd.set_option(...)` | 表を表示するとき、最大60列まで・幅200文字まで表示する設定 |

**期待される出力**

- 何も表示されなくて正常です(エラーが出なければ成功)。

> **注意**:このあと `sb` の関数を使うと、`NoAuthWarning: credentials were not supplied. Open data access only` という警告が出ます。これは「有料 API のログイン情報がない(無料データだけを使う)」という意味で、**エラーではありません**。無視して構いません。

### 2-3. セル2:小さな表(DataFrame)を作る

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル2**

```python
# notebooks/02_explore_data.ipynb  セル2
toy = pd.DataFrame(
    {
        "team": ["A", "B", "A", "B"],
        "player": ["p1", "p2", "p3", "p4"],
        "shots": [3, 5, 2, 1],
    }
)
toy
```

**期待される出力**

```
  team player  shots
0    A     p1      3
1    B     p2      5
2    A     p3      2
3    B     p4      1
```

(Notebook では、罫線つきの表で表示されます)

### 2-4. セル3:取り出す・絞り込む・集計する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル3**

```python
# notebooks/02_explore_data.ipynb  セル3
print(toy["shots"])                        # 1列を取り出す
print(toy[toy["team"] == "A"])             # 条件に合う行だけを取り出す
print(toy.groupby("team")["shots"].sum())  # チームごとに合計する
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `toy["shots"]` | `shots` 列だけを取り出す |
| `toy["team"] == "A"` | 各行について「team が A か」を判定し、True / False の列を作る |
| `toy[ 条件 ]` | 条件が True の行だけを残す(**絞り込み**。この書き方を今後何度も使う) |
| `toy.groupby("team")["shots"].sum()` | チームごとにグループ分けし、`shots` を合計する |

**期待される出力**

```
0    3
1    5
2    2
3    1
Name: shots, dtype: int64
  team player  shots
0    A     p1      3
2    A     p3      2
team
A    5
B    6
Name: shots, dtype: int64
```

### 手順2の完了チェック

- [ ] セル1がエラーなく実行できた
- [ ] セル3で、チームAの行だけが取り出せ、チームごとの合計(A=5、B=6)が出た
- [ ] 「`表[ 条件 ]` で行を絞り込む」ことを説明できる

---

## 手順3:大会一覧(competitions)を調べる

**所要時間:約1.0時間**

StatsBomb のオープンデータは、**大会(competition)→ シーズン(season)→ 試合(match)→ イベント(event)** の順に階層になっています。最初は、どんな大会が収録されているかを調べます。

```
competitions(大会+シーズンの一覧)
  └─ matches(その大会・シーズンの試合一覧)
        └─ events(1試合の全イベント:パス、シュートなど)
```

### 3-1. セル4:大会一覧を取得する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。インターネット接続が必要です。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル4**

```python
# notebooks/02_explore_data.ipynb  セル4
competitions = sb.competitions()
print(competitions.shape)
competitions.head()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `sb.competitions()` | 収録されている大会とシーズンの一覧を、表(DataFrame)で返す |
| `.shape` | (行数, 列数)。何行何列の表かを確認できる |
| `.head()` | 先頭の数行だけ表示する(表が大きいときの確認に使う) |

**期待される出力の例**(行数・列数は更新で変わることがあります)

```
NoAuthWarning: credentials were not supplied. Open data access only
(80, 12)
```

続いて、先頭5行の表が表示されます。

### 3-2. セル5:列の名前を確認する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル5**

```python
# notebooks/02_explore_data.ipynb  セル5
print(list(competitions.columns))
```

**期待される出力の例**

```
['competition_id', 'season_id', 'country_name', 'competition_name', 'competition_gender', 'competition_youth', 'competition_international', 'season_name', 'match_updated', 'match_updated_360', 'match_available_360', 'match_available']
```

**主な列の意味**

| 列名 | 意味 |
|---|---|
| `competition_id` | 大会のID(数字) |
| `season_id` | シーズンのID(数字)。**試合一覧を取るときは、この2つのIDの組み合わせが必要** |
| `competition_name` | 大会名(例:`FIFA World Cup`) |
| `season_name` | シーズン名(例:`2022`) |
| `competition_gender` | `male`(男子)か `female`(女子) |

### 3-3. セル6:ワールドカップに絞り込む

日本代表が出ていそうな大会として、まず名前に `World Cup` を含むものに絞ります。

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル6**

```python
# notebooks/02_explore_data.ipynb  セル6
wc = competitions[competitions["competition_name"].str.contains("World Cup", na=False)]
wc[["competition_id", "season_id", "competition_name", "season_name", "competition_gender"]]
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `competitions["competition_name"]` | 大会名の列 |
| `.str.contains("World Cup", na=False)` | 文字列に `World Cup` を含むか判定する。`na=False` は、値が空のとき「含まない」として扱う指定 |
| `competitions[ 条件 ]` | 手順2で練習した絞り込み |
| `wc[[...]]` | 列名のリストを渡して、見たい列だけを表示する(`[[` と二重の角括弧になる点に注意) |

**期待される出力の例**(2026年10月9日に公式データを確認した際の内容。あなたの出力が正です)

| competition_id | season_id | competition_name | season_name | competition_gender |
|---|---|---|---|---|
| 43 | 106 | FIFA World Cup | 2022 | male |
| 43 | 3 | FIFA World Cup | 2018 | male |
| 43 | 55 | FIFA World Cup | 1990 | male |
| 43 | 54 | FIFA World Cup | 1986 | male |
| 43 | 51 | FIFA World Cup | 1974 | male |
| 43 | 272 | FIFA World Cup | 1970 | male |
| 43 | 270 | FIFA World Cup | 1962 | male |
| 43 | 269 | FIFA World Cup | 1958 | male |
| 72 | 107 | Women's World Cup | 2023 | female |
| 72 | 30 | Women's World Cup | 2019 | female |
| 1470 | 274 | FIFA U20 World Cup | 1979 | male |

**確認すること**

- [ ] 男子(`FIFA World Cup`)の 2018 と 2022 があるか(日本代表の第一候補)
- [ ] 女子(`Women's World Cup`)の 2019 と 2023 があるか(代替候補)
- [ ] 上の表のID(`competition_id` と `season_id`)を、自分の画面の値で確認して、メモする

> **ポイント**:女子大会の名前は `Women's World Cup`(`FIFA` が付かない)、チーム名にも男子と違う表記が使われます。**「名前は推測せず、データの文字列を確認する」ことがここまでの教訓です。**

### 手順3の完了チェック

- [ ] `competitions.shape` で行数・列数が表示された
- [ ] `competitions.columns` の一覧を見て、`competition_id` と `season_id` があることを確認した
- [ ] `wc` の表に男子と女子のワールドカップが表示された
- [ ] 日本代表が出る可能性のある大会のID(男子 2018・2022、女子 2019・2023)をメモした

---

## 手順4:試合一覧(matches)から日本代表を探す

**所要時間:約1.75時間**

大会の次は、その大会・シーズンの**試合一覧**を取得します。「competitions → matches の順に絞る」流れです。

### 4-1. セル7(課題1):試合一覧を1つ取得する

まず、ID を指定して、1つの大会・シーズンの試合一覧を取る練習をします。

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル7**
  - 空欄を埋めるまでは、エラーになります(正常です)。

```python
# notebooks/02_explore_data.ipynb  セル7(課題1)
matches_2022 = sb.matches(competition_id=____, season_id=____)
print(matches_2022.shape)
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目の `____` | セル6の表で、`FIFA World Cup` の `2022` の行にある `competition_id` |
| 2つ目の `____` | 同じ行の `season_id` |

**期待される出力の例**

```
(64, 20)
```

(2022年男子ワールドカップは全64試合。列数は環境により違うことがあります。)

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/02_explore_data.ipynb  セル7(課題1)
matches_2022 = sb.matches(competition_id=43, season_id=106)
print(matches_2022.shape)
```

**答え合わせのあとに**

- 答えは、**あなたのセル6の表の値**です。上の `43` と `106` は2026年10月9日の確認時の値で、自分の表と違っていたら自分の表を優先してください。
- 数字の順番を逆にして書いた場合(`competition_id=106, season_id=43`)は、別の大会が取得されたり、エラーになります。キーワード引数(`competition_id=` のように名前付き)なので、**名前と値の対応**を確認してください。

**自分のコードが正解と違っても、動いていればOKな例**

- 数字を変数に入れて渡した(例:`cid = 43` → `competition_id=cid`)→ 動く。むしろ読みやすい書き方です。
- 別の大会(例:女子 2023)のIDを入れた → 動く。行数が変わるだけです。

**確認の仕方**

- `matches_2022.shape` の行数が、その大会の試合数(2022年男子なら64)に近い。

</details>

### 4-2. セル8:試合一覧の中身を見る

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル8**

```python
# notebooks/02_explore_data.ipynb  セル8
print(list(matches_2022.columns))
matches_2022[["match_id", "match_date", "home_team", "away_team", "home_score", "away_score"]].head()
```

**期待される出力の例**

```
['match_id', 'match_date', 'kick_off', 'competition', 'season', 'home_team', 'away_team', 'home_score', 'away_score', 'match_status', ...]
```

続いて、`match_id`、`match_date`、`home_team`(ホームチーム名)、`away_team`(アウェイチーム名)、`home_score`、`away_score` の表が表示されます。

**主な列の意味**

| 列名 | 意味 |
|---|---|
| `match_id` | 試合のID(数字)。**イベントデータを取るときに使う最重要の列** |
| `match_date` | 試合日 |
| `home_team` / `away_team` | チーム名の文字列 |
| `competition` / `season` | 大会名・シーズン名 |
| `competition_stage` | 大会の段階(例:`Group Stage`) |

> **列名が違う場合**:ライブラリの更新で列名が変わることがあります。`KeyError` が出たら、上の `print(list(...columns))` の出力を見て、実際にある列名に置き換えてください。

### 4-3. セル9:候補の大会すべての試合を集める

日本代表は、男子・女子の複数の大会に出ている可能性があります。セル6で絞った `wc`(ワールドカップ)の**すべてのシーズンの試合**を取得して、1つの表にまとめます。

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。数十秒かかることがあります。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル9**

```python
# notebooks/02_explore_data.ipynb  セル9
frames = []
for _, row in wc.iterrows():
    matches = sb.matches(
        competition_id=row["competition_id"],
        season_id=row["season_id"],
    )
    frames.append(matches)
    print(row["competition_name"], row["season_name"], len(matches))

all_matches = pd.concat(frames, ignore_index=True)
print(all_matches.shape)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `frames = []` | 取得した表を入れていく空のリスト |
| `for _, row in wc.iterrows():` | `wc` の表を1行ずつ取り出して繰り返す。`row` はその行、`_` は行番号(今回は使わない) |
| `row["competition_id"]` | その行の大会IDを取り出す |
| `frames.append(matches)` | 取得した試合の表を、リストに追加する |
| `pd.concat(frames, ignore_index=True)` | 複数の表を縦につなげて1つにする。`ignore_index=True` で行番号を振り直す |

**期待される出力の例**(試合数は例です)

```
FIFA World Cup 2022 64
FIFA World Cup 2018 64
FIFA World Cup 1990 ...
...
Women's World Cup 2023 64
Women's World Cup 2019 52
(xxx, 20)
```

### 4-4. セル10:「Japan」を含むチーム名を探す

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル10**

```python
# notebooks/02_explore_data.ipynb  セル10
teams = pd.concat([all_matches["home_team"], all_matches["away_team"]]).unique()
japan_names = sorted([t for t in teams if "Japan" in t])
print(japan_names)
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `pd.concat([home_team の列, away_team の列])` | ホームとアウェイのチーム名を縦につなげる |
| `.unique()` | 重複をなくして、チーム名の種類だけにする |
| `[t for t in teams if "Japan" in t]` | `teams` から、`Japan` という文字を含む名前だけを集める(リスト内包表記) |
| `sorted(...)` | 並べ替える |

**期待される出力の例**(2026年10月9日の確認時の例。あなたの出力が正です)

```
['Japan', "Japan Women's"]
```

**確認すること**

- [ ] 出力されたチーム名の文字列を、**一字一句そのまま**メモする(男子と女子で表記が違う点に注意)。
  - 例:男子は `Japan`、女子は `Japan Women's`(確認時の例)。
  - ほかのチーム名にも `W` や `Women's` など表記の違いがあります(確認時の例:`Scotland W`、`Argentina Women's`)。**以降は、自分の出力にある文字列だけを使います。**

> **出力が空のリスト `[]` だった場合**:日本代表がこの条件では見つかりませんでした。次のセル12(代替案)に進みます。

### 4-5. セル11:日本代表の試合一覧を作る

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル11**

```python
# notebooks/02_explore_data.ipynb  セル11
is_japan = all_matches["home_team"].isin(japan_names) | all_matches["away_team"].isin(japan_names)
japan_matches = all_matches[is_japan].sort_values("match_date").reset_index(drop=True)

japan_matches[
    ["match_id", "match_date", "competition", "season", "competition_stage",
     "home_team", "away_team", "home_score", "away_score"]
]
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `["home_team"].isin(japan_names)` | ホームチームの名前が、`japan_names` のどれかと一致するか判定する |
| `条件A \| 条件B` | 「AまたはB」。ホームまたはアウェイに日本がいる試合 |
| `.sort_values("match_date")` | 試合日の順に並べる |
| `.reset_index(drop=True)` | 行番号を0から振り直す |

**期待される出力の例**(確認時の例。実際は上の列がすべて並び、行数は大会ごとの日本の試合数になります)

| match_date | competition | season | competition_stage | home_team | away_team | home_score | away_score |
|---|---|---|---|---|---|---|---|
| 2018-06-28 | FIFA World Cup | 2018 | Group Stage | Japan | Poland | 0 | 1 |
| 2018-07-02 | FIFA World Cup | 2018 | Round of 16 | Belgium | Japan | 3 | 2 |
| 2019-06-10 | Women's World Cup | 2019 | Group Stage | Argentina Women's | Japan Women's | 0 | 0 |
| 2022-11-23 | FIFA World Cup | 2022 | Group Stage | Germany | Japan | 1 | 2 |
| ... | ... | ... | ... | ... | ... | ... | ... |

> 上の表は一部の行の例です。**日本代表のすべての試合が、あなたの画面の表には並びます**。左端の `match_id` も表示されるので、見たい試合の `match_id` をメモしてください。

**確認すること**

- [ ] `japan_matches` に、日本代表の試合が複数行表示された
- [ ] 男子と女子の両方がある場合は、どちらを使うか決める(**第一候補は男子日本代表**。女子でも手順は同じです)
- [ ] 使いたい試合の `match_id`(数字)を1つ、メモした(相手がベルギーの試合など、見応えのある試合がおすすめです)

### 4-6. セル12:日本代表が見つからなかった場合の代替案

> **このセルは、セル10で `japan_names` が空だった場合や、`japan_matches` が0行だった場合のみ実行します。** 日本代表が見つかっている場合は、スキップしてセル13に進みます。

**代替案の考え方**:このツールは「どのチームでも動く」ように作ります。日本代表が見つからなければ、他のチームの試合で先に進めます。フェーズ3以降のコードは変数名(`japan_matches` など)を変えずに進められるので、**あとで日本代表のデータが追加されたときは、チーム名を差し替えるだけ**です。

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル12**

```python
# notebooks/02_explore_data.ipynb  セル12(日本代表が見つからなかった場合のみ)
print(sorted(teams))  # 収録されているチーム名の一覧を表示する

KEYWORD = "____"  # 上の一覧から、使いたいチーム名の一部(例:好きな国名)を選んで書く

team_names = sorted([t for t in teams if KEYWORD in t])
print(team_names)

is_team = all_matches["home_team"].isin(team_names) | all_matches["away_team"].isin(team_names)
japan_matches = all_matches[is_team].sort_values("match_date").reset_index(drop=True)  # 変数名は japan_matches のまま進める
japan_matches[["match_id", "match_date", "home_team", "away_team", "home_score", "away_score"]]
```

**コードの解説**

- `KEYWORD` に入れた文字を含むチームの試合だけが、`japan_matches` に入ります(名前は `japan_matches` のままですが、中身は選んだチームの試合です)。
- 以降の「日本代表」は、すべて「あなたが選んだチーム」に読み替えます。

**さらに広く探したい場合(任意)**

- ワールドカップ以外の大会にも日本代表が出ていないか調べたいときは、セル6の `"World Cup"` の絞り込みを外し、`competitions` 全行でセル9のループを回します(約80回の通信で、数分かかります)。2026年10月9日の確認時は、日本代表が出るのはワールドカップの男子・女子と考えられましたが、データは更新されるため、この手順で最新状況を確かめられます。

### 4-7. 手順4のまとめ(自分の言葉で)

次の3つを、自分のメモに書いておきます。

| 項目 | あなたのメモ |
|---|---|
| 使うチーム名(`japan_names` の文字列そのまま) | 'Japan' |
| 使う試合の `match_id` | 7584 |
| その試合の対戦カードと日付 | 2018-07-02 Belgium vs Japan |

### 手順4の完了チェック

- [ ] セル7の課題を解き、答え合わせをした
- [ ] セル9で `all_matches` ができた
- [ ] セル10で `japan_names` の出力を確認し、実際の表記をメモした(または見つからなかった場合の代替案に進んだ)
- [ ] セル11で、日本代表(または代替チーム)の試合一覧が出た
- [ ] 使う試合の `match_id` を決めた

---

## 手順5:試合を1つ選び、イベントデータを取得する

**所要時間:約1.25時間**

### 5-1. セル13(課題2):試合を選ぶ

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル13**

```python
# notebooks/02_explore_data.ipynb  セル13(課題2)
TEAM_NAME = "____"   # japan_names の出力から、使うチーム名を一字一句そのままコピーする
MATCH_ID = ____      # セル11の表から選んだ match_id(数字。引用符 " " は付けない)

match_row = japan_matches[japan_matches["____"] == MATCH_ID]
print(match_row[["match_date", "home_team", "away_team", "home_score", "away_score"]])
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| `TEAM_NAME` の `____` | セル10の出力にあった文字列(例:男子なら、出力に表示された `Japan` などの表記) |
| `MATCH_ID` の `____` | セル11の表から選んだ `match_id`(整数) |
| 3つ目の `____` | 試合のIDが入っている列の名前 |

**期待される出力の例**

```
   match_date home_team away_team  home_score  away_score
x  20xx-xx-xx   ...       ...      ...         ...
```

(選んだ試合の1行が表示されます。)

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/02_explore_data.ipynb  セル13(課題2)
TEAM_NAME = "Japan"        # 例。あなたの japan_names の文字列を使う(女子なら出力にあった表記)
MATCH_ID = 7584            # 例。あなたの japan_matches の表から選んだ match_id を使う

match_row = japan_matches[japan_matches["match_id"] == MATCH_ID]
print(match_row[["match_date", "home_team", "away_team", "home_score", "away_score"]])
```

**答え合わせのあとに**

- 3つ目の空欄は `match_id` です。
- `TEAM_NAME` と `MATCH_ID` は、**あなたの出力に合わせた値**が正解です。上の例の `"Japan"` と `7584` は、確認時に見た男子2018年の対ベルギー戦の例で、あなたの表にない場合や違う試合を選んだ場合は、自分の値に置き換えてください。

**自分のコードが正解と違っても、動いていればOKな例**

- `MATCH_ID` に、自分で選んだ別の試合のIDを入れた → 動く。以降の出力が、その試合のものになるだけです。
- `japan_matches[japan_matches["match_id"] == MATCH_ID]` の代わりに `japan_matches.query("match_id == @MATCH_ID")` と書いた → 動く(pandas の別の書き方)。
- `MATCH_ID` を文字列(`"7584"`)にした → 1行も出ない。`match_id` は数字なので、引用符を外してください。

**確認の仕方**

- `match_row` に**ちょうど1行**が表示され、日付とチームが、選んだ試合と一致している。

</details>

### 5-2. セル14:イベントデータを取得する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル14**

```python
# notebooks/02_explore_data.ipynb  セル14
events = sb.events(match_id=MATCH_ID)
print(events.shape)
events.head()
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `sb.events(match_id=...)` | 指定した試合の**すべてのイベント**を、1行1イベントの表で返す |
| イベントとは | パス、シュート、ドリブル、ファウル、キックオフなど、試合で起きたあらゆるプレー |

**期待される出力の例**(行数は試合によって違います。1試合で3000行前後になることが多いです)

```
(3xxx, 1xx)
```

- 列数は100を超えることが多く、**ほとんどの列は、特定のイベント種別のときだけ値が入ります**(それ以外は空欄 `NaN`)。

### 5-3. セル15:イベントの種類とチームを確認する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル15**

```python
# notebooks/02_explore_data.ipynb  セル15
print(list(events.columns))
print(events["type"].value_counts().head(10))
print(events["team"].unique())
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `list(events.columns)` | すべての列名を一覧にする(どんな情報があるかの目次) |
| `events["type"]` | イベントの種類の列(`Pass`、`Shot`、`Carry` など) |
| `.value_counts()` | 値ごとの個数を数えて、多い順に並べる |
| `events["team"].unique()` | この試合に登場するチーム名(重複なし) |

**期待される出力の例**

```
['id', 'index', 'period', 'timestamp', 'minute', 'second', 'type', 'possession', 'possession_team', 'play_pattern', 'team', 'player', 'position', 'location', 'duration', ..., 'pass_end_location', 'pass_outcome', ..., 'shot_statsbomb_xg', 'shot_outcome', ...]
type
Pass              ...
Ball Receipt*     ...
Carry             ...
Pressure          ...
...
['チームA名' 'チームB名']
```

**このフェーズで使う主な列**

| 列名 | 意味 |
|---|---|
| `type` | イベントの種類(`Pass`、`Shot` など) |
| `team` | そのプレーをしたチーム名 |
| `player` | 選手名 |
| `minute` | 何分のプレーか |
| `location` | プレーが行われた位置。`[x, y]` の形のリスト |
| `pass_end_location` | パスの到達位置(`[x, y]`) |
| `pass_outcome` | パスの結果。**パスが成功したときは、この列が空欄(`NaN`)になる**(失敗のときだけ `Incomplete` などの値が入る) |
| `shot_statsbomb_xg` | シュートの xG(ゴールになる確率の期待値。0〜1) |
| `shot_outcome` | シュートの結果(`Goal`、`Saved` など) |

- [ ] `events["team"].unique()` の2つのチーム名のうち、1つが `TEAM_NAME` と**一字一句同じ**であることを確認する。
  - 一致しない場合は、`TEAM_NAME` の綴り(`'` の形や空白)を、出力からコピーし直します。

> **公式ドキュメントで確認してください**:列の意味・イベントの種類は、StatsBomb Open Data リポジトリの `doc` フォルダ(Open Data Events の仕様書 PDF)に説明があります。列名や仕様は変わることがあります。

### 手順5の完了チェック

- [ ] `match_row` に選んだ試合の1行が表示された
- [ ] `events.shape` で、数千行×100列超の表が取得できた
- [ ] `events["type"].value_counts()` の上位に `Pass` が入っている
- [ ] `events["team"].unique()` に、自分が選んだチーム名が含まれている

---

## 手順6:パスとシュートに絞り込み、座標を取り出す

**所要時間:約1.25時間**

### 6-1. StatsBomb の座標のルール

後のフェーズでピッチに描くため、座標の決まりを先に押さえます。

| ルール | 内容 |
|---|---|
| ピッチの大きさ | 横(x)が **0〜120**、縦(y)が **0〜80** の座標系(フェーズ1で `pitch_type="statsbomb"` と指定した理由) |
| 原点 | 左上が (0, 0)。y は**下に向かって大きくなる** |
| 攻撃の向き | 各チームのイベントは、**そのチームがx=120のゴールに向かって攻める**ように記録される |

- 上のルールは、StatsBomb Open Data の仕様書の説明にもとづく一般的な理解です。**正確な定義は、`doc` フォルダの仕様書で確認してください。**
- この「攻撃の向きの統一」のおかげで、両チームのパスマップを同じ向きで描けます。

### 6-2. セル16(課題3):パスとシュートに絞り込み、x・y 列を作る

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル16**

```python
# notebooks/02_explore_data.ipynb  セル16(課題3)
passes = events[events["____"] == "Pass"].copy()
shots = events[events["____"] == "Shot"].copy()

passes["x"] = passes["location"].str[____]
passes["y"] = passes["location"].str[____]

print(len(passes), len(shots))
passes[["minute", "team", "player", "location", "x", "y"]].head()
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目・2つ目の `____` | イベントの種類が入っている列の名前(セル15で `value_counts()` した列) |
| 3つ目の `____` | `[x, y]` のリストのうち、x は何番目か(Python は **0 から**数える) |
| 4つ目の `____` | 同じリストのうち、y は何番目か |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `events[events["type"] == "Pass"]` | イベントの種類が `Pass` の行だけに絞る |
| `.copy()` | 絞り込んだ結果のコピーを作る。これを付けないと、後で列を追加するときに `SettingWithCopyWarning` という警告が出ることがある |
| `passes["location"].str[0]` | `location` 列の各行のリスト `[x, y]` から、**0番目の要素(x)**を取り出す |
| `passes["x"] = ...` | 取り出した値を、新しい列 `x` として追加する |

**期待される出力の例**

```
712 14
```

のように、パス数とシュート数(2つの数字。数は試合によって違います)が表示され、続いて `minute`、`team`、`player`、`location`、`x`、`y` の表が表示されます。`location` が `[x, y]` の形で、`x` と `y` に分かれた数字が入っています。

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/02_explore_data.ipynb  セル16(課題3)
passes = events[events["type"] == "Pass"].copy()
shots = events[events["type"] == "Shot"].copy()

passes["x"] = passes["location"].str[0]
passes["y"] = passes["location"].str[1]

print(len(passes), len(shots))
passes[["minute", "team", "player", "location", "x", "y"]].head()
```

**答え合わせのあとに**

- 空欄の答え:1つ目・2つ目は `type`、3つ目は `0`、4つ目は `1`。

**自分のコードが正解と違っても、動いていればOKな例**

- `.copy()` を付けなかった → 動くことが多いが、`SettingWithCopyWarning` が出る場合がある。警告は赤い文字で出ますが、エラーではありません。付けるのがより安全です。
- `passes["x"] = passes["location"].apply(lambda v: v[0])` と書いた → 動く(別の書き方)。
- `events.query('type == "Pass"')` で絞り込んだ → 動く。結果は同じです。

**確認の仕方**

- `len(passes)` が数百、`len(shots)` が数個〜数十になっている。
- `passes` の `x` と `y` に数字が入っている(`NaN` が大量にあれば、列名や位置の指定を見直す)。

</details>

### 6-3. セル17:座標の範囲と、パスの成否を確認する

- [ ] **[VS Code]** 次のセルを追加し、入力して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル17**

```python
# notebooks/02_explore_data.ipynb  セル17
print(passes[["x", "y"]].describe())
print(passes["pass_outcome"].value_counts(dropna=False))
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `.describe()` | 最小・最大・平均などの統計を一覧にする |
| `value_counts(dropna=False)` | 値ごとの個数を数える。`dropna=False` で、空欄(`NaN`)も数える |

**期待される出力の例**

```
                x           y
count  7xx.000000  7xx.000000
mean    5x.xxxxxx   4x.xxxxxx
min     0.xxxxxx    0.xxxxxx
max   11x.xxxxxx   7x.xxxxxx
NaN                  ...
Incomplete           ...
Out                  ...
Pass Offside         ...
...
```

**確認すること**

- [ ] `x` の最小が 0 付近、最大が 120 付近。`y` の最小が 0 付近、最大が 80 付近(範囲が合っている)。
- [ ] `pass_outcome` の最多が `NaN`(**成功したパス**)になっている。

### 6-4. セル18(課題4):チームごとに集計する

- [ ] **[VS Code]** 次のセルを追加し、**空欄(`____`)を埋めて**実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル18**

```python
# notebooks/02_explore_data.ipynb  セル18(課題4)
pass_count = passes.groupby("____").size()
print(pass_count)

shot_summary = shots.groupby("____")["____"].agg(["count", "sum"])
print(shot_summary)
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | チームごとに数えたいので、チーム名の列 |
| 2つ目 | 同じく、チーム名の列 |
| 3つ目 | シュートの xG が入っている列(`shot_` で始まる列。セル15の一覧にある) |

**期待される出力の例**

```
team
チームA名    4xx
チームB名    3xx
dtype: int64
            count   sum
team
チームA名       x   x.xx
チームB名       x   x.xx
```

(`count` はシュート数、`sum` は xG の合計。`sum` は合計の xG です。)

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
# notebooks/02_explore_data.ipynb  セル18(課題4)
pass_count = passes.groupby("team").size()
print(pass_count)

shot_summary = shots.groupby("team")["shot_statsbomb_xg"].agg(["count", "sum"])
print(shot_summary)
```

**答え合わせのあとに**

- 空欄の答え:1つ目・2つ目は `team`、3つ目は `shot_statsbomb_xg`。

**自分のコードが正解と違っても、動いていればOKな例**

- `passes["team"].value_counts()` でチームごとのパス数を数えた → 動く。結果は `groupby("team").size()` と同じ(並び順だけ違うことがある)。
- `.agg(["count", "sum"])` の代わりに `.sum()` だけにした → xG の合計だけが出る。動きます。
- `.agg(["count", "sum", "mean"])` と `mean` を足した → 動く。1本あたりの平均 xG も分かります。

**確認の仕方**

- 2チームの行がそれぞれ出る。
- xG の合計が、実際の試合のスコアに近い大きさ(0.5〜4 程度)になる。

</details>

### 手順6の完了チェック

- [ ] `passes` と `shots` を作り、行数を確認した
- [ ] `passes` に `x`、`y` 列を作れた
- [ ] `x` が 0〜120、`y` が 0〜80 の範囲に収まっている
- [ ] `pass_outcome` が空欄(`NaN`)のものが「成功パス」であることを確認した
- [ ] チームごとのパス数と、シュート数・xG の合計を出せた

---

## 手順7:動いたコードを `loader.py` に移す

**所要時間:約0.75時間**

Notebook で試したコードのうち、**何度も使うもの**を `src/pitchviz/loader.py` に関数としてまとめます。フェーズ3以降でそのまま呼び出します。

### 7-1. 空の `__init__.py` を作る

`__init__.py` は、「このフォルダは Python のパッケージ(まとまり)です」という目印のファイルです。

- [ ] **[VS Code]** Explorer で `src/pitchviz` フォルダを右クリック → `New File` → `__init__.py` と入力して Enter。
  - **対象**:`src/pitchviz/__init__.py`
  - **新規作成か編集か**:新規作成(**中身は空のまま**でよい)
  - 全体の計画では、`__init__.py` はフェーズ5で作る予定でしたが、Notebook から読み込むため、**ここで先に空ファイルとして作ります**。フェーズ5で中身を書き足します(フェーズ5では MOD になります)。
- [ ] **[VS Code]** `Command + S` で保存する(空のままでも作られます)。

### 7-2. `loader.py` を作る

- [ ] **[VS Code]** Explorer で `src/pitchviz` を右クリック → `New File` → `loader.py` と入力して Enter。
  - **対象**:`src/pitchviz/loader.py`
  - **新規作成か編集か**:新規作成
- [ ] 次のコードの全文を貼り付けて、`Command + S` で保存する。

```python
# src/pitchviz/loader.py
"""StatsBomb Open Data の取得・絞り込みを行う関数(フェーズ2の最小版)。"""

import pandas as pd
from statsbombpy import sb


def get_competitions(keyword=""):
    """大会一覧を返す。keyword を含む大会名だけに絞る(空文字なら全部)。"""
    competitions = sb.competitions()
    if keyword:
        mask = competitions["competition_name"].str.contains(keyword, case=False, na=False)
        competitions = competitions[mask]
    return competitions.reset_index(drop=True)


def get_team_matches(competitions, team_keyword):
    """大会一覧の各シーズンの試合を集め、team_keyword を含むチームの試合だけを返す。"""
    frames = []
    for _, row in competitions.iterrows():
        matches = sb.matches(
            competition_id=row["competition_id"],
            season_id=row["season_id"],
        )
        frames.append(matches)

    all_matches = pd.concat(frames, ignore_index=True)
    is_home = all_matches["home_team"].str.contains(team_keyword, case=False, na=False)
    is_away = all_matches["away_team"].str.contains(team_keyword, case=False, na=False)
    return all_matches[is_home | is_away].sort_values("match_date").reset_index(drop=True)


def get_events(match_id):
    """1試合のイベントデータをすべて返す。"""
    return sb.events(match_id=match_id)


def add_xy(df, column="location", x_name="x", y_name="y"):
    """[x, y] のリストが入った列から、x と y の2列を追加した表を返す。"""
    result = df.copy()
    result[x_name] = result[column].str[0]
    result[y_name] = result[column].str[1]
    return result
```

**コードの解説**

| 記述 | 意味 |
|---|---|
| `def get_competitions(keyword=""):` | 関数の定義。`keyword` が引数。`=""` は「渡さなければ空文字」という初期値 |
| `"""..."""`(最初の文字列) | 関数の説明(docstring)。何をする関数かを書く習慣 |
| `case=False` | 大文字・小文字を区別しない |
| `get_team_matches(...)` | セル9〜11でやった「大会ごとの試合を集め、チームで絞り込む」処理を、1つの関数にまとめたもの |
| `team_keyword` | 検索に使う**文字の一部**(例:`Japan`)。`Japan` と `Japan Women's` の両方が見つかる |
| `add_xy(...)` | セル16でやった「`location` から x・y を取り出す」処理を、関数にまとめたもの |

### 7-3. セル19(課題5):`filter_events` 関数を書く

- [ ] **[VS Code]** `src/pitchviz/loader.py` の**末尾**(`add_xy` 関数の後ろ)に、次のコードを**追記**し、**空欄(`____`)を埋めて**保存する。
  - **対象**:`src/pitchviz/loader.py`
  - **新規作成か編集か**:既存ファイルの編集(`add_xy` 関数の後ろに足す)

```python
def filter_events(events, event_type, team_name=None):
    """イベント種別(例: "Pass")で絞り込む。team_name を渡すと、そのチームだけにする。"""
    result = events[events["____"] == event_type]
    if team_name is not None:
        result = result[result["____"] == team_name]
    return result.copy()
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | イベントの種類が入っている列(セル15で使った列) |
| 2つ目 | チーム名が入っている列 |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```python
def filter_events(events, event_type, team_name=None):
    """イベント種別(例: "Pass")で絞り込む。team_name を渡すと、そのチームだけにする。"""
    result = events[events["type"] == event_type]
    if team_name is not None:
        result = result[result["team"] == team_name]
    return result.copy()
```

**答え合わせのあとに**

- 空欄の答え:1つ目は `type`、2つ目は `team`。

**自分のコードが正解と違っても、動いていればOKな例**

- `if team_name is not None:` の代わりに `if team_name:` と書いた → 動く(通常は同じ結果)。
- `result` を最初に `events.copy()` としてから順に絞り込んだ → 動く。
- 戻り値の `.copy()` を付けなかった → 動くが、後で列を追加するときに警告が出ることがある。

**確認の仕方**

- 次のセル19で、`filter_events(events, "Pass")` の行数が、セル16の `len(passes)` と一致する。

</details>

### 7-4. セル19:Notebook から `loader.py` を呼び出して確認する

- [ ] **[VS Code]** Notebook `notebooks/02_explore_data.ipynb` に戻り、次のセルを追加して実行する。
  - **対象**:`notebooks/02_explore_data.ipynb` の **セル19**

```python
# notebooks/02_explore_data.ipynb  セル19
from pitchviz.loader import add_xy, filter_events, get_competitions, get_events, get_team_matches

wc_check = get_competitions("World Cup")
japan_check = get_team_matches(wc_check, "Japan")   # 日本代表が見つからなかった場合は、選んだチームの名前の一部に変える
events_check = get_events(MATCH_ID)

passes_check = add_xy(filter_events(events_check, "Pass", TEAM_NAME))
shots_check = filter_events(events_check, "Shot", TEAM_NAME)

print(len(japan_check), len(japan_matches))
print(len(events_check) == len(events))
print(len(passes_check), len(shots_check))
passes_check[["minute", "player", "x", "y"]].head()
```

**期待される出力の例**

```
(日本代表の試合数) (japan_matches の行数と同じ数)
True
(自チームのパス数) (自チームのシュート数)
```

続いて、`minute`、`player`、`x`、`y` の表が表示されます。

**確認すること**

- [ ] 1行目の2つの数字が同じ(自作関数が、Notebook で作った表と同じ結果を返している)
- [ ] 2行目が `True`
- [ ] `passes_check` の `x`・`y` に数字が入っている

### 手順7の完了チェック

- [ ] `src/pitchviz/__init__.py` と `src/pitchviz/loader.py` ができている
- [ ] 課題5を解いて、答え合わせした
- [ ] セル19が、エラーなく実行できた
- [ ] `loader.py` を書き換えたとき、セルの再実行だけで反映される(`%autoreload` の効果)ことを理解した

---

## 手順8:README にクレジットを入れ、コミットする

**所要時間:約0.75時間**

### 8-1. README に、データのクレジットを追加する(仮)

利用条件(手順1-2)にもとづき、README にデータ元を明記します。**最終版はフェーズ6で完成させます**。ここでは、クレジットの文章を先に入れておきます。

- [ ] **[VS Code]** Explorer で `README.md`(プロジェクトルート直下)を開く。
  - **対象**:`README.md`
  - **新規作成か編集か**:既存ファイルの編集
  - **編集内容**:ファイルの**末尾**に、次の内容を追記する。
- [ ] 次のコードを追記し、`Command + S` で保存する。

```markdown
<!-- README.md (末尾に追記) -->

## Data / クレジット

This project uses StatsBomb Open Data.
Data source: [StatsBomb](https://github.com/statsbomb/open-data)

本プロジェクトは StatsBomb Open Data を使用しています。
利用条件(クレジット表記・ロゴ等)は、公式リポジトリの README と LICENSE を確認してください。
```

- さらに、進捗欄を更新します。
  - **編集内容**:`## 進捗` の下の `- [x] フェーズ1:環境構築` の**次の行**に、次の1行を足す。

```markdown
- [x] フェーズ2:データ取得と構造の理解
```

> **重要**:StatsBomb の README には、公開する場合にロゴを使う旨の記載があります(手順1-2)。**ロゴの配置は、フェーズ6で、利用条件の原文を確認したうえで行います。**

### 8-2. Notebook を保存する

- [ ] **[VS Code]** `Command + S` で `02_explore_data.ipynb` を保存する。

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

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/phase2_data.md
	notebooks/02_explore_data.ipynb
	src/

no changes added to commit (use "git add" and/or "git commit -a")
```

**確認すること**

- `modified: README.md`(クレジットを追記したため)。
- `docs/phase2_data.md`(この手順書)、`notebooks/02_explore_data.ipynb`、`src/`(`__init__.py` と `loader.py`)が Untracked に出る。
- **`.venv/` や `data/` が出ていない**こと。
- `src/` の下に `__pycache__/` が見えても、`.gitignore` により除外されます。表示されなければ正常です。
- 自分で追加した別のファイル(例:`docs/` の独自のメモ)が出る場合もあります。それらは含めても除外してもよいです。

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
	new file:   docs/phase2_data.md
	new file:   notebooks/02_explore_data.ipynb
	modified:   README.md
	new file:   src/pitchviz/__init__.py
	new file:   src/pitchviz/loader.py
```

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git commit -m "Phase 2: explore StatsBomb open data and add minimal loader"
```

期待される出力の例:

```
[main xxxxxxx] Phase 2: explore StatsBomb open data and add minimal loader
 5 files changed, xxx insertions(+)
 create mode 100644 docs/phase2_data.md
 create mode 100644 notebooks/02_explore_data.ipynb
 create mode 100644 src/pitchviz/__init__.py
 create mode 100644 src/pitchviz/loader.py
```

- コミットメッセージは、日本語でも構いません(例:`フェーズ2: StatsBomb データの調査と loader.py の最小版`)。

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

- [ ] **[Browser]** `https://github.com/あなたのユーザー名/pitchviz` を開き、`src/pitchviz/loader.py`、`notebooks/02_explore_data.ipynb`、README のクレジットが表示されることを確認する。

### 8-6. 振り返り

次の質問に、1〜2行で自分の言葉で答えてみてください。

1. 「大会 → 試合 → イベント」の順に絞る理由は何ですか?

    →　大会ごとに試合が分けられていて、試合ごとにイベントが別ファイルのため

2. `sb.matches()` を呼ぶのに、`competition_id` と `season_id` の**両方**が必要なのはなぜですか?
    
    → 同じ大会でも年が違えば違う試合であり、組み合わせで一意に特定できるようにするため
3. `passes = events[events["type"] == "Pass"]` は、何をしていますか?

    → イベント全体から種類が`Pass`の行だけを取り出している
4. パスの結果が `NaN` のとき、そのパスは成功ですか? 失敗ですか?
    → 成功
5. チーム名を「推測で書かず、データの文字列を確認する」べき理由を、今回の例で説明できますか?
    → 男子は`Japan`、女子は`Japan Women's`のように表記が違って、間違えると絞り込みで０件になるため

- [ ] 1に「大会ごとに試合が分かれており、試合ごとにイベントが別ファイルのため」のように答えられる
- [ ] 2に「同じ大会でもシーズン(年)が違えば試合が違うため、組み合わせで1つに決まる」のように答えられる
- [ ] 3に「イベント全体の表から、種類が `Pass` の行だけを取り出している」のように答えられる
- [ ] 4に「成功(失敗や無効のときだけ値が入る)」と答えられる
- [ ] 5に「男子は `Japan`、女子は `Japan Women's` のように表記が違い、間違えると絞り込みで0件になるため」のように答えられる

### 手順8の完了チェック

- [ ] README に、データのクレジットと進捗が追記された
- [ ] `git status` で、想定したファイルだけが表示された
- [ ] `git commit` が成功した
- [ ] `git push` が成功し、GitHub に反映された
- [ ] 振り返りの5問に答えられた

---

## 手順9:つまずきやすい点と対処法

### 9-1. エラー別の対処表

| 症状・エラーメッセージの例 | 原因 | 対処 |
|---|---|---|
| `NoAuthWarning: credentials were not supplied. Open data access only` | StatsBomb の有料 API 用のログイン情報がない(**警告であり、エラーではない**) | 無料のオープンデータだけを使うので、無視して構いません |
| `requests.exceptions.ConnectionError: HTTPSConnectionPool(host='raw.githubusercontent.com', ...)` | インターネットに接続できていない、または一時的に GitHub に届かない | 接続を確認し、数分待ってセルを再実行する |
| `ModuleNotFoundError: No module named 'pitchviz'` | `sys.path.append("../src")` を実行していない、または `src/pitchviz/__init__.py` がない | セル1を実行し直す。`src/pitchviz/__init__.py` があるか確認する。Notebook が `notebooks/` フォルダの中にあるか確認する |
| `ModuleNotFoundError: No module named 'pitchviz.loader'` | `loader.py` のファイル名の綴りが違う、または保存していない | Explorer で `src/pitchviz/loader.py` があることを確認し、`Command + S` で保存する |
| `ImportError: cannot import name 'filter_events' from 'pitchviz.loader'` | 課題5の関数を `loader.py` に追記していない、または保存していない | `loader.py` の末尾に関数があるか確認し、保存してから、セル19を再実行する。それでもだめなら Restart してセル1から順に実行する |
| `loader.py` を直したのに、結果が変わらない | 古い内容を読み込んだままになっている | セル1に `%autoreload 2` が入っているか確認する。入っていなければ、Restart してセル1から実行し直す |
| `KeyError: 'home_team'`(または `'competition'` など) | ライブラリの更新などで、列名が違う | `print(list(matches.columns))` で実際の列名を確認し、その名前に置き換える |
| `AttributeError: Can only use .str accessor with string values!` | 対象の列が文字列ではない(辞書や数値など) | `matches["home_team"].head()` で中身を確認する。想定と違う形なら、Claude / ChatGPT に出力を見せて相談する |
| `japan_names` が `[]`(空) | ワールドカップ以外にしか日本がいない、または今のデータには日本代表がいない | 手順4-6(セル12)の代替案へ。または、`wc` の絞り込みを外して全大会を調べる |
| 日本の試合が少ししか出ない | 大会に出ていない、収録されている試合が一部である | データは一部の試合のみ収録されていることがある。出た試合で進めてよい |
| `Empty DataFrame`(0行) | チーム名の綴りや引用符(`'`)が一致していない | `events["team"].unique()` の出力から、チーム名をそのままコピーして貼る |
| `japan_matches[japan_matches["match_id"] == MATCH_ID]` が0行 | `MATCH_ID` を文字列にした、または表にない値を入れた | 引用符を外す。セル11の表にある `match_id` を使う |
| `ValueError: Cannot index with multidimensional key` または `TypeError: unhashable type: 'list'` | `[[ ]]` と `[ ]` の書き間違い | 列を複数選ぶときは `df[["a", "b"]]`、1列だけなら `df["a"]` |
| `SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame` | 絞り込んだ表に、直接列を追加した | 絞り込みの最後に `.copy()` を付ける(エラーではなく警告) |
| `passes["x"]` が全部 `NaN` | `location` 列の中身が想定と違う、列名の綴りが違う | `passes["location"].head()` を表示し、`[x, y]` の形か確認する |
| 次のようなエラー:`AttributeError: partially initialized module 'pandas' ...` | 以前の読み込みの失敗が、Notebook に残っている | Notebook 上部の **Restart** を押し、セル1から順に実行する(フェーズ1の手順9-1も参照) |
| セル9が遅い・止まっているように見える | 複数の大会の試合を、都度ダウンロードしている | 数十秒〜数分は正常。2分以上たっても進まない場合は、ネットワークを確認し、セルを中断(■)して再実行する |
| `git push` で拒否された | リモートに、手元にない変更がある | `git pull --rebase` を実行してから、もう一度 `git push` する。詳しくは Claude / ChatGPT に出力を貼って相談する |

### 9-2. 「合っているか分からない」ときの確認方法

- **件数を、実際の試合のスコアと照らす**:シュート数や xG の合計が、あまりに大きすぎる・小さすぎる(例:0本、100本)場合は、絞り込みを見直す。
- **別の試合でも動くか**:`MATCH_ID` を変えて、同じコードで動くか確認する(動けば、ツールの汎用性が確認できます)。
- **目で確かめる**:`events[events["type"] == "Shot"][["minute", "team", "player", "shot_outcome"]]` を表示し、ゴールの数がスコアと合うか見る。

---

## 手順10:Claude / ChatGPT に質問するときのコツ(データ編)

### 10-1. データの質問に、必ず入れるもの

1. **やりたいこと**:「日本代表の試合を絞り込みたい」
2. **実行したセルのコード全文**
3. **エラー文の全文**(最初の `Traceback` から、最後のエラー名の行まで)
4. **表の中身を確認した結果**:次のような出力を、**テキスト**で貼る
   - `df.shape`(行数と列数)
   - `list(df.columns)`(列名の一覧)
   - `df.head()`(先頭数行。ただし、列が多いときは必要な列だけ)
   - `df["列名"].head()` や `type(df["列名"][0])`(中身の形)
5. **環境**:`pip list` のうち、`statsbombpy` / `pandas` の版

### 10-2. 表の貼り方

- **大きな表をすべて貼らない**:`.head()` で先頭5行にする。列が多いときは、`df[["match_id", "home_team", "away_team"]].head()` のように必要な列だけにする。
- **スクリーンショットだけでなく、テキストでも貼る**:数字や文字が正確に伝わります。
- 次のようにバッククォート3つで囲んで貼る。

````
```
(ここにエラー文や表の出力を貼る)
```
````

### 10-3. 質問の例

> macOS、Python 3.13.3、Jupyter(VS Code)で、StatsBomb Open Data を使っています。次のセルで `KeyError: 'home_team'` が出ました。
>
> ```python
> is_home = all_matches["home_team"].isin(japan_names)
> ```
>
> `all_matches` の `list(all_matches.columns)` の出力は次のとおりです。
>
> ```
> (ここに列名の一覧を貼る)
> ```
>
> 原因と、初学者向けの直し方を教えてください。

### 10-4. 回答の使い方

- **「この列は何ですか?」と聞くときは、StatsBomb の `doc` フォルダの仕様書の名前を添える**と、より正確な説明が得られます。
- AI が示した列名・関数名は、**必ず自分の画面の `columns` や出力で、実在するか確認する**(ライブラリの版により違うことがあります)。
- 分からないままコードを貼らず、「この1行は何をしますか?」と聞いてから実行する。

---

## このフェーズ終了時のディレクトリツリー

`NEW` は新しく作ったファイル、`MOD` は変更したファイルです。

```
~/projects/pitchviz/
├── .git/
├── .gitignore
├── .venv/
├── README.md                     # MOD(クレジットと進捗を追記)
├── requirements.txt
├── docs/
│   ├── 00_overview.md
│   ├── phase1_setup.md
│   └── phase2_data.md            # NEW
├── notebooks/
│   ├── 01_setup_check.ipynb
│   └── 02_explore_data.ipynb     # NEW
├── src/
│   └── pitchviz/
│       ├── __init__.py           # NEW(空。フェーズ5で中身を書く)
│       └── loader.py             # NEW(大会・試合・イベントの取得と絞り込み)
├── outputs/
│   └── .gitkeep
└── data/                         # (空。Git管理外)
```

---

## フェーズ2 最終チェックリスト

**データの理解**

- [ ] 「大会 → 試合 → イベント」の階層を説明できる
- [ ] 日本代表の収録状況(男子・女子)を、実際のデータで確認した
- [ ] チーム名の正確な表記(`japan_names` の文字列)をメモした
- [ ] 使う試合の `match_id` を1つ決めた
- [ ] StatsBomb の利用条件(クレジット・ロゴ)を原文で確認した

**動くもの**

- [ ] `events` から、パスとシュートに絞り込める
- [ ] `x` と `y` の座標列を作れる
- [ ] チームごとのパス数と、シュート数・xG の合計を出せる
- [ ] `loader.py` の関数を Notebook から呼び出せる

**Git / GitHub**

- [ ] README にクレジットを追記した
- [ ] `git log --oneline` に、フェーズ2のコミットがある
- [ ] GitHub にフェーズ2の内容が反映されている

すべてにチェックが付けば、フェーズ2は完了です。

---

## 次のフェーズへ

フェーズ3では、今回取り出した `passes` を使って、次のことを行います。

- mplsoccer の `Pitch` に、パスを矢印で描く
- チームごとに、パスマップを描き分ける
- 画像を `outputs/` に保存する(例:`outputs/pass_map_チーム名_対戦相手.png`)

準備ができたら「フェーズ3をお願いします」と指示してください。

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| StatsBomb Open Data(データ・仕様書・利用条件) | `https://github.com/statsbomb/open-data`(`doc` フォルダ、`LICENSE.pdf`) |
| statsbombpy | `https://github.com/statsbomb/statsbombpy` |
| pandas | `https://pandas.pydata.org/docs/`(「10 minutes to pandas」) |
| mplsoccer | `https://mplsoccer.readthedocs.io` |
