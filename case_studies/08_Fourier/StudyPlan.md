# Case Study 08 — The Discrete Fourier Transform

## Objective

Build up an understanding of the Discrete Fourier Transform (DFT) from a
minimal mathematical background: complex numbers, the unit circle, and basic
linear algebra operations. The goal is conceptual clarity — understanding what
the DFT does, why it works, and how to use it — not just memorizing the formula.

## Prerequisites Assumed

- Complex numbers: what they are, addition, multiplication, the polar form
- The unit circle: e^{iθ} = cos θ + i sin θ
- Linear algebra basics: vectors, dot products, matrix-vector multiplication


## Notation

An N-dimensional Fourier Transform kernel (the matrix) is denoted $F_N$.
The kernel entry at row k, column n is:

$$F_N[k, n] = e^{-2\pi i \, k \, n \,/\, N}$$

We ignore the $1/\sqrt{N}$ normalization factor for now to keep the patterns
visible.

We write the forward transform as $F_N \mathbf{x} = \mathbf{X}$, where
$\mathbf{x}$ is the time-domain vector (our data) and $\mathbf{X}$ is the
frequency-domain vector (the transform output).


## 1. The Trivial Case: N=1

What is the Fourier transform of `[3]`? A 1-D "time series" with one sample.

$F_1 = [1]$

The transform is just the value itself: $F_1 \cdot [3] = [3]$. There is only
one frequency (the constant/mean component), and it equals the signal.

**Exercise:** Convince yourself that $F_1$ is its own inverse: $F_1(F_1([x])) = [x]$.

**Answer:** $F_1 = [1]$, so $F_1 \cdot F_1 = [1] \cdot [1] = [1] = I_1$.
Applying it twice returns the original value. Trivial but establishes the
pattern: the DFT is invertible.


## 2. N=2: The Smallest Non-Trivial Case

The DFT matrix for N=2:

$$F_2 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

This comes directly from the kernel $e^{-2\pi i \, k \, n / 2}$:
- Row 0: $e^0 = 1$ for both n=0 and n=1
- Row 1, n=0: $e^0 = 1$; Row 1, n=1: $e^{-\pi i} = -1$

Apply it to a concrete vector, say $[a, b]^T$:

$$F_2 \cdot \begin{pmatrix} a \\ b \end{pmatrix} = \begin{pmatrix} a + b \\ a - b \end{pmatrix}$$

Row 0 gives the **sum** — the constant component of the signal.
Row 1 gives the **difference** — the "highest frequency" for 2 points: how
much the signal oscillates between its two samples.

No "just go with it" here: it's addition and subtraction, and the matrix
comes entirely from evaluating $e^{-2\pi i \, k \, n / 2}$.


## 3. The Kernel

The discrete kernel is: $e^{-2\pi i \, k \, n / N}$

- **N** = dimension of the signal (number of samples)
- **k** = frequency index (which row of the transform matrix; runs 0 to N−1)
- **n** = time index (which column / which sample; runs 0 to N−1)

The full transform matrix $F_N$ is built by evaluating this kernel for all
(k, n) pairs. Each entry is a point on the unit circle. The matrix is N×N
and transforms an N-element signal into N frequency coefficients.

**Key point:** Every element of $\mathbf{x}$ participates in producing each
element of $\mathbf{X}$. The k-th frequency coefficient $X[k]$ is a
weighted sum of *all* N time-domain samples — each weighted by its
corresponding kernel value $e^{-2\pi i \, k \, n / N}$. This is the dot
product of the signal with the k-th detector. Nothing is local; every
detector "listens to" the entire signal.


## 4. Visualizing the Kernel

The key visual: for each N, lay out an N×N grid of unit circle diagrams.
Row k, column n shows the kernel value $e^{-2\pi i \, k \, n / N}$ as a dot
on the unit circle with a phasor line from the origin.

### N=1 through N=7 (stacked)

![DFT Kernel N=1 to N=7](images/dft_kernel_N1_to_N7.png)

**Patterns to observe:**
- Row 0 (k=0): all dots sit at angle 0 (the point 1+0i). This is the
  constant-component detector — it sums the signal with equal weight.
- Row 1 (k=1): dots rotate uniformly around the circle, one step of
  $2\pi/N$ per column.
- Row k: dots rotate k times as fast as row 1.
- The last row (k=N−1) rotates in the opposite direction from row 1 — it's
  the conjugate of row 1.

### N=14 (conjugate-pair ordering)

![DFT Kernel N=14 paired](images/dft_kernel_N14_paired.png)

Here the rows are **reordered** to emphasize conjugate pairs. For real-valued
input data, the DFT output at frequency k is the complex conjugate of the
output at frequency N−k. Placing these rows adjacent makes the mirror
symmetry visible: k and N−k rotate in opposite directions at the same speed.

**Row ordering:** k=0 (constant), k=7 (Nyquist / π phase), then pairs
(1, 13), (2, 12), (3, 11), (4, 10), (5, 9), (6, 8).


