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

def filter_events(events, event_type, team_name=None):
    """イベント種別(例: "Pass")で絞り込む。team_name を渡すと、そのチームだけにする。"""
    result = events[events["type"] == event_type]
    if team_name is not None:
        result = result[result["team"] == team_name]
    return result.copy()

def get_passes(events, team_name):
    """指定チームのパスを返す。x, y, end_x, end_y(座標)と is_complete(成功パスか)の列を付ける。"""
    passes = filter_events(events, "Pass", team_name)
    passes = add_xy(passes, "location", "x", "y")
    passes = add_xy(passes, "pass_end_location", "end_x", "end_y")
    passes["is_complete"] = passes["pass_outcome"].isna()
    passes = passes.dropna(subset=["x", "y", "end_x", "end_y"]).copy()
    passes[["x", "y", "end_x", "end_y"]] = passes[["x", "y", "end_x", "end_y"]].astype(float)
    return passes.reset_index(drop=True)


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


def find_match_date(matches, match_id):
    """get_team_matches() の結果の表から、match_id の試合の日付(文字列)を返す。"""
    row = matches[matches["match_id"] == match_id]
    if len(row) == 0:
        raise ValueError(f"match_id {match_id} is not in the matches table")
    return str(row["match_date"].iloc[0])
