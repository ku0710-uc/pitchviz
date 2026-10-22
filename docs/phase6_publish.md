# フェーズ6:README と公開

> 保存先:`~/projects/pitchviz/docs/phase6_publish.md`
> このフェーズの終わりには、「README・サンプル画像・クレジットが整った PitchViz が、GitHub で Public になり、`v0.1.0` のリリースが作られている」状態になります。

| 項目 | 内容 |
|---|---|
| 目標 | README を完成させ、StatsBomb の利用条件に沿って公開前の整理をし、GitHub で公開して、最初のリリース(`v0.1.0`)を作る |
| 想定所要時間 | 約5時間(下の内訳を参照) |
| 終了時の「動くもの」 | 誰でも `https://github.com/あなたのユーザー名/pitchviz` を開いて、サンプル画像つきの README を読み、手順どおりに `make_maps(...)` を実行できる |

### 作業ラベルの見方

- **[Terminal]**:ターミナルでの作業
- **[VS Code]**:VS Code での作業
- **[Browser]**:ブラウザでの作業

### 所要時間の内訳

| 手順 | 内容 | 目安 |
|---|---|---|
| 1 | 事前準備(状態確認・「公開するもの/しないもの」の棚卸し) | 0.5h |
| 2 | 利用条件の再確認とロゴの扱いを決める | 0.75h |
| 3 | README 用のサンプル画像を作る(課題1) | 0.5h |
| 4 | README を完成させる(課題2) | 1.0h |
| 5 | LICENSE を入れるか決める(任意) | 0.25h |
| 6 | 公開前の最終チェックと、コミット | 0.75h |
| 7 | 公開する(履歴をまっさらにして、Public にする) | 0.75h |
| 8 | 最初のリリース `v0.1.0` を作る(課題3) | 0.5h |
| | 合計 | 5.0h |

### このフェーズについての大事な前提

- **これまでで、いちばん「取り消しにくい」作業です。** GitHub で Public にすると、世界中の誰でも中身を見られます。手順6の最終チェックを終えるまでは、リポジトリを **Private** にしておいてください。
- **リポジトリを、すでに Public にしている場合があります。** フェーズ1の手順書は、公開範囲を「どちらでも可(迷ったら Private)」としていました。フェーズ3〜5の手順書には「Private のままにしてください」と書きましたが、Public で進めてきた方もいます。**手順1-4で、いまの状態を確認して、Public なら、先に Private に切り替えます。**
- **コードの確認範囲について**:この手順書の作成環境では、次のものを確認できていません。
  - **Media Pack の「Usage Rights」(ロゴの使用条件)の中身**。ページが JavaScript で後から表示される画面で、私は読めませんでした。**あなた自身が、手順2で原文を読んで、判断します。**
  - GitHub の画面の細かい表示(ボタンの名前や位置は、変わることがあります)。
  - `gh` コマンドの実際の出力(この環境では GitHub にログインしていないため)。`gh` の引数(`--public`、`--source`、`--push`、`--add-topic`、`--notes-file` など)は、`gh` 2.89.0 の `--help` で存在を確認しました。
  - 本物の mplsoccer での、画像の見た目。
- **確認できたもの**:`git` の一連の操作(履歴をまっさらにして、別のリモートへ push し、タグを付ける流れ)を、ローカルの空のリポジトリで最後まで実行しました。`grep -c` による Notebook の出力の確認、`.gitignore` が `docs/images/` の画像を除外しないこと、`output_dir="docs/images"` でサンプル画像が作られること、実行する場所を間違えると保存先がずれることも、実際に動かして確認しました。
- **「期待される出力」の数字や名前は例です。** あなたの試合・ユーザー名によって違います。`あなたのユーザー名` は、あなたの GitHub のユーザー名に置き換えてください。
- **このフェーズは、法律の助言ではありません。** 利用条件の「読み方」と「手順」を示します。判断に迷う点は、原文(`LICENSE.pdf`、Media Pack)と、StatsBomb の案内で確認してください。

### 今回やること・やらないこと

| やること | やらないこと |
|---|---|
| README の完成(サンプル画像・使い方・クレジット) | StatsBomb のデータ(試合データ)をリポジトリに入れること |
| Notebook の出力を消す | StatsBomb のロゴ画像のファイルを、確認なしでリポジトリに入れること |
| 履歴をまっさらにして、新しい Public リポジトリを作る | 旧リポジトリ(Private)の削除 |
| `v0.1.0` のリリースを作る | PyPI への公開(`pip install pitchviz` を可能にすること。今回の範囲外) |

---

