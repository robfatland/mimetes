# Case Study 08 — Fourier and Laplace Discrete and Continuous Transforms

## Objective

Understand the Fourier and Laplace Transforms in relation to one another. At the outset: Build some math mechanics for the "Discrete Fourier Transform (DFT)" from a minimal mathematical background: Familiarity with complex numbers and the complex unit circle and basic linear algebra. The DFT machinery is fun in its own right (so I claim) so this first part (sections 1 - 4) is done in a *fait accompli* manner... and then we just abandon it! In favor of a different discrete transform. And from there we transubstantiate into continuous versions of the discrete machinery, somehow arriving at the Fourier and Laplace transforms. That much is the easy part. The difficult part comes next: demonstrating that these transforms have some useful purpose.


## Prerequisites Assumed


- Complex numbers: what they are, addition, multiplication, the polar form
- The complex unit circle: $e^{iθ} = \cos θ + i \sin θ$.
- Linear algebra basics: vectors, dot products, matrix-vector multiplication
    - Complex numbers will be elements of linear transformation matrices...
        - ...so it is a collision of worlds

## Notation


This is where we begin simply presenting machinery for the interested reader to ingest. If you do not have paper and pencil on hand: Now would be a good time.


We begin with $N$ ordered real numbers: Our data. Since it is ordered we can suppose it exists along an axis of *time*. For some reason we want to transform it to a different representation with a different axis: Not *time* but inverse time, i.e. *frequency*. To effect this transformation we will multiply our data (organized as a column vector) by something we call a *kernel*. An N-dimensional Fourier Transform kernel is an $N \times N$ matrix denoted $F_N$. We hope -- since we are using a matrix -- that the transform will prove to be linear. Now in an abuse of terminology we also say that the kernel entry at row k, column n of this matrix is the kernel:


$$F_N[k, n] = e^{-2\pi i \, k \, n \,/\, N}$$


This is the almost-complete specification of the N-dimensional transform. There is a factor of $1/\sqrt{N}$ that will come in to play shortly (a normalization factor) but for now to keep things simple we ignore it.


The Fourier transform going from time to frequency is said to be in the *forward* direction. The transformation is written as an equation: $F_N \; \mathbf{x} = \mathbf{X}$, where $\mathbf{x}$ is the time-domain vector containing our data. Then $\mathbf{X}$ is a *frequency-domain* vector: The forward transform result. As noted: The output is in terms of a new independent variable. (The transform changes the independent variable, in contrast to an operator like $\frac{d}{dx}$, which leaves the independent variable unchanged.)



## 1. Building up transforms from $N=1$

### 1.1 $N = 1$

What is the Fourier transform of `[3]`? This is a 1-D "time series" vector with but one sample: $3$. Well with $N = 1$ we have only $k = n = 0$ so...


$F_1 = [1]$


The transform is just the one data value itself: $F_1 \cdot [3] = [3]$.


**Exercise:** Convince yourself that $F_1$ is its own inverse: $F_1(F_1([x])) = [x]$.


**Answer:** $F_1 = [1]$, so $F_1 \cdot F_1 = [1] \cdot [1] = [1] = I_1$.
This is to suggest that the forward Discrete Fourier Transform is invertible.


### 1.2 $N=2$, the smallest non-trivial case


The DFT matrix for N=2 using the kernel recipe:


$$F_2 = \begin{pmatrix} 1 & \;1 \\ 1 & -1 \end{pmatrix}$$


- Row 0 ($k=0$): $e^0 = 1$ for $n=0$ and $n=1$
- Row 1 ($k=1$): $n=0$: $e^0 = 1$; then $n=1$: $e^{-\frac{2\pi i}{2}} = -1$


Apply this to a data vector: We use the convention of a column vector written one of two ways: $[a, b]^T$ or equivalently $\begin{pmatrix} a \\ b \end{pmatrix}$.


$$F_2 \cdot \begin{pmatrix} a \\ b \end{pmatrix} = \begin{pmatrix} a + b \\ a - b \end{pmatrix}$$


Row 0 gives the **sum** — the constant component of the signal. Row 1 gives the **difference** — the "highest frequency" for 2 points: how much the signal oscillates between its two samples.


