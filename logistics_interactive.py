"""
logistics_interactive.py — Interactive cobweb diagram for the logistics map.

Uses matplotlib widgets (sliders) to explore x_{n+1} = r * x_n * (1 - x_n).

Controls:
  - r (coarse): 2.5 to 4.0, quantized to hundredths
  - r (fine):  -0.01 to +0.01, quantized to ten-thousandths
  - x0 (seed): 0.01 to 0.99

The effective r = coarse + fine.

Usage:
    python logistics_interactive.py

Requires a display (X11 forwarding or native). If running in WSL, ensure
an X server is available or use `export DISPLAY=:0` or similar.
"""

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- Configuration ---
N_ITERATIONS = 80  # number of cobweb iterations to draw
R_COARSE_MIN, R_COARSE_MAX = 0.0, 4.0
R_COARSE_INIT = 3.2
R_FINE_MIN, R_FINE_MAX = -0.01, 0.01
R_FINE_INIT = 0.0
X0_MIN, X0_MAX = 0.01, 0.99
X0_INIT = 0.2


def logistics(x, r):
    return r * x * (1 - x)


def compute_cobweb(r, x0, n_iter):
    """Compute cobweb path: pairs of (x, y) for vertical and horizontal segments."""
    xs = [x0, x0]
    ys = [0, logistics(x0, r)]
    x = x0
    for _ in range(n_iter):
        y = logistics(x, r)
        # Vertical: (x, x) to (x, f(x))  [already have (x, f(x)) from prev]
        # Horizontal: (x, f(x)) to (f(x), f(x))
        xs.append(y)
        ys.append(y)
        # Vertical: (f(x), f(x)) to (f(x), f(f(x)))
        x = y
        y2 = logistics(x, r)
        xs.append(x)
        ys.append(y2)
    return xs, ys


# --- Set up figure ---
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.32)

# Initial plot
r_init = R_COARSE_INIT + R_FINE_INIT
x_line = np.linspace(0, 1, 500)
y_parabola = logistics(x_line, r_init)

line_parabola, = ax.plot(x_line, y_parabola, 'b-', linewidth=2, label=f'f(x) = r·x·(1−x)')
line_diag, = ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='y = x')

cobweb_xs, cobweb_ys = compute_cobweb(r_init, X0_INIT, N_ITERATIONS)
line_cobweb, = ax.plot(cobweb_xs, cobweb_ys, 'r-', linewidth=0.6, alpha=0.7)
dot_start, = ax.plot(X0_INIT, 0, 'go', markersize=8, zorder=5)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_xlabel('$x_n$')
ax.set_ylabel('$x_{n+1}$')
ax.grid(True, alpha=0.2)
title = ax.set_title(f'Cobweb — r = {r_init:.4f}, x₀ = {X0_INIT:.3f}', fontsize=12)

# --- Sliders ---
ax_r_coarse = plt.axes([0.15, 0.19, 0.70, 0.03])
ax_r_fine = plt.axes([0.15, 0.14, 0.70, 0.03])
ax_x0 = plt.axes([0.15, 0.09, 0.70, 0.03])
ax_niter = plt.axes([0.15, 0.04, 0.70, 0.03])

slider_r_coarse = Slider(ax_r_coarse, 'r (coarse)', R_COARSE_MIN, R_COARSE_MAX,
                          valinit=R_COARSE_INIT, valstep=0.01)
slider_r_fine = Slider(ax_r_fine, 'r (fine)', R_FINE_MIN, R_FINE_MAX,
                        valinit=R_FINE_INIT, valstep=0.0001)
slider_x0 = Slider(ax_x0, 'x₀ (seed)', X0_MIN, X0_MAX,
                    valinit=X0_INIT, valstep=0.01)
slider_niter = Slider(ax_niter, 'iterations', 0, 400,
                       valinit=N_ITERATIONS, valstep=1)


def update(val):
    r = slider_r_coarse.val + slider_r_fine.val
    x0 = slider_x0.val
    n_iter = int(slider_niter.val)

    # Update parabola
    y_new = logistics(x_line, r)
    line_parabola.set_ydata(y_new)

    # Update cobweb
    xs, ys = compute_cobweb(r, x0, n_iter)
    line_cobweb.set_data(xs, ys)

    # Update start dot
    dot_start.set_data([x0], [0])

    # Update title
    title.set_text(f'Cobweb — r = {r:.4f}, x₀ = {x0:.3f}')

    fig.canvas.draw_idle()


slider_r_coarse.on_changed(update)
slider_r_fine.on_changed(update)
slider_x0.on_changed(update)
slider_niter.on_changed(update)

plt.show()
