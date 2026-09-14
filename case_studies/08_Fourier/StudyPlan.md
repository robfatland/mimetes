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


### 3.1 Detection


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


### 3.2 The DC term: a special case of the k=0 dot product


The very first dot product — the projection onto row $k=0$ — is worth naming.
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





### 3.3 An intermezzo on the **inner products of complex-valued vectors**


One vector is in column format, the other in row format, and one or the other is conjugated before the sum of products calculation is carried out.


 In physics, particularly quantum mechanics: The first/left vector is conjugated: 
 
 
 $$\langle a | b \rangle = \sum_i \overline{a_i} \cdot b_i$$
 
 
 So the bra $\langle a|$ is the conjugated row vector and the ket $|b\rangle$ is a plain column vector. The math convention often conjugates the second argument instead, giving the same result.




## 4. Invertibility, Orthogonality, and Change of Basis


The dot-product idea has implications that we'll look at briefly here in section 4 before we go flying off on a tangent in section 5. Dot products measure how closely two vectors are aligned. Here we have the rows of $F_N$ each acting as a detector for a particular frequency of oscillation in the time-series data. Furthermore each detector vector is orthogonal to all the others: Their pairwise dot products give zero. This -- we claim -- makes the Fourier transform an invertible, information-preserving rotation in $N$-space.


The **orthogonality claim:** For distinct rows the inner product
$\langle \mathbf{u}, \mathbf{v} \rangle = \sum_n u_n \overline{v_n}$ is zero.
Worked check ($F_4$, rows 1 and 2): row 1 $=[1,-i,-1,i]$, row 2 $=[1,-1,1,-1]$,
and $1 + i - 1 - i = 0$. Each row has magnitude $\sqrt{N}$, so with $1/\sqrt{N}$
normalization the rows form an **orthonormal basis** for $\mathbb{C}^N$. (The *normal* part means the row vectors of the Fourier Transform -- once they are properly scaled by a factor of $\frac{1}{\sqrt{N}}$ -- have magnitude 1, regardless of how big $N$ is.) The DFT as such is therefore a **unitary transformation** — a rigid rotation from the time-domain basis to the frequency-domain basis that does not lose information and does not distort distances.


- No info loss: The forward Fourier transform has an inverse that recovers 
all of the original $\vec{x}$. 
- Distance preserved: If two arbitrary data vectors $\vec{x}$ and $\vec{y}$ are separated by difference vector $\vec{s}$ with length $|\vec{s}|$ then the difference vector between FT(x) and FT(y) also has length $|\vec{s}|$.


**Rows are periodic (cyclic).** Row k advances by $-2\pi k/N$ per tick; after
$N$ ticks the kernel has made $k$ full turns and returned to $1+0i$. The $(N+1)$-th tick would land on the first tick. Each row is periodic with period $N$ — which is why the DFT applies to periodic (or periodically extended) signals.


**Invertibility.** Because the rows are orthogonal, $F_N \cdot \overline{F_N}
= N \cdot I$: The inverse exists. We are scaling both forward and inverse Fourier transforms by a factor of $\frac{1}{\sqrt{N}}$ to keep the $k$-row vectors normalized; plus it has a nice symmetry. Here (noting the change in sign of the exponential) is the inverse Fourier Transform kernel.


$$F_N^{-1}[n, k] = \frac{1}{\sqrt{N}}\, e^{+2\pi i\, k\, n / N}$$


The only change from the forward transform is the **sign flip in the exponent**
($-2\pi i \to +2\pi i$). This means the inverse transform is the complex conjugate of the forward transform. As a summarizing narrative: The forward transform decomposes by correlating the data with clockwise spinners ('detectors'). The inverse transform recomposes the original data by summing counter-clockwise spinners weighted by amplitudes, specifically the amplitudes of the Fourier Transform of the data. 


**Normalization conventions.** The symmetric choice ($1/\sqrt{N}$ on both
transforms) is elegant but not universal. NumPy (`numpy.fft`) puts the full
$1/N$ on the inverse and none on the forward. The physics is identical; only
the bookkeeping changes.


