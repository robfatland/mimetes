"""
resnet_diagram.py — Visual diagram of ResNet-18 fine-tuning architecture.

Output:
    images/resnet_architecture.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)


def draw_architecture():
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-1.2, 3.5)
    ax.axis('off')

    # --- Input image (far left) ---
    img_rect = mpatches.FancyBboxPatch((0, 0.5), 1.6, 2.0,
                                        boxstyle="round,pad=0.05",
                                        facecolor='lightyellow',
                                        edgecolor='black', linewidth=1.5)
    ax.add_patch(img_rect)

    # Check if cheshire cat image exists, otherwise use text
    cat_path = OUTPUT_DIR / "cheshire_cat.png"
    if cat_path.exists():
        img = plt.imread(str(cat_path))
        ax.imshow(img, extent=[0.1, 1.5, 0.7, 2.3], aspect='auto', zorder=5)
    else:
        ax.text(0.8, 1.5, 'cat?', fontsize=14, ha='center', va='center',
                color='purple', weight='bold')

    ax.text(0.8, 0.25, '32x32x3', fontsize=9, ha='center')
    ax.text(0.8, -0.05, 'Input', fontsize=10, ha='center', style='italic')

    # --- Arrow to backbone ---
    ax.annotate('', xy=(2.2, 1.5), xytext=(1.8, 1.5),
                arrowprops=dict(arrowstyle='->', lw=2))

    # --- Frozen Backbone (compact block) ---
    backbone = mpatches.FancyBboxPatch((2.0, 0.4), 4.5, 2.2,
                                        boxstyle="round,pad=0.1",
                                        facecolor='lightblue',
                                        edgecolor='steelblue', linewidth=2.5)
    ax.add_patch(backbone)

    # Represent 17 layers as stacked thin rectangles
    for i in range(17):
        x = 2.3 + i * 0.24
        shade = 0.4 + 0.6 * (i / 16)  # gradient from light to dark
        rect = mpatches.Rectangle((x, 0.8), 0.18, 1.4,
                                   facecolor=(0.2, 0.4, shade),
                                   edgecolor='none', alpha=0.6)
        ax.add_patch(rect)

    ax.text(4.25, 2.85, 'FROZEN BACKBONE', fontsize=11,
            ha='center', weight='bold', color='steelblue')
    ax.text(4.25, -0.15, '17 conv layers, 11.17M params (unchanged)',
            fontsize=10, ha='center', color='steelblue')

    # --- Arrow backbone to head ---
    ax.annotate('', xy=(7.1, 1.5), xytext=(6.7, 1.5),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='darkred'))
    ax.text(6.9, 1.9, '512', fontsize=10, ha='center', color='gray')

    # --- Trainable Head (graph with 32 blue dots → 6 red dots) ---
    head = mpatches.FancyBboxPatch((7.2, 0.3), 3.0, 2.4,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightyellow',
                                    edgecolor='darkred', linewidth=2.5)
    ax.add_patch(head)

    # 32 blue input dots (4 columns of 8) — shifted left
    in_dots_x = [7.4, 7.7, 8.0, 8.3]
    in_dots_y = np.linspace(0.6, 2.4, 8)
    all_in = []
    for ix in in_dots_x:
        for iy in in_dots_y:
            ax.plot(ix, iy, 'o', color='steelblue', markersize=3)
            all_in.append((ix, iy))

    # Label under LHS dots
    ax.text(7.85, 0.4, '512', fontsize=9, ha='center', color='steelblue')

    # 6 red output dots
    out_x = 9.7
    out_ys = np.linspace(0.8, 2.2, 6)
    for oy in out_ys:
        ax.plot(out_x, oy, 'o', color='darkred', markersize=5)

    # Label under RHS dots
    ax.text(out_x, 0.4, '10', fontsize=9, ha='center', color='darkred')

    # Draw some connection lines (not all — too dense)
    for i in range(0, len(all_in), 4):
        for oy in out_ys:
            ax.plot([all_in[i][0], out_x], [all_in[i][1], oy],
                    '-', color='darkred', linewidth=0.2, alpha=0.3)

    ax.text(8.7, 2.95, 'TRAINABLE HEAD', fontsize=11,
            ha='center', weight='bold', color='darkred')
    ax.text(8.7, -0.15, '(5120 + 10 params)', fontsize=9,
            ha='center', color='darkred')

    # --- Arrow to output ---
    ax.annotate('', xy=(10.8, 1.5), xytext=(10.4, 1.5),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='darkgreen'))

    # --- Output (narrower) ---
    output = mpatches.FancyBboxPatch((10.9, 0.2), 2.0, 2.6,
                                      boxstyle="round,pad=0.1",
                                      facecolor='honeydew',
                                      edgecolor='darkgreen', linewidth=2)
    ax.add_patch(output)

    classes = ['airplane', 'auto', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']
    scores = [0.02, 0.01, 0.05, 0.82, 0.01, 0.03, 0.01, 0.02, 0.01, 0.02]

    for i, (cls, score) in enumerate(zip(classes, scores)):
        y = 2.5 - i * 0.24
        bar_width = score * 1.0
        color = 'darkgreen' if score > 0.5 else 'lightgray'
        ax.barh(y, bar_width, height=0.17, left=11.6, color=color, alpha=0.7)
        ax.text(11.55, y, cls, fontsize=7, ha='right', va='center')
        if score > 0.1:
            ax.text(11.65 + bar_width, y, f'{score:.0%}', fontsize=7,
                    va='center', color='darkgreen', weight='bold')

    ax.text(11.9, -0.15, 'argmax = "cat"', fontsize=10,
            ha='center', weight='bold', color='darkgreen')

    # Title
    ax.text(7.0, 3.4, 'ResNet-18 Fine-Tuning: Frozen Backbone + Trainable Head',
            fontsize=13, ha='center', weight='bold')

    plt.tight_layout()
    out_path = OUTPUT_DIR / "resnet_architecture.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    draw_architecture()