This is the machinery of the DFT kernel $e^{-2\pi i \, k \, n / 2}$. As $N$ gets progressively larger $\dots 3, \; 4, \; 5, \; \dots$ the calculation of the matrix is a bit more work but a nice pattern will emerge.


## 2. The Kernel examined and visualized


### 2.1 The utility of $k$, $n$, and $N$


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


### 2.2 Visualizing the Kernel

For each N, we lay out an $N \times N$ grid of unit circle diagrams corresponding to row k and column n. The blue line + dot shows the kernel value $e^{-2\pi i \, k \, n / N}$ on the complex unit circle: A phasor. It can be helpful to scan each row from left to right just as it is used in the matrix multiply applied to the (data) column vector.


#### N=1 through N=7 (stacked)


![DFT Kernel N=1 to N=7](images/dft_kernel_N1_to_N7.png)


**Patterns to observe:**
- Row 0 (k=0): all dots sit at angle 0 (the point 1+0i). This is the
  constant-component detector — it sums the signal with equal weight.
- Row 1 (k=1): dots rotate uniformly around the circle, one step of
  $2\pi/N$ per column.
- Row k: dots rotate k times as fast as row 1.
- The last row (k=N−1) rotates in the opposite direction from row 1 — the conjugate of row 1.


#### N=14 in conjugate-pair ordering


A note on the figure below: it uses a **different row ordering** from the
stacked $N=1 \dots 7$ figure above. The rows have been rearranged so the eye
can catch a piece of geometry — most rows come in **mirror-image pairs**.


![DFT Kernel N=14 paired](images/dft_kernel_N14_paired.png)


Look at any adjacent pair: the two rows sweep out the same set of points on the
unit circle, but one spins clockwise while the other spins counter-clockwise.
Same speed, opposite direction. That is purely an
observation about the picture.


*Why* this pairing matters, and what it has to do with the fact that our data
is real-valued, is a genuinely useful result — but it depends on ideas we have
not built yet, so we defer it to Section 6. For the moment, just enjoy the
symmetry.


**Row ordering used in the figure:** k=0 (the non-spinning row), k=7 (the lone
row with no partner — it advances exactly half a turn per tick), then the
mirror pairs (1, 13), (2, 12), (3, 11), (4, 10), (5, 9), (6, 8).


## 3. The DFT as N Dot Products


To this point we have begun to explore the *discrete* Fourier Transform as a
sort of curious fait accompli, a device that is interesting but has no
apparent purpose. The next section will unapologetically go a little ways
further down this exploratory path with a vague promise that the utility will
eventually become clear. But then, dear reader, we take a sudden sharp
departure into a related discrete transform, namely the transform attributed
to Laplace. The idea will be to see a transformation of this discrete
transform based on a power series to a continuous or integral transform. Then
we will try the same feat on the discrete Fourier Transform. In so doing we
hope to pick up two transforms in one parallelized exposition; and from there
proceed to practical utility.


Each row of the kernel matrix defines a "detector" — a complex sinusoid at
a specific frequency. The DFT of a signal is just N dot products: project
the signal onto each detector. A large projection (large magnitude) means
that frequency is strongly present in the signal.


**Aha!** The DFT is just N dot products against N different spinning
phasors. Every sample in $\mathbf{x}$ contributes to every coefficient in
$\mathbf{X}$.


In linear algebra terms: $F_N$ is a change-of-basis matrix. It rotates your
signal from the time basis into the frequency basis. The coefficients in the
new basis tell you "how much of each frequency."


### The DC term: a special case of the k=0 dot product


The very first dot product — the projection onto row k=0 — is worth naming.
Row 0 is all ones: $[1, 1, \ldots, 1]$, the only row of $F_N$ where nothing
rotates. Its dot product with the signal is simply $x_0 + x_1 + \cdots +
x_{N-1}$, the sum of all samples (with $1/\sqrt{N}$ normalization, $\sqrt{N}$
times the mean).


This k=0 component is universally called the **DC term** in signal
processing. The name comes from electrical engineering: "Direct Current" is a
constant voltage, as opposed to Alternating Current, which oscillates. The DC
term is the non-oscillating part of the signal — the constant offset, the
mean. When you see "DC component" in any spectral context, it means the
zero-frequency term, the average value. It is nothing more than the first of
the N dot products, the one against the detector that does not spin.


