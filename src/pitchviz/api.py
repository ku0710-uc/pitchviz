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
    others = [t for t in teams if t != team_name]
    return others[0]


def list_players(events, team_name):
    """そのチームの選手名(イベントに登場した人)を、アルファベット順のリストで返す。"""
    rows = events[events["team"] == team_name]
    return sorted(rows["player"].dropna().unique())


def _select_player(table, events, team_name, player_name, what):
    """player_name が None ならそのまま返す。指定があれば、その選手の行だけにして返す。"""
    if player_name is None:
        return table
    selected = table[table["player"] == player_name]
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