**Real data and conjugate pairs.** For real input, the Fourier transform element $k$ is the complex conjugate of element $N-k$. That is: $X[k] = \overline{X[N-k]}$. This is because in $F_N$, rows k and N−k are complex conjugates: They spin oppositely at the same speed. So the output is redundant: frequencies 0 through N/2 carry everything; the "negative frequencies" are the mirror image. This is the practical meaning of complex output from real-valued time series — magnitude and phase come in conjugate pairs.


**Change of basis.** The same vector has two descriptions: The time basis description and the frequency basis description. In the time basis the information about data point zero ($x_0$) is identically $x_0$. It is localized. However, in the *frequency* basis, the information about data point zero $x_0$ is distributed across all $N$ elements of the transform vector.
Neither representation is more "real"; they are two coordinate systems for one object — and the localized/delocalized contrast is a "time–frequency uncertainty tradeoff".


Fun fact about **Convolution** and **Convolutional Neural Networks**: One of the useful features of the DFT we will eventually arrive at is fast execution of a mathematical operation called *convolution*. This relates to the operation of *Convolutional Neural Networks* (abbreviated CNN). CNNs are an important tool in the machine learning toolbox and are engaged within this repo for case studies 1 and 4. And now: On to the Laplace detour.


## 5. From Discrete Power Series to the Continuous Laplace Transform


This is a narrative swerve: We will develop the integral (continuous) Laplace transform from a discrete transform that will prove to be related to the Fourier Transform. We'll go at this in three stages: A *finite* sum called the z-transform, extension to an *infinite* sum called a generating function, and then moving on to a *continuous* limit called the Laplace integral.


> **Attribution.** We follow the pedagogical arc of:
>
> Arthur Mattuck, *Lecture 19: Introduction to the Laplace Transform*,
> **18.03 Differential Equations**, MIT OpenCourseWare, Massachusetts
> Institute of Technology. (Course as taught in Spring 2010; video lectures
> recorded live in Spring 2003.)
> <https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010>
> License: CC BY-NC-SA 4.0 (MIT OCW). Content here is a rephrasing/adaptation,
> not a reproduction.



### 5.1 The finite analog of the DFT: the z-transform


Recall from above that the DFT is a finite-dimensional linear operator: it
maps an N-vector to an N-vector via N dot products using phasors that spin at various constant rates. We'll shoot for something more *general* than the DFT: Given a fixed value $x$ and a finite sequence of $N$ data values $a_0, a_1, \ldots, a_{N-1}$, define


$$Z_N(x) \;=\; \sum_{n=0}^{N-1} a_n\, x^{n}.$$


This is called the z-transform. It is a polynomial in the free continuous variable $x$. The *data* from our earlier DFT work (the column vector) is now the $a_i$ sequence: The coefficients of the $x$ polynomial are the data. So apologies for the confusion but the data in the DFT work was labeled $x_0, \dots, x_{N-1}$; and it is now labeled $a_0, \dots, a_{N-1}$. And then $x$ is being repurposed as a complex-valued free variable whose various powers give us the z-transform polynomial.


In the DFT the column vector data were subjected to the transform as a sequence of $N$ dot products with complex-valued vectors. We now recreate the Fourier transform using the z-transform as defined above.


The $N$ roots of unity are $N$ numbers on the complex unit circle spaced evenly apart by angle $2 \pi / N$. The first of these roots is $1$ and by the convention of the Fourier transform the list continues in the clockwise direction from there. I will use these $N$ roots of unity as values of the free variable $x$. I intend to generate $N$ z-transforms for the $N$ values of the free variable $x$: That is: I use my list N roots of unity as x-values for this multiple z-transform calculation. I reiterate that my N data values are a_0, ..., a_{N-1}. For these I choose to use my N time-series data points. The result will be an N-dimensional Fourier transform of said data.


In the DFT work above I started with time-series data and produced a transform. Here I start with time-series data and -- by selecting my $x$ values just so -- produce the identical transform. 