## 4. Invertibility, Orthogonality, and Change of Basis (condensed)


Everything below is the payoff of the dot-product picture: the rows of $F_N$
are orthogonal, which makes the transform an invertible, information-
preserving rotation. Condensed here so we can push on to the Laplace parallel.


**Rows are orthogonal.** For distinct rows the inner product
$\langle \mathbf{u}, \mathbf{v} \rangle = \sum_n u_n \overline{v_n}$ is zero.
Worked check ($F_4$, rows 1 and 2): row 1 $=[1,-i,-1,i]$, row 2 $=[1,-1,1,-1]$,
and $1 + i - 1 - i = 0$. Each row has magnitude $\sqrt{N}$, so with $1/\sqrt{N}$
normalization the rows form an **orthonormal basis** for $\mathbb{C}^N$. The
DFT is therefore a **unitary transformation** — a rotation from the
time-domain basis to the frequency-domain basis that loses no information and
distorts no distances.


**Rows are periodic (cyclic).** Row k advances by $-2\pi k/N$ per tick; after
N ticks it has made k full turns and returned to $1+0i$. The (N+1)-th tick
lands on the first. Each row is periodic with period N — which is why the DFT
applies to periodic (or periodically extended) signals.


**Invertibility.** Because the rows are orthogonal, $F_N \cdot \overline{F_N}
= N \cdot I$, so the inverse is the conjugate kernel scaled by $1/N$:


$$F_N^{-1}[n, k] = \frac{1}{N}\, e^{+2\pi i\, k\, n / N}, \qquad
F_N^{-1} = \frac{1}{N}\,\overline{F_N}.$$


The only changes from the forward transform are a **sign flip in the exponent**
($-2\pi i \to +2\pi i$) and a **scale factor**. Intuitively: the forward
transform decomposes by correlating against clockwise spinners; the inverse
recomposes by summing counter-clockwise spinners at the discovered amplitudes.
The sign flip *is* the conjugation. ($F_2$ is a degenerate case: its entries
are real ($\pm 1$), so $F_2 \cdot F_2 = 2I$ and $\tfrac{1}{\sqrt2}F_2$ is its
own inverse. $F_3$ has genuinely complex entries ($\omega = e^{-2\pi i/3}$), so
it is *not* its own inverse and forces the conjugate-inverse formula above.)


**Normalization conventions.** The symmetric choice ($1/\sqrt{N}$ on both
transforms) is elegant but not universal. NumPy (`numpy.fft`) puts the full
$1/N$ on the inverse and none on the forward. The physics is identical; only
the bookkeeping differs.


**Real data and conjugate pairs.** For real input, $X[k] = \overline{X[N-k]}$,
because rows k and N−k are complex conjugates (they spin oppositely at the same
speed). So the output is redundant: frequencies 0 through N/2 carry everything;
the "negative frequencies" are the mirror image. This is the practical meaning
of complex output from real-valued time series — magnitude and phase come in
conjugate pairs.


**Change of basis.** The same vector has two descriptions. In the time basis,
$\mathbf{x} = \sum_n x_n \mathbf{e}_n$, a sum of scaled impulses (maximally
localized). In the frequency basis, $\mathbf{x} = \sum_k X_k \mathbf{f}_k$, a
sum of scaled sinusoids (maximally delocalized). The unitary DFT rotates
between these orthonormal bases without stretching or losing anything. Neither
is more "real"; they are two coordinate systems for one object — and the
localized/delocalized contrast is the time–frequency uncertainty tradeoff.


**Convolution and CNNs (forward pointer).** The convolution theorem —
pointwise multiplication in the frequency domain equals convolution in the
time domain — is the operation at the heart of CNNs and the bridge back to
case studies 01 and 04. We will return to it after the Laplace detour.


## 5. From Discrete Power Series to the Continuous Laplace Transform


This is the sharp departure promised in Section 3. Rather than treat Laplace's
transform as a formula handed down from above, we build it up in three moves:
first a *finite* sum that is the natural sibling of the DFT (the z-transform),
then the *infinite* sum (the generating function), then the *continuous* limit
(the Laplace integral). Each move loosens one constraint.


