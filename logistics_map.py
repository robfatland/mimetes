"""
logistics_map.py — Generate a bifurcation diagram and a cobweb (spiderweb) diagram
for the logistics map x_{n+1} = r * x_n * (1 - x_n).

Output:
    images/logistics_bifurcation.png
    images/logistics_cobweb.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for WSL (no display needed)
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)


def bifurcation_diagram():
    """Generate the classic bifurcation diagram: x_steady vs r."""
    r_values = np.linspace(2.5, 4.0, 2000)
    iterations = 1000   # total iterations per r
    last = 300          # plot only the last N (steady state or attractor)

    fig, ax = plt.subplots(figsize=(14.4, 8.4))

    for r in r_values:
        x = 0.5  # initial condition
        # Iterate to reach attractor
        for _ in range(iterations - last):
            x = r * x * (1 - x)
        # Collect attractor values
        xs = []
        for _ in range(last):
            x = r * x * (1 - x)
            xs.append(x)
        ax.plot([r] * last, xs, ',', color='black', markersize=0.2)

    # Annotate regimes
    ax.axvline(3.0, color='blue', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.axvline(3.449, color='orange', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.axvline(3.57, color='red', alpha=0.3, linestyle='--', linewidth=0.8)

    ax.text(2.75, 0.95, 'stable\nfixed point', fontsize=9, color='blue', ha='center')
    ax.text(3.22, 0.95, 'period\n2', fontsize=9, color='orange', ha='center')
    ax.text(3.51, 0.95, 'period\ndoubling', fontsize=9, color='red', ha='center')
    ax.text(3.78, 0.95, 'chaos', fontsize=9, color='darkred', ha='center')

    ax.set_xlabel('r (growth rate parameter)')
    ax.set_ylabel('x (steady-state values)')
    ax.set_title('Logistics Map Bifurcation Diagram\n'
                 r'$x_{n+1} = r \cdot x_n \cdot (1 - x_n)$')
    ax.set_xlim(2.5, 4.0)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "logistics_bifurcation.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    plt.close()


def cobweb_diagram(r=3.2, x0=0.2, n_steps=50, filename=None):
    """
    Generate a cobweb (spiderweb) diagram showing iteration of the logistics map.
    Shows convergence (or oscillation/chaos) by bouncing between f(x) and y=x.
    """
    fig, ax = plt.subplots(figsize=(9.6, 9.6))

    # Plot f(x) = r*x*(1-x)
    x_line = np.linspace(0, 1, 500)
    y_line = r * x_line * (1 - x_line)
    ax.plot(x_line, y_line, 'b-', linewidth=2, label=f'f(x) = {r}·x·(1−x)')
    ax.plot(x_line, x_line, 'k--', linewidth=1, label='y = x')

    # Cobweb iteration
    x = x0
    for i in range(n_steps):
        y = r * x * (1 - x)
        # Vertical line from (x, x) to (x, f(x))
        ax.plot([x, x], [x, y], 'r-', linewidth=0.7, alpha=0.7)
        # Horizontal line from (x, f(x)) to (f(x), f(x))
        ax.plot([x, y], [y, y], 'r-', linewidth=0.7, alpha=0.7)
        x = y

    ax.set_xlabel('x_n')
    ax.set_ylabel('x_{n+1}')
    ax.set_title(f'Cobweb Diagram — Logistics Map (r={r}, x₀={x0})\n'
                 'Red lines trace the iteration path')
    ax.legend(loc='upper left')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    fname = filename or f"logistics_cobweb_r{r:.1f}.png"
    out_path = OUTPUT_DIR / fname
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    bifurcation_diagram()
    cobweb_diagram(r=2.8, x0=0.1, n_steps=30)   # converges to fixed point
    cobweb_diagram(r=3.2, x0=0.1, n_steps=50)   # period-2 oscillation
    cobweb_diagram(r=3.5, x0=0.1, n_steps=50)   # period-4
    cobweb_diagram(r=3.9, x0=0.1, n_steps=80)   # chaos