## 5. The DFT as N Dot Products

Each row of the kernel matrix defines a "detector" — a complex sinusoid at
a specific frequency. The DFT of a signal is just N dot products: project
the signal onto each detector. A large projection (large magnitude) means
that frequency is strongly present in the signal.

**Aha moment:** The DFT is just N dot products against N different spinning
phasors. Every sample in $\mathbf{x}$ contributes to every coefficient in
$\mathbf{X}$.

In linear algebra terms: $F_N$ is a change-of-basis matrix. It rotates your
signal from the time basis into the frequency basis. The coefficients in the
new basis tell you "how much of each frequency."


## 6. The DC Term (a jargon note)

The k=0 frequency component is universally called the **DC term** in signal
processing. The name comes from electrical engineering: "Direct Current"
refers to a constant voltage (as opposed to Alternating Current, which
oscillates). In our context, the k=0 component is the non-oscillating part
of the signal — the constant offset, the mean. It's the only row of $F_N$
where nothing rotates: all entries are 1.

This term will appear in every spectral analysis context. When you see "DC
component" it means: the average value, the zero-frequency term.


## 7. Invertibility: $F_2$ and $F_3$

### $F_2$: almost its own inverse

Without a scalar factor, $F_2 \cdot F_2 = \begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix} = 2I$.

Applying $F_2$ twice scales by N=2. All kernel entries of $F_2$ are real
(+1 and −1), so the matrix happens to equal its own conjugate. The only
issue is the scale factor.

If we define the normalized transform as $\frac{1}{\sqrt{N}} F_N$, then:

$$\left(\frac{1}{\sqrt{2}} F_2\right)^2 = \frac{1}{2} \cdot 2I = I$$

With symmetric normalization, the $N=2$ transform is its own inverse.

### $F_3$: not its own inverse

$$F_3 = \begin{pmatrix} 1 & 1 & 1 \\ 1 & \omega & \omega^2 \\ 1 & \omega^2 & \omega^4 \end{pmatrix} \quad \text{where } \omega = e^{-2\pi i / 3}$$

Here $\omega = -\frac{1}{2} - i\frac{\sqrt{3}}{2}$ — a complex number off
the real line. The kernel has left the real axis. If we compute $F_3 \cdot F_3$
we do NOT get a scalar multiple of the identity. Instead:

$$F_3 \cdot F_3 \neq c \cdot I$$

The reason: $F_3$ is not equal to its own conjugate. The matrix has complex
entries, and squaring it does not produce the cancellations needed for
identity. This forces us to confront the inverse properly.

### The inverse transform

The inverse of $F_N$ is:

$$F_N^{-1}[n, k] = \frac{1}{N} \, e^{+2\pi i \, k \, n \,/\, N}$$

The only differences from the forward transform:
1. **Sign change in the exponent:** $-2\pi i$ becomes $+2\pi i$
2. **Scale factor of $1/N$**

With symmetric normalization ($1/\sqrt{N}$ on both forward and inverse),
the inverse kernel is the complex conjugate of the forward kernel:

$$F_N^{-1} = \frac{1}{N} \overline{F_N}$$

**Motivating the sign change:** Each row of $F_N$ spins clockwise (negative
angle). The inverse spins counter-clockwise (positive angle). The
orthogonality of the rows guarantees that when you correlate the output
$\mathbf{X}$ with the counter-clockwise phasors, you recover $\mathbf{x}$.
Intuitively: the forward transform *decomposes* by correlating against
clockwise spinners; the inverse *recomposes* by summing counter-clockwise
spinners at the discovered amplitudes.

Another way to see it: $F_N \cdot \overline{F_N} = N \cdot I$. The
orthogonality proof shows that rows of $F_N$ dotted with conjugate rows
(i.e., rows of $\overline{F_N}$) give N on the diagonal and 0 off-diagonal.
So $\overline{F_N} / N$ is the inverse. The sign flip *is* the conjugation.

**Note on normalization conventions:** The symmetric choice ($1/\sqrt{N}$
on both transforms) is elegant but not universal. A common alternative
places the full $1/N$ on the inverse and uses no scalar on the forward
transform. This is the convention in NumPy (`numpy.fft`). The physics is
identical; only the bookkeeping differs.


## 8. Further Exercises and Explorations

### The first row: what does it do?

For every $F_N$ the first row (k=0) is all ones: $[1, 1, 1, \ldots, 1]$.

When we apply $F_N$ to a vector $[x_0, x_1, \ldots, x_{N-1}]^T$, the first
output element is $x_0 + x_1 + \cdots + x_{N-1}$ — the sum of all samples.
With the $1/\sqrt{N}$ normalization this becomes $\sqrt{N}$ times the mean.
This is the DC term (Section 6).

### Real-valued data and conjugate pairs

**Question:** We consider real-valued input vectors. What is the connection
between real-valued data and the rows of the DFT pairing off as complex
conjugates?