> **Attribution.** This section follows the pedagogical arc of:
>
> Arthur Mattuck, *Lecture 19: Introduction to the Laplace Transform*,
> **18.03 Differential Equations**, MIT OpenCourseWare, Massachusetts
> Institute of Technology. (Course as taught in Spring 2010; video lectures
> recorded live in Spring 2003.)
> <https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/resources/lecture-19-introduction-to-the-laplace-transform/>
> License: CC BY-NC-SA 4.0 (MIT OCW). Content here is a rephrasing/adaptation,
> not a reproduction.
>
> The power-series-as-transform motivation and the two worked examples below
> ($a_n = 1$ and $a_n = 1/n!$) are drawn from that lecture. **One thing still
> to eyeball:** the lecture *identity, title, and instructor* are confirmed
> from MIT's own pages, but the transcript body could not be re-fetched to
> independently verify that these two specific examples sit in Lecture 19
> (vs. an adjacent lecture). Skim the video/transcript once to confirm the
> examples before publishing or presenting.


### 5.1 The finite analog of the DFT: the z-transform


Recall from Section 6 that the DFT is a finite-dimensional linear operator: it
maps an N-vector to an N-vector by N dot products against spinning phasors.
There is a finite object one step more general than the DFT. Given a finite
sequence $a_0, a_1, \ldots, a_{N-1}$, define


$$Z_N(x) \;=\; \sum_{n=0}^{N-1} a_n\, x^{n}.$$


This is a truncated **z-transform** (equivalently, a polynomial in $x$ whose
coefficients are the data). It is *not yet* the DFT — it is a function of a
free variable $x$. The DFT is what you get by **evaluating this polynomial at
the N roots of unity**: set $x = e^{-2\pi i k / N}$ for $k = 0, 1, \ldots, N-1$,
and


$$Z_N\!\left(e^{-2\pi i k / N}\right) \;=\; \sum_{n=0}^{N-1} a_n\,
e^{-2\pi i k n / N} \;=\; X[k].$$


So the DFT is the z-transform *sampled on the unit circle*. This is the hinge
of the whole section: the finite Fourier operator and the finite power series
are the same object seen from two angles — one evaluates at special points,
the other keeps $x$ free.


### 5.2 Letting the sum go infinite: the generating function


Now drop the truncation. Let the sequence run forever and keep $x$ free:


$$A(x) \;=\; \sum_{n=0}^{\infty} a_n\, x^{n}.$$


This infinite power series has a proper name: it is the **(ordinary)
generating function** of the sequence $\{a_n\}$ — the same object a
signal processor calls the **z-transform**. Read it as a *transform*: feed in
a discrete sequence, get back a single function of $x$. All the information in
the sequence is repackaged into one function, provided the series converges
(which for now we take to mean $|x| < 1$, deferring careful convergence
questions).


Two examples make the packaging concrete. Both are borrowed from the MIT
lecture noted above (attribution still owed).


**Example A: the all-ones sequence, $a_n = 1$.**


$$A(x) \;=\; \sum_{n=0}^{\infty} x^{n} \;=\; \frac{1}{1 - x}
\qquad (|x| < 1).$$


The humble geometric series. An infinite, structureless sequence of 1's
collapses into a single tidy rational function. This is the generating
function's whole appeal: an unwieldy sequence becomes a compact closed form.


**Example B: the reciprocal-factorial sequence, $a_n = 1/n!$.**


$$A(x) \;=\; \sum_{n=0}^{\infty} \frac{x^{n}}{n!} \;=\; e^{x}
\qquad (\text{all } x).$$


The sequence $1, 1, \tfrac12, \tfrac16, \tfrac{1}{24}, \ldots$ packages
into the exponential. Note this one converges everywhere — the factorial in
the denominator tames the series. The contrast with Example A (which needs
$|x|<1$) is exactly the convergence subtlety that will matter when we pass to
the integral.


### 5.3 Making the index continuous: the Laplace integral


The final move is to let the *index itself* become continuous. Replace the
discrete index $n$ by a continuous variable $t$, the coefficients $a_n$ by a
function $a(t)$, and the sum by an integral:


$$\sum_{n=0}^{\infty} a_n\, x^{n} \;\longrightarrow\;
\int_{0}^{\infty} a(t)\, x^{t}\, dt.$$


The awkward piece is $x^t$. Convergence of the power series wanted $0 < x < 1$;
write that region cleanly with the substitution