A second version of what we are up to follows: As noted the definition of $Z_N(x)$ above is called a truncated **z-transform** as a function of a free variable $x$.  Letting $k = 0, 1, \ldots, N-1$ and using our data as the $a_i$ coefficients results in


$$Z_N\!\left(e^{-2\pi i k / N}\right) \;=\; \sum_{n=0}^{N-1} a_n\,
e^{-2\pi i k n / N} \;=\; X[k].$$


The DFT is the z-transform *sampled on the unit circle*. The finite Fourier operator is a particular application of the finite power series.


### 5.2 Letting the sum go infinite: the generating function


Now let the sequence run forever and keep $x$ free:


$$\sum_{n=0}^{\infty} a_n\, x^{n} \;=\; A(x) $$


or -- viewing $a$ as a function of $n$ -- equivalently


$$\sum_{n=0}^{\infty} a(n)\, x^{n} \;=\; A(x) $$



This infinite power series has a proper name: it is the **(ordinary)
generating function** of the sequence $\{a_n\}$ — the same object a
signal processor calls the **z-transform**. Reading it as a *transform*: feed in
a discrete sequence, get back a function of $x$. The information in
the sequence is repackaged into the function, provided the series converges
(which for now we take to mean $|x| < 1$, deferring careful convergence
questions). In the other direction, the function is said to "generate" the sequence because the sequence is recoverable from it: The $a_n$ are Taylor coefficients: $a_n = \frac{1}{n!}\frac{d^n}{dx^n}A(x)\big|_{x=0}$. The function $A(x)$ "generates" the sequence as extracted coefficients. In short: Generation goes from function to sequence.



**Example: the all-ones sequence, $a_n = 1$.**


$$A(x) \;=\; \sum_{n=0}^{\infty} x^{n} \;=\; \frac{1}{1 - x}
\qquad (|x| < 1).$$


This is the geometric series: From an infinite polynomial with all $1$ coefficients resolves as a compact closed form. An interesting stretch exercise is to sort out the cases $a_n = n$ and $a_n = \frac{1}{n}$.


**Example: the reciprocal-factorial sequence, $a_n = 1/n!$.**


$$A(x) \;=\; \sum_{n=0}^{\infty} \frac{x^{n}}{n!} \;=\; e^{x}
\qquad (\text{all } x).$$


The sequence $1, 1, \tfrac12, \tfrac16, \tfrac{1}{24}, \ldots$ produces
the exponential. This converges everywhere — the factorial in
the denominator forces convergence for any $x$; we do not need to stipulate $|x|<1$. However we will hold onto this qualifier as more generally convergent for $a_n$ sequences.


Here in 5.2 we can notice that the DFT has fallen off the back of the truck: Given $|x| < 1$ we are unable to use roots of unity for $x$. 


The next step proceeds with $x$ real, not complex. This narrative bounces
between them a bit so let's say that it is easier to move forward using 
real numbers but the full complex picture is more complete and therefore
our ultimate goal.



### 5.3 Making the index continuous: the Laplace integral


In the infinite series generating function we treat the $a$ sequence as "a function of an integer index: $n = 0, \; 1, \; \dots$" The next move is to let this index be continuous: Replace the discrete index $n$ by a continuous variable $t$; and so replace the coefficients $a_n$ by a
function $a(t)$. So the sum is replaced by an integral.


$$ 0 \le t < \infty$$


$$\sum_{n=0}^{\infty} a_n\, x^{n} \;\longrightarrow\;
\int_{0}^{\infty} a(t)\, x^{t}\, dt = A(x)$$


