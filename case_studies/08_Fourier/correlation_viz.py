"""
correlation_viz.py — Illustrate correlation of a reference function with a signal.

Uses a sphinx-like shape (inspired by the rep-tile sphinx decomposition) as the
reference, embedded in a mostly-zero vector of length N=42. The sphinx profile
is [0, 1, 1, 2, 1, 1, 0] — a stepped bump with a peak, vaguely evoking the
stepped silhouette of the hexagonal sphinx tile.

Shows three cases:
  1. No overlap: signal sphinx is far from reference sphinx → inner product ≈ 0
  2. Partial overlap: signal sphinx partially overlaps reference → moderate inner product
  3. Precise overlap: signal sphinx aligns exactly with reference → maximum inner product

Output:
    images/correlation_sphinx.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

N = 42

# Sphinx profile: a stepped bump inspired by the sphinx rep-tile silhouette
SPHINX = np.array([0, 1, 1, 1, 2, 1, 0], dtype=float) / 3.0
SPHINX_LEN = len(SPHINX)


def embed_sphinx(position):
    """
    Embed the sphinx shape into a zero vector of length N, starting at `position`.
    """
    vec = np.zeros(N)
    start = position
    end = min(start + SPHINX_LEN, N)
    actual_len = end - start
    vec[start:end] = SPHINX[:actual_len]
    return vec


def compute_inner_product(ref, sig):
    """Compute the inner product (correlation at zero lag)."""
    return np.dot(ref, sig)


def plot_correlation_cases():
    """
    Three-row figure showing no overlap, partial overlap, and precise overlap.
    Each row has 3 panels: reference, signal, element-wise product.
    All plots use continuous lines (not bar charts).
    """
    ref_start = 17  # center the sphinx in the reference vector
    reference = embed_sphinx(ref_start)

    # Three signal cases
    cases = [
        ("No overlap", embed_sphinx(3)),                  # far left
        ("Partial overlap", embed_sphinx(13)),            # shifted, partial overlap
        ("Precise overlap", embed_sphinx(ref_start)),     # exact match
    ]

    fig, axes = plt.subplots(3, 3, figsize=(14, 8))

    for row, (label, signal) in enumerate(cases):
        product = reference * signal
        ip = compute_inner_product(reference, signal)
        x = np.arange(N)

        # Reference
        ax_ref = axes[row, 0]
        ax_ref.plot(x, reference, 'steelblue', linewidth=1.8)
        ax_ref.fill_between(x, reference, alpha=0.2, color='steelblue')
        ax_ref.set_ylim(-0.3, 2.5)
        ax_ref.set_xlim(-1, N)
        if row == 0:
            ax_ref.set_title('Reference', fontsize=11, weight='bold')
        ax_ref.set_ylabel(label, fontsize=10, weight='bold', rotation=0,
                          labelpad=80, va='center')
        ax_ref.axhline(0, color='gray', linewidth=0.5)

        # Signal
        ax_sig = axes[row, 1]
        ax_sig.plot(x, signal, 'darkorange', linewidth=1.8)
        ax_sig.fill_between(x, signal, alpha=0.2, color='darkorange')
        ax_sig.set_ylim(-0.3, 2.5)
        ax_sig.set_xlim(-1, N)
        if row == 0:
            ax_sig.set_title('Signal', fontsize=11, weight='bold')
        ax_sig.axhline(0, color='gray', linewidth=0.5)

        # Element-wise product
        ax_prod = axes[row, 2]
        ax_prod.plot(x, product, 'green', linewidth=1.8)
        ax_prod.fill_between(x, product, alpha=0.25, color='green')
        ax_prod.set_ylim(-0.3, 4.5)
        ax_prod.set_xlim(-1, N)
        if row == 0:
            ax_prod.set_title('Element-wise Product', fontsize=11, weight='bold')
        ax_prod.axhline(0, color='gray', linewidth=0.5)

        # Annotate with inner product value
        ax_prod.text(0.95, 0.85, f'Inner product = {ip:.1f}',
                     transform=ax_prod.transAxes, fontsize=11, weight='bold',
                     ha='right', va='top',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                               edgecolor='gray'))

    fig.suptitle('Correlation as Inner Product: Sphinx Reference vs. Signal\n'
                 '(N=42, zero-lag dot product of aligned vectors)',
                 fontsize=13, weight='bold')
    plt.tight_layout()

    out_path = OUTPUT_DIR / "correlation_sphinx.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out_path}")
    plt.close()


def plot_scanning_correlation():
    """
    Scanning correlation: slide the sphinx reference across a signal containing
    three sphinxes at different positions and amplitudes (3, 5, 4).
    
    Top panel: the signal (three sphinxes superimposed on zeros).
    Middle panel: the unit-amplitude reference sphinx (shown at center).
    Bottom panel: the correlation sequence — inner product at each shift.
    Peaks appear at the exact positions of the three sphinxes.
    """
    # Use a longer signal for this demonstration
    M = 100  # signal length
    sphinx = SPHINX  # unit sphinx (already scaled by 1/3)

    # Build signal with three sphinxes at different positions and amplitudes
    signal = np.zeros(M)
    sphinx_placements = [(15, 3.0), (45, 5.0), (75, 4.0)]  # (position, amplitude)
    for pos, amp in sphinx_placements:
        end = min(pos + SPHINX_LEN, M)
        actual = end - pos
        signal[pos:end] += amp * sphinx[:actual]

    # Compute scanning correlation (cross-correlation, no wrapping)
    # At each shift s, compute dot product of sphinx with signal[s:s+SPHINX_LEN]
    n_shifts = M - SPHINX_LEN + 1
    correlation = np.zeros(n_shifts)
    for s in range(n_shifts):
        segment = signal[s:s + SPHINX_LEN]
        correlation[s] = np.dot(sphinx, segment)

    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=False)

    # Top: signal
    ax_sig = axes[0]
    x_sig = np.arange(M)
    ax_sig.plot(x_sig, signal, 'darkorange', linewidth=1.8)
    ax_sig.fill_between(x_sig, signal, alpha=0.2, color='darkorange')
    ax_sig.axhline(0, color='gray', linewidth=0.5)
    ax_sig.set_xlim(-1, M)
    ax_sig.set_ylabel('Amplitude', fontsize=10)
    ax_sig.set_title('Signal: three sphinxes (amplitudes 3, 5, 4)', fontsize=11,
                     weight='bold')
    # Mark sphinx positions
    for pos, amp in sphinx_placements:
        ax_sig.annotate(f'amp={amp:.0f}', xy=(pos + SPHINX_LEN // 2, amp * sphinx.max()),
                        xytext=(pos + SPHINX_LEN // 2, amp * sphinx.max() + 0.15),
                        fontsize=9, ha='center', color='darkred')

    # Middle: reference
    ax_ref = axes[1]
    ref_display = np.zeros(M)
    ref_pos = M // 2 - SPHINX_LEN // 2
    ref_display[ref_pos:ref_pos + SPHINX_LEN] = sphinx
    ax_ref.plot(x_sig, ref_display, 'steelblue', linewidth=1.8)
    ax_ref.fill_between(x_sig, ref_display, alpha=0.2, color='steelblue')
    ax_ref.axhline(0, color='gray', linewidth=0.5)
    ax_ref.set_xlim(-1, M)
    ax_ref.set_ylabel('Amplitude', fontsize=10)
    ax_ref.set_title('Reference: unit sphinx (slid across signal at every offset)',
                     fontsize=11, weight='bold')

    # Bottom: correlation sequence
    ax_corr = axes[2]
    x_corr = np.arange(n_shifts)
    ax_corr.plot(x_corr, correlation, 'green', linewidth=1.8)
    ax_corr.fill_between(x_corr, correlation, alpha=0.2, color='green')
    ax_corr.axhline(0, color='gray', linewidth=0.5)
    ax_corr.set_xlim(-1, M)
    ax_corr.set_xlabel('Shift position', fontsize=10)
    ax_corr.set_ylabel('Inner product', fontsize=10)
    ax_corr.set_title('Correlation sequence: inner product at each shift',
                      fontsize=11, weight='bold')
    # Mark peaks
    for pos, amp in sphinx_placements:
        if pos < n_shifts:
            ax_corr.annotate(f'{correlation[pos]:.2f}',
                             xy=(pos, correlation[pos]),
                             xytext=(pos, correlation[pos] + 0.02),
                             fontsize=9, ha='center', weight='bold', color='darkgreen')

    fig.suptitle('Scanning Correlation: Slide the reference across the signal\n'
                 'One inner product per shift position → peaks reveal sphinx locations',
                 fontsize=13, weight='bold')
    plt.tight_layout()

    out_path = OUTPUT_DIR / "correlation_scanning.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    plot_correlation_cases()
    plot_scanning_correlation()
