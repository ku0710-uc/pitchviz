
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st

from pitchviz.loader import (
    get_competitions,
    get_team_matches,
    get_events,
)
from pitchviz.api import get_teams, list_players, make_maps


st.set_page_config(
    page_title="PitchViz",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ PitchViz")
st.write("StatsBomb Open Dataを使ったサッカーのパスマップ・ショットマップ生成ツール")

st.caption(
    "Data: StatsBomb Open Data. "
    "公開・共有時はStatsBombの利用条件を確認してください。"
)


@st.cache_data(ttl=3600)
def load_matches():
    competitions = get_competitions("World Cup")
    return get_team_matches(competitions, "Japan")


@st.cache_data(ttl=3600)
def load_events(match_id):
    return get_events(int(match_id))


try:
    matches = load_matches()

    if matches.empty:
        st.warning("対象となる試合が見つかりませんでした。")
        st.stop()

    matches["match_date"] = matches["match_date"].astype(str)

    matches["match_label"] = (
        matches["match_date"]
        + " | "
        + matches["home_team"]
        + " vs "
        + matches["away_team"]
    )

    selected_label = st.selectbox(
        "試合を選択",
        matches["match_label"].tolist(),
    )

    match = matches[
        matches["match_label"] == selected_label
    ].iloc[0]

    match_id = int(match["match_id"])
    match_date = match["match_date"]

    st.write(f"試合ID: {match_id}")

    events = load_events(match_id)
    teams = get_teams(events)

    team_name = st.selectbox(
        "対象チーム",
        teams,
    )

    players = ["チーム全体"] + list_players(events, team_name)

    player_label = st.selectbox(
        "対象選手",
        players,
    )

    player_name = (
        None if player_label == "チーム全体"
        else player_label
    )

    if st.button("マップを生成", type="primary"):
        with st.spinner("マップを生成しています..."):
            with TemporaryDirectory() as temp_dir:
                output_dir = Path(temp_dir)

                paths = make_maps(
                    match_id,
                    team_name,
                    player_name=player_name,
                    match_date=match_date,
                    output_dir=output_dir,
                    logo_path=None,
                    events=events,
                )

                titles = ["パスマップ", "ショットマップ"]

                for title, path in zip(titles, paths):
                    path = Path(path)
                    image_bytes = path.read_bytes()

                    st.subheader(title)
                    st.image(image_bytes, use_container_width=True)

                    st.download_button(
                        label=f"{title}をPNGでダウンロード",
                        data=image_bytes,
                        file_name=path.name,
                        mime="image/png",
                        key=f"download_{title}",
                    )

except Exception as e:
    st.error(
        "データの取得またはマップの生成に失敗しました。"
    )
    st.caption(f"エラー詳細: {type(e).__name__}: {e}")