## 手順1:事前準備(状態確認・「公開するもの/しないもの」の棚卸し)

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
git log --oneline | head -5
git remote -v
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
xxxxxxx Phase 5: add make_pass_map/make_shot_map/make_maps entry functions and pyproject.toml
xxxxxxx Phase 4: ...
xxxxxxx Phase 3: ...
xxxxxxx Phase 2: ...
xxxxxxx Phase 1: ...
origin	https://github.com/あなたのユーザー名/pitchviz.git (fetch)
origin	https://github.com/あなたのユーザー名/pitchviz.git (push)
```

- フェーズ5のコミットが済んでいない場合は、先にフェーズ5の手順7を終えてください。
- `git remote -v` の `origin` が、いまのリポジトリ(Private または Public)です。手順7で、この名前を付け替えます。

### 1-2. フェーズ2・5のメモを手元に用意する

```
使うチーム名:     ______(例:Japan)
使う match_id:    ______(例:7584)
対戦カードと日付: ______(例:2018-07-02 Belgium vs Japan)
```

- フェーズ5のセル2の `TEAM_NAME`、`MATCH_ID`、`MATCH_DATE` の値と同じです。

### 1-3. 「公開するもの/しないもの」の棚卸し

公開すると、リポジトリの**履歴の全部**(これまでのコミットのすべて)が見えます。まず、何が入っているかを整理します。

| もの | いまの状態 | 公開の方針 | 理由 |
|---|---|---|---|
| `src/pitchviz/*.py`、`pyproject.toml`、`requirements.txt` | Git に入っている | **公開する** | 自分で書いたコード |
| `docs/00_overview.md`〜`phase5_*.md` | Git に入っている | **公開する**(任意で外してもよい) | 手順書。学習の記録として残せる |
| `notebooks/*.ipynb` | Git に入っている。**出力にデータの行や画像が残っている** | **出力を消してから**公開する | 利用条件 1.2.1:データを第三者に配布・複製してはいけない |
| `outputs/*.png` | Git の対象外(`.gitignore`) | 公開しない(そのまま) | 作業用の画像 |
| `assets/*.png`(ロゴ) | Git の対象外(`.gitignore`) | **手順2で確認するまで、公開しない** | ロゴの再配布が、未確認 |
| `.venv/`、`data/` | Git の対象外 | 公開しない(そのまま) | 環境の実体・キャッシュ |
| **Git の履歴**(過去のコミット) | **古いコミットに、Notebook の出力(データの行・画像)が残っている** | **履歴ごと公開しない。手順7で、履歴をまっさらにする。すでに Public なら、先に Private にする(手順1-4)** | 出力を消しても、過去のコミットには残っているため |
| コミットの作者メール | フェーズ1で noreply メールを設定した(はず) | 手順6で確認する | 本物のメールアドレスを公開しないため |

> **履歴の問題が、いちばん見落としやすい点です。** いまの Notebook の出力を消してから Public にしても、**過去のコミットを開けば、消す前の出力が見えます**。そのため、手順7では、いまの内容だけを1つ目のコミットにした、新しいリポジトリを作ります。

### 1-4. いまのリポジトリが Public か Private か、確認する(重要)

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pwd
gh repo view --json visibility,url,forkCount,stargazerCount
```

期待される出力の例(項目の並びは、違うことがあります):

```
{"forkCount":0,"stargazerCount":0,"url":"https://github.com/あなたのユーザー名/pitchviz","visibility":"PUBLIC"}
```

| `visibility` | 意味 | 次にすること |
|---|---|---|
| `"PRIVATE"` | 非公開 | 何もせず、手順1-5へ進む |
| `"PUBLIC"` | **すでに公開されている** | 下の「Public だった場合」を、**先に**行う |

#### Public だった場合

**なぜ先に切り替えるのか**:手順1-3のとおり、古いコミットには、Notebook の出力(データの行・画像)が残っています。Public の間は、誰でも、その古いコミットを開けます。StatsBomb の利用条件 1.2.1 は、データを第三者に配布・複製しないことを求めています。私は法的な判断はできないので、**安全側に、いったん非公開に戻します**。手順6の確認を終えたあとで、手順7の方法で、あらためて公開します。

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
gh repo edit --visibility private --accept-visibility-change-consequences
gh repo view --json visibility
```

期待される出力の例:

```
{"visibility":"PRIVATE"}
```

- ブラウザで切り替える場合は、**[Browser]** リポジトリのページで `Settings` → 下の方の `Danger Zone` → `Change repository visibility` の **`Change visibility`** → `Make private` を選び、画面の指示(リポジトリ名の入力など)に従います。

**Private にすると起きること**(GitHub Docs「Setting repository visibility」の内容)

| 項目 | どうなるか |
|---|---|
| フォーク(他の人が作ったコピー) | **公開フォークは、公開のまま残ります**(元のリポジトリとは、切り離されます) |
| スター・ウォッチ | **消えます**(元に戻せません) |
| GitHub Pages | 公開していた場合は、**自動で非公開になります**(このプロジェクトでは、使っていないはずです) |

- 上の出力の `forkCount` が **0 以外**の場合、他の人が作ったコピーが残っている可能性があります。Private にしても、**そのコピーは消えません**。`forkCount` が 0 で、スターもほぼなければ、影響は小さいです。
- **すでに誰かが、`git clone` などで、手元に保存している場合も、取り戻せません。** ここでできるのは、「これ以上、見える状態を続けない」ことです。
- **Private にしても、GitHub 以外のサービス(検索エンジンのキャッシュなど)に残っている内容を、確実に消せるかは、GitHub Docs のこのページには書かれていません。** 気になる場合は、GitHub のサポートに問い合わせてください。
- Private にしている間も、あなた自身は、これまでどおり `git push` できます。

### 手順1の完了チェック

- [ ] `(.venv)` が行頭に表示されている
- [ ] `git status` が `working tree clean` で、フェーズ5までのコミットがある
- [ ] フェーズ2・5のメモ(チーム名・`match_id`・日付)が手元にある
- [ ] 「過去のコミットに、出力が残っている」ことが、なぜ問題か説明できる
- [ ] `gh repo view --json visibility` で、いまのリポジトリが **PRIVATE** になっている(Public だった場合は、1-4で切り替えた)

---

## 手順2:利用条件の再確認とロゴの扱いを決める

**所要時間:約0.75時間**

### 2-1. `LICENSE.pdf` の、公開に関わる部分を読み直す

- [ ] **[Browser]** `https://github.com/statsbomb/open-data` を開き、リポジトリの中の `LICENSE.pdf`(フェーズ2で読んだもの)を開く。
- [ ] 次の表の条項を、**原文で**探して読む。

| 条項(原文の番号) | 内容(要点) | このプロジェクトでの意味 |
|---|---|---|
| 1.2.1 | データを、編集・歪曲・配布・複製・販売・第三者への提供をしてはいけない | **データそのものを、リポジトリに入れない**。Notebook の出力に残ったデータの行も、同じ扱いにする |
| 1.2.2 | データ、または、データから作った分析を、**商業的に利用してはいけない** | 販売・広告収入・有料サービスにしない。**README にも、非営利と書く** |
| 1.4 | StatsBomb のデータから作った分析を**公開する場合は、StatsBomb のロゴで出典を示す**必要がある | **公開する画像・README に、StatsBomb のロゴを入れる** |
| 2.2 | 利用者の名前とメールアドレスを、StatsBomb に登録することを**お願いしている**(asks) | フェーズ2で、あなたが決めた方針のままで構いません(メモを見返す) |
| 3.2〜3.4 | データは「現状のまま」提供され、正確さの保証はない | README に「正確性は保証されない」と書く |

- 公式リポジトリの README にも、同じ趣旨の記載があります(`If you publish, share or distribute any research, analysis or insights based on this data, please state the data source as StatsBomb and use our logo, available in our Media Pack.`)。

### 2-2. Media Pack の「Usage Rights」(使用条件)を確認する

ロゴを使うことは、**利用条件で求められています**(1.4)。一方、**ロゴの画像ファイルを、リポジトリに入れて配ってよいか**は別の問題で、Media Pack 側の使用条件に書かれている可能性があります。**私は、この中身を確認できていません。**

- [ ] **[Browser]** `https://statsbomb.com/media-pack/` を開く(`Hudl Statsbomb Logos` のコレクションの画面に移動します)。
- [ ] 画面上部の **`Usage Rights`** のメニューを開く。ロゴの画像(例:`hudl-statsbomb-logo-default`)をクリックして、**詳細の画面**に使用条件の記載があるかも確認する。
  - ダウンロードのボタンを押すと、「ダウンロードの理由を入力してください」と出ることがあります。フェーズ2・3でロゴを入手したときと同じ画面です。
- [ ] 見つかった使用条件の原文を、**そのまま**メモに写す(ない場合は「記載なし」と書く)。

```
Media Pack の Usage Rights(確認日:2026-__-__)
原文: ____________________________________________
  (例の観点: 再配布してよいか / 改変してよいか / 商用か非商用か / 表示のしかたの指定)
```

### 2-3. ロゴの扱いを決める

| 確認の結果 | ロゴ画像のファイル(`assets/*.png`) | サンプル画像・README |
|---|---|---|
| **A:原文に、公開リポジトリでの再配布を許可する旨が、明確に書かれている** | `.gitignore` の `assets/*.png` を消して、Git に含めてもよい(任意) | サンプル画像は、ロゴ入りで公開する。README にもロゴを表示してよい |
| **B:記載がない・読み取れない・判断に迷う(既定の選択)** | **Git に含めない(いまの `.gitignore` のまま)**。README に「ロゴは Media Pack から入手して `assets/` に置く」と書く | サンプル画像は、**ロゴ入り**で公開する(下の補足を参照)。README には、ロゴ画像のファイルは置かず、文章で出典を書く |
| **C:再配布や公開での使用を、禁止する旨が書かれている** | Git に含めない | 手順7に進まず、Private のままにする。StatsBomb に確認する(Media Pack・`statsbomb.com` の連絡先) |

- **迷ったら B** にします。**ロゴのファイルを配らない**ほうが、安全側です。
- **補足(B の考え方)**:利用条件 1.4 は、「分析を公開するときは、ロゴで出典を示す」ことを**求めています**。フェーズ3・4で作った画像には、図の右下にロゴが入っています。公開するサンプル画像は、**この要件を満たすために、ロゴ入りのままにします**。一方、**ロゴの元のファイル(`assets/*.png`)を、誰でも取り出せる形で配る**ことは、別の問題なので、確認できるまで行いません。
- 以降の手順は、**B を前提**に書きます。A にした場合は、手順4の README で、ロゴの画像を表示する行を足せます(手順4-5の補足)。
- [ ] 選んだ結果(A / B / C)を、メモに書く。

```
ロゴの扱い: ____(A / B / C)   理由: ____________________
```

### 2-4. 「出典の表記」を、画像と README の両方に入れる

| 場所 | 表記 | 状態 |
|---|---|---|
| 画像の左下 | `Data: StatsBomb Open Data`(ショットマップは、あとに `marker size = xG` も付く) | フェーズ3・4で、すでに入っている |
| 画像の右下 | StatsBomb のロゴ | フェーズ3・4で、入っている(`assets/statsbomb_logo_white.png` がある場合) |
| README | `Data source: StatsBomb` と、公式リポジトリへのリンク | 手順4で完成させる |

- **ロゴなしで作った画像は、公開しません。** `[warn] logo not found` が出ていないか、手順3で確認します。

### 手順2の完了チェック

- [ ] `LICENSE.pdf` の 1.2.1・1.2.2・1.4 を、原文で読み直した
- [ ] Media Pack の `Usage Rights` を開き、原文を(または「記載なし」を)メモした
- [ ] ロゴの扱い(A / B / C)を決めて、メモした
- [ ] 「ロゴを使うこと(1.4で求められている)」と「ロゴのファイルを配ること(別の確認が必要)」の違いを、説明できる
- [ ] (C の場合)Private のまま、手順3以降の準備だけ進める

---

## 手順3:README 用のサンプル画像を作る(課題1)

**所要時間:約0.5時間**

README に載せる画像を、`docs/images/` に作ります。`outputs/` は Git の対象外なので、公開用の画像は別のフォルダに分けます。

### 3-1. 画像の保存先を作る

- [ ] **[Terminal]** `~/projects/pitchviz`(プロジェクトのルート)で実行。

```bash
pwd
mkdir -p docs/images
ls docs
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
00_overview.md     images             phase1_setup.md    phase2_data.md ...
```

### 3-2. サンプル画像を作る(課題1)

フェーズ5で作った `make_maps` を使います。**保存先を `docs/images` にする**のが、今回のポイントです。

- [ ] **[Terminal]** **`~/projects/pitchviz`(プロジェクトのルート)で**実行する。**空欄(`____`)を埋めて**から実行します。

```bash
pwd
python -c "from pitchviz import make_maps; print(make_maps(____, '____', match_date='____', output_dir='____'))"
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目 | 試合の番号(`match_id`)。手順1-2のメモ。数字なので、引用符は付けない |
| 2つ目 | チーム名。メモの値を一字一句そのまま(例:`Japan`) |
| 3つ目 | 試合の日付(`YYYY-MM-DD` の形)。メモの値 |
| 4つ目 | 保存先のフォルダ。手順3-1で作ったフォルダを、**プロジェクトのルートからの相対パス**で書く |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```bash
python -c "from pitchviz import make_maps; print(make_maps(7584, 'Japan', match_date='2018-07-02', output_dir='docs/images'))"
```

(`7584`・`Japan`・`2018-07-02` は例です。あなたのメモの値にします。)

**期待される出力の例**(ダウンロードに数十秒かかることがあります。`NoAuthWarning` は警告で、エラーではありません)

```
[PosixPath('docs/images/pass_map_japan_belgium.png'), PosixPath('docs/images/shot_map_japan_belgium.png')]
```

**答え合わせのあとに**

- 空欄の答え:`7584`、`Japan`、`2018-07-02`、`docs/images`。

**自分のコードが正解と違っても、動いていればOKな例**

- `output_dir` を、`'docs/images/'`(末尾に `/`)と書いた → 動く(同じ場所に保存される)。
- Notebook(セル)で、`make_maps(7584, "Japan", match_date="2018-07-02", output_dir=PROJECT_ROOT / "docs" / "images")` のように書いた → 動く。`PROJECT_ROOT` は `from pitchviz.api import PROJECT_ROOT` で読み込みます。この書き方なら、実行する場所に関係なく、同じ場所に保存されます。
- `python -c "..."` ではなく、`.py` ファイルに書いて実行した → 動く。ただし、**実行する場所(プロジェクトのルート)**は同じです。

**注意:相対パスは、「実行したフォルダ」が基準になります**

- `output_dir='docs/images'` は、**いま作業しているフォルダ**の下の `docs/images` になります。`notebooks/` で実行すると、`notebooks/docs/images/` ができてしまいます(私の検証環境でも、実際にそうなりました)。
- フェーズ5の `PROJECT_ROOT`(実行場所に依存しない)は、**`output_dir` を渡さない場合の初期値**にだけ使われます。自分で相対パスを渡す場合は、実行する場所に気をつけてください。

</details>

### 3-3. できた画像を確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pwd
ls docs/images
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
pass_map_japan_belgium.png	shot_map_japan_belgium.png
```

- [ ] **[VS Code]** Explorer で `docs/images/pass_map_*.png` を開き、次を確認する(ショットマップも同じ)。
  - タイトル(`Japan pass map vs Belgium` など)・凡例が入っている
  - 左下に `Data: StatsBomb Open Data` の文字がある
  - **右下に、StatsBomb のロゴがある**(手順2-4)
  - 手順1-2のメモの試合の図になっている(対戦相手が合っている)
- ターミナルに `[warn] logo not found: ...` と出ていた場合は、**ロゴなしで保存されています**。`ls assets` でロゴ(`statsbomb_logo_white.png`)があるか確認して、作り直してください(手順9の対処表。フェーズ5の8-1の対処表にも、同じ警告の説明があります)。
- [ ] **[Terminal]** この画像が、**Git の対象外になっていない**ことを確認する(コミットに入れるため)。

```bash
git check-ignore -v docs/images/pass_map_japan_belgium.png
echo "終了コード: $?"
```

期待される出力:

```
終了コード: 1
```

- 何も表示されず、**終了コードが `1`** なら、Git の対象です(コミットに入ります)。`.gitignore:...` の行が表示された場合は、除外されています。`.gitignore` の `outputs/*` や `assets/*.png` は、`docs/images/` には当てはまらないはずです。表示されたら、その行の内容を確認してください。

### 手順3の完了チェック

- [ ] `docs/images/` に、パスマップとショットマップの PNG が1枚ずつある
- [ ] 画像に、タイトル・凡例・`Data: StatsBomb Open Data`・StatsBomb のロゴが入っている
- [ ] `notebooks/docs/` など、**間違った場所に画像が作られていない**(`ls notebooks`)
- [ ] `git check-ignore` の終了コードが `1`(Git の対象)になっている

---

## 手順4:README を完成させる(課題2)

**所要時間:約1.0時間**

いまの README は、フェーズ1で作った「仮」に、進捗とクレジットを足したものです。公開用に、**全体を書き直します**。

### 4-1. README に入れる内容を決める

| 順番 | 見出し | 書くこと | 読む人にとっての意味 |
|---|---|---|---|
| 1 | タイトル+一言の説明 | 何をするツールか | 3秒で、自分に関係あるかが分かる |
| 2 | サンプル画像 | パスマップとショットマップの例 | 完成形が、すぐに見える |
| 3 | インストール | コマンドを、順番に | 手元で動かせる |
| 4 | 使い方 | `make_maps(...)` の1行 | 最短で、画像が作れる |
| 5 | 関数の一覧 | 引数と返り値の表 | 応用できる |
| 6 | データとクレジット | StatsBomb への出典・ロゴ・利用条件 | **利用条件 1.4 の要件** |
| 7 | 免責・注意 | 非公式・非営利・正確性の保証なし | **利用条件 1.2.2・3.x への配慮** |
| 8 | ライセンス | コードの扱い | 使ってよい範囲が分かる |
| 9 | フォルダ構成 | 主なファイルの説明 | コードを読む人の案内 |

- **フェーズごとの進捗(`## 進捗` のチェックリスト)は、README から外します。** 公開 README の読み手には、作業の進み具合は関係ありません。進捗は `docs/` の手順書に残っています。

### 4-2. 書き方の補足

- 画像は、**相対パス**で書きます(`docs/images/...`)。GitHub は、リポジトリ内の相対パスの画像を表示します。
- **ファイル名の大文字・小文字は、一字一句そろえる**必要があります。Mac は区別しませんが、GitHub は区別します(手順9の対処表)。
- `あなたのユーザー名` の部分は、自分のユーザー名に置き換えます。
- **「動作確認した環境」には、実際に確認したことだけを書きます**(推測で、他の OS や Python の版を書かない)。

### 4-3. README を書き換える(課題2)

- [ ] **[VS Code]** Explorer で `README.md`(プロジェクトのルート直下)を開く。
  - **対象**:`README.md`
  - **新規作成か編集か**:既存ファイルの編集(**中身を全部消して、次の内容に置き換える**)
- [ ] **空欄(`____`)を埋めて**から貼り付け、`Command + S` で保存する。

以下の内容は、Markdown のコードブロックの中に入っています。**外側のコードブロック(```` ````markdown ```` と ```` ```` ````)は含めずに**、中身だけを貼り付けてください。

````markdown
# PitchViz

[StatsBomb Open Data](https://github.com/statsbomb/open-data) を使って、サッカー日本代表の**パスマップ**と**ショットマップ**(xG をマーカーの大きさで表示)をピッチ上に描き、PNG で保存する Python ツールです。

| パスマップ | ショットマップ |
|---|---|
| ![パスマップの例](docs/images/pass_map_japan_belgium.png) | ![ショットマップの例](docs/images/shot_map_japan_belgium.png) |

*例:2018-07-02 Belgium vs Japan(`match_id` 7584)*

## できること

- 試合(`match_id`)とチーム名を指定して、**1行で**パスマップとショットマップを保存する
- 選手名を指定して、その選手だけのパスマップ・ショットマップを保存する
- ショットマップは、シュート1本ごとの xG(ゴールの期待値)をマーカーの大きさで表し、ゴールを色で区別する

## インストール

動作確認した環境:macOS、Python 3.13.3、VS Code

```bash
git clone https://github.com/あなたのユーザー名/pitchviz.git
cd pitchviz
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### ロゴ画像(任意)

StatsBomb のロゴ画像は、このリポジトリには**含まれていません**。図の右下にロゴを入れるには、[Media Pack](https://statsbomb.com/media-pack/) から、白1色のロゴをダウンロードして、次の場所に置いてください。

```
assets/statsbomb_logo_white.png
```

置かない場合は、`[warn] logo not found: ...` と表示され、ロゴなしで保存されます。**作った画像を公開・共有する場合は、下の「データとクレジット」に従って、StatsBomb のロゴで出典を示してください。**

## 使い方

```python
from pitchviz import make_maps, make_shot_map, list_players

# パスマップとショットマップを、1行で保存する(outputs/ に保存される)
paths = make_maps(____, "____", match_date="____")
print(paths)

# 選手を指定する(選手名は list_players で確認する)
make_shot_map(7584, "Japan", player_name="Genki Haraguchi", match_date="2018-07-02")
```

- 画像は、`outputs/` に `pass_map_<チーム>_<相手>.png`、`shot_map_<チーム>_<相手>.png` の名前で保存されます。
- `match_id` とチーム名は、次のようにして調べられます。

```python
from pitchviz.loader import get_competitions, get_team_matches

matches = get_team_matches(get_competitions("World Cup"), "Japan")
print(matches[["match_id", "match_date", "home_team", "away_team"]])
```

## 主な関数

| 関数 | 何をするか | 返すもの |
|---|---|---|
| `make_pass_map(match_id, team_name, player_name=None, match_date=None, ...)` | パスマップを保存する | 保存先のパス |
| `make_shot_map(match_id, team_name, player_name=None, match_date=None, ...)` | ショットマップを保存する | 保存先のパス |
| `make_maps(match_id, team_name, player_name=None, match_date=None, ...)` | 上の2つを続けて実行する | 保存先のパスのリスト |
| `list_players(events, team_name)` | そのチームの選手名の一覧 | 選手名のリスト |

## データとクレジット

This project uses StatsBomb Open Data.
Data source: [StatsBomb](https://github.com/statsbomb/open-data)

If you publish, share or distribute any research, analysis or insights based on this data, please state the data source as StatsBomb and use their logo, available in the [Media Pack](https://statsbomb.com/media-pack/).

本プロジェクトは StatsBomb Open Data を使用しています。

- **データは、このリポジトリに含まれていません。** 実行時に、StatsBomb の公開リポジトリから取得します。
- StatsBomb のデータから作った分析・画像を公開・共有する場合は、**StatsBomb のロゴで出典を示してください**。
- 利用条件は、公式リポジトリの `LICENSE.pdf`(StatsBomb Public Data User Agreement)を必ず確認してください。

## 免責・注意

- このプロジェクトは、**個人の学習目的の非公式のもの**で、StatsBomb(Hudl)とは関係がありません。
- データまたはデータから作った分析の**商業的な利用は、StatsBomb の利用条件で禁止されています**。このプロジェクトは非営利です。
- データの正確さ・完全さは保証されません。画像は、StatsBomb の見解を示すものではありません。

## ライセンス

コードは MIT License です(`LICENSE` を参照)。**データ・StatsBomb のロゴ・サンプル画像は対象外**で、StatsBomb の利用条件に従います。

## フォルダ構成

```
pitchviz/
├── src/pitchviz/     # 本体(loader.py: データ取得 / pass_map.py / shot_map.py / api.py: 入口の関数)
├── notebooks/        # 試作・動作確認の Notebook
├── docs/             # 作業手順書と、README 用のサンプル画像(docs/images/)
├── outputs/          # 生成した画像の保存先(Git の対象外)
├── assets/           # ロゴ画像の置き場(Git の対象外)
├── pyproject.toml
└── requirements.txt
```
````

**ヒント**

| 空欄 | ヒント |
|---|---|
| 「使い方」の `make_maps(____, "____", match_date="____")` | 手順3-2で使った、`match_id`・チーム名・日付(メモの値)。**画像と同じ試合**にする |

**コードの解説**

| 記述 | 意味 |
|---|---|
| `\| パスマップ \| ショットマップ \|` の表 | Markdown の表。画像を2枚、横に並べるために使う |
| `![説明](docs/images/...png)` | 画像を表示する書き方。`[ ]` の中は、画像が表示できないときの代わりの文(説明文) |
| ```` ```bash ```` | シェルのコマンドのコードブロック。コピーしやすくなる |
| `Data source: [StatsBomb](...)` | データ元の明記(利用条件 1.4・公式 README の求め) |
| 「データは、このリポジトリに含まれていません」 | 利用条件 1.2.1(データの再配布の禁止)に配慮していることを示す |
| 「**データ・StatsBomb のロゴ・サンプル画像は対象外**」 | コードに付けるライセンス(MIT)が、StatsBomb のデータや画像まで許可するわけではない、という線引き |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

「使い方」のコードブロックの1か所だけを示します(他の部分は、上のままです)。

```python
paths = make_maps(7584, "Japan", match_date="2018-07-02")
```

(`7584`・`Japan`・`2018-07-02` は例です。あなたのメモの値にします。)

**答え合わせのあとに**

- 空欄の答え:`match_id`(数字)、チーム名、日付。手順3-2のコマンドと**同じ値**であれば合っています。

**自分のコードが正解と違っても、動いていればOKな例**

- `make_maps(match_id=7584, team_name="Japan", match_date="2018-07-02")` と、引数の名前を付けて書いた → 動く(`make_maps` の引数の名前と同じ)。
- `match_date` を省いた → 動く。ただし、図のタイトルが `date n/a` になる。README の説明と画像が食い違うので、書いておくのがおすすめ。
- README の画像の下の例の文(`*例:...*`)を、自分の試合の対戦カード・日付に直した → それが正解。**自分の試合に合わせて、書き換える**のが正しい。

</details>

### 4-4. プレビューで確認する

- [ ] **[VS Code]** `README.md` を開いた状態で、`Command + Shift + V` を押す(Markdown のプレビューが開く)。
- [ ] 次を確認する。
  - サンプル画像が2枚、横に並んで表示される(表示されない場合は、手順9の対処表)
  - 表・コードブロックが、崩れていない
  - 「インストール」のコードが、1行ずつ、読める形になっている
  - `____` や `あなたのユーザー名` が、**残っていない**(自分のユーザー名に置き換える。`あなたのユーザー名` が残るのは、`git clone` の URL の1か所だけのはず)
- [ ] **[Terminal]** `~/projects/pitchviz` で、`____` の残りがないか検索する。

```bash
pwd
grep -n "____" README.md
echo "終了コード: $?"
```

期待される出力:

```
終了コード: 1
```

- 何も表示されず、**終了コードが `1`**(見つからない)なら OK です。行が表示されたら、その行の空欄を埋めてください。

### 4-5. (ロゴの扱いが A の場合だけ)README にロゴを表示する

- 手順2-3で **A** を選び、`.gitignore` の `assets/*.png` の行を消して、`assets/statsbomb_logo_default.png` を Git に含めると決めた場合だけ、「データとクレジット」の見出しの直下に、次の1行を足せます。

```markdown
![StatsBomb](assets/statsbomb_logo_default.png)
```

- **B(既定)を選んだ場合は、この行を足しません**(画像のファイルが公開されないため、表示されません)。

### 手順4の完了チェック

- [ ] README を、公開用の内容に書き換えた(進捗のチェックリストは外した)
- [ ] 課題2の空欄を埋めて、手順3の画像と**同じ試合**になっている
- [ ] プレビューで、サンプル画像が2枚表示された
- [ ] `grep -n "____" README.md` が何も表示しない(終了コード `1`)
- [ ] 「データとクレジット」に、StatsBomb への出典・ロゴ・利用条件が書いてある
- [ ] 「免責・注意」に、非公式・非営利・正確性の保証なし、が書いてある

---

## 手順5:LICENSE を入れるか決める(任意)

**所要時間:約0.25時間**

`LICENSE` ファイルは、「このコードを、他の人が、どこまで使ってよいか」を示すものです。**入れなくても、公開はできます**(その場合は、他の人は、原則として、コードを自由には使えません)。

### 5-1. 入れるか決める

| 選び方 | 意味 | README の「ライセンス」欄 |
|---|---|---|
| **A:MIT License を入れる** | 誰でも、コードを自由に使える・改変できる。作者は責任を負わない。使うときに、著作権表示を残す | 手順4-3のとおり(`コードは MIT License です`) |
| **B:入れない** | 他の人は、原則として、コードを自由には使えない | 「ライセンス」欄を、`ライセンスは未設定です。` に書き換える |

- どちらが正しい、というものではありません。**学習の記録として公開するだけなら B でも構いません。** 他の人に使ってほしいなら A です。
- ライセンスの種類の比較は、GitHub の案内サイト(`https://choosealicense.com/`)で確認できます。**この判断は法律の助言ではありません。**
- **どちらを選んでも、データ・StatsBomb のロゴ・サンプル画像は、StatsBomb の利用条件に従います**(README に、そう書いてあります)。MIT License は、コードにだけ付けるものです。

### 5-2. A を選んだ場合:`LICENSE` を作る

- [ ] **[VS Code]** Explorer で、プロジェクトのルート直下の空いたところを右クリック → `New File` → `LICENSE`(拡張子なし・大文字)と入力して作る。
  - **対象**:`LICENSE`(プロジェクトのルート直下)
  - **新規作成か編集か**:新規作成
- [ ] 次の内容を貼り付ける。**`____` の2か所**(西暦と名前)を埋めて、`Command + S` で保存する。

```text
MIT License

Copyright (c) 2026 ____

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

| 空欄 | 書くこと |
|---|---|
| `2026` の後ろの `____` | 著作権者の名前。本名でなくても、GitHub のユーザー名で構いません(公開される名前です) |

- 上の文面は、MIT License の標準の文面です。**文面を、自分で書き換えないでください**(`pyproject.toml` や GitHub の「ライセンスの自動認識」は、標準の文面を前提にしています)。
- 西暦は、このフェーズを実施する年にします。

### 5-3. B を選んだ場合

- [ ] **[VS Code]** `README.md` の「ライセンス」の本文を、次の1行に書き換えて保存する。

```markdown
ライセンスは未設定です。なお、データ・StatsBomb のロゴ・サンプル画像は、StatsBomb の利用条件に従います。
```

### 手順5の完了チェック

- [ ] MIT License を入れるか、入れないかを決めた
- [ ] (A の場合)`LICENSE` を作り、`____` を埋めた
- [ ] (B の場合)README の「ライセンス」欄を書き換えた
- [ ] README の「ライセンス」欄と、`LICENSE` の有無が、食い違っていない

---

## 手順6:公開前の最終チェックと、コミット

**所要時間:約0.75時間**

**ここで見つけたものは、公開前なら、直せます。** 公開したあとでは、直しても、過去の版には残ります。ひとつずつ確認してください。

### 6-1. Notebook の出力を消す

Notebook は、**コードだけでなく、実行結果(出力)も一緒にファイルに保存**されます。フェーズ2〜5の出力には、**データの行や、データから作った画像**が残っています(利用条件 1.2.1)。

- [ ] **[VS Code]** `notebooks/` の Notebook を、**1つずつ**(`01`〜`05` の5つ)開き、上部のツールバーの **`Clear All Outputs`**(日本語表示では「すべての出力をクリア」。表示は VS Code の版で違います)を押して、`Command + S` で保存する。
  - 実行番号(`[3]` など)が残っても構いません。**出力(セルの下に出る表・画像・文字)が消えていれば OK** です。
- [ ] **[Terminal]** `~/projects/pitchviz` で、出力が残っていないか確認する。

```bash
pwd
grep -c '"output_type"' notebooks/*.ipynb
grep -l "image/png" notebooks/*.ipynb
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
notebooks/01_setup_check.ipynb:0
notebooks/02_explore_data.ipynb:0
notebooks/03_pass_map.ipynb:0
notebooks/04_shot_map.ipynb:0
notebooks/05_use_function.ipynb:0
```

- 1つ目の `grep -c` は、`"output_type"`(出力が入っている目印)の**行数**を数えます。**すべて `:0`** になれば OK です。0 でないものは、その Notebook の出力が残っています。もう一度、1つ目の手順をやり直してください。
- 2つ目の `grep -l` は、画像の出力が残っているファイルの名前を表示します。**何も表示されなければ OK** です。
- `grep` は、**一致する行がないとき、終了コードが `1` になります**(エラーではありません)。数字(`:0`)と、何も表示されないことを見てください。

### 6-2. データのファイルが入っていないか確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pwd
ls -A data
git ls-files | grep -i -E "\.(csv|json|parquet|pkl|xlsx)$"
echo "終了コード: $?"
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
終了コード: 1
```

- `ls -A data` は、`data/` の中身を表示します。**何も表示されなければ、空**で OK です(`data/` が Git の対象外であることも、フェーズ1で設定済みです)。
- 2つ目は、Git が管理しているファイルの中に、データ形式のファイルがないかの確認です。**何も表示されず、終了コードが `1`** なら OK です。ファイル名が表示されたら、それを公開してよいか確認してください。

### 6-3. 個人情報が入っていないか確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。コミットの作者メールを確認する。

```bash
pwd
git config user.email
git log --format='%an <%ae>' | sort -u
gh api user --jq '.id'
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
12345678+あなたのユーザー名@users.noreply.github.com
あなたの名前 <12345678+あなたのユーザー名@users.noreply.github.com>
12345678
```

- **最後の行(あなたの GitHub の ID)の数字が、メールの `+` の前の数字と、まったく同じ**であることを確認してください。**1桁でも違うと、別の人のアカウントのコミットとして表示されてしまいます**(実際に、1桁足りなくて、別のアカウントに結びついた例があります)。メールを手で打たず、次の「直す方法」のように、`gh` の出力から作るのが確実です。

- メールアドレスが、**`数字+ユーザー名@users.noreply.github.com`** の形(フェーズ1で控えた noreply メール)になっていれば OK です。本物のメールアドレスが出た場合は、**手順7のコミットの前に**、次で直します(このリポジトリだけに効く設定です)。

```bash
git config user.email "$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、Mac のユーザー名・コンピュータ名が、ファイルに混ざっていないか検索する。

```bash
git grep -n -i -- "$(whoami)"
git grep -n -i -- "$(hostname -s)"
git grep -n -E "ghp_|github_pat_|-----BEGIN"
echo "終了コード: $?"
```

- 1つ目と2つ目は、**あなたの Mac のユーザー名・コンピュータ名**が、Git が管理しているファイルに書かれていないかの検索です(`/Users/ユーザー名/...` のパスや、ターミナルの表示を貼ったメモに入りがちです)。3つ目は、アクセストークン(`ghp_...`、`github_pat_...`)や秘密鍵の目印の検索です。
- **何も表示されなければ OK** です。表示された場合は、その行を確認します。
  - あなたの **GitHub のユーザー名が、Mac のユーザー名と同じ**場合、README の `git clone https://github.com/ユーザー名/...` の行は、一致して表示されます。これは、公開する名前なので問題ありません。
  - それ以外(`/Users/あなたの Mac のユーザー名/...` のパスなど)は、書き換えるか、そのファイルを公開しないものとして扱います(次の 6-4)。
  - `ghp_` などが表示された場合は、**トークンが書かれています。すぐに、そのトークンを、GitHub の `Settings → Developer settings` で無効にして**ください。公開しては、いけません。

### 6-4. `docs/` の中の、自分のメモを確認する

`docs/` には、私が出した手順書のほかに、**あなたが作ったメモ**(例:`機能確認.md`、`手順8.md`)があるかもしれません。ターミナルの出力を貼ったメモには、Mac のユーザー名・コンピュータ名が入っていることがあります。

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pwd
ls docs
```

- [ ] 手順書(`00_overview.md`、`phase1_setup.md`〜`phase6_publish.md`)以外のファイルを、**1つずつ開いて**、公開してよい内容か確認する。
- 公開したくないものは、リポジトリの外に移します(`~/projects/pitchviz-notes` は例です)。

```bash
mkdir -p ~/projects/pitchviz-notes
mv "docs/メモのファイル名.md" ~/projects/pitchviz-notes/
```

- 手順書(`phase*.md`)は、`あなたのユーザー名` のような**置き換え用の文字**で書かれているので、そのまま公開できます。ただし、**自分で手を入れて、本物のパスや名前を書き込んだ場合は**、6-3 の検索で見つかります。

### 6-5. Git が管理しているファイルの一覧を、目で確認する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
pwd
git ls-files
git ls-files | grep -E "^(assets|outputs|data|\.venv)/"
```

期待される出力の例(2つ目のコマンドは、`outputs/.gitkeep` の1行だけが表示されます):

```
/Users/あなたのユーザー名/projects/pitchviz
.gitignore
LICENSE
README.md
docs/00_overview.md
...
docs/images/pass_map_japan_belgium.png
docs/images/shot_map_japan_belgium.png
notebooks/01_setup_check.ipynb
...
pyproject.toml
requirements.txt
src/pitchviz/__init__.py
src/pitchviz/api.py
...
outputs/.gitkeep
```

- 確認すること:
  - **`assets/` の画像、`outputs/` の PNG(`.gitkeep` 以外)、`.venv/`、`data/` が出ていない**
  - `docs/images/` に、サンプル画像が2枚ある
  - 知らないファイルが入っていない

### 6-6. 変更をコミットする(まだ、いまのリポジトリ=Private に)

ここまでの変更は、いつもの手順で、いまのリポジトリ(手順1-4で、Private になっているもの)に記録します。

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git status
```

期待される出力の例:

```
On branch main
Changes not staged for commit:
	modified:   README.md
	modified:   notebooks/01_setup_check.ipynb
	modified:   notebooks/02_explore_data.ipynb
	modified:   notebooks/03_pass_map.ipynb
	modified:   notebooks/04_shot_map.ipynb
	modified:   notebooks/05_use_function.ipynb

Untracked files:
	LICENSE
	docs/images/
	docs/phase6_publish.md
```

- `LICENSE` は、手順5で B を選んだ場合は出ません。
- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git add .
git status
```

期待される出力の例:

```
On branch main
Changes to be committed:
	new file:   LICENSE
	new file:   docs/images/pass_map_japan_belgium.png
	new file:   docs/images/shot_map_japan_belgium.png
	new file:   docs/phase6_publish.md
	modified:   README.md
	modified:   notebooks/01_setup_check.ipynb
	...
```

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git commit -m "Phase 6: complete README, add sample images, clear notebook outputs"
git push
```

期待される出力の例:

```
[main xxxxxxx] Phase 6: complete README, add sample images, clear notebook outputs
 ...
To https://github.com/あなたのユーザー名/pitchviz.git
   xxxxxxx..yyyyyyy  main -> main
```

- コミットメッセージは、日本語でも構いません(例:`フェーズ6: README を完成、サンプル画像を追加、Notebook の出力を消去`)。
- この push は、**まだ Private のリポジトリ**への push です(手順1-4で、Private になっていることを確認済みのはず)。公開は、次の手順7です。

### 手順6の完了チェック

- [ ] Notebook 5つの出力を消し、`grep -c '"output_type"'` がすべて `:0` になった
- [ ] `data/` が空で、データ形式のファイルが Git に入っていない
- [ ] コミットの作者メールが noreply になっている
- [ ] Mac のユーザー名・コンピュータ名・トークンが、ファイルに混ざっていない
- [ ] `docs/` の自分のメモを確認し、公開したくないものを外に移した
- [ ] `git ls-files` で、ロゴ・`outputs/` の画像・`.venv/` が入っていないことを確認した
- [ ] 手順6-6のコミットと push を済ませた

---

## 手順7:公開する(履歴をまっさらにして、Public にする)

**所要時間:約0.75時間**

### 7-1. なぜ「新しいリポジトリ」を作るのか

手順1-3で見たとおり、いまのリポジトリの**古いコミットには、Notebook の出力(データの行・画像)が残っています**。

| 方法 | 内容 | 起きること |
|---|---|---|
| そのまま公開する(すでに Public ならそのままにする) | 履歴ごと公開される | 古いコミットを開くと、消す前の出力が見える |
| 履歴を書き換えて、上書きで push する | 難しい操作。**GitHub に、古いコミットが一定期間、残ることがある** | 初学者には、おすすめしない |
| **新しいリポジトリを作り、いまの内容だけを、1つ目のコミットにする(この手順書の方法)** | いまのファイルだけが入った、新しい履歴を作る | 古いコミットは、公開されない |

- 古いリポジトリは、**名前を変えて、Private のまま残します**(消しません)。いつでも、過去の履歴を見られます。
- この方法の利点:**公開される内容は、手順6で確認したファイルだけ**になります。

### 7-2. 公開の最終確認

**ここから先は、Public にする操作です。** 次の表で、すべて「はい」なら進みます。

| 確認 | はい |
|---|---|
| Notebook の出力が消えている(6-1) | [ ] |
| データのファイル・個人情報・トークンが入っていない(6-2〜6-4) | [ ] |
| ロゴの扱いを決めて、メモした(2-3)。ロゴのファイルは Git に入っていない(B の場合) | [ ] |
| README に、StatsBomb への出典と、非営利・非公式の記載がある(4-3) | [ ] |
| サンプル画像に、ロゴと `Data: StatsBomb Open Data` が入っている(3-3) | [ ] |
| 手順2-3で C(禁止)ではなかった | [ ] |

- [ ] **[Terminal]** `~/projects/pitchviz` で、GitHub にログインできているか確認する。

```bash
pwd
git status
gh auth status
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
On branch main
nothing to commit, working tree clean
github.com
  ✓ Logged in to github.com account あなたのユーザー名 (keyring)
  ...
```

- `You are not logged into any GitHub hosts` と出た場合は、フェーズ1の手順3の `gh auth login` をやり直します。
- `nothing to commit, working tree clean` でない場合は、手順6-6に戻ります。

### 7-3. いまのリポジトリの名前を変える

いまの Private リポジトリが `pitchviz` という名前を使っているので、新しい公開用に、この名前を空けます。

- [ ] **[Browser]** `https://github.com/あなたのユーザー名/pitchviz` を開き、`Settings` → `General` → **`Repository name`** を `pitchviz-private` に変えて、`Rename` を押す。
  - 画面の表示は、GitHub の更新で変わることがあります。見つからない場合は、次の `gh` コマンドでも変えられます。

```bash
gh repo rename pitchviz-private
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、ローカルの設定を合わせる。**名前を `private` に付け替え**て、URL も新しい名前にします。

```bash
git remote rename origin private
git remote set-url private https://github.com/あなたのユーザー名/pitchviz-private.git
git remote -v
```

期待される出力の例:

```
private	https://github.com/あなたのユーザー名/pitchviz-private.git (fetch)
private	https://github.com/あなたのユーザー名/pitchviz-private.git (push)
```

- これ以降、`private` が、古い(Private の)リポジトリです。**`origin` は、次の手順で、新しい公開用に付けます。**

### 7-4. ローカルで、新しい(まっさらな)履歴を作る

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。まず、いまの `main` に別の名前を付けて**取っておき**ます(古い履歴は、消えません)。

```bash
pwd
git branch -m main main-private
git branch
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
* main-private
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、履歴のない `main` を新しく作る。

```bash
git checkout --orphan main
git status --short | head -5
```

期待される出力の例(ファイルが、すべて「新規」として並びます):

```
Switched to a new branch 'main'
A  .gitignore
A  LICENSE
A  README.md
A  docs/00_overview.md
A  docs/images/pass_map_japan_belgium.png
```

- `--orphan` は、「前のコミットを引き継がない、新しいブランチ」を作る指定です。ファイルの中身は、そのままです。
- `.gitignore` の設定は引き継がれるので、`assets/` の画像や `outputs/` の PNG は、**入りません**(6-5の確認と同じです)。

- [ ] **[Terminal]** `~/projects/pitchviz` で、コミットする。

```bash
git add -A
git status
git commit -m "Initial public release"
git log --oneline
git log --format='%an <%ae>'
```

期待される出力の例:

```
[main (root-commit) xxxxxxx] Initial public release
 ... files changed, ... insertions(+)
xxxxxxx Initial public release
あなたの名前 <12345678+あなたのユーザー名@users.noreply.github.com>
```

- **`git log --oneline` の行が1つだけ**で、作者が noreply メールなら OK です。あわせて、メールの `+` の前の数字が、`gh api user --jq '.id'` の出力と**同じ**ことを確認してください(手順6-3)。
- `git status` の一覧に、`assets/` や `outputs/` の PNG、`.venv/` が**出ていない**ことも確認してください(出ていたら、コミットの前に、手順6-5に戻ります)。

### 7-5. 新しい Public リポジトリを作って、push する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。**これで、リポジトリが公開されます。**

```bash
gh repo create pitchviz --public --source=. --remote=origin --push --description "Pass maps and shot maps (xG) of Japan national team from StatsBomb Open Data"
```

期待される出力の例(行は、`gh` の版で違います):

```
✓ Created repository あなたのユーザー名/pitchviz on GitHub
  https://github.com/あなたのユーザー名/pitchviz
✓ Added remote https://github.com/あなたのユーザー名/pitchviz.git
Enumerating objects: xx, done.
...
✓ Pushed commits to https://github.com/あなたのユーザー名/pitchviz.git
```

**コマンドの解説**

| 部分 | 意味 |
|---|---|
| `gh repo create pitchviz` | `pitchviz` という名前のリポジトリを、GitHub に作る |
| `--public` | 公開(Public)にする |
| `--source=.` | いまのフォルダ(`~/projects/pitchviz`)を、元にする |
| `--remote=origin` | 作ったリポジトリを、`origin` という名前で登録する |
| `--push` | いまのコミットを、そのまま push する |
| `--description "..."` | リポジトリの説明文(GitHub のページの上部に出る) |

- 「ブラウザで作る」場合は、`https://github.com/new` で、Repository name を `pitchviz`、**Public** を選び、**`Add a README file`・`Add .gitignore`・`Choose a license` のチェックを、すべて外して**(すでにファイルがあるため)作ります。その後、画面に出る手順どおりに、次を実行します。

```bash
git remote add origin https://github.com/あなたのユーザー名/pitchviz.git
git push -u origin main
```

- [ ] **[Terminal]** `~/projects/pitchviz` で、登録先を確認する。

```bash
git remote -v
git branch -vv
```

期待される出力の例:

```
origin	https://github.com/あなたのユーザー名/pitchviz.git (fetch)
origin	https://github.com/あなたのユーザー名/pitchviz.git (push)
private	https://github.com/あなたのユーザー名/pitchviz-private.git (fetch)
private	https://github.com/あなたのユーザー名/pitchviz-private.git (push)
* main         xxxxxxx [origin/main] Initial public release
  main-private yyyyyyy [private/main] Phase 6: complete README, add sample images, clear notebook outputs
```

- `main` が **公開用(`origin`)**、`main-private` が**古い Private(`private`)**です。この対応が合っているか、必ず見てください。

### 7-6. リポジトリの説明とトピックを設定する

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
gh repo edit --add-topic soccer --add-topic football-analytics --add-topic statsbomb --add-topic mplsoccer --add-topic matplotlib --add-topic python
```

- トピックは、GitHub で、リポジトリを探しやすくするための**タグ**です。ブラウザで設定する場合は、リポジトリのページ右側の「About」の歯車のアイコンから変えられます。

### 7-7. ログインしていない状態で、見え方を確認する

- [ ] **[Browser]** **プライベートウィンドウ**(ログインしていない状態になります。Safari なら `File → New Private Window`)で、`https://github.com/あなたのユーザー名/pitchviz` を開く。

| 確認 | 期待 | OK |
|---|---|---|
| ページが表示される | ログインなしで見える(= Public) | [ ] |
| README の画像 | サンプル画像が2枚、表示される | [ ] |
| README の「データとクレジット」 | 出典・利用条件の案内が表示される | [ ] |
| `assets/` フォルダ | **ない**(ロゴのファイルが入っていない。B の場合) | [ ] |
| `outputs/` フォルダ | `.gitkeep` だけがある | [ ] |
| `notebooks/` の Notebook を開く | コードだけで、表・画像の出力が**ない** | [ ] |
| `Commits` の数 | **1** | [ ] |
| コミットの作者 | noreply メール(本名・本物のメールが出ていない)。作者のアイコンと名前が、**自分のアカウント** | [ ] |
| `docs/` | 手順書と `images/` だけ(自分の非公開メモが入っていない) | [ ] |
| `License` | (A の場合)右側に MIT License と表示される | [ ] |

- **コミットの作者が、自分のアカウントか**は、画面だけでなく、次のコマンドでも確認できます。1つ目が、自分のログイン名と同じなら OK です。

```bash
gh api repos/{owner}/{repo}/commits --jq '.[] | [.sha[0:7], .author.login] | @tsv'
gh api user --jq '.login'
```

- 1つでも期待と違えば、**そのリポジトリを、いったん Private に戻す**ことができます。

```bash
gh repo edit --visibility private --accept-visibility-change-consequences
```

- 直したあとで、もう一度 Public にするときは、`--visibility public` に変えて、同じコマンドを実行します。
- **画像が表示されない**場合は、手順9の対処表(ファイル名の大文字小文字、コミットされていない、など)を見てください。

### 7-8. これからの、push の使い分け

| ブランチ | つながる先 | 公開 |
|---|---|---|
| `main` | `origin`(新しい **Public** リポジトリ) | **公開される** |
| `main-private` | `private`(古い **Private** リポジトリ) | 公開されない |

- 今後の作業は、**`main` で行い、`git push` するだけ**で、公開リポジトリに反映されます。
- **`main-private` は、公開リポジトリに push しません。** `git push origin main-private` のような、`origin` を指定した push はしないでください(古い履歴が、公開されてしまいます)。
- いま `main` にいる状態では、`git push` は、`origin`(公開用)に向かいます。**push の前に、`git branch` で、どのブランチにいるか確認する**習慣をつけてください。

### 手順7の完了チェック

- [ ] 公開の最終確認の表が、すべて「はい」になった
- [ ] 古いリポジトリを `pitchviz-private` に改名し、Private のまま残した
- [ ] `git log --oneline` の行が、1つだけ(新しい履歴)になっている
- [ ] `gh repo create ... --public --push` が成功した(またはブラウザで作って push した)
- [ ] `git branch -vv` で、`main` が `origin`、`main-private` が `private` につながっている
- [ ] プライベートウィンドウで、7-7の確認表がすべて OK になった

---

## 手順8:最初のリリース `v0.1.0` を作る(課題3)

**所要時間:約0.5時間**

**リリース**は、「この時点の版」に名前(版番号)を付けて、GitHub の `Releases` のページに載せるものです。後から、この版に戻ったり、この版を指して説明したりできます。

### 8-1. 版番号を決める

- `pyproject.toml` の `version = "0.1.0"` と、**リリースの版番号をそろえます**(`v` を付けて `v0.1.0`)。
- [ ] **[Terminal]** `~/projects/pitchviz` で確認する。

```bash
pwd
grep -n "^version" pyproject.toml
```

期待される出力の例:

```
/Users/あなたのユーザー名/projects/pitchviz
7:version = "0.1.0"
```

| 版番号の読み方 | 意味 |
|---|---|
| `0.1.0` | 「最初の、動く版」を表す、よくある付け方(メジャー.マイナー.パッチ) |
| 先頭の `v` | タグの名前の習慣(`v0.1.0`)。`pyproject.toml` の `version` には付けない |

### 8-2. タグを付けて push する(課題3)

**タグ**は、「この時点のコミット」に付ける名前です。リリースは、タグを元に作られます。**空欄(`____`)を埋めて**から実行します。

- [ ] **[Terminal]** `~/projects/pitchviz` で実行。

```bash
git tag -a ____ -m "First release"
git push origin ____
git tag
```

**ヒント**

| 空欄 | ヒント |
|---|---|
| 1つ目と2つ目(同じ値が入る) | 手順8-1の、`v` を付けた版番号 |

<details>
<summary>▼ 答え(自分で考えてから開く)</summary>

```bash
git tag -a v0.1.0 -m "First release"
git push origin v0.1.0
git tag
```

**期待される出力の例**

```
Enumerating objects: 1, done.
...
To https://github.com/あなたのユーザー名/pitchviz.git
 * [new tag]         v0.1.0 -> v0.1.0
v0.1.0
```

**答え合わせのあとに**

- 空欄の答え:2つとも `v0.1.0`。

**自分のコードが正解と違っても、動いていればOKな例**

- `git tag v0.1.0`(`-a` と `-m` なし)で付けた → 動く(「軽いタグ」。リリースは作れる。`-a` を付けた「注釈つきタグ」のほうが、作成者・日付・メッセージが残るので、おすすめ)。
- `git push --tags` で、まとめて push した → 動く(すべてのタグを push する)。ただし、**今後、不要なタグも一緒に push される**ので、`git push origin v0.1.0` と名前を指定するほうが安全。

**注意**

- **`git push` だけでは、タグは push されません。** `git push origin タグ名` が必要です(手順9の対処表)。
- **`origin` を指定します。** `private` に push すると、古い Private のリポジトリにタグが付きます。

</details>

### 8-3. GitHub のリリースを作る

- [ ] **[Browser]** `https://github.com/あなたのユーザー名/pitchviz` を開き、右側の `Releases` → `Create a new release`(または `Draft a new release`)を押す。
- [ ] 次のように入力する。

| 項目 | 入力 |
|---|---|
| `Choose a tag` | `v0.1.0`(手順8-2で push したタグを選ぶ) |
| `Release title` | `v0.1.0` |
| 説明(本文) | 下の文章(自分の内容に合わせて直す) |

```markdown
## PitchViz v0.1.0 — 最初のリリース

StatsBomb Open Data から、サッカー日本代表のパスマップとショットマップ(xG をマーカーの大きさで表示)を描いて、PNG で保存します。

### できること
- `make_maps(match_id, team_name, match_date=...)` の1行で、パスマップとショットマップを保存する
- `player_name=` を渡して、選手別の画像を保存する

### 使い方
README の「インストール」「使い方」を参照してください。

### 注意
- データは含まれていません。実行時に StatsBomb の公開リポジトリから取得します。
- データから作った分析を公開する場合は、StatsBomb の利用条件に従い、StatsBomb のロゴで出典を示してください。
```

- [ ] `Publish release` を押す。
- 「`gh` で作る」場合は、次のコマンドでも作れます。

```bash
gh release create v0.1.0 --verify-tag --title "v0.1.0" --notes "First release: make_maps / make_shot_map / make_pass_map. Data is not included; see README for the StatsBomb terms."
```

- `--verify-tag` は、「そのタグが、リモートにあること」を確認してから作る指定です。タグを push し忘れていると、ここで止まります。

### 8-4. リリースを確認する

- [ ] **[Browser]** プライベートウィンドウで、`https://github.com/あなたのユーザー名/pitchviz/releases` を開く。

| 確認 | 期待 |
|---|---|
| リリースの名前 | `v0.1.0`(`Latest` の印が付く) |
| 本文 | 書いた文章が表示される |
| `Assets` | `Source code (zip)` と `Source code (tar.gz)` が、自動で付いている |

- `Source code` は、そのタグの時点のリポジトリの内容を、GitHub が自動で固めたものです。**手順6・7で確認した内容と同じ**なので、データやロゴのファイルは含まれません。
- **自分で、データやロゴのファイルを、リリースに添付しません。**

### 手順8の完了チェック

- [ ] `pyproject.toml` の版と、タグの版(`v0.1.0`)がそろっている
- [ ] 課題3の空欄を埋めて、タグを `origin` に push した
- [ ] GitHub の `Releases` に、`v0.1.0` が表示されている
- [ ] 自分で添付したファイル(データ・ロゴ)がない

---

## 手順9:つまずきやすい点と対処法

### 9-1. エラー別の対処表

| 症状・エラーメッセージの例 | 原因 | 対処 |
|---|---|---|
| README のサンプル画像が表示されない(壊れた画像のアイコン) | ① 画像のファイルが、コミットされていない ② ファイル名の大文字・小文字・綴りが、README と違う(**Mac は区別せず、GitHub は区別する**) ③ パスが違う | `git ls-files docs/images` で、ファイルがあるか確認する。README の `docs/images/...` と、一字一句比べる。ブラウザで、画像のファイルを直接開いて確認する |
| `docs/images/` の画像が、Git に入らない(`git status` に出ない) | `.gitignore` に除外されている | `git check-ignore -v docs/images/pass_map_japan_belgium.png` で、どの行が除外しているか確認する(手順3-3) |
| `notebooks/docs/images/` ができていた | `output_dir='docs/images'` を、`notebooks/` で実行した(相対パスは、**実行した場所**が基準) | プロジェクトのルートで実行し直す。間違えて作った `notebooks/docs/` は、`rm -r notebooks/docs` で消す |
| `[warn] logo not found: .../assets/statsbomb_logo_white.png` が出て、画像にロゴがない | ロゴの画像が、`assets/` にない | `ls assets` で確認する。ロゴなしの画像は、**公開しない**。ロゴを置き直して、画像を作り直す(手順3-2) |
| `grep -c '"output_type"' notebooks/*.ipynb` で、`:0` 以外が出る | Notebook の出力が、残っている | その Notebook を開いて、`Clear All Outputs` → `Command + S`。もう一度確認する(手順6-1) |
| `git grep -n -i -- "$(whoami)"` で、行が表示される | あなたの Mac のユーザー名が、ファイルに書かれている(`/Users/ユーザー名/...` のパスなど) | 表示されたファイルと行を開いて、書き換える。公開しないメモなら、リポジトリの外に移す(手順6-4) |
| `error: remote origin already exists.` | すでに `origin` がある状態で、`git remote add origin ...` を実行した | `git remote -v` で確認する。古い `origin` を、先に `git remote rename origin private` で付け替える(手順7-3) |
| `fatal: A branch named 'main-private' already exists.` | 手順7-4を、2回実行した | `git branch` で、いまの状態を確認する。すでに `main-private` があるなら、`git branch -m main main-private` は、もう実行しない |
| `GraphQL: Name already exists on this account (createRepository)` など、「名前がすでにある」というエラー(`gh repo create`) | 古いリポジトリが、まだ `pitchviz` という名前のまま | 手順7-3で、古いリポジトリを `pitchviz-private` に改名したか確認する(GitHub の `Settings → General`) |
| `! [rejected] main -> main (non-fast-forward)` | 新しい履歴の `main` を、**古いリポジトリ**に push しようとした(`origin` が古い方を指している) | `git remote -v` で、`origin` が新しい公開用か確認する。古い方に push するのは、**やめる**(上書きしない) |
| `fatal: refusing to merge unrelated histories` | 新しい `main` と、古い `main-private` を、`git pull` や `git merge` で合体させようとした | 合体させない。新しい履歴と古い履歴は、別のものとして扱う |
| `You are not logged into any GitHub hosts. To log in, run: gh auth login` | `gh` にログインしていない | `gh auth login`(フェーズ1の手順3)。ログイン後、`gh auth status` で確認する |
| ずっと Public で進めてきたのに、手順書は「Private のまま」と書いてある | フェーズ1は「どちらでも可」。フェーズ3〜5の手順書は、Private を前提にしていた | 手順1-4で、`gh repo view --json visibility` を実行し、Public なら先に Private に切り替える。そのあと手順2以降へ |
| `fatal: tag 'v0.1.0' already exists` | 同じ名前のタグを、2回付けた | `git tag` で一覧を確認する。すでに正しいタグがあるなら、付け直さず、`git push origin v0.1.0` に進む |
| リリースの画面で、`v0.1.0` のタグが選べない | タグを、`origin` に push していない(`git push` だけでは、タグは push されない) | `git push origin v0.1.0` を実行する(手順8-2) |
| `gh release create` で、タグがリモートにない旨のエラーが出る(`--verify-tag` を付けたとき) | タグを、`origin` に push していない | `git push origin v0.1.0` のあとに、もう一度実行する |
| 公開したあとで、見せたくないものが入っていたと気づいた | 手順6の確認の漏れ | **すぐに、`gh repo edit --visibility private --accept-visibility-change-consequences` で、Private に戻す**。ファイルを直して、手順7をやり直す(新しいリポジトリを作り直す)。トークンが入っていた場合は、**先に、トークンを無効にする** |
| `git push` したら、`main-private` のほうに push されそうで不安 | どのブランチにいるか分からない | `git branch` で、`*` が付いているブランチを確認する。`main` なら `origin`(公開用)、`main-private` なら `private` に向かう(手順7-8) |

### 9-2. 「公開できているか分からない」ときの確認方法

- **ログインしていない状態で開く**:プライベートウィンドウで、リポジトリの URL を開く。ページが出れば Public です。
- **コマンドで確認する**:次のコマンドで、公開の状態が分かります。

```bash
gh repo view --json visibility,url
```

期待される出力の例:

```
{"url":"https://github.com/あなたのユーザー名/pitchviz","visibility":"PUBLIC"}
```

- **古い Private のリポジトリが、Private のままか確認する**:`gh repo view あなたのユーザー名/pitchviz-private --json visibility` で、`"visibility":"PRIVATE"` と出れば OK です。

---

## 手順10:Claude / ChatGPT に質問するときのコツ(公開・README 編)

### 10-1. 公開に関する質問に、必ず入れるもの

1. **やりたいこと**:「GitHub で、`pitchviz` のリポジトリを Public にしたい。StatsBomb のデータを含めたくない」
2. **実行したコマンドと、その出力の全文**(最初のエラー行から、最後まで)
3. **次の確認コマンドの出力**:

```bash
pwd
git status
git branch -vv
git remote -v
git log --oneline | head -5
git ls-files
```

4. **README の該当部分**(画像が出ないときは、画像の行と、`git ls-files docs/images` の出力)

### 10-2. 貼ってはいけないもの

- **アクセストークン**(`ghp_...`、`github_pat_...`)や、`gh auth token` の出力
- **本物のメールアドレス**、秘密鍵、パスワード
- **`.env` のような、設定ファイルの中身**
- 貼る前に、出力の中に上のものが混ざっていないか、**必ず目で確認**してください。混ざっていたら、その部分を `<削除>` に書き換えます。

### 10-3. 質問の例

> macOS、GitHub CLI(`gh`)を使っています。Private のリポジトリ `pitchviz` を改名して、履歴のない新しい `main` を作り(`git checkout --orphan main`)、`gh repo create pitchviz --public --source=. --remote=origin --push` を実行しました。次のエラーが出ました。
>
> (エラー文の全文)
>
> `git remote -v` と `git branch -vv` の出力は、次のとおりです。
>
> (出力)
>
> 原因として何が考えられますか? 古い Private のリポジトリに、影響が出ない方法を、初学者向けに教えてください。

### 10-4. 回答の使い方

- **公開・削除・上書きに関わるコマンド**(`git push --force`、`git filter-repo`、`gh repo delete`、`--visibility public`)を提案されたら、**実行する前に**、「このコマンドは何を変えますか? 元に戻せますか?」と質問してください。
- AI が示した `gh` のコマンドの引数は、`gh repo create --help` などで、**実在するか確認**してください(`gh` の版で、引数が変わることがあります)。
- StatsBomb の利用条件の解釈(ロゴを配ってよいか、など)を AI に聞いても、**最終的な根拠は、原文(`LICENSE.pdf`、Media Pack)**です。AI の回答は、原文を読むための補助にします。

---

## このフェーズ終了時のディレクトリツリー

`NEW` は新しく作ったファイル、`MOD` は変更したファイルです。

```
~/projects/pitchviz/
├── .git/                              # MOD(履歴を、新しい1コミットから作り直した)
├── .gitignore
├── .venv/
├── LICENSE                            # NEW(MIT を選んだ場合。任意)
├── README.md                          # MOD(公開用に全面書き換え)
├── pyproject.toml
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
│   ├── phase5_function.md
│   ├── phase6_publish.md              # NEW
│   └── images/                        # NEW
│       ├── pass_map_japan_belgium.png     # NEW(README 用のサンプル。例)
│       └── shot_map_japan_belgium.png     # NEW(README 用のサンプル。例)
├── notebooks/
│   ├── 01_setup_check.ipynb           # MOD(出力を消した)
│   ├── 02_explore_data.ipynb          # MOD(出力を消した)
│   ├── 03_pass_map.ipynb              # MOD(出力を消した)
│   ├── 04_shot_map.ipynb              # MOD(出力を消した)
│   └── 05_use_function.ipynb          # MOD(出力を消した)
├── src/
│   └── pitchviz/
│       ├── __init__.py
│       ├── loader.py
│       ├── pass_map.py
│       ├── shot_map.py
│       └── api.py
├── outputs/
│   ├── .gitkeep
│   └── (作業用の PNG。Git管理外)
└── data/                              # (空。Git管理外)
```

- `00_overview.md` の完成形のツリーと比べると、`assets/`(フェーズ3)、`docs/images/`・`LICENSE`(フェーズ6)が増えています。いずれも、手順書の進行上、必要になって増えたものです。
- **GitHub 側の状態**:`あなたのユーザー名/pitchviz`(**Public**・履歴は1コミット・`v0.1.0` のリリース)と、`あなたのユーザー名/pitchviz-private`(**Private**・これまでの全履歴)の、2つのリポジトリになります。

---

## 手順11:振り返り

次の質問に、1〜2行で自分の言葉で答えてみてください。

1. 利用条件 1.2.1 と 1.4 は、それぞれ、このプロジェクトの何に関係しますか?
2. 「ロゴを使うこと」と「ロゴのファイルを、リポジトリに入れて配ること」は、なぜ別の問題として扱ったのですか?
3. Notebook の出力を消しただけでは足りず、新しいリポジトリを作ったのは、なぜですか?
4. `main` と `main-private` は、それぞれ、どこにつながっていますか? 間違えて push すると、何が起きますか?
5. `git push` だけでは、リリースのタグが GitHub に届かないのは、なぜですか?

- [ ] 1に「1.2.1 はデータをリポジトリに入れない・Notebook の出力に残さない、1.4 は公開する画像にロゴで出典を示す」のように答えられる
- [ ] 2に「1.4 はロゴで出典を示すことを求めているが、ロゴの元ファイルを配ってよいかは、Media Pack の使用条件で別に確認が必要だから」のように答えられる
- [ ] 3に「古いコミットを開くと、消す前の出力が見えるから」のように答えられる
- [ ] 4に「`main` は公開用の `origin`、`main-private` は古い `private`。`origin` に `main-private` を push すると、古い履歴が公開されるから」のように答えられる
- [ ] 5に「タグは、コミットとは別に扱われ、`git push origin タグ名` で送る必要があるから」のように答えられる

---

## フェーズ6 最終チェックリスト

**README とサンプル画像**

- [ ] `docs/images/` に、ロゴ入りのサンプル画像が2枚ある
- [ ] README に、サンプル画像・インストール・使い方・クレジット・免責・ライセンスがある
- [ ] `grep -n "____" README.md` が何も表示しない

**利用条件への対応**

- [ ] 画像に `Data: StatsBomb Open Data` と StatsBomb のロゴが入っている(1.4)
- [ ] データのファイルも、Notebook の出力も、リポジトリに入っていない(1.2.1)
- [ ] README に、非営利・非公式・正確性の保証なし、と書いてある(1.2.2・3.x)
- [ ] ロゴの扱い(A / B / C)を決めて、メモした。B の場合、ロゴのファイルは Git に入っていない

**公開**

- [ ] 新しいリポジトリ `pitchviz` が **Public** になり、`Commits` が1つになっている
- [ ] 古いリポジトリが `pitchviz-private`(**Private**)で残っている
- [ ] プライベートウィンドウで、README・画像・Notebook(出力なし)が確認できた
- [ ] `git branch -vv` で、`main` が `origin`、`main-private` が `private` につながっている

**リリース**

- [ ] `v0.1.0` のタグを `origin` に push した
- [ ] GitHub の `Releases` に `v0.1.0` が表示されている

すべてにチェックが付けば、フェーズ6は完了です。**PitchViz の完成です。**

---

## 完成の確認(最初の目標との対応)

| 最初の目標 | できたこと | どこで |
|---|---|---|
| StatsBomb Open Data を使う | データを取得して、絞り込めるようになった | フェーズ2 |
| 日本代表のパスマップを描く | ピッチ上に、パスを矢印で描いた | フェーズ3 |
| シュートを、xG をマーカーの大きさで描く | ショットマップを描いた | フェーズ4 |
| 試合とチーム/選手を指定して、画像を保存する関数 | `make_maps` / `make_shot_map` / `make_pass_map` | フェーズ5 |
| README と GitHub での公開 | README・サンプル画像・クレジット・`v0.1.0` | フェーズ6 |

## このあと(任意)

- 他の試合・他のチーム(例:女子日本代表。`get_team_matches` の検索語を変えて、表記をデータで確認する)で、画像を作る
- ヒートマップ・パスネットワークなど、別の図を `src/pitchviz/` に足す(フェーズ3〜5と同じ「Notebook で試す → `.py` に移す → `api.py` から呼ぶ」の流れ)
- 公開したリポジトリは、**これまでと同じ手順**(`git add` → `git commit` → `git push`)で更新できます。**更新のたびに、手順6の確認(出力・個人情報・ロゴ)をしてください。**

**参考:公式ドキュメント(確認先)**

| 対象 | 確認先 |
|---|---|
| StatsBomb Open Data(データ・利用条件) | `https://github.com/statsbomb/open-data`(`LICENSE.pdf`) |
| StatsBomb の Media Pack(ロゴ・Usage Rights) | `https://statsbomb.com/media-pack/` |
| GitHub CLI(`gh repo create`・`gh release create`・`gh repo edit`) | `https://cli.github.com/manual/` |
| GitHub Docs(リポジトリの公開範囲・リリースの管理) | `https://docs.github.com/` |
| Git(`checkout --orphan`・`tag`) | `https://git-scm.com/docs` |
| ライセンスの選び方(MIT など) | `https://choosealicense.com/` |
