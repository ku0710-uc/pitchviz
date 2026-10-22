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
    if TEAM_KEYWORD.lower() in row["home_team"].lower():
        return row["home_team"]
    return row["away_team"]


def match_label(row):
    """選択肢に表示する文字列。例: 2018-07-02  Belgium vs Japan"""
    return f'{row["match_date"]}  {row["home_team"]} vs {row["away_team"]}'


st.title("PitchViz: 日本代表のパスマップ・シュートマップ")
st.caption("StatsBomb Open Data から作った、パスマップとシュートマップ(xG をマーカーの大きさで表示)です。")

if not DEFAULT_LOGO_PATH.exists():
    st.warning(
        "この環境には StatsBomb のロゴのファイルがないため、ここで作る画像には、ロゴが入りません。"
        "ロゴのない画像は、公開・配布しないでください。"
    )

matches = load_matches()
if len(matches) == 0:
    st.error("試合の一覧を取得できませんでした。少し時間をおいて、もう一度開いてください。")
    st.stop()

left, middle, right = st.columns(3)
with left:
    match_index = st.selectbox(
        "試合",
        options=list(matches.index),
        format_func=lambda i: match_label(matches.loc[i]),
    )

row = matches.loc[match_index]
japan_team = pick_team(row)
other_team = row["away_team"] if japan_team == row["home_team"] else row["home_team"]
match_id = int(row["match_id"])
match_date = str(row["match_date"])

with middle:
    team_name = st.selectbox("チーム", options=[japan_team, other_team])

events = load_events(match_id)
players = list_players(events, team_name)

with right:
    choice = st.selectbox("選手", options=[ALL_PLAYERS] + players)

player_name = None if choice == ALL_PLAYERS else choice


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

tab_pass, tab_shot = st.tabs(["パスマップ", "シュートマップ"])
tab_specs = [
    (tab_pass, "pass", "この選手のパスは、データにありません。"),
    (tab_shot, "shot", "この選手のシュートは、データにありません(シュートを打っていない選手です)。"),
]

for tab, kind, empty_message in tab_specs:
    with tab:
        try:
            file_name, png = render_map(kind, match_id, team_name, player_name, match_date)
        except ValueError as error:
            st.info(empty_message)
            st.caption(f"詳細: {error}")
        else:
            st.image(BytesIO(png), width="stretch")
            st.download_button(
                label="PNG をダウンロード",
                data=png,
                file_name=file_name,
                mime="image/png",
                on_click="ignore",
                key=f"download_{kind}",
            )

st.divider()
st.markdown(
    f"データ: [StatsBomb Open Data]({OPEN_DATA_URL})。"
    "非公式・非営利の学習用の画面です。データの正確性は保証しません。"
)