**Answer:** When the input $\mathbf{x}$ is real, the DFT output satisfies
$X[k] = \overline{X[N-k]}$ — the output at frequency k is the complex
conjugate of the output at frequency N−k. This is because rows k and N−k
of $F_N$ are themselves complex conjugates of each other (they rotate in
opposite directions at the same speed). Taking the dot product of a real
vector with conjugate row-vectors produces conjugate results.

This means for real data, the DFT output is redundant: you only need
frequencies 0 through N/2. The "negative frequencies" (k > N/2) carry no
new information — they're the mirror image.

### Rows as cyclic functions

**Question:** View each row of the DFT as a clock hand sweeping out equal
angles with each tick (from one n value to the next). If we follow the hand
to n = N−1 and then allow one additional tick: where do we end up?

**Answer:** Row k advances by angle $-2\pi k / N$ per tick. After N ticks
the total angle is $-2\pi k$ — exactly k full rotations, returning to the
starting point (1 + 0i). The (N+1)-th tick lands on the same point as the
first tick. Each row of the DFT is a **periodic function with period N**.
The kernel values repeat cyclically. This is why the DFT applies to periodic
or periodically-extended signals.

### Orthogonality of rows

**Exercise:** Calculate the inner product of any two distinct rows of $F_4$
or $F_5$. (Remember: for complex vectors, the inner product is
$\langle \mathbf{u}, \mathbf{v} \rangle = \sum_n u_n \overline{v_n}$.)

**Worked example ($F_4$, rows k=1 and k=2):**

Row 1: $[1, \; e^{-i\pi/2}, \; e^{-i\pi}, \; e^{-i3\pi/2}] = [1, -i, -1, i]$

Row 2: $[1, \; e^{-i\pi}, \; e^{-2i\pi}, \; e^{-3i\pi}] = [1, -1, 1, -1]$

Inner product: $\sum_n \text{row}_1[n] \cdot \overline{\text{row}_2[n]}$

$= 1\cdot 1 + (-i)\cdot(-1) + (-1)\cdot 1 + i\cdot(-1) = 1 + i - 1 - i = 0$

**Result:** The inner product of any two distinct rows is zero. The rows are
**orthogonal**.

**Does this hold for any $F_N$?** Yes. This is a general property: the rows
of $F_N$ form an orthogonal set. Moreover, each row has magnitude $\sqrt{N}$
(since it has N entries each of magnitude 1). So with the $1/\sqrt{N}$
normalization, the rows form an **orthonormal basis** for $\mathbb{C}^N$.

**Interpretation in vector space language:** The DFT is a unitary
transformation — a rotation (in N-dimensional complex space) from the
time-domain basis to the frequency-domain basis. No information is lost,
no distances are distorted. It's a perfect change of coordinates.


## 9. Change of Basis

The time-domain representation of a signal $\mathbf{x} = [x_0, x_1, \ldots, x_{N-1}]^T$ is:

$$\mathbf{x} = x_0 \mathbf{e}_0 + x_1 \mathbf{e}_1 + \cdots + x_{N-1} \mathbf{e}_{N-1}$$

where $\mathbf{e}_n$ is the standard basis vector: all zeros with a 1 at
position n. Each $x_n$ is the amplitude of the n-th impulse. The signal is
literally a sum of scaled impulses.

The DFT changes the basis. The frequency-domain representation of the same
vector is:

$$\mathbf{x} = X_0 \mathbf{f}_0 + X_1 \mathbf{f}_1 + \cdots + X_{N-1} \mathbf{f}_{N-1}$$

where $\mathbf{f}_k$ is the k-th frequency basis vector (a complex sinusoid
at frequency k), and $X_k$ is the complex amplitude of that sinusoid in the
signal.

Same vector, two descriptions:
- **Time basis:** "I am this amplitude at this moment, that amplitude at that
  moment, ..."
- **Frequency basis:** "I am this much of frequency 0, that much of
  frequency 1, ..."

The unitary DFT rotates between these two orthonormal bases without
stretching or losing anything. Neither representation is more "real" — they
are two coordinate systems for the same object.

The time-domain basis vectors are maximally localized (each is a single
spike). The frequency-domain basis vectors are maximally delocalized (each
fills the entire signal). This is the uncertainty tradeoff: precise in time
= spread in frequency, and vice versa.


## 10. Real-Valued Data (TBD)

We operate on real-valued time series. What does it mean that the output is
complex? The conjugate symmetry property. Magnitude and phase interpretation.


## 10. Connection to Convolution and CNNs (Future)

The convolution theorem: pointwise multiplication in frequency domain equals
convolution in time domain. This is the operation at the heart of CNNs.
Bridge to case studies 01 and 04.


## Visualization Approach

- Python scripts in this directory generate matplotlib figures → PNG
- PNGs are inlined here and in the slide deck
- Generate: `python dft_kernel_viz.py`

## Status

🔲 In development