The $x^t$ piece of this expression is unpleasant so we shall manipulate that exponential to be in terms of base $e$; while preserving the convergence of the result (what previously we facilitated with $0 < x < 1$; taking $x$ as real.


$$x = e^{\log x}$$


$$x^t = e^{t \log x} = (e^{\log x})^t$$


Keeping $x$ in a workable range: 


$$0 < x < 1$$


This means the log of $x$ will be negative: $\log x < 0$.


So let's define a new positive-valued variable $s$ as $-s = \log x$. Some arithmetic: $x^t = e^{t\log x} = e^{-st}$. Now with these not-too-profound even "cosmetic" changes (also re-naming the input function $a(t)$ as $f(t)$) we arrive at:





$$\boxed{\;\int_{0}^{\infty} f(t) e^{-st} dt = F(s) = \mathcal{L}\{f\}(s)}$$


which is the **Laplace transform**. 


The Laplace transform is the continuous analog of the generating function from above. The decaying kernel $e^{-st}$ plays the role that $x^n$
played in the sum, and the requirement that $s > 0$ is the continuous version of
$|x| < 1$. The one-sided integral (0 to $\infty$) is inherited from
the power series starting at $n = 0$.


### 5.4 In parallel: The DFT $\to$ the continuous Fourier transform


In parallel fashion we produce the continuous Fourier transform. From the DFT kernel $e^{-2\pi i k n / N}$: let the sample index $n$ become continuous time $t$. The sum becomes an integral, and the discrete frequency index becomes a continuous frequency $\omega$:


$$X[k] = \frac{1}{\sqrt{N}} \sum_{n=0}^{N-1} x_n\, e^{-2\pi i k n / N}
\;\longrightarrow\;
\hat{f}(\omega) \;=\; \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt.$$


This resembles the Laplace journey above but let's do a little refinement of our working description:


- **Laplace** 
  - travels the power-series / z-transform route
  - uses the substitution $x = e^{-s}$
  - has a **real decaying** kernel $e^{-st}$
  - has a **one-sided** integral ($0$ to $\infty$) tied to convergence
- **Fourier** 
  - travels the DFT route
  - lets $N \to \infty$ *and* 
  - lets the sample spacing $\to 0$ (a period-to-infinity limit)
  - uses a **purely oscillating** kernel $e^{-i\omega t}$ 
  - uses a **two-sided** integral ($-\infty$ to $\infty$).


### 5.5 Fourier as a slice of Laplace


In the development of the Laplace transform above $s$ was a real independent variable. However we can widen the picture by allowing $s$ to be complex: $s = \sigma + i \omega$. The Laplace transform kernel is then $e^{-st} = e^{-\sigma t}\, e^{-i\omega t}$ — a decay factor times an oscillation. Setting $\sigma = 0$ (i.e. $s = i\omega$, the imaginary axis) kills the decay and leaves the pure oscillation $e^{-i\omega t}$: exactly the Fourier kernel.


The Fourier transform is the Laplace transform restricted to the imaginary
axis. Laplace is the general case that also allows real decay. From here we turn to use cases: What are they used for?


### 5.6 Let's go to the movies


So far we have a kind of $2 \times 2 \times 2 = 8$-dimensional space for this introduction to two transforms. That's the first dimension: Fourier vs Laplace. The second is Discrete vs Continuous. The third is Real vs Complex. The next step is to go watch the following videos with the rewind button handy. This is about 15 hours worth of material intended to leverage some of the best instructional material ever produced; freely available on YouTube.


I'm starting with a sketch of the arc with the idea of filling in the links and providing short reviews. 


- 3B1B
  - Fourier
  - Differential Equations
  - Laplace (sequence of 3)
- MIT OCW
  - Gil Strang: Linear Algebra
  - ODEs
  - Laplace
- Steve Brunton


## 6. Examples of Use (in development)


The goal of this section: let each transform earn its keep by solving a real
problem. Ideally a matched pair, so the parallel structure of Section 5 pays
off in application as well as derivation.

- **Fourier — the heat equation (planned).** The classic. Fourier's own
  motivating problem: heat diffusion on a rod (or ring). Transforming the PDE
  in space turns $\partial_t u = \alpha\, \partial_{xx} u$ into a decoupled
  set of ODEs in the Fourier coefficients, each decaying as
  $e^{-\alpha k^2 t}$ — high frequencies die fastest, which is *why* diffusion
  smooths. Ties directly back to the change-of-basis picture of Section 4.

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
