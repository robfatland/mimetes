"""
dft_kernel_viz.py — Visualize the DFT kernel e^{-2πi k n / N} as unit circle diagrams.

For each dimension N, produces an N×N grid of unit circle subplots.
Row k, column n shows the kernel value e^{-2πi k n / N} as a dot on the unit circle
with a phasor line from the origin.

Outputs:
    images/dft_kernel_N1_to_N7.png   — stacked vertically, N=1 through N=7
    images/dft_kernel_N19.png        — separate figure for N=19
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)


def draw_kernel_grid(N, axes_grid):
    """
    Draw an N×N grid of unit circle diagrams for DFT dimension N.
    axes_grid: 2D array of matplotlib axes, shape (N, N)
    """
    for k in range(N):
        for n in range(N):
            ax = axes_grid[k, n] if N > 1 else axes_grid

            # Unit circle
            theta = np.linspace(0, 2 * np.pi, 100)
            ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=0.5, alpha=0.4)

            # Axes (the "plus")
            ax.axhline(0, color='gray', linewidth=0.3)
            ax.axvline(0, color='gray', linewidth=0.3)

            # Kernel value: e^{-2πi k n / N}
            angle = -2 * np.pi * k * n / N
            x = np.cos(angle)
            y = np.sin(angle)

            # Phasor line (no arrowhead) + dot
            ax.plot([0, x], [0, y], 'b-', linewidth=1.0, alpha=0.7)
            ax.plot(x, y, 'bo', markersize=4)

            # Formatting
            ax.set_xlim(-1.4, 1.4)
            ax.set_ylim(-1.4, 1.4)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])

            # Label top row and left column
            if k == 0:
                ax.set_title(f'n={n}', fontsize=7, pad=2)
            if n == 0:
                ax.set_ylabel(f'k={k}', fontsize=7, rotation=0, labelpad=15,
                              va='center')


def make_stacked_figure(N_values, filename):
    """
    Create a vertically stacked figure with one N×N kernel grid per N value.
    """
    # Calculate total height needed
    cell_size = 0.6  # inches per subplot cell
    gap = 0.8  # inches between N blocks
    total_rows = sum(N_values)
    fig_width = max(N_values) * cell_size + 2.0
    fig_height = total_rows * cell_size + len(N_values) * gap + 1.0

    fig = plt.figure(figsize=(fig_width, fig_height))

    # Track vertical position
    current_bottom = 1.0 - 0.02  # start near top (in figure coords)

    for N in N_values:
        block_height = N * cell_size / fig_height
        block_width = N * cell_size / fig_width
        left = 0.15
        bottom = current_bottom - block_height

        # Create subplot grid for this N
        axes = []
        for k in range(N):
            row_axes = []
            for n in range(N):
                ax_left = left + n * (block_width / N)
                ax_bottom = bottom + (N - 1 - k) * (block_height / N)
                ax_w = block_width / N * 0.9
                ax_h = block_height / N * 0.9
                ax = fig.add_axes([ax_left, ax_bottom, ax_w, ax_h])
                row_axes.append(ax)
            axes.append(row_axes)

        axes = np.array(axes)

        # Draw the kernel grid
        if N == 1:
            draw_kernel_grid(N, axes[0, 0])
        else:
            draw_kernel_grid(N, axes)

        # Label this block
        fig.text(left - 0.08, bottom + block_height / 2,
                 f'N={N}', fontsize=11, weight='bold', rotation=90,
                 va='center', ha='center')

        current_bottom = bottom - gap / fig_height

    fig.suptitle('DFT Kernel: $e^{-2\\pi i \\, k \\, n \\,/\\, N}$',
                 fontsize=14, weight='bold', y=0.995)

    out_path = OUTPUT_DIR / filename
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out_path}")
    plt.close()


def make_single_figure(N, filename):
    """
    Create a standalone N×N kernel grid figure for a single N value.
    """
    cell_size = 0.55
    fig_size = N * cell_size + 1.5

    fig, axes = plt.subplots(N, N, figsize=(fig_size, fig_size))
    if N == 1:
        axes = np.array([[axes]])

    draw_kernel_grid(N, axes)

    fig.suptitle(f'DFT Kernel (N={N}): $e^{{-2\\pi i \\, k \\, n \\,/\\, {N}}}$',
                 fontsize=12, weight='bold')
    plt.tight_layout()

    out_path = OUTPUT_DIR / filename
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out_path}")
    plt.close()


def make_paired_figure(N, filename):
    """
    Create an N×N kernel grid with rows reordered to show conjugate pairs.
    For N=14: k=0, k=7 (Nyquist), then pairs (1,13), (2,12), (3,11), (4,10), (5,9), (6,8).
    Pairs are visually emphasized with alternating background shading.
    """
    # Build the k ordering: DC, Nyquist, then pairs
    k_order = [0, N // 2]  # DC and Nyquist
    for j in range(1, N // 2):
        k_order.append(j)
        k_order.append(N - j)

    cell_size = 0.55
    fig_width = N * cell_size + 2.0
    fig_height = N * cell_size + 2.5

    fig, axes = plt.subplots(N, N, figsize=(fig_width, fig_height))

    # Pair coloring: row index in the reordered layout
    # Rows 0,1 are DC and Nyquist (no pair shading)
    # Rows 2-3 are pair 1, rows 4-5 are pair 2, etc.
    pair_colors = ['#e8f4fd', '#fff8e1']  # light blue, light yellow alternating

    for row_idx, k in enumerate(k_order):
        # Determine background color for pairing emphasis
        if row_idx >= 2:
            pair_num = (row_idx - 2) // 2
            bg_color = pair_colors[pair_num % 2]
        else:
            bg_color = '#f0f0f0'  # gray for DC and Nyquist

        for n in range(N):
            ax = axes[row_idx, n]

            # Background shading for pair emphasis
            ax.set_facecolor(bg_color)

            # Unit circle
            theta = np.linspace(0, 2 * np.pi, 100)
            ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=0.5, alpha=0.4)

            # Axes (the "plus")
            ax.axhline(0, color='gray', linewidth=0.3)
            ax.axvline(0, color='gray', linewidth=0.3)

            # Kernel value: e^{-2πi k n / N}
            angle = -2 * np.pi * k * n / N
            x = np.cos(angle)
            y = np.sin(angle)

            # Phasor line + dot
            ax.plot([0, x], [0, y], 'b-', linewidth=1.0, alpha=0.7)
            ax.plot(x, y, 'bo', markersize=3.5)

            # Formatting
            ax.set_xlim(-1.4, 1.4)
            ax.set_ylim(-1.4, 1.4)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])

            # Column labels on top row
            if row_idx == 0:
                ax.set_title(f'n={n}', fontsize=6, pad=2)

        # Row label: k value
        axes[row_idx, 0].set_ylabel(f'k={k}', fontsize=7, rotation=0,
                                     labelpad=15, va='center')

    # Title with notice about non-standard ordering
    fig.suptitle(
        f'DFT Kernel (N={N}): $e^{{-2\\pi i \\, k \\, n \\,/\\, {N}}}$\n'
        r'$\mathbf{NOTE:}$ Rows reordered to show conjugate pairs'
        ' — k and N\u2212k rotate in opposite directions',
        fontsize=10, weight='bold', y=1.02
    )

    plt.tight_layout()

    out_path = OUTPUT_DIR / filename
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    # Stacked figure: N=1 through N=7
    make_stacked_figure([1, 2, 3, 4, 5, 6, 7], "dft_kernel_N1_to_N7.png")

    # Paired conjugate figure: N=14
    make_paired_figure(14, "dft_kernel_N14_paired.png")
