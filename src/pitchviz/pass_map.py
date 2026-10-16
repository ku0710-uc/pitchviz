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

def make_filename(team_name, opponent_name, prefix="pass_map"):
    """例: ("Japan", "Belgium") -> "pass_map_japan_belgium.png" """
    names = [prefix, team_name, opponent_name]
    parts = []
    for name in names:
        name = name.lower().replace("'", "")
        name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
        parts.append(name)
    return "_".join(parts) + ".png"
