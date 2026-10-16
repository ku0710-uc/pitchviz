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
        "shots": len(shots),
        "goals": int(shots["is_goal"].sum()),
        "xg": float(shots["xg"].sum()),
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