$$x = e^{-s}, \qquad s > 0 \;\Longleftrightarrow\; 0 < x < 1,$$


so that $x^{t} = e^{-st}$. The integral becomes


$$\boxed{\;\mathcal{L}\{a\}(s) \;=\; \int_{0}^{\infty} a(t)\, e^{-st}\, dt\;}$$


which is the **Laplace transform**. It is the continuous analog of a
generating function: the decaying kernel $e^{-st}$ plays the role that $x^n$
played in the sum, and the requirement $s > 0$ is the continuous echo of
$|x| < 1$. The one-sided integral (0 to $\infty$) is inherited directly from
the power series starting at $n = 0$.


### 5.4 The parallel move: DFT $\to$ continuous Fourier transform


The same discrete → continuous passage, run on the Fourier side, produces the
continuous Fourier transform. Start from the DFT kernel $e^{-2\pi i k n / N}$;
let the sample index $n$ become continuous time $t$, the sum become an
integral, and the discrete frequency index become a continuous frequency
$\omega$:


$$X[k] = \sum_{n=0}^{N-1} x_n\, e^{-2\pi i k n / N}
\;\longrightarrow\;
\hat{f}(\omega) \;=\; \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt.$$


Structurally this mirrors the Laplace passage, but honesty requires naming one
difference in *which knob is turned*:


- **Laplace** arrives via the power-series / z-transform route and the
  substitution $x = e^{-s}$: a **real decaying** kernel $e^{-st}$ and a
  **one-sided** integral ($0$ to $\infty$), tied to convergence.
- **Fourier** arrives by taking the DFT and letting $N \to \infty$ *and* the
  sample spacing $\to 0$ (a period-to-infinity limit): a **purely
  oscillating** kernel $e^{-i\omega t}$ and a **two-sided** integral
  ($-\infty$ to $\infty$).


### 5.5 The punchline: Fourier is a slice of Laplace


The two developments converge. Write the Laplace variable as $s = \sigma +
i\omega$. The kernel is then $e^{-st} = e^{-\sigma t}\, e^{-i\omega t}$ — a
decay factor times an oscillation. Setting $\sigma = 0$ (i.e. $s = i\omega$,
the imaginary axis) kills the decay and leaves the pure oscillation
$e^{-i\omega t}$: exactly the Fourier kernel.


So the Fourier transform is the Laplace transform restricted to the imaginary
axis, and Laplace is the general case that also allows real decay. Two
transforms, one parallelized exposition — which is precisely the payoff
promised back in Section 5. From here we turn to what they are *for*.


## 6. Examples of Use (in development)

The goal of this section: let each transform earn its keep by solving a real
problem. Ideally a matched pair, so the parallel structure of Section 7 pays
off in application as well as derivation.

- **Fourier — the heat equation (planned).** The classic. Fourier's own
  motivating problem: heat diffusion on a rod (or ring). Transforming the PDE
  in space turns $\partial_t u = \alpha\, \partial_{xx} u$ into a decoupled
  set of ODEs in the Fourier coefficients, each decaying as
  $e^{-\alpha k^2 t}$ — high frequencies die fastest, which is *why* diffusion
  smooths. Ties directly back to the change-of-basis picture of Section 6.

- **Laplace — an initial-value ODE (candidate).** Laplace's natural home:
  solving a linear ODE with initial conditions by turning differentiation into
  multiplication by $s$, solving algebraically, and inverting. A damped
  oscillator or an RC/RL circuit would make the real-decay kernel
  ($\sigma \neq 0$) do visible work, complementing the purely oscillatory heat
  example.

- **Geoscience tie-in (stretch).** If a glacier / climate time-series example
  can carry the Fourier half (spectral analysis of a periodic signal), prefer
  it over a generic textbook problem to keep the case study anchored in the
  project's domain.

**Open items:**
- Pick the Laplace example and confirm it exercises $\sigma \neq 0$.
- Decide how much worked algebra to show vs. delegate to a Python cell.
- Each example needs a visual per the slides convention (heat decay animation
  frames; pole diagram for the Laplace example).
## Visualization Approach

- Python scripts in this directory generate matplotlib figures → PNG
- PNGs are inlined here and in the slide deck
- Generate: `python dft_kernel_viz.py`

## Status

🔲 In development
