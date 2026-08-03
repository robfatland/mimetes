"""
detector_viz.py — From cosine correlation to the phase-insensitive complex detector.

Four stages building toward the DFT's key property: |X[k]| is immune to time shifts.

Stage 1: Cosine detector — single inner product selects frequency
Stage 2: Phase failure — cosine detector misses phase-shifted signals
Stage 3: Cos + sin together — two projections catch all phases
Stage 4: Complex exponential — one operation, magnitude is phase-invariant

Output:
    images/detector_stage1_frequency.png
    images/detector_stage2_phase_failure.png
    images/detector_stage3_quadrature.png
    images/detector_stage4_complex.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

N = 64  # signal length
n = np.arange(N)
K_DETECT = 5  # the frequency we're detecting


def stage1_frequency():
    """
    Stage 1: Cosine detector selects its own frequency.
    Reference: cos(2π·5·n/N)
    Signals: A) same frequency same phase, B) same freq half amplitude,
             C) different frequency (k=3)
    """
    ref = np.cos(2 * np.pi * K_DETECT * n / N)

    signals = [
        ("Same frequency (k=5), amplitude=1", 1.0 * np.cos(2 * np.pi * 5 * n / N)),
        ("Same frequency (k=5), amplitude=0.5", 0.5 * np.cos(2 * np.pi * 5 * n / N)),
        ("Different frequency (k=3)", 1.0 * np.cos(2 * np.pi * 3 * n / N)),
    ]

    fig, axes = plt.subplots(len(signals), 3, figsize=(14, 8))

    for row, (label, signal) in enumerate(signals):
        product = ref * signal
        ip = np.dot(ref, signal)

        # Reference
        ax = axes[row, 0]
        ax.plot(n, ref, 'steelblue', linewidth=1.5)
        ax.fill_between(n, ref, alpha=0.15, color='steelblue')
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, N - 1)
        if row == 0:
            ax.set_title('Reference: cos(2π·5·n/N)', fontsize=10, weight='bold')
        ax.set_ylabel(label, fontsize=8, rotation=0, labelpad=120, va='center')

        # Signal
        ax = axes[row, 1]
        ax.plot(n, signal, 'darkorange', linewidth=1.5)
        ax.fill_between(n, signal, alpha=0.15, color='darkorange')
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, N - 1)
        if row == 0:
            ax.set_title('Signal', fontsize=10, weight='bold')

        # Product + inner product
        ax = axes[row, 2]
        ax.plot(n, product, 'green', linewidth=1.5)
        ax.fill_between(n, product, alpha=0.2, color='green')
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, N - 1)
        if row == 0:
            ax.set_title('Product (sum = inner product)', fontsize=10, weight='bold')
        ax.text(0.95, 0.85, f'⟨ref, sig⟩ = {ip:.1f}',
                transform=ax.transAxes, fontsize=10, weight='bold',
                ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                          edgecolor='gray'))

    fig.suptitle('Stage 1: A cosine detector selects its frequency\n'
                 'No scanning needed — one inner product covers the full signal',
                 fontsize=12, weight='bold')
    plt.tight_layout()
    out = OUTPUT_DIR / "detector_stage1_frequency.png"
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out}")
    plt.close()


def stage2_phase_failure():
    """
    Stage 2: Cosine detector fails when signal is phase-shifted.
    Reference: cos(2π·5·n/N)
    Signal: cos(2π·5·n/N + φ) for φ = 0, π/4, π/2, 3π/4, π
    """
    ref = np.cos(2 * np.pi * K_DETECT * n / N)

    phases = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
    phase_labels = ['0', 'π/4', 'π/2', '3π/4', 'π']

    fig, axes = plt.subplots(len(phases), 3, figsize=(14, 11))

    for row, (phi, phi_label) in enumerate(zip(phases, phase_labels)):
        signal = np.cos(2 * np.pi * K_DETECT * n / N + phi)
        product = ref * signal
        ip = np.dot(ref, signal)

        # Reference
        ax = axes[row, 0]
        ax.plot(n, ref, 'steelblue', linewidth=1.5)
        ax.fill_between(n, ref, alpha=0.15, color='steelblue')
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, N - 1)
        if row == 0:
            ax.set_title('Reference: cos', fontsize=10, weight='bold')
        ax.set_ylabel(f'φ = {phi_label}', fontsize=10, weight='bold',
                      rotation=0, labelpad=45, va='center')

        # Signal
        ax = axes[row, 1]
        ax.plot(n, signal, 'darkorange', linewidth=1.5)
        ax.fill_between(n, signal, alpha=0.15, color='darkorange')
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, N - 1)
        if row == 0:
            ax.set_title('Signal: cos(... + φ)', fontsize=10, weight='bold')

        # Product
        ax = axes[row, 2]
        ax.plot(n, product, 'green', linewidth=1.5)
        ax.fill_between(n, product, alpha=0.2, color='green')
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(0, N - 1)
        if row == 0:
            ax.set_title('Product', fontsize=10, weight='bold')

        color = 'darkgreen' if abs(ip) > 1 else ('darkred' if abs(ip) < 1 else 'gray')
        ax.text(0.95, 0.85, f'⟨ref, sig⟩ = {ip:.1f}',
                transform=ax.transAxes, fontsize=10, weight='bold',
                ha='right', va='top', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                          edgecolor='gray'))

    fig.suptitle('Stage 2: Phase failure — the cosine detector is blind to phase shifts\n'
                 'Same frequency present in all signals, but inner product drops to zero at φ=π/2',
                 fontsize=12, weight='bold')
    plt.tight_layout()
    out = OUTPUT_DIR / "detector_stage2_phase_failure.png"
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out}")
    plt.close()


def stage3_quadrature():
    """
    Stage 3: Using both cos and sin (quadrature pair) catches all phases.
    For each phase shift, compute both projections and show that
    sqrt(cos_proj² + sin_proj²) is constant.
    """
    ref_cos = np.cos(2 * np.pi * K_DETECT * n / N)
    ref_sin = -np.sin(2 * np.pi * K_DETECT * n / N)  # negative sine matches DFT convention

    phases = np.linspace(0, 2 * np.pi, 13)  # 0 to 2π in steps
    cos_projections = []
    sin_projections = []
    magnitudes = []

    for phi in phases:
        signal = np.cos(2 * np.pi * K_DETECT * n / N + phi)
        cp = np.dot(ref_cos, signal)
        sp = np.dot(ref_sin, signal)
        cos_projections.append(cp)
        sin_projections.append(sp)
        magnitudes.append(np.sqrt(cp**2 + sp**2))

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Top: cos and sin projections vary with phase
    ax = axes[0]
    phase_deg = np.degrees(phases)
    ax.plot(phase_deg, cos_projections, 'steelblue', linewidth=2,
            marker='o', markersize=5, label='cos projection')
    ax.plot(phase_deg, sin_projections, 'darkorange', linewidth=2,
            marker='s', markersize=5, label='sin projection')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_xlabel('Phase shift φ (degrees)', fontsize=10)
    ax.set_ylabel('Inner product value', fontsize=10)
    ax.set_title('Individual projections vary with phase', fontsize=11, weight='bold')
    ax.legend(fontsize=10)
    ax.set_xlim(0, 360)
    ax.grid(True, alpha=0.3)

    # Bottom: magnitude is constant
    ax = axes[1]
    ax.plot(phase_deg, magnitudes, 'green', linewidth=2.5,
            marker='D', markersize=6)
    ax.axhline(magnitudes[0], color='green', linewidth=1, linestyle='--', alpha=0.5)
    ax.set_xlabel('Phase shift φ (degrees)', fontsize=10)
    ax.set_ylabel('Magnitude √(cos² + sin²)', fontsize=10)
    ax.set_title('Combined magnitude is CONSTANT — phase-insensitive!',
                 fontsize=11, weight='bold', color='darkgreen')
    ax.set_xlim(0, 360)
    ax.set_ylim(0, magnitudes[0] * 1.3)
    ax.grid(True, alpha=0.3)
    ax.text(0.5, 0.3, f'Constant value = {magnitudes[0]:.1f} = N/2 = {N}/2',
            transform=ax.transAxes, fontsize=11, ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='honeydew',
                      edgecolor='green'))

    fig.suptitle('Stage 3: Cos + Sin together → phase-insensitive magnitude\n'
                 'Two detectors (π/2 apart) catch all orientations of the signal',
                 fontsize=12, weight='bold')
    plt.tight_layout()
    out = OUTPUT_DIR / "detector_stage3_quadrature.png"
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out}")
    plt.close()


def stage4_complex():
    """
    Stage 4: The complex exponential e^{-2πikn/N} = cos - i·sin does both at once.
    Show that |X[k]| is invariant under time shifts of the signal.
    """
    # Complex detector (row k of DFT)
    detector = np.exp(-2j * np.pi * K_DETECT * n / N)

    # Signal at various time shifts (integer shifts)
    shifts = np.arange(0, N, 4)  # shift by 0, 4, 8, ..., N-4 samples
    magnitudes = []
    phases_out = []

    base_signal = np.cos(2 * np.pi * K_DETECT * n / N)  # pure cosine at freq k

    for shift in shifts:
        # Circular shift
        shifted = np.roll(base_signal, shift)
        # Complex inner product
        X_k = np.dot(detector, shifted)
        magnitudes.append(np.abs(X_k))
        phases_out.append(np.angle(X_k))

    fig, axes = plt.subplots(3, 1, figsize=(12, 9))

    # Top: example shifted signals
    ax = axes[0]
    for i, shift in enumerate([0, 3, 7, 11]):
        shifted = np.roll(base_signal, shift)
        alpha = 0.4 + 0.15 * i
        ax.plot(n, shifted, linewidth=1.2, alpha=alpha,
                label=f'shift={shift}')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_xlim(0, N - 1)
    ax.set_ylim(-1.4, 1.4)
    ax.set_title('Signal: cos(2π·5·n/N) at various time shifts', fontsize=11,
                 weight='bold')
    ax.legend(fontsize=9, ncol=4, loc='upper right')
    ax.set_ylabel('Amplitude', fontsize=10)

    # Middle: |X[k]| is constant
    ax = axes[1]
    ax.plot(shifts, magnitudes, 'green', linewidth=2.5, marker='D', markersize=5)
    ax.axhline(magnitudes[0], color='green', linewidth=1, linestyle='--', alpha=0.5)
    ax.set_xlabel('Time shift (samples)', fontsize=10)
    ax.set_ylabel('|X[k]|', fontsize=10)
    ax.set_title('|X[k]| is CONSTANT regardless of time shift',
                 fontsize=11, weight='bold', color='darkgreen')
    ax.set_xlim(0, shifts[-1])
    ax.set_ylim(0, magnitudes[0] * 1.4)
    ax.grid(True, alpha=0.3)

    # Bottom: phase rotates linearly with shift
    ax = axes[2]
    ax.plot(shifts, np.degrees(phases_out), 'purple', linewidth=2,
            marker='o', markersize=5)
    ax.set_xlabel('Time shift (samples)', fontsize=10)
    ax.set_ylabel('arg(X[k]) (degrees)', fontsize=10)
    ax.set_title('Phase rotates linearly — time shift becomes phase shift',
                 fontsize=11, weight='bold', color='purple')
    ax.set_xlim(0, shifts[-1])
    ax.grid(True, alpha=0.3)

    fig.suptitle('Stage 4: Complex detector e$^{-2πikn/N}$ — magnitude is time-shift invariant\n'
                 'A time shift in the signal becomes a phase rotation in X[k], but |X[k]| stays the same',
                 fontsize=12, weight='bold')
    plt.tight_layout()
    out = OUTPUT_DIR / "detector_stage4_complex.png"
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out}")
    plt.close()


if __name__ == "__main__":
    stage1_frequency()
    stage2_phase_failure()
    stage3_quadrature()
    stage4_complex()
